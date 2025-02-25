from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoParecerResponse
from datetime import date
from typing import Optional
from src.cache import cache

pap_router = APIRouter(tags=["Plano de Ação - Parecer"])

@pap_router.get("/plano_acao_parecer",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Pareceres dos Planos de Ação - TED.",
                response_description="Lista Paginada de Pareceres relativas aos Planos de Ação - TED",
                response_model=PaginatedPlanoAcaoParecerResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_parecer_plano_acao_ted(
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    id_parecer: Optional[int] = Query(None, description="Identificador Único do Parecer"),
    tp_analise_parecer: Optional[str] = Query(None, description="Tipo da Análise do Parecer do Plano de Ação"),
    resultado_parecer: Optional[str] = Query(None, description="Resultado do Parecer do Plano de Ação"),
    tx_parecer: Optional[str] = Query(None, description="Parecer do Plano de Ação"),
    plano_acao_hist_fk: Optional[int] = Query(None, description="Número do Histórico do Plano de Ação"),
    dt_data_parecer: Optional[str] = Query(None, description="Data do Parecer do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
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
        query = select(models.PlanoAcaoParecer).where(
            and_(
                models.PlanoAcaoParecer.id_plano_acao == id_plano_acao if id_plano_acao is not None else True,
                models.PlanoAcaoParecer.id_parecer == id_parecer if id_parecer is not None else True,
                models.PlanoAcaoParecer.tp_analise_parecer.ilike(f"%{tp_analise_parecer}%") if tp_analise_parecer is not None else True,
                models.PlanoAcaoParecer.resultado_parecer.ilike(f"%{resultado_parecer}%") if resultado_parecer is not None else True,
                models.PlanoAcaoParecer.tx_parecer.ilike(f"%{tx_parecer}%") if tx_parecer is not None else True,
                models.PlanoAcaoParecer.plano_acao_hist_fk == plano_acao_hist_fk if plano_acao_hist_fk is not None else True,
                cast(models.PlanoAcaoParecer.dt_data_parecer, Date) == date.fromisoformat(dt_data_parecer) if dt_data_parecer is not None else True
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