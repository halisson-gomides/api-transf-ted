from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedTermoExecucaoResponse
from datetime import date
from typing import Optional
from src.cache import cache

tde_router = APIRouter(tags=["Termo de Execução"])

@tde_router.get("/termo_execucao",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Termos de Execução - TED.",
                response_description="Lista Paginada de Termos de Execução relativas aos Planos de Ação - TED",
                response_model=PaginatedTermoExecucaoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_termo_execucao_ted(
    id_termo: Optional[int] = Query(None, description="Identificador Único do Termo"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    tx_situacao_termo: Optional[str] = Query(None, description="Situação do Termo de Execução"),
    tx_num_processo_sei: Optional[str] = Query(None, description="Número do Processo SEI de Execução"),
    dt_assinatura_termo: Optional[str] = Query(None, description="Data de Assinatura do Termo de Execução", pattern="^\d{4}-\d{2}-\d{2}$"),
    dt_divulgacao_termo: Optional[str] = Query(None, description="Data de Divulgação do Termo de Execução", pattern="^\d{4}-\d{2}-\d{2}$"),
    in_minuta_padrao: Optional[bool] = Query(None, description="Indicador Minuta Padrão do Termo de Execução"),
    tx_numero_ns_termo: Optional[str] = Query(None, description="Número NS do Termo de Execução"),
    dt_recebimento_termo: Optional[str] = Query(None, description="Data do Recebimento do Termo de Execução", pattern="^\d{4}-\d{2}-\d{2}$"),
    dt_efetivacao_termo: Optional[str] = Query(None, description="Data da Efetivação do Termo de Execução", pattern="^\d{4}-\d{2}-\d{2}$"),
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
        query = select(models.TermoExecucao).where(
            and_(
                models.TermoExecucao.id_termo == id_termo if id_termo is not None else True,
                models.TermoExecucao.id_plano_acao == id_plano_acao if id_plano_acao is not None else True,
                models.TermoExecucao.tx_situacao_termo.ilike(f"%{tx_situacao_termo}%") if tx_situacao_termo is not None else True,
                models.TermoExecucao.tx_num_processo_sei.ilike(f"%{tx_num_processo_sei}%") if tx_num_processo_sei is not None else True,
                cast(models.TermoExecucao.dt_assinatura_termo, Date) == date.fromisoformat(dt_assinatura_termo) if dt_assinatura_termo is not None else True,
                cast(models.TermoExecucao.dt_divulgacao_termo, Date) == date.fromisoformat(dt_divulgacao_termo) if dt_divulgacao_termo is not None else True,
                models.TermoExecucao.in_minuta_padrao == in_minuta_padrao if in_minuta_padrao is not None else True,
                models.TermoExecucao.tx_numero_ns_termo == tx_numero_ns_termo if tx_numero_ns_termo is not None else True,
                cast(models.TermoExecucao.dt_recebimento_termo, Date) == date.fromisoformat(dt_recebimento_termo) if dt_recebimento_termo is not None else True,
                cast(models.TermoExecucao.dt_efetivacao_termo, Date) == date.fromisoformat(dt_efetivacao_termo) if dt_efetivacao_termo is not None else True
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