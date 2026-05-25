## Asistente de Soporte con LangChain, RAG y LangGraph

## 🧠 Descripción del proyecto
Este proyecto implementa un **asistente de soporte al cliente** utilizando:

- **RAG (Retrieval-Augmented Generation)** para consultar políticas internas  
- **Memoria** para mantener el contexto entre mensajes  
- **Tools** para ejecutar acciones (buscar pedidos, calcular reembolsos)  
- **LangGraph** para controlar el flujo del agente  
- **FastAPI** como interfaz HTTP  
- **ChromaDB** como vector store  
- **Embeddings locales de HuggingFace** (sin necesidad de OpenAI)  
- **LLM local servido desde LLM Studio** mediante API OpenAI-compatible  

El resultado es un asistente capaz de responder preguntas sobre políticas, consultar pedidos, calcular reembolsos y mantener conversaciones coherentes por sesión.

---

## 🏗️ Arquitectura general

```
Usuario → FastAPI → LangGraph Agent → (RAG + Tools + Memoria)
                                   ↳ ChromaDB (políticas)
                                   ↳ Tools (buscar pedido, reembolso)
                                   ↳ LLM Studio (modelo local)
```

---

## 📦 Requisitos

### Software necesario
- Python 3.10+
- LLM Studio (para servir el modelo local)
- PostgreSQL (solo si activas memoria persistente, no incluida en este README)
- Git

### Dependencias Python
Se instalan automáticamente con:

```
pip install -r requirements.txt
```

Incluyen:

- langchain  
- langgraph  
- fastapi  
- uvicorn  
- chromadb  
- langchain-huggingface  
- langchain-chroma  
- sentence-transformers  

---

## 📁 Estructura del proyecto

```
.
├── agente.py               # Lógica del agente LangGraph
├── main.py                 # API FastAPI
├── ingestar.py             # Indexación de políticas en ChromaDB
├── politicas.txt           # Base de conocimiento
├── chroma_db/              # Vector store persistente
├── requirements.txt
└── README.md
```

---

## 🔧 Instalación

### 1. Clonar el repositorio

```
git clone <url-del-repo>
cd lab-web-support-assistant-with-langchain
```

### 2. Crear entorno virtual

```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```
pip install -r requirements.txt
```

---

## 📚 Paso 1 — Indexar la base de conocimiento (RAG)

Asegúrate de que `politicas.txt` contiene al menos 10 políticas.

Luego ejecuta:

```
python ingestar.py
```

Esto creará la carpeta `chroma_db/` con los embeddings.

---

## 🤖 Paso 2 — Configurar LLM Studio

1. Abre LLM Studio  
2. Carga un modelo local (Llama 3, Mistral, Gemma…)  
3. Ve a la pestaña **Server**  
4. Activa **OpenAI Compatible Server**  
5. Copia la URL (ej: `http://localhost:1234/v1`)  
6. Esa URL debe estar configurada en `agente.py`:

```python
modelo = ChatOpenAI(
    model="local-model",
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    temperature=0
)
```

---

## 🚀 Paso 3 — Ejecutar la API

```
uvicorn main:app --reload
```

La API estará disponible en:

```
http://127.0.0.1:8000
```

Documentación interactiva:

```
http://127.0.0.1:8000/docs
```

---

## 💬 Uso del endpoint `/chat`

### POST `/chat`

Envía un mensaje al asistente:

```json
{
  "session_id": "cliente123",
  "mensaje": "¿Cuál es vuestra política de devoluciones?"
}
```

Respuesta:

```json
{
  "respuesta": "Nuestra política de devoluciones indica que..."
}
```

### DELETE `/chat/{session_id}`

Reinicia la memoria de una sesión:

```
DELETE /chat/cliente123
```

---

## 🧠 ¿Cómo funciona el agente?

### 🔍 RAG (Retrieval-Augmented Generation)
El agente busca en ChromaDB los fragmentos más relevantes de `politicas.txt` y los incluye como contexto en cada respuesta.

### 🛠️ Tools
El agente puede ejecutar funciones reales:

- `buscar_pedido(pedido_id)`
- `calcular_reembolso(total, porcentaje)`

LangGraph detecta cuándo el modelo quiere llamar a una tool y ejecuta la función correspondiente.

### 🧠 Memoria por sesión
Cada `session_id` mantiene su propio historial.  
Dos sesiones distintas no comparten contexto.

### 🔄 LangGraph
Controla el flujo:

1. Nodo LLM  
2. Si el modelo pide usar una tool → nodo Tools  
3. Vuelve al LLM  
4. Respuesta final  

---

## 🧪 Ejemplos de uso

### Pregunta sobre políticas
```
"¿Cuál es vuestra política de envíos?"
```

### Consultar un pedido
```
"Busca el pedido PED-1234"
```

### Calcular un reembolso
```
"Si pagué 100€, ¿cuánto sería un reembolso del 30%?"
```

### Conversación con memoria
```
"¿Cuál es la política de devoluciones?"
"¿Y si ya pasaron 20 días?"
```

---

## 🎯 Conclusión

Este proyecto demuestra cómo construir un asistente de soporte completo combinando:

- RAG  
- Tools  
- Memoria  
- LangGraph  
- FastAPI  
- LLM local  

Todo funcionando sin depender de OpenAI.

