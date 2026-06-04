import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import re
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================================
# RF01 DATASET DE VENDAS
# =========================================================================
def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com dados intencionalmente sujos."""
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares", "Tablet": "Celulares",
                  "Monitor": "Computadores", "Teclado": "Periféricos", "Mouse": "Periféricos",
                  "Headset": "Periféricos"}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    clientes = [f"Cliente_{i:03d}" for i in range(1, 51)]

    data_inicio = datetime(2024, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)
        preco_base = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
                      "Monitor": 1200, "Teclado": 250, "Mouse": 120, "Headset": 350}[produto]
        preco = round(preco_base * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))

        # Inserindo dados intencionalmente sujos para limpeza
        if random.random() < 0.05:
            quantidade = None          # valor nulo
        if random.random() < 0.04:
            preco = None               # valor nulo
        if random.random() < 0.03:
            produto = "  " + produto   # espaço extra (string suja)

        dados.append({
            "id_venda": i + 1,
            "data_venda": data.strftime("%Y-%m-%d") if random.random() > 0.02 else "DATA INVÁLIDA",
            "cliente": random.choice(clientes),
            "produto": produto,
            "categoria": categorias.get(produto.strip(), "Outros"),
            "regiao": random.choice(regioes),
            "quantidade": quantity if 'quantity' in locals() else quantidade, # Ajuste de segurança
            "preco_unitario": preco
        })

    return pd.DataFrame(dados)

# =========================================================================
# CÓDIGO PARA BULA / TESTE DE EXECUÇÃO
# =========================================================================
# Aqui nós chamamos a função para gerar os dados e salvamos em um arquivo CSV
df_bruto = gerar_dataset_vendas()
df_bruto.to_csv("vendas.csv", index=False)
print(f"Dataset gerado com {len(df_bruto)} registros.")
print(df_bruto.head())
# =========================================================================
# RF02 – INSPECTIONAR E DESCREVER OS DADOS
# =========================================================================
def inspecionar_dados(df):
    """Exibe as informações estruturais básicas do DataFrame."""
    print("\n" + "="*50)
    print("      RF02 - INSPEÇÃO INICIAL DOS DADOS BRUTOS")
    print("="*50)
    
    # 1. Dimensões do Dataset
    print(f"\n🔹 Dimensões do Dataset: {df.shape[0]} linhas e {df.shape[1]} colunas.")
    
    # 2. Visualização das primeiras linhas
    print("\n🔹 Primeiras 5 linhas do Dataset:")
    print(df.head())
    
    # 3. Informações dos tipos de colunas
    print("\n🔹 Informações das Colunas e Tipos de Dados:")
    print(df.info())
    
    # 4. Contagem de Valores Nulos
    print("\n🔹 Quantidade de Valores Nulos por Coluna:")
    nulos = df.isnull().sum()
    print(nulos[nulos > 0] if nulos.sum() > 0 else "Nenhum valor nulo encontrado.")
    print("="*50)

# =========================================================================
# EXECUÇÃO DO PIPELINE (Ponto de Entrada Inicial)
# =========================================================================
if __name__ == "__main__":
    # Passo 1: Gera os dados (RF01)
    df_vendas = df_vendas = gerar_dataset_vendas()
    
    # Salva o arquivo bruto em CSV para garantir o requisito de leitura/escrita
    df_vendas.to_csv("vendas.csv", index=False)
    print("✅ RF01: Dataset de vendas gerado e salvo como 'vendas.csv'.")
    
    # Passo 2: Inspeciona os dados brutos (RF02)
    inspecionar_dados(df_vendas)
    # =========================================================================
# RF03 – LIMPAR E TRATAR OS DADOS
# =========================================================================
def limpar_dados(df):
    """Realiza a limpeza de strings, tratamento de nulos e remoção de dados inválidos."""
    print("\n" + "="*50)
    print("      RF03 - LIMPEZA E TRATAMENTO DOS DADOS")
    print("="*50)
    
    # Criamos uma cópia para não alterar o DataFrame original bruto
    df_limpo = df.copy()
    
    # 1. Limpeza de espaços extras nas strings (Requisito RF13 - Expressões Regulares / Strings)
    print("🔹 Removendo espaços em branco extras nos nomes dos produtos...")
    df_limpo['produto'] = df_limpo['produto'].str.strip()
    
    # 2. Tratamento de Valores Nulos (Substituição pela mediana para evitar distorções)
    print("🔹 Tratando valores nulos em 'quantidade' e 'preco_unitario'...")
    mediana_qtd = df_limpo['quantidade'].median()
    mediana_preco = df_limpo['preco_unitario'].median()
    
    df_limpo['quantidade'] = df_limpo['quantidade'].fillna(mediana_qtd)
    df_limpo['preco_unitario'] = df_limpo['preco_unitario'].fillna(mediana_preco)
    
    # 3. Eliminar linhas com datas inválidas
    print("🔹 Filtrando e removendo registros com datas inválidas...")
    linhas_antes = len(df_limpo)
    df_limpo = df_limpo[df_limpo['data_venda'] != "DATA INVÁLIDA"]
    linhas_depois = len(df_limpo)
    print(f"👉 Removidos {linhas_antes - linhas_depois} registros com problemas de data.")
    
    # Converter a coluna de data para o tipo datetime correto do Python
    df_limpo['data_venda'] = pd.to_datetime(df_limpo['data_venda'])
    
    # Verificação final de nulos
    nulos_restantes = df_limpo.isnull().sum().sum()
    print(f"✅ Limpeza concluída! Valores nulos restantes: {nulos_restantes}")
    print("="*50)
    
    return df_limpo
# =========================================================================
# RF04 – COMPUTAR ESTATÍSTICAS DESCRITIVAS
# =========================================================================
def computar_estatisticas(df):
    """Calcula métricas estatísticas e financeiras do dataset limpo."""
    print("\n" + "="*50)
    print("      RF04 - ESTATÍSTICAS DESCRITIVAS GERAIS")
    print("="*50)
    
    # Criar uma coluna de Faturamento (Quantidade * Preço Unitário) para análise
    df['faturamento'] = df['quantidade'] * df['preco_unitario']
    
    # 1. Cálculos Gerais utilizando métodos do Pandas
    faturamento_total = df['faturamento'].sum()
    total_produtos = df['quantidade'].sum()
    preco_medio = df['preco_unitario'].mean()
    ticket_medio = df['faturamento'].mean()
    
    print(f"🔹 Faturamento Total: R$ {faturamento_total:,.2f}")
    print(f"🔹 Total de Itens Vendidos: {int(total_produtos)} unidades")
    print(f"🔹 Preço Unitário Médio: R$ {preco_medio:.2f}")
    print(f"🔹 Ticket Médio por Venda: R$ {ticket_medio:.2f}")
    
    # 2. Resumo estatístico do Pandas (.describe) para as colunas numéricas
    print("\n🔹 Resumo Estatístico das Variáveis Numéricas:")
    print(df[['quantidade', 'preco_unitario', 'faturamento']].describe())
    print("="*50)
    
    return df
# =========================================================================
# RF06 – FILTRAGEM DE DADOS POR CONDIÇÃO
# =========================================================================
def filtrar_dados(df):
    """Aplica filtros condicionais para extrair subconjuntos de dados."""
    print("\n" + "="*50)
    print("      RF06 - FILTRAGEM CONDICIONAL DE DADOS")
    print("="*50)
    
    # 1. Filtro de Vendas de Alto Valor (> R$ 5000)
    print("\n🔹 Extraindo vendas de alto valor (Faturamento > R$ 5.000,00):")
    vendas_alto_valor = df[df['faturamento'] > 5000]
    print(f"👉 Encontradas {len(vendas_alto_valor)} vendas que faturaram mais de R$ 5.000,00.")
    if len(vendas_alto_valor) > 0:
        print(vendas_alto_valor[['id_venda', 'produto', 'regiao', 'faturamento']].head())
    
    # 2. Filtro Regional (Apenas região Sul)
    print("\n🔹 Isolando registros da Região Sul:")
    vendas_sul = df[df['regiao'] == 'Sul']
    print(f"👉 Encontradas {len(vendas_sul)} vendas realizadas na Região Sul.")
    print("="*50)
    
    return df
# =========================================================================
# RF07 – EXPORTAÇÃO DE RESULTADOS
# =========================================================================
def exportar_resultados(df):
    """Exporta subconjuntos de dados filtrados para arquivos CSV."""
    print("\n" + "="*50)
    print("      RF07 - EXPORTAÇÃO DE RESULTADOS (CSV)")
    print("="*50)
    
    # Gerando os mesmos filtros para exportação segura
    vendas_alto_valor = df[df['faturamento'] > 5000]
    vendas_sul = df[df['regiao'] == 'Sul']
    
    # Salvando os arquivos usando o método .to_csv do Pandas
    print("💾 Salvando arquivo 'vendas_alto_valor.csv'...")
    vendas_alto_valor.to_csv("vendas_alto_valor.csv", index=False)
    
    print("💾 Salvando arquivo 'vendas_regiao_sul.csv'...")
    vendas_sul.to_csv("vendas_regiao_sul.csv", index=False)
    
    print("✅ Arquivos exportados com sucesso para a pasta do projeto!")
    print("="*50)
    # =========================================================================
# RF08 – VISUALIZAÇÃO DE DADOS (GRÁFICOS)
# =========================================================================
def gerar_graficos(df):
    """Gera gráficos estatísticos com base nos dados limpos e salvos."""
    import matplotlib.pyplot as plt
    
    print("\n" + "="*50)
    print("      RF08 - GERAÇÃO DE GRÁFICOS VISUAIS")
    print("="*50)
    
    # Prepara os dados do gráfico: Agrupa faturamento por região
    faturamento_regiao = df.groupby('regiao')['faturamento'].sum().sort_values(ascending=False)
    
    # Criar a figura do gráfico
    plt.figure(figsize=(8, 5))
    
    # Criar gráfico de barras coloridas
    faturamento_regiao.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    # Configurar títulos e etiquetas do gráfico
    plt.title('Faturamento Total por Região', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Regiões', fontsize=12)
    plt.ylabel('Faturamento (R$)', fontsize=12)
    plt.xticks(rotation=0) # Mantém os nomes das regiões retos
    plt.grid(axis='y', linestyle='--', alpha=0.7) # Linhas de grade no fundo
    
    # Ajustar espaçamento automático
    plt.tight_layout()
    
    # Salvar o gráfico como imagem na pasta do projeto
    nome_grafico = "faturamento_por_regiao.png"
    plt.savefig(nome_grafico)
    plt.close()
    
    print(f"📊 Gráfico gerado com sucesso e salvo como '{nome_grafico}'!")
    print("="*50)
# =========================================================================
# EXECUÇÃO DO PIPELINE (Ponto de Entrada Inicial)
# =========================================================================
# =========================================================================
# RF05 – AGRUPAMENTO DE DADOS E MÉTRICAS
# =========================================================================
def agrupar_dados(df):
    """Agrupa os dados por região e categoria para análise de performance."""
    print("\n" + "="*50)
    print("      RF05 - ANÁLISE POR REGIÃO E CATEGORIA")
    print("="*50)
    
    # 1. Faturamento por Região
    print("\n🔹 Faturamento Total por Região:")
    faturamento_regiao = df.groupby('regiao')['faturamento'].sum().sort_values(ascending=False)
    print(faturamento_regiao.map("R$ {:,.2f}".format))
    
    # 2. Quantidade de Itens por Categoria
    print("\n🔹 Quantidade de Itens Vendidos por Categoria:")
    qtd_categoria = df.groupby('categoria')['quantidade'].sum().sort_values(ascending=False)
    print(qtd_categoria.map("{:.0f} unidades".format))
    print("="*50)
    
    return df
if __name__ == "__main__":
    # Passo 1: Gera os dados (RF01)
    df_vendas = gerar_dataset_vendas()
    df_vendas.to_csv("vendas.csv", index=False)
    print("✅ RF01: Dataset de vendas gerado e salvo como 'vendas.csv'.")
    
    # Passo 2: Inspeciona os dados brutos (RF02)
    inspecionar_dados(df_vendas)
    
    # Passo 3: Executa a limpeza dos dados (RF03)
    df_vendas_limpo = limpar_dados(df_vendas)
    # Passo 4: Computa as estatísticas descritivas (RF04)
    df_vendas_analisado = computar_estatisticas(df_vendas_limpo)
    # Passo 5: Agrupa e analisa por região/categoria (RF05)
    df_vendas_agrupado = agrupar_dados(df_vendas_analisado)
    # Passo 6: Filtra os dados por condições específicas (RF06)
    df_vendas_filtrado = filtrar_dados(df_vendas_agrupado)
    # Passo 7: Exporta os resultados gerados para novos arquivos (RF07)
    exportar_resultados(df_vendas_filtrado)
    # Passo 8: Gera gráficos visuais de performance (RF08)
    gerar_graficos(df_vendas_filtrado)
    
