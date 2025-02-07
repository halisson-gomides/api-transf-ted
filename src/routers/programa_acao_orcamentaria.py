from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaAcaoOrcamentariaResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

pgao_router = APIRouter(tags=["Programa - Ação Orçamentária"])
config = Settings()


@pgao_router.get("/programa_acao_orcamentaria",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Ações Orçamentárias dos Programas - TED.",
                response_description="Lista Paginada de Ações Orçamentárias dos Programas - TED",
                response_model=PaginatedProgramaAcaoOrcamentariaResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_programa_acao_orcamentaria_ted(
    tx_codigo_acao_orcamentaria: Optional[str] = Query(None, description="Código da Ação Orçamentária"),
    tx_descricao_acao_orcamentaria: Optional[str] = Query(None, description="Descrição do Programa da Ação Ornamentária"),
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),
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
        query = select(models.ProgramaAcaoOrcamentaria).where(
            and_(
                models.ProgramaAcaoOrcamentaria.tx_codigo_acao_orcamentaria == tx_codigo_acao_orcamentaria if tx_codigo_acao_orcamentaria else True,
                models.ProgramaAcaoOrcamentaria.tx_descricao_acao_orcamentaria.ilike(f"%{tx_descricao_acao_orcamentaria}%") if tx_descricao_acao_orcamentaria else True,
                models.ProgramaAcaoOrcamentaria.id_programa == id_programa if id_programa else True
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