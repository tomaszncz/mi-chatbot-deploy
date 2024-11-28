import streamlit as st 
from groq import Groq

#Agregar el nobmbre a nuestra pestaña e icono 
st.set_page_config(page_title="Mi chat de IA", page_icon= "colocar un icono encontrado en internet", layout="centered")

#titulo a la aplicación 

st.title("Mi primera Aplicación de Streamlit")

#Entrada de Texto - Input
nombre = st.text_input("¿cuál es tu nombre?") #smailliw

#boton para mostrar un saludo 
if st.button("Saludar"):
    st.write(f'hola {nombre}, Bienvenido a mi chatbot')

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def configurar_pagina():
    #Agregamos un título principal a nuestra página 
    st.title("Mi chat de Inteligencia Artificial")
    st.sidebar.title("Configuración de la IA") #Creamos un sidebar
    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options = modelos, index=0)
    return elegirModelo



#Clase 7

def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"]
    return Groq(api_key=claveSecreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model= modelo,
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes=[]

    

#clase 8
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()



#clase 9 - función
#Chat completo es la caja que almacena el chatbot la respuesta que me da a mí como usuario.
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat() #Función de esta clase
    mensaje = st.chat_input("Por favor, escribí un mensaje")
    if mensaje:
        actualizar_historial("user", mensaje, "🧑")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()

if __name__ == "__main__":
    main()