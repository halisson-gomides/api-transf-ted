from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaResponse
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

pg_router = APIRouter(tags=["Programa"])
config = Settings()


@pg_router.get("/programa",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Programas - TED.",
                response_description="Lista Paginada de Programas - TED",
                response_model=PaginatedProgramaResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_programa_ted(
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),
    tx_codigo_programa: Optional[str] = Query(None, description="Código do Programa"),
    aa_ano_programa: Optional[int] = Query(None, description="Ano do Programa", gt=0),
    tx_situacao_programa: Optional[str] = Query(None, description="Situação do Programa"),
    tx_nome_programa: Optional[str] = Query(None, description="Nome do Programa"),
    sigla_unidade_descentralizadora: Optional[str] = Query(None, description="Sigla da Unidade Descentralizadora"),
    unidade_descentralizadora: Optional[str] = Query(None, description="Unidade Descentralizadora"),
    sigla_unidade_responsavel_acompanhamento: Optional[str] = Query(None, description="Sigla da Unidade Responsável do Acompanhamento"),
    unidade_responsavel_acompanhamento: Optional[str] = Query(None, description="Unidade Responsável do Acompanhamento"),
    tx_nome_institucional_programa: Optional[str] = Query(None, description="Nome Institucional do Programa"),
    tx_objetivo_programa: Optional[str] = Query(None, description="Objetivo do Programa"),
    tx_descricao_programa: Optional[str] = Query(None, description="Descrição do Programa"),
    in_grupo_investimento_obra: Optional[bool] = Query(None, description="Indicador do Grupo de Investimento da Obra"),
    in_grupo_investimento_servico: Optional[bool] = Query(None, description="Indicador do Grupo de Investimento de Serviço"),
    in_grupo_investimento_equipamento: Optional[bool] = Query(None, description="Indicador do Grupo de Investimento de Equipamento"),
    in_autoriza_subdescentralizacao_outro: Optional[str] = Query(None, description="Indicador Autoriza Subdescentralização de Outro"),
    in_autoriza_realizacao_despesas: Optional[str] = Query(None, description="Indicador Autoriza Relização de Despesas"),
    in_autoriza_execucao_creditos_descentralizada: Optional[str] = Query(None, description="Indicador Autoriza Execução de Créditos Descentralizada"),
    in_beneficiario_especifico: Optional[bool] = Query(None, description="Indicador de Beneficiário Específico"),
    dt_recebimento_plano_beneficiario_inicio: Optional[str] = Query(None, description="Data de Início do Recebimento do Plano de Beneficiário", pattern="^\d{4}-\d{2}-\d{2}$"),
    dt_recebimento_plano_beneficiario_fim: Optional[str] = Query(None, description="Data Final do Recebimento do Plano de Beneficiário", pattern="^\d{4}-\d{2}-\d{2}$"),
    in_chamamento_publico: Optional[bool] = Query(None, description="Indicador de Chamamento Público"),
    dt_recebimento_plano_chamamento_inicio: Optional[str] = Query(None, description="Data de Início do Recebimento do Plano de Chamamento", pattern="^\d{4}-\d{2}-\d{2}$"),
    dt_recebimento_plano_chamamento_fim: Optional[str] = Query(None, description="Data Final do Recebimento do Plano de Chamamento", pattern="^\d{4}-\d{2}-\d{2}$"),
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
        query = select(models.Programa).where(
            and_(
                models.Programa.id_programa == id_programa if id_programa else True,
                models.Programa.tx_codigo_programa == tx_codigo_programa if tx_codigo_programa else True,
                models.Programa.aa_ano_programa == aa_ano_programa if aa_ano_programa else True,
                models.Programa.tx_situacao_programa.ilike(f"%{tx_situacao_programa}%") if tx_situacao_programa else True,
                models.Programa.tx_nome_programa.ilike(f"%{tx_nome_programa}%") if tx_nome_programa else True,
                models.Programa.sigla_unidade_descentralizadora == sigla_unidade_descentralizadora if sigla_unidade_descentralizadora else True,
                models.Programa.unidade_descentralizadora.ilike(f"%{unidade_descentralizadora}%") if unidade_descentralizadora else True,
                models.Programa.sigla_unidade_responsavel_acompanhamento == sigla_unidade_responsavel_acompanhamento if sigla_unidade_responsavel_acompanhamento else True,
                models.Programa.unidade_responsavel_acompanhamento.ilike(f"%{unidade_responsavel_acompanhamento}%") if unidade_responsavel_acompanhamento else True,
                models.Programa.tx_nome_institucional_programa.ilike(f"%{tx_nome_institucional_programa}%") if tx_nome_institucional_programa else True,
                models.Programa.tx_objetivo_programa.ilike(f"%{tx_objetivo_programa}%") if tx_objetivo_programa else True,
                models.Programa.tx_descricao_programa.ilike(f"%{tx_descricao_programa}%") if tx_descricao_programa else True,
                models.Programa.in_grupo_investimento_obra == in_grupo_investimento_obra if in_grupo_investimento_obra is not None else True,
                models.Programa.in_grupo_investimento_servico == in_grupo_investimento_servico if in_grupo_investimento_servico is not None else True,
                models.Programa.in_grupo_investimento_equipamento == in_grupo_investimento_equipamento if in_grupo_investimento_equipamento is not None else True,
                models.Programa.in_autoriza_subdescentralizacao_outro == in_autoriza_subdescentralizacao_outro if in_autoriza_subdescentralizacao_outro is not None else True,
                models.Programa.in_autoriza_realizacao_despesas == in_autoriza_realizacao_despesas if in_autoriza_realizacao_despesas is not None else True,
                models.Programa.in_autoriza_execucao_creditos_descentralizada == in_autoriza_execucao_creditos_descentralizada if in_autoriza_execucao_creditos_descentralizada is not None else True,
                models.Programa.in_beneficiario_especifico == in_beneficiario_especifico if in_beneficiario_especifico is not None else True,
                cast(models.Programa.dt_recebimento_plano_beneficiario_inicio, Date) == date.fromisoformat(dt_recebimento_plano_beneficiario_inicio) if dt_recebimento_plano_beneficiario_inicio else True,
                cast(models.Programa.dt_recebimento_plano_beneficiario_fim, Date) == date.fromisoformat(dt_recebimento_plano_beneficiario_fim) if dt_recebimento_plano_beneficiario_fim else True,
                models.Programa.in_chamamento_publico == in_chamamento_publico if in_chamamento_publico else True,
                cast(models.Programa.dt_recebimento_plano_chamamento_inicio, Date) == date.fromisoformat(dt_recebimento_plano_chamamento_inicio) if dt_recebimento_plano_chamamento_inicio else True,
                cast(models.Programa.dt_recebimento_plano_chamamento_fim, Date) == date.fromisoformat(dt_recebimento_plano_chamamento_fim) if dt_recebimento_plano_chamamento_fim else True
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
                            #detail=config.ERROR_MESSAGE_INTERNAL