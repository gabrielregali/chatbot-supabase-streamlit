# -*- coding: utf-8 -*-
import streamlit as st
import os
import numpy as np 
from google import genai
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client # SDK Oficial

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="RAG Chatbot Sun Tzu", 
    layout="centered"
)

# --- CONFIGURACIÓN DE CLAVES (SEGURO PARA STREAMLIT CLOUD) ---

try:
    # Las claves son cargadas desde st.secrets.
    # En Streamlit Cloud se cargan desde el panel web de "Secrets".
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    
except KeyError as e:
    # Si la clave no se encuentra, detiene la ejecución y muestra un error.
    st.error(f"Error: Falta la clave {e} en la configuración de secretos de Streamlit. Por favor, añádela.")
    st.stop()
    
# Parámetros que no son secretos
N_RESULTS = 144 
TABLA_RPC_SUPABASE = 'final_rag_call'


# --- CACHE DE RECURSOS ---

@st.cache_resource
def load_bert_model():
    """Carga y cachea el modelo de embeddings para la búsqueda."""
    try:
        return SentenceTransformer("all-mpnet-base-v2") 
    except Exception as e:
        st.error(f"Error al cargar el modelo BERT: {e}")
        st.stop()

@st.cache_resource
def init_gemini_client(api_key):
    """Inicializa y cachea el cliente de Gemini."""
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Error al inicializar el cliente Gemini: {e}")
        st.stop()

@st.cache_resource
def init_supabase_client(url, key):
    """Inicializa y cachea el cliente de Supabase."""
    try:
        supabase_client: Client = create_client(url, key)
        return supabase_client
    except Exception as e:
        st.error(f"Error al inicializar cliente de Supabase: {e}")
        st.stop()

# --- INICIALIZACIÓN DE CLIENTES ---
bert_model = load_bert_model()
gemini_client = init_gemini_client(GEMINI_API_KEY)
supabase_client = init_supabase_client(SUPABASE_URL, SUPABASE_KEY) # Cliente de Supabase

# --- FUNCIONES RAG ---

def get_embedding(text: str) -> list:
    """Paso 1: Convierte el texto de consulta en un vector (embedding)."""
    embedding = bert_model.encode(text)
    return embedding.tolist()

def retrieve_context(query_embedding: list):
    """
    Paso 2: Busca en Supabase usando la función RPC de UN solo argumento JSON (final_rag_call).
    """
    
    # 💥 CRÍTICO: Usamos el nombre del WORKAROUND JSON para forzar la llamada.
    RPC_NAME = 'final_rag_call' 
    
    # 1. Parámetros (El vector como STRING es crucial, se convierte a TEXT en SQL)
    embedding_as_string = str(query_embedding) # <-- ¡CONVERTIDO A STRING!
    
    # El SDK enviará este diccionario como el único argumento JSON
    params = {
        'query_embedding': embedding_as_string, # <-- Enviamos STRING, que PostgreSQL trata como TEXT
        'match_count': N_RESULTS,
        'filter': {}
    }
    
    try:
        # 2. Llamar a la función RPC usando el SDK
        response = supabase_client.rpc(
        "final_rag_call",
        {
        "match_count": N_RESULTS,
        "query_embedding": embedding_as_string
        }
        ).execute()

        response_data = response.data
        
        if not response_data:
             st.info("No se encontró información relevante en la base de datos.")
             return ""

        # 3. Procesar la respuesta
        contexto = "\n---\n".join([doc['content'] for doc in response_data])
        return contexto
        
    except Exception as e:
        st.error(f"Error al llamar a la RPC de Supabase: {e}")
        st.error(f"No pude encontrar información relevante en la base de datos para responder a esa pregunta. Intenta reformularla.")
        return ""


def generate_response(prompt: str, context: str):
    """Paso 3: Genera la respuesta usando Gemini con el contexto recuperado."""
    
    # Crea el prompt final
    full_prompt = (
        f"Eres un experto en el libro El Arte de la Guerra de Sun Tzu. "
        f"Usa únicamente el contexto proporcionado para responder a la pregunta. "
        f"Si el contexto no contiene la respuesta, di que no puedes responder basándote en la información suministrada.\n\n"
        f"Contexto: \"{context}\"\n\n"
        f"Pregunta: {prompt}"
    )

    try:
        # Llamar al modelo
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"Error al generar respuesta con Gemini: {e}"


# --- LÓGICA PRINCIPAL DE STREAMLIT ---

st.title("🛡️ Sun Tzu: Chatbot RAG")
st.caption("Pregúntale sobre El Arte de la Guerra. Este chatbot usa **RAG** con pgvector y Gemini.")

# Inicializar el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar la entrada del usuario
if prompt := st.chat_input("Hazme una pregunta sobre estrategia militar..."):
    # 1. Mostrar la pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Buscando en Sun Tzu y generando respuesta..."):
        # 2. Obtener el embedding de la pregunta
        query_embedding = get_embedding(prompt)

        # 3. Recuperar el contexto de Supabase
        context = retrieve_context(query_embedding)
        
        if context:
            # 4. Generar la respuesta usando Gemini con el contexto
            response = generate_response(prompt, context)
        else:
            # Si retrieve_context falló, ya mostró un error
            response = "Lo siento, no pude obtener contexto relevante de la base de datos."

    # 5. Mostrar la respuesta
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # 6. Guardar la respuesta en el historial
    st.session_state.messages.append({"role": "assistant", "content": response})