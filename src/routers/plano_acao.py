from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAcaoResponse
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

pa_router = APIRouter(tags=["Plano de Ação"])
config = Settings()


@pa_router.get("/plano_acao",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Planos de Ação - TED.",
                response_description="Lista Paginada de Planos de Ação - TED",
                response_model=PaginatedPlanoAcaoResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_plano_acao_ted(
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação"),
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),
    sigla_unidade_descentralizada: Optional[str] = Query(None, description="Sigla da Unidade Descentralizada"),
    unidade_descentralizada: Optional[str] = Query(None, description="Unidade Descentralizada"),
    sigla_unidade_responsavel_execucao: Optional[str] = Query(None, description="Sigla da Unidade Responsável da Execução"),
    unidade_responsavel_execucao: Optional[str] = Query(None, description="Unidade Responsável da Execução"),
    vl_total_plano_acao: Optional[float] = Query(None, description="Valor Total do Plano de Ação"),
    dt_inicio_vigencia: Optional[str] = Query(None, description="Data do Início da Vigência do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    dt_fim_vigencia: Optional[str] = Query(None, description="Data Final da Vigência do Plano de Ação", pattern="^\d{4}-\d{2}-\d{2}$"),
    tx_objeto_plano_acao: Optional[str] = Query(None, description="Objeto do Plano de Ação"),
    tx_justificativa_plano_acao: Optional[str] = Query(None, description="Justificativa do Plano de Ação"),
    in_forma_execucao_direta: Optional[bool] = Query(None, description="Indicador da Forma de Execução Direta"),
    in_forma_execucao_particulares: Optional[bool] = Query(None, description="Indicador da Forma de Execução Particulares"),
    in_forma_execucao_descentralizada: Optional[bool] = Query(None, description="Indicador da Forma de Execução Descentralizada"),
    tx_situacao_plano_acao: Optional[str] = Query(None, description="Situação do Plano de Ação"),
    aa_ano_plano_acao: Optional[int] = Query(None, description="Ano do Plano de Ação", gt=0),
    vl_beneficiario_especifico: Optional[float] = Query(None, description="Valor do Beneficiário Específico"),
    vl_chamamento_publico: Optional[float] = Query(None, description="Valor do Chamamento Público"),
    sq_instrumento: Optional[str] = Query(None, description="Sequencial do Instrumento"),
    aa_instrumento: Optional[int] = Query(None, description="Ano do Instrumento", gt=0),
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
        query = select(models.PlanoAcao).where(
            and_(
                models.PlanoAcao.id_plano_acao == id_plano_acao if id_plano_acao else True,
                models.PlanoAcao.id_programa == id_programa if id_programa else True,
                models.PlanoAcao.sigla_unidade_descentralizada.ilike(f"%{sigla_unidade_descentralizada}%") if sigla_unidade_descentralizada else True,
                models.PlanoAcao.unidade_descentralizada.ilike(f"%{unidade_descentralizada}%") if unidade_descentralizada else True,
                models.PlanoAcao.sigla_unidade_responsavel_execucao.ilike(f"%{sigla_unidade_responsavel_execucao}%") if sigla_unidade_responsavel_execucao else True,
                models.PlanoAcao.unidade_responsavel_execucao.ilike(f"%{unidade_responsavel_execucao}%") if unidade_responsavel_execucao else True,
                models.PlanoAcao.vl_total_plano_acao == vl_total_plano_acao if vl_total_plano_acao else True,
                cast(models.PlanoAcao.dt_inicio_vigencia, Date) == date.fromisoformat(dt_inicio_vigencia) if dt_inicio_vigencia else True,
                cast(models.PlanoAcao.dt_fim_vigencia, Date) == date.fromisoformat(dt_fim_vigencia) if dt_fim_vigencia else True,
                models.PlanoAcao.tx_objeto_plano_acao.ilike(f"%{tx_objeto_plano_acao}%") if tx_objeto_plano_acao else True,
                models.PlanoAcao.tx_justificativa_plano_acao == tx_justificativa_plano_acao if tx_justificativa_plano_acao else True,
                models.PlanoAcao.in_forma_execucao_direta == in_forma_execucao_direta if in_forma_execucao_direta is not None else True,
                models.PlanoAcao.in_forma_execucao_particulares == in_forma_execucao_particulares if in_forma_execucao_particulares is not None else True,
                models.PlanoAcao.in_forma_execucao_descentralizada == in_forma_execucao_descentralizada if in_forma_execucao_descentralizada is not None else True,
                models.PlanoAcao.tx_situacao_plano_acao.ilike(f"%{tx_situacao_plano_acao}%") if tx_situacao_plano_acao else True,
                models.PlanoAcao.aa_ano_plano_acao == aa_ano_plano_acao if aa_ano_plano_acao else True,
                models.PlanoAcao.vl_beneficiario_especifico == vl_beneficiario_especifico if vl_beneficiario_especifico else True,
                models.PlanoAcao.vl_chamamento_publico == vl_chamamento_publico if vl_chamamento_publico else True,
                models.PlanoAcao.sq_instrumento == sq_instrumento if sq_instrumento else True,
                models.PlanoAcao.aa_instrumento == aa_instrumento if aa_instrumento else True
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
                            detail=e.__repr__())