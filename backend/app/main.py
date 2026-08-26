from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.routes.finestre import router as finestre_router
from app.routes.pergole import router as pergole_router
from app.routes.portoncini import router as portoncini_router
from app.routes.product_families import router as product_families_router
from app.routes.quote_requests import router as quote_requests_router

app = FastAPI(
    title="Coges Configurator API",
    description="Prototipo: configuratore infissi multi-categoria con stima prezzo (dati fittizi).",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_families_router)
app.include_router(finestre_router)
app.include_router(portoncini_router)
app.include_router(pergole_router)
app.include_router(quote_requests_router)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
