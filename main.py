from contextlib import asynccontextmanager
from fastapi import FastAPI
import orjson
from fastapi.responses import RedirectResponse, ORJSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import logging
from appconfig import Settings
from cashews.contrib.fastapi import (
    CacheEtagMiddleware,
    CacheRequestControlMiddleware    
)

from src.database import Database
from src.cache import setup_cache

# Importando Rotas
from src.routers.programa import pg_router
# from src.routers.plano_acao_especial import pa_router
# from src.routers.empenho_especial import em_router
# from src.routers.documento_habil import dh_router
# from src.routers.ordem_pagamento_especial import op_router
# from src.routers.historico_pagamento_especial import hist_router
# from src.routers.relatorio_gestao_especial import rg_router
# from src.routers.plano_trabalho_especial import pt_router
# from src.routers.executor_especial import ex_router
# from src.routers.meta_especial import me_router
# from src.routers.finalidade_especial import fe_router

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize instances
settings = Settings()
db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load before the app starts
    logger.info("Iniciando aplicação...")
    try:
        # Inicializa o Banco de Dados
        await db.init_db()        
        # Configure o cache
        setup_cache(settings)
        logger.info("Aplicação iniciada com sucesso!")
    except Exception as e:
        logger.error(f"Erro na inicialização: {str(e)}")
        raise
    yield
    # load after the app has finished
    # ...
    

app = FastAPI(lifespan=lifespan, 
              docs_url=None, 
              title=settings.APP_NAME, 
              description=settings.APP_DESCRIPTION,
              openapi_tags=settings.APP_TAGS,
              default_response_class=ORJSONResponse,              
              swagger_ui_parameters={"defaultModelExpandDepth": -1})
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluindo Middlewares
app.add_middleware(CacheEtagMiddleware)
app.add_middleware(CacheRequestControlMiddleware)

# setup_cache(settings)

# Incluindo Rotas
app.include_router(pg_router)
# app.include_router(pa_router)
# app.include_router(em_router)
# app.include_router(dh_router)
# app.include_router(op_router)
# app.include_router(hist_router)
# app.include_router(rg_router)
# app.include_router(pt_router)
# app.include_router(ex_router)
# app.include_router(me_router)
# app.include_router(fe_router)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.APP_NAME + " - Documentação",        
        swagger_favicon_url="/static/icon.jpg"
    )


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

# Run in terminal
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload