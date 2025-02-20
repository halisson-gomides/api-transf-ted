
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    CACHE_SERVER_URL: str        
    CACHE_TTL: str = "30m"  
    CACHE_EARLY_TTL: str = "28m"  
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_TAGS: list = [
        {
            "name": "Programa",
            "description": "Dados relativos aos Programas - TED.",
        },
        {
            "name": "Programa - Beneficiário",
            "description": "Dados relativos aos Beneficiários dos Programas - TED.",
        },
        {
            "name": "Programa - Ação Orçamentária",
            "description": "Dados relativos a Ações Orçamentárias dos Programas - TED.",
        },
        {
            "name": "Plano de Ação",
            "description": "Dados relativos a Planos de Ação - TED.",
        },
        {
            "name": "Plano de Ação - Meta",
            "description": "Dados relativos a Metas dos Planos de Ação - TED.",
        },
        {
            "name": "Plano de Ação - Etapa",
            "description": "Dados relativos às Etapas dos Planos de Ação - TED.",
        },
        {
            "name": "Plano de Ação - Análise",
            "description": "Dados relativos às Análises dos Planos de Ação - TED.",
        },
        {
            "name": "Plano de Ação - Parecer",
            "description": "Dados relativos aos Pareceres dos Planos de Ação - TED",
        },
        {
            "name": "Termo de Execução",
            "description": "Dados relativos aos Termos de Execução - TED",
        },
        {
            "name": "Nota de Crédito",
            "description": "Dados relativos às Notas de Crédito - TED.",
        },
        {
            "name": "Evento",
            "description": "Dados relativos aos Eventos - TED",
        },
        {
            "name": "Programação Financeira",
            "description": "Dados relativos a Programações Financeiras - TED",
        },
        {
            "name": "TRF",
            "description": "Dados relativos ao TRF - TED",
        },
    ]
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 200
    ERROR_MESSAGE_NO_PARAMS: str = "Nenhum parâmetro de consulta foi informado."
    ERROR_MESSAGE_INTERNAL: str = "Erro Interno Inesperado."