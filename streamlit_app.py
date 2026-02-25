import streamlit as st

# ==========================================
# 1. Configuración inicial y Estado (State)
# ==========================================
st.set_page_config(page_title="Formulario por Pasos", page_icon="📝")

# Inicializamos la variable que controla en qué ventana/paso estamos
if 'ventana_actual' not in st.session_state:
    st.session_state.ventana_actual = 1

# Inicializamos un diccionario para guardar los datos a lo largo de las ventanas
if 'datos_registro' not in st.session_state:
    st.session_state.datos_registro = {}

# Funciones de navegación
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
    
    # Leemos los datos previos si el usuario retrocedió
    nombre_previo = st.session_state.datos_registro.get('nombre', '')
    apellido_previo = st.session_state.datos_registro.get('apellido', '')
    
    nombre = st.text_input("Nombre", value=nombre_previo)
    apellido = st.text_input("Apellido", value=apellido_previo)
    
    if st.button("Siguiente ➡️"):
        # Validación: Asegurarse de que llenó los campos
        if nombre.strip() == "" or apellido.strip() == "":
            st.error("⚠️ Debes completar Nombre y Apellido para continuar.")
        else:
            # Guardamos la info y avanzamos
            st.session_state.datos_registro['nombre'] = nombre
            st.session_state.datos_registro['apellido'] = apellido
            siguiente_ventana()
            st.rerun() # Fuerza la recarga para mostrar la siguiente ventana

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
    
    # Botones de navegación en columnas
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
    
    # Mostramos los datos recolectados en las ventanas anteriores
    st.json(st.session_state.datos_registro)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Atrás para corregir"):
            ventana_anterior()
            st.rerun()
            
    with col2:
        if st.button("✅ Registrar Datos"):
            st.success("¡Registro completado con éxito!")
            st.balloons()
            
            # Aquí pondrías tu código para guardar en una Base de Datos, Excel, etc.
            # ej: guardar_en_bd(st.session_state.datos_registro)
            
            # Botón para registrar a una nueva persona
            if st.button("Registrar otra persona"):
                reiniciar_formulario()
                st.rerun()