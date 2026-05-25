# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agente import agente
from langgraph.checkpoint.postgres import PostgresCheckpointer

# ── FastAPI ────────────────────────────────────────────────────────────────────
app = FastAPI()


class MensajeRequest(BaseModel):
    session_id: str
    mensaje: str

@app.post("/chat")
def chat(request: MensajeRequest):
    config = {"configurable": {"thread_id": request.session_id}}
    resultado = agente.invoke(
        {"mensajes": [HumanMessage(content=request.mensaje)]},
        config=config
    )
    return {"respuesta": resultado["mensajes"][-1].content}

@app.delete("/chat/{session_id}")
def limpiar_sesion(session_id: str):
    # El MemorySaver no expone borrado directo; en producción usar PostgresCheckpointer
    return {"mensaje": f"Sesión {session_id} cerrada"}

@app.get("/chat/{session_id}/historial")
def historial(session_id: str):
    # Accedemos al checkpointer del agente
    cp: PostgresCheckpointer = agente.checkpointer

    checkpoint = cp.get(thread_id=session_id)

    if not checkpoint:
        return {"historial": []}

    mensajes = checkpoint["state"]["mensajes"]

    return {
        "session_id": session_id,
        "historial": [
            {"tipo": m.__class__.__name__, "contenido": m.content}
            for m in mensajes
        ]
    }