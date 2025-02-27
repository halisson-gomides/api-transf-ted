from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedProgramacaoFinanceiraResponse
from datetime import date
from typing import Optional
from src.cache import cache


pfi_router = APIRouter(tags=["Programação Financeira"])


@pfi_router.get("/programacao_financeira",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Programação Financeira - TED.",
                response_description="Lista Paginada de Programações Financeiras relativos aos Planos de Ação - TED",
                response_model=PaginatedProgramacaoFinanceiraResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_programacao_financeira_ted(
    id_programacao: Optional[int] = Query(None, description="Identificador Único Programação Financeira"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    tp_pf_tipo_programacao: Optional[str] = Query(None, description="Tipo de Programação Financeira", max_length=1),
    tx_minuta_programacao: Optional[str] = Query(None, description="Código da Minuta da Programação Financeira"),
    tx_numero_programacao: Optional[str] = Query(None, description="Número da Programação Financeira"),
    tx_situacao_programacao: Optional[str] = Query(None, description="Status da Programação Financeira"),
    tx_observacao_programacao: Optional[str] = Query(None, description="Observação da Programação Financeira"),
    ug_emitente_programacao: Optional[str] = Query(None, description="Código da Unidade Gestora Emitente da Programação Financeira"),
    ug_favorecida_programacao: Optional[str] = Query(None, description="Código da Unidade Gestora Favorecida da Programação Financeira"),
    dh_recebimento_programacao: Optional[str] = Query(None, description="Data do Recebimento da Programação Financeira", pattern="^\d{4}-\d{2}-\d{2}$"),
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
        query = select(models.ProgramacaoFinanceira).where(
            and_(
                models.ProgramacaoFinanceira.id_programacao == id_programacao if id_programacao is not None else True,
                models.ProgramacaoFinanceira.id_plano_acao == id_plano_acao if id_plano_acao is not None else True,
                models.ProgramacaoFinanceira.tp_pf_tipo_programacao.ilike(tp_pf_tipo_programacao) if tp_pf_tipo_programacao is not None else True,
                models.ProgramacaoFinanceira.tx_minuta_programacao == tx_minuta_programacao if tx_minuta_programacao is not None else True,
                models.ProgramacaoFinanceira.tx_numero_programacao == tx_numero_programacao if tx_numero_programacao is not None else True,
                models.ProgramacaoFinanceira.tx_situacao_programacao.ilike(f"%{tx_situacao_programacao}%") if tx_situacao_programacao is not None else True,
                models.ProgramacaoFinanceira.tx_observacao_programacao.ilike(f"%{tx_observacao_programacao}%") if tx_observacao_programacao is not None else True,
                models.ProgramacaoFinanceira.ug_emitente_programacao == ug_emitente_programacao if ug_emitente_programacao is not None else True,
                models.ProgramacaoFinanceira.ug_favorecida_programacao == ug_favorecida_programacao if ug_favorecida_programacao is not None else True,
                cast(models.ProgramacaoFinanceira.dh_recebimento_programacao, Date) == date.fromisoformat(dh_recebimento_programacao) if dh_recebimento_programacao is not None else True,
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