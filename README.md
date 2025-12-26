# 🛡️ **Sun Tzu: Chatbot RAG**

Asistente inteligente basado en la arquitectura **RAG (Retrieval-Augmented Generation)** que responde consultas sobre el libro *"El Arte de la Guerra"* utilizando una base de datos vectorial propia.



---

## 🌟 **Características Principales**
* **IA Estratégica:** Respuestas precisas basadas exclusivamente en el contexto del libro para evitar alucinaciones.
* **Arquitectura Eficiente:** Migración exitosa de n8n a **Python puro** para optimizar el control y eliminar costes.
* **Búsqueda Semántica:** Implementación de `pgvector` en **Supabase** para recuperar información por significado y no solo por palabras clave.
* **Coste Cero:** Solución desplegada íntegramente en capas gratuitas (Streamlit Cloud + Gemini API).

---

## 🛠️ **Stack Tecnológico**
* **Lenguaje:** Python 3.x
* **Motor de IA (LLM):** Google Gemini 2.5 Flash
* **Base de Datos Vectorial:** Supabase (PostgreSQL + pgvector)
* **Modelo de Embeddings:** `all-mpnet-base-v2` (BERT)
* **Interfaz de Usuario:** Streamlit

---

## 🚀 **Instalación Rápida**

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/gabrielregali/chatbot-supabase-streamlit.git](https://github.com/gabrielregali/chatbot-supabase-streamlit.git)
    ```
2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurar Secretos (`.streamlit/secrets.toml`):**
    ```toml
    GEMINI_API_KEY = "tu_api_key"
    SUPABASE_URL = "tu_url_proyecto"
    SUPABASE_KEY = "tu_anon_key"
    ```
4.  **Ejecutar la App:**
    ```bash
    streamlit run app.py
    ```

---

## 🏭 **Aplicación en Mantenimiento Industrial**
Este proyecto funciona como una **Prueba de Concepto (PoC)** para la **Ingeniería de Confiabilidad**. La misma lógica permite cargar manuales técnicos de maquinaria pesada para:
* **Reducción del MTTR** mediante consultas rápidas de averías.
* **Digitalización del conocimiento** de expertos en mantenimiento.
* **Asistencia en procedimientos** de seguridad **LOTO** de forma conversacional.

---

🔗 **App en vivo:** [https://chatbot-supabase-app-fmfm8zqgqnbqwrkaebv4cv.streamlit.app/]

👤 **Autor:** [Gabriel Alfredo Regali]
