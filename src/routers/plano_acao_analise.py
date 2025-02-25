from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoAnaliseResponse
from datetime import date
from typing import Optional
from src.cache import cache

paa_router = APIRouter(tags=["Plano de Ação - Análise"])

@paa_router.get("/plano_acao_analise",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Análises dos Planos de Ação - TED.",
                response_description="Lista Paginada de Análises relativas aos Planos de Ação - TED",
                response_model=PaginatedPlanoAcaoAnaliseResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_analise_plano_acao_ted(
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    id_analise: Optional[int] = Query(None, description="Identificador Único da Análise"),
    tx_justificativa_analise: Optional[str] = Query(None, description="Justificativa da Análise do Plano de Ação"),
    resultado_analise: Optional[str] = Query(None, description="Resultado da Análise do Plano de Ação"),
    tx_situacao_analise: Optional[str] = Query(None, description="Situação da Análise do Plano de Ação"),
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
        query = select(models.PlanoAcaoAnalise).where(
            and_(
                models.PlanoAcaoAnalise.id_plano_acao == id_plano_acao if id_plano_acao is not None else True,
                models.PlanoAcaoAnalise.id_analise == id_analise if id_analise is not None else True,
                models.PlanoAcaoAnalise.tx_justificativa_analise.ilike(f"%{tx_justificativa_analise}%") if tx_justificativa_analise is not None else True,
                models.PlanoAcaoAnalise.resultado_analise.ilike(f"%{resultado_analise}%") if resultado_analise is not None else True,
                models.PlanoAcaoAnalise.tx_situacao_analise.ilike(f"%{tx_situacao_analise}%") if tx_situacao_analise is not None else True
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