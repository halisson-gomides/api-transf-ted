from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedNotaCreditoResponse
from datetime import date
from typing import Optional
from src.cache import cache

ndc_router = APIRouter(tags=["Nota de Crédito"])

@ndc_router.get("/nota_credito",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Nota de Crédito - TED.",
                response_description="Lista Paginada de Notas de Crédito relativas aos Planos de Ação - TED",
                response_model=PaginatedNotaCreditoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_nota_credito_ted(
    id_nota: Optional[int] = Query(None, description="Identificador Único da Nota de Crédito"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    tx_minuta_nota: Optional[str] = Query(None, description="Minuta da Nota de Crédito"),
    tx_numero_nota: Optional[str] = Query(None, description="Número da Nota de Crédito"),
    dt_emissao_nota: Optional[str] = Query(None, description="Data de Emissão da Nota de Crédito", pattern="^\d{4}-\d{2}-\d{2}$"),
    cd_gestao_emitente_nota: Optional[str] = Query(None, description="Código da Gestão Emitente da Nota de Crédito"),
    cd_gestao_favorecida_nota: Optional[str] = Query(None, description="Código da Gestão Favorecida da Nota de Crédito"),
    tx_situacao_nota: Optional[str] = Query(None, description="Situação da Nota de Crédito"),
    cd_ug_emitente_nota: Optional[str] = Query(None, description="Código da Unidade Gestora Emitente da Nota de Crédito"),
    cd_ug_favorecida_nota: Optional[str] = Query(None, description="Código da Unidade Gestora Favorecida da Nota de Crédito"),
    tx_observacao_nota: Optional[str] = Query(None, description="Observação da Nota de Crédito"),
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
        query = select(models.NotaCredito).where(
            and_(
                models.NotaCredito.id_nota == id_nota if id_nota is not None else True,
                models.NotaCredito.id_plano_acao == id_plano_acao if id_plano_acao is not None else True,
                models.NotaCredito.tx_minuta_nota == tx_minuta_nota if tx_minuta_nota is not None else True,
                models.NotaCredito.tx_numero_nota == tx_numero_nota if tx_numero_nota is not None else True,
                cast(models.NotaCredito.dt_emissao_nota, Date) == date.fromisoformat(dt_emissao_nota) if dt_emissao_nota is not None else True,
                models.NotaCredito.cd_gestao_emitente_nota == cd_gestao_emitente_nota if cd_gestao_emitente_nota is not None else True,
                models.NotaCredito.cd_gestao_favorecida_nota == cd_gestao_favorecida_nota if cd_gestao_favorecida_nota is not None else True,
                models.NotaCredito.tx_situacao_nota.ilike(f"%{tx_situacao_nota}%") if tx_situacao_nota is not None else True,
                models.NotaCredito.cd_ug_emitente_nota == cd_ug_emitente_nota if cd_ug_emitente_nota is not None else True,
                models.NotaCredito.cd_ug_favorecida_nota == cd_ug_favorecida_nota if cd_ug_favorecida_nota is not None else True,
                models.NotaCredito.tx_observacao_nota.ilike(f"%{tx_observacao_nota}%") if tx_observacao_nota is not None else True
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