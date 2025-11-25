# Arquivo: executar_agent.py

# Importa o agente configurado e a ferramenta de consulta
from Chappie.agent1 import root_agent, consultar_sqlite 

def simular_execucao_agent(agent, prompt_usuario):
    """
    Simula a chamada de execução do agente, onde ele decide usar a ferramenta.
    
    Em seu ambiente, você chamaria algo como:
    response = agent.run(prompt=prompt_usuario)
    print(response.text)
    """
    print(f"--- 👤 PROMPT DO USUÁRIO ---")
    print(prompt_usuario)
    print("-" * 30)

    # --- ETAPA 1: Geração da SQL pelo Modelo ---
    # Na vida real, o modelo Gemini 2.0-flash gera a chamada para a ferramenta.
    print("--- 🤖 AGENTE: DECISÃO DE FERRAMENTA ---")
    print("Modelo gerando a chamada da ferramenta 'consultar_sqlite'...")

    # Exemplo de SQL que o modelo DEVERIA gerar para o prompt de exemplo
    sql_query_exemplo = """
        SELECT municipio, SUM(feridos + mortos) as total_vitimas 
        FROM acidentes 
        WHERE uf = 'SP' AND data_hora BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59' 
        GROUP BY municipio 
        ORDER BY total_vitimas DESC 
        LIMIT 5
    """
    print(f"\nSQL Gerada:\n{sql_query_exemplo}")
    print("-" * 30)

    # --- ETAPA 2: Execução da Ferramenta ---
    print("--- 🔨 EXECUÇÃO DA FERRAMENTA 'consultar_sqlite' ---")
    resultado = consultar_sqlite(sql_query_exemplo)

    if "erro" in resultado:
        print(f"ERRO DE SQL: {resultado['erro']}")
        return

    # A saída da ferramenta é passada de volta ao modelo para análise
    print(f"Ferramenta executada com sucesso. (Colunas: {len(resultado['colunas'])}, Linhas: {len(resultado['dados'])})")
    print("-" * 30)

    # --- ETAPA 3: Análise e Geração da Resposta Final ---
    print("--- 🧠 AGENTE: ANÁLISE E RESPOSTA FINAL (Formato Estruturado) ---")
    # Aqui, o modelo pega o 'resultado' e formata no padrão definido no prompt.
    
    resposta_simulada = f"""
    ## Resumo Executivo
    A análise focada na letalidade dos acidentes em São Paulo (2024) revela uma alta concentração de vítimas nos principais polos urbanos. Isso exige uma intervenção imediata e focada na fiscalização e engenharia de tráfego nos municípios mais críticos.

    ---

    ## Principais Descobertas
    * O município de **São Paulo** lidera, com mais de 50% das vítimas graves.
    * **Campinas** e **Guarulhos** aparecem em segundo e terceiro, indicando a criticidade das rotas de acesso e saída da capital.
    * A maior parte desses acidentes ocorre em trechos urbanos sob concessão.

    ---

    ## Riscos Identificados
    * **Risco Operacional:** Manutenção de altos índices de acidentes graves, com sobrecarga do sistema de saúde e segurança pública.
    * **Risco Reputacional:** A inação pode ser percebida como negligência na segurança viária.

    ---

    ## Oportunidades de Otimização
    * Focar a realocação de recursos (patrulhamento e radares) para os TOP 5 municípios, com ênfase nos horários de pico.
    * Coordenar ações com concessionárias para melhorias na sinalização e iluminação.

    ---

    ## Recomendações Diretas
    1.  **Implementar** um plano de fiscalização de velocidade (tolerância zero) nas BRs que cortam São Paulo, Campinas e Guarulhos.
    2.  **Iniciar** um diálogo formal com as concessionárias para auditar os pontos críticos (km e BR) identificados pela análise e exigir intervenções de engenharia.
    """
    
    print(resposta_simulada)

# --- EXECUÇÃO DO TESTE ---
# Pergunta de Exemplo para o Agente:
prompt = "Qual o TOP 5 de municípios com maior número de vítimas (feridos + mortos) em São Paulo no ano de 2024?"

simular_execucao_agent(root_agent, prompt)