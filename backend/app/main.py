from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_models
from .routers import router as score_router
from .routers_extra import router as extra_router

settings = get_settings()

app = FastAPI(title=settings.app_name)

# Allow all origins for now; tighten this list when integrating with auth.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(score_router, prefix=settings.api_prefix)
app.include_router(extra_router, prefix=settings.api_prefix)
