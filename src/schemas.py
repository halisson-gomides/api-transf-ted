from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from datetime import date, datetime


# Template para paginacao
class PaginatedResponseTemplate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    data: List[Any]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int
# --------------------------------------


class EventoResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_nota: int
    cd_evento: Optional[str]
    cd_ptres_evento: Optional[str]
    cd_fonte_recurso_evento: Optional[str]
    cd_plano_interno_evento: Optional[str]
    vl_evento: Optional[float]
    cd_ug_responsavel_evento: Optional[str]
    codigo_natureza: Optional[str]
    descricao_natureza: Optional[str]
    nome_esfera_orcamentaria: Optional[str]

class PaginatedEventoResponse(PaginatedResponseTemplate):
    data: List[EventoResponse]
   

class NotaCreditoResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_nota: int
    id_plano_acao: Optional[int]
    tx_minuta_nota: Optional[str]
    tx_numero_nota: Optional[str]
    dt_emissao_nota: Optional[datetime]
    cd_gestao_emitente_nota: Optional[str]
    cd_gestao_favorecida_nota: Optional[str]
    tx_situacao_nota: Optional[str]
    cd_ug_emitente_nota: Optional[str]
    cd_ug_favorecida_nota: Optional[str]
    tx_observacao_nota: Optional[str]


class PaginatedNotaCreditoResponse(PaginatedResponseTemplate):
    data: List[NotaCreditoResponse]
 

class PlanoAcaoResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_plano_acao: int
    id_programa: Optional[int]
    sigla_unidade_descentralizada: Optional[str]
    unidade_descentralizada: Optional[str]
    sigla_unidade_responsavel_execucao: Optional[str]
    unidade_responsavel_execucao: Optional[str]
    vl_total_plano_acao: Optional[float]
    dt_inicio_vigencia: Optional[date]
    dt_fim_vigencia: Optional[date]
    tx_objeto_plano_acao: Optional[str]
    tx_justificativa_plano_acao: Optional[str]
    in_forma_execucao_direta: Optional[bool]
    in_forma_execucao_particulares: Optional[bool]
    in_forma_execucao_descentralizada: Optional[bool]
    tx_situacao_plano_acao: Optional[str]
    aa_ano_plano_acao: Optional[int]
    vl_beneficiario_especifico: Optional[float]
    vl_chamamento_publico: Optional[float]
    sq_instrumento: Optional[str]
    aa_instrumento: Optional[int]


class PaginatedPlanoAcaoResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoResponse]
 

class PlanoAcaoAnaliseResponse(BaseModel):    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_plano_acao: int
    id_analise: Optional[int]
    tx_justificativa_analise: Optional[str]
    resultado_analise: Optional[str]
    tx_situacao_analise: Optional[str]


class PaginatedPlanoAcaoAnaliseResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoAnaliseResponse]


class PlanoAcaoEtapaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_etapa: Optional[int]
    id_meta: Optional[int]
    nr_numero_etapa: Optional[int]
    tx_nome_etapa: Optional[str]
    tx_descricao_etapa: Optional[str]
    nr_quantidade_etapa: Optional[int]
    vl_valor_unitario_etapa: Optional[float]
    dt_inicio_vigencia_etapa: Optional[date]
    dt_fim_vigencia_etapa: Optional[date]
    unidade_medida_etapa: Optional[str]


class PaginatedPlanoAcaoEtapaResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoEtapaResponse]


class PlanoAcaoMetaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_plano_acao: int
    id_meta: Optional[int]
    nr_numero_meta: Optional[int]
    tx_nome_meta: Optional[str]
    tx_descricao_meta: Optional[str]
    tp_unidade_meta: Optional[str]
    nr_quantidade_meta: Optional[int]
    vl_valor_unitario_meta: Optional[float]
    dt_inicio_vigencia_meta: Optional[date]
    dt_fim_vigencia_meta: Optional[date]


class PaginatedPlanoAcaoMetaResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoMetaResponse]


class PlanoAcaoParecerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_plano_acao: int
    id_parecer: Optional[int]
    tp_analise_parecer: Optional[str]
    resultado_parecer: Optional[str]
    tx_parecer: Optional[str]
    plano_acao_hist_fk: Optional[int]
    dt_data_parecer: Optional[datetime]


class PaginatedPlanoAcaoParecerResponse(PaginatedResponseTemplate):
    data: List[PlanoAcaoParecerResponse]


class ProgramaResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_programa: int
    tx_codigo_programa: Optional[str]
    aa_ano_programa: Optional[int]
    tx_situacao_programa: Optional[str]
    tx_nome_programa: Optional[str]
    sigla_unidade_descentralizadora: Optional[str]
    unidade_descentralizadora: Optional[str]
    sigla_unidade_responsavel_acompanhamento: Optional[str]
    unidade_responsavel_acompanhamento: Optional[str]
    tx_nome_institucional_programa: Optional[str]
    tx_objetivo_programa: Optional[str]
    tx_descricao_programa: Optional[str]
    in_grupo_investimento_obra: Optional[bool]
    in_grupo_investimento_servico: Optional[bool]
    in_grupo_investimento_equipamento: Optional[bool]
    in_autoriza_subdescentralizacao_outro: Optional[str]
    in_autoriza_realizacao_despesas: Optional[str]
    in_autoriza_execucao_creditos_descentralizada: Optional[str]
    in_beneficiario_especifico: Optional[bool]
    dt_recebimento_plano_beneficiario_inicio: Optional[date]
    dt_recebimento_plano_beneficiario_fim: Optional[date]
    in_chamamento_publico: Optional[bool]
    dt_recebimento_plano_chamamento_inicio: Optional[date]
    dt_recebimento_plano_chamamento_fim: Optional[date]


class PaginatedProgramaResponse(PaginatedResponseTemplate):
    data: List[ProgramaResponse]
 

class ProgramaAcaoOrcamentariaResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    tx_codigo_acao_orcamentaria: str
    tx_descricao_acao_orcamentaria: Optional[str]
    id_programa: Optional[int]


class PaginatedProgramaAcaoOrcamentariaResponse(PaginatedResponseTemplate):
    data: List[ProgramaAcaoOrcamentariaResponse]


class ProgramaBeneficiarioResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    tx_codigo_siorg: str
    tx_nome_beneficiario: Optional[str]
    vl_valor_beneficiario: Optional[float]
    id_programa: Optional[int]


class PaginatedProgramaBeneficiarioResponse(PaginatedResponseTemplate):
    data: List[ProgramaBeneficiarioResponse]


class ProgramacaoFinanceiraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_programacao: int
    id_plano_acao: Optional[int]
    tp_pf_tipo_programacao: Optional[str]
    tx_minuta_programacao: Optional[str]
    tx_numero_programacao: Optional[str]
    tx_situacao_programacao: Optional[str]
    tx_observacao_programacao: Optional[str]
    ug_emitente_programacao: Optional[str]
    ug_favorecida_programacao: Optional[str]
    dh_recebimento_programacao: Optional[datetime]


class PaginatedProgramacaoFinanceiraResponse(PaginatedResponseTemplate):
    data: List[ProgramacaoFinanceiraResponse]


class TermoExecucaoResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_termo: int
    id_plano_acao: Optional[int]
    tx_situacao_termo: Optional[str]
    tx_num_processo_sei: Optional[str]
    dt_assinatura_termo: Optional[date]
    dt_divulgacao_termo: Optional[date]
    in_minuta_padrao: Optional[bool]
    tx_numero_ns_termo: Optional[str]
    dt_recebimento_termo: Optional[datetime]
    dt_efetivacao_termo: Optional[datetime]


class PaginatedTermoExecucaoResponse(PaginatedResponseTemplate):
    data: List[TermoExecucaoResponse]


class TrfResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_programacao: int
    cd_vinculacao_trf: Optional[int]
    cd_fonte_recurso_trf: Optional[str]
    cd_categoria_gasto_trf: Optional[str]
    vl_valor_trf: Optional[float]
    cd_situacao_contabil_trf: Optional[str]


class PaginatedTrfResponse(PaginatedResponseTemplate):
    data: List[TrfResponse]