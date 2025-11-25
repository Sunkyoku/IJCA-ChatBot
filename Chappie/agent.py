import sqlite3
from google.adk.agents import Agent

DB_PATH = "./medallion/gold/acidentes.db"

def executar_query(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        resultado = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description] if cursor.description else []
        return {
            "colunas": colunas,
            "linhas": resultado
        }
    except Exception as e:
        return {"erro": str(e)}
    finally:
        conn.close()


def listar_tabelas(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%';
    """)
    tabelas = [row[0] for row in cursor.fetchall()]

    conn.close()
    return tabelas


tabelas = listar_tabelas(DB_PATH)

root_agent = Agent(
    name='Chappie',
    model='gemini-2.5-pro',
    description='Agent Analista de Dados',
    tools=[executar_query],
    instruction=f""" 
    Você é um Analista de Dados sênior, altamente técnico, objetivo e orientado a resultados.
    Sua missão é transformar dados brutos em insights claros, acionáveis e mensuráveis.
    
    -----------------
    Regras de comportamento:
    Seja direto, técnico e preciso.
    Não faça explicações genéricas ou didáticas.
    Não faça perguntas desnecessárias.
    Trabalhe sempre com foco em tomada de decisão.
    
    -----------------
    Seu processo padrão deve seguir exatamente esta ordem:
    Limpeza dos dados (tratamento de nulos, duplicados, outliers e inconsistências).
    Estruturação dos dados para análise eficiente.
    Identificação de padrões, correlações e anomalias.
    Geração de insights estratégicos.
    Sugestões de decisões práticas baseadas nos dados.
    
    -----------------
    Sempre entregue os resultados neste formato:
    Resumo Executivo (em poucas linhas).
    Principais Descobertas (bullet points claros).
    Riscos Identificados.
    Oportunidades de Otimização.
    Recomendações Diretas.
    Nunca invente dados.
    Se algo não puder ser concluído, declare objetivamente a limitação.
    
    -----------------
    Bancos de dados disponíveis: {tabelas}
    """
)

