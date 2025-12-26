🛡️ Sun Tzu: Chatbot RAG
Asistente inteligente basado en RAG (Retrieval-Augmented Generation) que responde consultas sobre "El Arte de la Guerra" utilizando una base de datos vectorial propia.

🌟 Características
IA Estratégica: Respuestas precisas basadas exclusivamente en el contexto del libro.

Arquitectura Eficiente: Migrado de n8n a Python para optimizar costos y control.

Búsqueda Semántica: Uso de pgvector en Supabase para encontrar fragmentos relevantes.

Cero Costo: Corre íntegramente en capas gratuitas (Streamlit Cloud + Gemini API).

🛠️ Stack Tecnológico
Lenguaje: Python

LLM: Google Gemini 2.5 Flash

Base de Datos: Supabase (PostgreSQL + pgvector)

Embeddings: all-mpnet-base-v2 (BERT)

Interfaz: Streamlit

🚀 Instalación Rápida
Clonar repositorio:

Bash

git clone https://github.com/tu-usuario/tu-repositorio.git
Instalar dependencias:

Bash

pip install -r requirements.txt
Configurar Secretos: Crea un archivo .streamlit/secrets.toml con tus llaves:

Ini, TOML

GEMINI_API_KEY = "tu_key"
SUPABASE_URL = "tu_url"
SUPABASE_KEY = "tu_key"
Ejecutar:

Bash

streamlit run app.py
🏭 Aplicación Industrial
Este proyecto es una prueba de concepto para Ingeniería de Confiabilidad. La misma lógica puede aplicarse a manuales de mantenimiento industrial para reducir el MTTR y digitalizar el conocimiento técnico.

🔗 App en vivo: [https://chatbot-supabase-app-fmfm8zqgqnbqwrkaebv4cv.streamlit.app/]

👤 Autor: [Gabriel Alfredo Regali]
