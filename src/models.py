from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional

db_schema = 'api_transferegov_ted'

class BaseModel(SQLModel, table=False):
    __table_args__ = {"schema": db_schema}


# Tabela nota_credito
class NotaCredito(BaseModel, table=True):
    __tablename__ = "nota_credito"
    
    id_nota: int = Field(primary_key=True)
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao")
    tx_minuta_nota: str | None = None
    tx_numero_nota: str | None = None
    dt_emissao_nota: datetime | None = None
    cd_gestao_emitente_nota: str | None = None
    cd_gestao_favorecida_nota: str | None = None
    tx_situacao_nota: str | None = None
    cd_ug_emitente_nota: str | None = None
    cd_ug_favorecida_nota: str | None = None
    tx_observacao_nota: str | None = None


# Tabela evento
class Evento(BaseModel, table=True):
    __tablename__ = "evento"
    
    id_nota: int = Field(foreign_key=f"{db_schema}.nota_credito.id_nota", primary_key=True)
    cd_evento: str | None = None
    cd_ptres_evento: str | None = None
    cd_fonte_recurso_evento: str | None = None
    cd_plano_interno_evento: str | None = None
    vl_evento: float | None = None
    cd_ug_responsavel_evento: str | None = None
    codigo_natureza: str = Field(primary_key=True)
    descricao_natureza: str | None = None
    nome_esfera_orcamentaria: str | None = None
    

# Tabela plano_acao
class PlanoAcao(BaseModel, table=True):
    __tablename__ = "plano_acao"
    
    id_plano_acao: int = Field(primary_key=True)
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa")
    sigla_unidade_descentralizada: str | None = None
    unidade_descentralizada: str | None = None
    sigla_unidade_responsavel_execucao: str | None = None
    unidade_responsavel_execucao: str | None = None
    vl_total_plano_acao: float | None = None
    dt_inicio_vigencia: date | None = None
    dt_fim_vigencia: date | None = None
    tx_objeto_plano_acao: str | None = None
    tx_justificativa_plano_acao: str | None = None
    in_forma_execucao_direta: bool | None = None
    in_forma_execucao_particulares: bool | None = None
    in_forma_execucao_descentralizada: bool | None = None
    tx_situacao_plano_acao: str | None = None
    aa_ano_plano_acao: int | None = None
    vl_beneficiario_especifico: float | None = None
    vl_chamamento_publico: float | None = None
    sq_instrumento: str | None = None
    aa_instrumento: int | None = None


# Tabela plano_acao_analise
class PlanoAcaoAnalise(BaseModel, table=True):
    __tablename__ = "plano_acao_analise"
    
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao")
    id_analise: int = Field(primary_key=True)
    tx_justificativa_analise: str | None = None
    resultado_analise: str | None = None
    tx_situacao_analise: str | None = None


# Tabela plano_acao_etapa
class PlanoAcaoEtapa(BaseModel, table=True):
    __tablename__ = "plano_acao_etapa"
    
    id_etapa: int = Field(primary_key=True)
    id_meta: int = Field(foreign_key=f"{db_schema}.plano_acao_meta.id_meta")
    nr_numero_etapa: int | None = None
    tx_nome_etapa: str | None = None
    tx_descricao_etapa: str | None = None
    nr_quantidade_etapa: int | None = None
    vl_valor_unitario_etapa: float | None = None
    dt_inicio_vigencia_etapa: date | None = None
    dt_fim_vigencia_etapa: date | None = None
    unidade_medida_etapa: str | None = None


# Tabela plano_acao_meta
class PlanoAcaoMeta(BaseModel, table=True):
    __tablename__ = "plano_acao_meta"
    
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao")
    id_meta: int = Field(primary_key=True)
    nr_numero_meta: int | None = None
    tx_nome_meta: str | None = None
    tx_descricao_meta: str | None = None
    tp_unidade_meta: str | None = None
    nr_quantidade_meta: int | None = None
    vl_valor_unitario_meta: float | None = None
    dt_inicio_vigencia_meta: date | None = None
    dt_fim_vigencia_meta: date | None = None


# Tabela plano_acao_parecer
class PlanoAcaoParecer(BaseModel, table=True):
    __tablename__ = "plano_acao_parecer"
    
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao")
    id_parecer: int = Field(primary_key=True)
    tp_analise_parecer: str | None = None
    resultado_parecer: str | None = None
    tx_parecer: str | None = None
    plano_acao_hist_fk: int | None = None
    dt_data_parecer: datetime | None = None


# Tabela programa
class Programa(BaseModel, table=True):
    __tablename__ = "programa"
    
    id_programa: int = Field(primary_key=True)
    tx_codigo_programa: str | None = None
    aa_ano_programa: int | None = None
    tx_situacao_programa: str | None = None
    tx_nome_programa: str | None = None
    sigla_unidade_descentralizadora: str | None = None
    unidade_descentralizadora: str | None = None
    sigla_unidade_responsavel_acompanhamento: str | None = None
    unidade_responsavel_acompanhamento: str | None = None
    tx_nome_institucional_programa: str | None = None
    tx_objetivo_programa: str | None = None
    tx_descricao_programa: str | None = None
    in_grupo_investimento_obra: bool | None = None
    in_grupo_investimento_servico: bool | None = None
    in_grupo_investimento_equipamento: bool | None = None
    in_autoriza_subdescentralizacao_outro: str | None = None
    in_autoriza_realizacao_despesas: str | None = None
    in_autoriza_execucao_creditos_descentralizada: str | None = None
    in_beneficiario_especifico: bool | None = None
    dt_recebimento_plano_beneficiario_inicio: date | None = None
    dt_recebimento_plano_beneficiario_fim: date | None = None
    in_chamamento_publico: bool | None = None
    dt_recebimento_plano_chamamento_inicio: date | None = None
    dt_recebimento_plano_chamamento_fim: date | None = None


# Tabela programa_acao_orcamentaria
class ProgramaAcaoOrcamentaria(BaseModel, table=True):
    __tablename__ = "programa_acao_orcamentaria"
    
    tx_codigo_acao_orcamentaria: str = Field(primary_key=True)
    tx_descricao_acao_orcamentaria: str | None = None
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa")


# Tabela programa_beneficiario
class ProgramaBeneficiario(BaseModel, table=True):
    __tablename__ = "programa_beneficiario"
    
    tx_codigo_siorg: str = Field(primary_key=True)
    tx_nome_beneficiario: str | None = None
    vl_valor_beneficiario: float | None = None
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa")


# Tabela programacao_financeira
class ProgramacaoFinanceira(BaseModel, table=True):
    __tablename__ = "programacao_financeira"
    
    id_programacao: int = Field(primary_key=True)
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao")
    tp_pf_tipo_programacao: str | None = None
    tx_minuta_programacao: str | None = None
    tx_numero_programacao: str | None = None
    tx_situacao_programacao: str | None = None
    tx_observacao_programacao: str | None = None
    ug_emitente_programacao: str | None = None
    ug_favorecida_programacao: str | None = None
    dh_recebimento_programacao: datetime | None = None


# Tabela termo_execucao
class TermoExecucao(BaseModel, table=True):
    __tablename__ = "termo_execucao"
    
    id_termo: int = Field(primary_key=True)
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao.id_plano_acao")
    tx_situacao_termo: str | None = None
    tx_num_processo_sei: str | None = None
    dt_assinatura_termo: date | None = None
    dt_divulgacao_termo: date | None = None
    in_minuta_padrao: bool | None = None
    tx_numero_ns_termo: str | None = None
    dt_recebimento_termo: datetime | None = None
    dt_efetivacao_termo: datetime | None = None


# Tabela trf
class Trf(BaseModel, table=True):
    __tablename__ = "trf"
    
    id_programacao: int = Field(foreign_key=f"{db_schema}.programacao_financeira.id_programacao")
    cd_vinculacao_trf: int = Field(primary_key=True)
    cd_fonte_recurso_trf: str = Field(primary_key=True)
    cd_categoria_gasto_trf: str = Field(primary_key=True)
    vl_valor_trf: float | None = None
    cd_situacao_contabil_trf: str | None = None