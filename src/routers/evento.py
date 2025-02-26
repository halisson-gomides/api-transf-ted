from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedEventoResponse
from datetime import date
from typing import Optional
from src.cache import cache
import asyncio


evt_router = APIRouter(tags=["Evento"])


@evt_router.get("/evento",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Evento - TED.",
                response_description="Lista Paginada de Eventos relativos aos Planos de Ação - TED",
                response_model=PaginatedEventoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_evento_ted(
    id_nota: Optional[int] = Query(None, description="Identificador Único da Nota de Crédito"),
    cd_evento: Optional[str] = Query(None, description="Código do Evento"),
    cd_ptres_evento: Optional[str] = Query(None, description="Código PTRES do Evento"),
    cd_fonte_recurso_evento: Optional[str] = Query(None, description="Código da Fonte de Recurso do Evento"),
    cd_plano_interno_evento: Optional[str] = Query(None, description="Código do Plano Interno do Evento"),
    vl_evento: Optional[float] = Query(None, description="Valor do Evento"),
    cd_ug_responsavel_evento: Optional[str] = Query(None, description="Código da Unidade Gestora Responsável do Evento"),
    codigo_natureza: Optional[str] = Query(None, description="Código de Natureza do Evento"),
    descricao_natureza: Optional[str] = Query(None, description="Descrição de Natureza do Evento"),
    nome_esfera_orcamentaria: Optional[str] = Query(None, description="Nome da Esfera Orçamentária do Evento"),
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
        query = select(models.Evento).where(
            and_(
                models.Evento.id_nota == id_nota if id_nota is not None else True,
                models.Evento.cd_evento == cd_evento if cd_evento is not None else True,
                models.Evento.cd_ptres_evento == cd_ptres_evento if cd_ptres_evento is not None else True,
                models.Evento.cd_fonte_recurso_evento == cd_fonte_recurso_evento if cd_fonte_recurso_evento is not None else True,
                models.Evento.cd_plano_interno_evento == cd_plano_interno_evento if cd_plano_interno_evento is not None else True,
                models.Evento.vl_evento == vl_evento if vl_evento is not None else True,
                models.Evento.cd_ug_responsavel_evento == cd_ug_responsavel_evento if cd_ug_responsavel_evento is not None else True,
                models.Evento.codigo_natureza == codigo_natureza if codigo_natureza is not None else True,
                models.Evento.descricao_natureza.ilike(f"%{descricao_natureza}%") if descricao_natureza is not None else True,
                models.Evento.nome_esfera_orcamentaria.ilike(f"%{nome_esfera_orcamentaria}%") if nome_esfera_orcamentaria is not None else True
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