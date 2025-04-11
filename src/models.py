from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional

db_schema = 'api_transferegov_ted'

class BaseModel(SQLModel, table=False):
    __table_args__ = {"schema": db_schema}

# Tabela evento
class Evento(BaseModel, table=True):
    __tablename__ = "evento"
    
    id_nota: int = Field(primary_key=True)
    cd_evento: str
    cd_ptres_evento: str
    cd_fonte_recurso_evento: str
    cd_plano_interno_evento: str
    vl_evento: float
    cd_ug_responsavel_evento: str
    codigo_natureza: str = Field(primary_key=True)
    descricao_natureza: str
    nome_esfera_orcamentaria: str

# Tabela nota_credito
class NotaCredito(BaseModel, table=True):
    __tablename__ = "nota_credito"
    
    id_nota: int = Field(primary_key=True)
    id_plano_acao: int
    tx_minuta_nota: str
    tx_numero_nota: str
    dt_emissao_nota: datetime
    cd_gestao_emitente_nota: str
    cd_gestao_favorecida_nota: str
    tx_situacao_nota: str
    cd_ug_emitente_nota: str
    cd_ug_favorecida_nota: str
    tx_observacao_nota: str

# Tabela plano_acao
class PlanoAcao(BaseModel, table=True):
    __tablename__ = "plano_acao"
    
    id_plano_acao: int = Field(primary_key=True)
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa", primary_key=True)
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
    
    id_plano_acao: int = Field(primary_key=True)
    id_analise: int = Field(primary_key=True)
    tx_justificativa_analise: str
    resultado_analise: str
    tx_situacao_analise: str

# Tabela plano_acao_etapa
class PlanoAcaoEtapa(BaseModel, table=True):
    __tablename__ = "plano_acao_etapa"
    
    id_etapa: int = Field(primary_key=True)
    id_meta: int = Field(primary_key=True)
    nr_numero_etapa: int
    tx_nome_etapa: str
    tx_descricao_etapa: str
    nr_quantidade_etapa: int
    vl_valor_unitario_etapa: float
    dt_inicio_vigencia_etapa: date
    dt_fim_vigencia_etapa: date
    unidade_medida_etapa: str

# Tabela plano_acao_meta
class PlanoAcaoMeta(BaseModel, table=True):
    __tablename__ = "plano_acao_meta"
    
    id_plano_acao: int = Field(primary_key=True)
    id_meta: int = Field(primary_key=True)
    nr_numero_meta: int
    tx_nome_meta: str
    tx_descricao_meta: str
    tp_unidade_meta: str
    nr_quantidade_meta: int
    vl_valor_unitario_meta: float
    dt_inicio_vigencia_meta: date
    dt_fim_vigencia_meta: date

# Tabela plano_acao_parecer
class PlanoAcaoParecer(BaseModel, table=True):
    __tablename__ = "plano_acao_parecer"
    
    id_plano_acao: int = Field(primary_key=True)
    id_parecer: int = Field(primary_key=True)
    tp_analise_parecer: str
    resultado_parecer: str
    tx_parecer: str
    plano_acao_hist_fk: int
    dt_data_parecer: datetime

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
    tx_descricao_acao_orcamentaria: str
    id_programa: int = Field(primary_key=True)

# Tabela programa_beneficiario
class ProgramaBeneficiario(BaseModel, table=True):
    __tablename__ = "programa_beneficiario"
    
    tx_codigo_siorg: str = Field(primary_key=True)
    tx_nome_beneficiario: str
    vl_valor_beneficiario: float
    id_programa: int = Field(primary_key=True)

# Tabela programacao_financeira
class ProgramacaoFinanceira(BaseModel, table=True):
    __tablename__ = "programacao_financeira"
    
    id_programacao: int = Field(primary_key=True)
    id_plano_acao: int = Field(primary_key=True)
    tp_pf_tipo_programacao: str
    tx_minuta_programacao: str
    tx_numero_programacao: str
    tx_situacao_programacao: str
    tx_observacao_programacao: str
    ug_emitente_programacao: str
    ug_favorecida_programacao: str
    dh_recebimento_programacao: datetime

# Tabela termo_execucao
class TermoExecucao(BaseModel, table=True):
    __tablename__ = "termo_execucao"
    
    id_termo: int = Field(primary_key=True)
    id_plano_acao: int
    tx_situacao_termo: str
    tx_num_processo_sei: str
    dt_assinatura_termo: date
    dt_divulgacao_termo: date
    in_minuta_padrao: bool
    tx_numero_ns_termo: str
    dt_recebimento_termo: datetime
    dt_efetivacao_termo: datetime

# Tabela trf
class Trf(BaseModel, table=True):
    __tablename__ = "trf"
    
    id_programacao: int = Field(primary_key=True)
    cd_vinculacao_trf: int = Field(primary_key=True)
    cd_fonte_recurso_trf: str = Field(primary_key=True)
    cd_categoria_gasto_trf: str = Field(primary_key=True)
    vl_valor_trf: float
    cd_situacao_contabil_trf: str