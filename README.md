# Projeto Pipeline de Vendas - 2026

Este projeto consiste em um pipeline automatizado para processamento, análise e filtragem de dados de vendas, desenvolvido como critério de avaliação. O sistema aplica conceitos avançados de Programação Orientada a Objetos (POO), manipulação de dados com Pandas e NumPy, além de validações robustas com Expressões Regulares (Regex).

## 🚀 Requisitos Implementados

- **RF01 (Carregar Dataset):** Leitura otimizada do arquivo de dados utilizando a biblioteca Pandas.
- **RF05 e RF06 (Métricas Agregadas & Segmentação):** Agrupamentos com `groupby` para extração de métricas de faturamento por região.
- **RF07 (Estatísticas com NumPy):** Cálculos matemáticos e estatísticos aplicados sobre o dataset de vendas.
- **RF09 e RF10 (Estrutura de Classes e Herança):** Arquitetura baseada em POO com uma classe mãe (`AnaliseBase`) e uma classe filha (`PipelineVendas`) gerenciando o fluxo.
- **RF11 e RF12 (Filtros Avançados):** Tratamento de dados utilizando funções Lambda e Expressões Regulares (Regex) para higienização e segmentação.
- **RF13 (Exportação JSON):** Geração e exportação automática dos dados tratados para o arquivo `vendas_limpas.json`.
- **RF14 (Execução do Pipeline completo):** Ponto de entrada unificado no arquivo principal para execução em lote.

## 📁 Estrutura do Repositório

- `salesinsight.py`: Código-fonte principal com a arquitetura do pipeline.
- `vendas_limpas.json`: Arquivo gerado após o processamento dos filtros.
- `faturamento_por_regiao.png`: Gráfico gerado a partir das análises estatísticas.

## 🛠️ Como Executar o Projeto

1. Certifique-se de ter o Python e as dependências instaladas (`pandas`, `numpy`, `matplotlib`, `seaborn`).
2. Execute o arquivo principal através do terminal:
   ```bash
   python salesinsight.py
