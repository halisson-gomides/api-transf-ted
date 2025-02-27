from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedTrfResponse
from datetime import date
from typing import Optional
from src.cache import cache


trf_router = APIRouter(tags=["TRF"])


@trf_router.get("/trf",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de TRF - TED.",
                response_description="Lista Paginada de TRFs - TED",
                response_model=PaginatedTrfResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_trf_ted(
    id_programacao: Optional[int] = Query(None, description="Identificador Único Programação Financeira"),
    cd_vinculacao_trf: Optional[int] = Query(None, description="Código de Vinculação TRF"),
    cd_fonte_recurso_trf: Optional[str] = Query(None, description="Código de Fonte Recurso do TRF"),
    cd_categoria_gasto_trf: Optional[str] = Query(None, description="Código Categoria Gasto TRF"),
    vl_valor_trf: Optional[float] = Query(None, description="Valor do TRF"),
    cd_situacao_contabil_trf: Optional[str] = Query(None, description="Código de Situação Contábil do TRF"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]    
    
    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)
    
    try:
        query = select(models.Trf).where(
            and_(
                models.Trf.id_programacao == id_programacao if id_programacao is not None else True,
                models.Trf.cd_vinculacao_trf == cd_vinculacao_trf if cd_vinculacao_trf is not None else True,
                models.Trf.cd_fonte_recurso_trf == cd_fonte_recurso_trf if cd_fonte_recurso_trf is not None else True,
                models.Trf.cd_categoria_gasto_trf == cd_categoria_gasto_trf if cd_categoria_gasto_trf is not None else True,
                models.Trf.vl_valor_trf == vl_valor_trf if vl_valor_trf is not None else True,
                models.Trf.cd_situacao_contabil_trf.ilike(f"%{cd_situacao_contabil_trf}%") if cd_situacao_contabil_trf is not None else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)