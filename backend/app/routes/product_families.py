from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["product-families"])


class ProductFamily(BaseModel):
    slug: str
    name: str
    description: str


# Metadati statici di navigazione: non ci sono prezzi o dati di catalogo qui,
# solo cio' che serve al frontend per costruire la pagina di selezione
# categoria. I dati di catalogo veri e propri vengono da /api/catalog/{slug}.
PRODUCT_FAMILIES = [
    ProductFamily(
        slug="finestre",
        name="Finestre",
        description="Finestre, portefinestre e scorrevoli in alluminio, PVC e legno.",
    ),
    ProductFamily(
        slug="portoncini",
        name="Portoncini",
        description="Porte blindate d'ingresso.",
    ),
    ProductFamily(
        slug="pergole",
        name="Pergole",
        description="Pergole bioclimatiche per esterni.",
    ),
]


@router.get("/product-families", response_model=list[ProductFamily])
def get_product_families() -> list[ProductFamily]:
    return PRODUCT_FAMILIES
