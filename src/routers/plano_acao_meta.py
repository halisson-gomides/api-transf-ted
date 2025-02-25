from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoMetaResponse
from datetime import date
from typing import Optional
from src.cache import cache

pam_router = APIRouter(tags=["Plano de Ação - Meta"])


@pam_router.get("/plano_acao_meta",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Metas dos Planos de Ação - TED.",
                response_description="Lista Paginada de Metas relativas aos Planos de Ação - TED",
                response_model=PaginatedPlanoAcaoMetaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_meta_plano_acao_ted(
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    id_meta: Optional[int] = Query(None, description="Identificador Único da Meta"),
    nr_numero_meta: Optional[int] = Query(None, description="Número da Meta do Plano de Ação", ge=0),
    tx_nome_meta: Optional[str] = Query(None, description="Nome da Meta do Plano de Ação"),
    tx_descricao_meta: Optional[str] = Query(None, description="Descrição da Meta do Plano de Ação"),
    tp_unidade_meta: Optional[str] = Query(None, description="Tipo de Unidade da Meta do Plano de Ação"),
    nr_quantidade_meta: Optional[int] = Query(None, description="Número de Quantidade da Meta do Plano de Ação"),
    vl_valor_unitario_meta: Optional[float] = Query(None, description="Valor Unitário da Meta do Plano de Ação"),
    dt_inicio_vigencia_meta: Optional[str] = Query(None, description="Data de Início da Vigência de Meta do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    dt_fim_vigencia_meta: Optional[str] = Query(None, description="Data Final da Vigência de Meta do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
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
        query = select(models.PlanoAcaoMeta).where(
            and_(
                models.PlanoAcaoMeta.id_plano_acao == id_plano_acao if id_plano_acao else True,
                models.PlanoAcaoMeta.id_meta == id_meta if id_meta else True,
                models.PlanoAcaoMeta.nr_numero_meta == nr_numero_meta if nr_numero_meta is not None else True,
                models.PlanoAcaoMeta.tx_nome_meta.ilike(f"%{tx_nome_meta}%") if tx_nome_meta else True,
                models.PlanoAcaoMeta.tx_descricao_meta.ilike(f"%{tx_descricao_meta}%") if tx_descricao_meta else True,
                models.PlanoAcaoMeta.tp_unidade_meta == tp_unidade_meta if tp_unidade_meta else True,
                models.PlanoAcaoMeta.nr_quantidade_meta == nr_quantidade_meta if nr_quantidade_meta else True,
                models.PlanoAcaoMeta.vl_valor_unitario_meta == vl_valor_unitario_meta if vl_valor_unitario_meta else True,
                cast(models.PlanoAcaoMeta.dt_inicio_vigencia_meta, Date) == date.fromisoformat(dt_inicio_vigencia_meta) if dt_inicio_vigencia_meta else True,
                cast(models.PlanoAcaoMeta.dt_fim_vigencia_meta, Date) == date.fromisoformat(dt_fim_vigencia_meta) if dt_fim_vigencia_meta else True
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