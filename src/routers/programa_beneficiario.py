from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaBeneficiarioResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

pgb_router = APIRouter(tags=["Programa - Beneficiário"])
config = Settings()


@pgb_router.get("/programa_beneficiario",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Beneficiários dos Programas - TED.",
                response_description="Lista Paginada de Beneficiários dos Programas - TED",
                response_model=PaginatedProgramaBeneficiarioResponse
                )
@cache.early(ttl=config.CACHE_TTL, early_ttl=config.CACHE_EARLY_TTL)
async def consulta_programa_beneficiario_ted(
    tx_codigo_siorg: Optional[str] = Query(None, description="Código SIORG"),
    tx_nome_beneficiario: Optional[str] = Query(None, description="Nome do Beneficiário"),
    vl_valor_beneficiario: Optional[float] = Query(None, description="Valor do Beneficiário"),
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
        query = select(models.ProgramaBeneficiario).where(
            and_(
                models.ProgramaBeneficiario.tx_codigo_siorg == tx_codigo_siorg if tx_codigo_siorg else True,
                models.ProgramaBeneficiario.tx_nome_beneficiario.ilike(f"%{tx_nome_beneficiario}%") if tx_nome_beneficiario else True,
                models.ProgramaBeneficiario.vl_valor_beneficiario == vl_valor_beneficiario if vl_valor_beneficiario else True,
                models.ProgramaBeneficiario.id_programa == id_programa if id_programa else True
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