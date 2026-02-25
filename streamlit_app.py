import streamlit as st
import gspread # Importante: necesitas instalar esta librería (pip install gspread)

# ==========================================
# 0. Función para guardar en Google Sheets
# ==========================================
def guardar_en_gsheets(datos):
    try:
        # 1. Autenticación usando los secretos de Streamlit (.streamlit/secrets.toml)
        # Nota: Asegúrate de tener configurado tu archivo secrets.toml con las credenciales de Google
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        
        # 2. Abrir el documento por su nombre exacto (debe estar compartido con el correo de servicio)
        documento = gc.open("Base_de_Datos_Registro")
        hoja = documento.sheet1 # Selecciona la primera pestaña del Excel
        
        # 3. Preparar los datos en una lista plana (una fila)
        nueva_fila = [
            datos.get('nombre', ''), 
            datos.get('apellido', ''), 
            datos.get('email', ''), 
            datos.get('telefono', '')
        ]
        
        # 4. Añadir la fila al final del documento
        hoja.append_row(nueva_fila)
        return True
    except Exception as e:
        st.error(f"Error al guardar en Google Sheets: {e}")
        return False

# ==========================================
# 1. Configuración inicial y Estado (State)
# ==========================================
st.set_page_config(page_title="Formulario por Pasos", page_icon="📝")

if 'ventana_actual' not in st.session_state:
    st.session_state.ventana_actual = 1

if 'datos_registro' not in st.session_state:
    st.session_state.datos_registro = {}

def siguiente_ventana():
    st.session_state.ventana_actual += 1

def ventana_anterior():
    st.session_state.ventana_actual -= 1

def reiniciar_formulario():
    st.session_state.ventana_actual = 1
    st.session_state.datos_registro = {}

# ==========================================
# 2. Interfaz de Usuario
# ==========================================
st.title("📝 Registro de Información")

# Barra de progreso visual
progreso = st.progress(st.session_state.ventana_actual / 3)

# ------------------------------------------
# VENTANA 1: Datos Personales
# ------------------------------------------
if st.session_state.ventana_actual == 1:
    st.header("Paso 1: Datos Personales")
    st.write("Por favor, ingresa tu información básica.")
    
    nombre_previo = st.session_state.datos_registro.get('nombre', '')
    apellido_previo = st.session_state.datos_registro.get('apellido', '')
    
    nombre = st.text_input("Nombre", value=nombre_previo)
    apellido = st.text_input("Apellido", value=apellido_previo)
    
    if st.button("Siguiente ➡️"):
        if nombre.strip() == "" or apellido.strip() == "":
            st.error("⚠️ Debes completar Nombre y Apellido para continuar.")
        else:
            st.session_state.datos_registro['nombre'] = nombre
            st.session_state.datos_registro['apellido'] = apellido
            siguiente_ventana()
            st.rerun()

# ------------------------------------------
# VENTANA 2: Datos de Contacto
# ------------------------------------------
elif st.session_state.ventana_actual == 2:
    st.header("Paso 2: Datos de Contacto")
    st.write("¿Cómo podemos contactarte?")
    
    email_previo = st.session_state.datos_registro.get('email', '')
    telefono_previo = st.session_state.datos_registro.get('telefono', '')
    
    email = st.text_input("Correo Electrónico", value=email_previo)
    telefono = st.text_input("Teléfono", value=telefono_previo)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Atrás"):
            ventana_anterior()
            st.rerun()
            
    with col2:
        if st.button("Siguiente ➡️"):
            if email.strip() == "" or telefono.strip() == "":
                st.error("⚠️ Debes completar el Correo y el Teléfono para continuar.")
            elif "@" not in email:
                st.error("⚠️ Por favor, ingresa un correo válido.")
            else:
                st.session_state.datos_registro['email'] = email
                st.session_state.datos_registro['telefono'] = telefono
                siguiente_ventana()
                st.rerun()

# ------------------------------------------
# VENTANA 3: Confirmación y Guardado
# ------------------------------------------
elif st.session_state.ventana_actual == 3:
    st.header("Paso 3: Confirmación")
    st.write("Por favor, revisa que tus datos sean correctos antes de guardar:")
    
    st.json(st.session_state.datos_registro)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Atrás para corregir"):
            ventana_anterior()
            st.rerun()
            
    with col2:
        # Aquí ejecutamos el guardado al presionar el botón
        if st.button("✅ Registrar Datos"):
            
            with st.spinner("Guardando en Google Sheets..."):
                exito = guardar_en_gsheets(st.session_state.datos_registro)
            
            if exito:
                st.success("¡Registro completado y guardado en la nube con éxito!")
                st.balloons()
                
                # Desplegamos el botón para reiniciar solo si se guardó bien
                if st.button("Registrar otra persona"):
                    reiniciar_formulario()
                    st.rerun()
