from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoEtapaResponse
from datetime import date
from typing import Optional
from src.cache import cache

pae_router = APIRouter(tags=["Plano de Ação - Etapa"])


@pae_router.get("/plano_acao_etapa",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Etapas dos Planos de Ação - TED.",
                response_description="Lista Paginada de Etapas relativas aos Planos de Ação - TED",
                response_model=PaginatedPlanoAcaoEtapaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_etapa_plano_acao_ted(
    id_etapa: Optional[int] = Query(None, description="Identificador Único da Etapa do Plano de Ação"),
    id_meta: Optional[int] = Query(None, description="Identificador Único da Meta"),
    nr_numero_etapa: Optional[int] = Query(None, description="Número da Etapa do Plano de Ação", ge=0),
    tx_nome_etapa: Optional[str] = Query(None, description="Nome da Etapa do Plano de Ação"),
    tx_descricao_etapa: Optional[str] = Query(None, description="Descrição da Etapa do Plano de Ação"),
    nr_quantidade_etapa: Optional[int] = Query(None, description="Número de Quantidade da Etapa do Plano de Ação"),
    vl_valor_unitario_etapa: Optional[float] = Query(None, description="Valor Unitário da Etapa do Plano de Ação"),
    dt_inicio_vigencia_etapa: Optional[str] = Query(None, description="Data de Início da Vigência da Etapa do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    dt_fim_vigencia_etapa: Optional[str] = Query(None, description="Data Final da Vigência da Etapa do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    unidade_medida_etapa: Optional[str] = Query(None, description="Unidade de Medida da Etapa do Plano de Ação"),
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
        query = select(models.PlanoAcaoEtapa).where(
            and_(
                models.PlanoAcaoEtapa.id_etapa == id_etapa if id_etapa is not None else True,
                models.PlanoAcaoEtapa.id_meta == id_meta if id_meta is not None else True,
                models.PlanoAcaoEtapa.nr_numero_etapa == nr_numero_etapa if nr_numero_etapa is not None else True,
                models.PlanoAcaoEtapa.tx_nome_etapa.ilike(f"%{tx_nome_etapa}%") if tx_nome_etapa is not None else True,
                models.PlanoAcaoEtapa.tx_descricao_etapa.ilike(f"%{tx_descricao_etapa}%") if tx_descricao_etapa is not None else True,
                models.PlanoAcaoEtapa.nr_quantidade_etapa == nr_quantidade_etapa if nr_quantidade_etapa is not None else True,
                models.PlanoAcaoEtapa.vl_valor_unitario_etapa == vl_valor_unitario_etapa if vl_valor_unitario_etapa is not None else True,
                cast(models.PlanoAcaoEtapa.dt_inicio_vigencia_etapa, Date) == date.fromisoformat(dt_inicio_vigencia_etapa) if dt_inicio_vigencia_etapa is not None else True,
                cast(models.PlanoAcaoEtapa.dt_fim_vigencia_etapa, Date) == date.fromisoformat(dt_fim_vigencia_etapa) if dt_fim_vigencia_etapa is not None else True,
                models.PlanoAcaoEtapa.unidade_medida_etapa.ilike(f"%{unidade_medida_etapa}%") if unidade_medida_etapa is not None else True
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