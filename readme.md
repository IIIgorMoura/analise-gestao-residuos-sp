# ♻️ Análise de Gestão de Resíduos Sólidos Urbanos (São Paulo)
**Parceria Técnica: ONG Limpa Brasil**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red.svg)](https://share.streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Cleaning-green.svg)](https://pandas.pydata.org/)

## Visão Geral
Este projeto analisa o histórico de coleta de resíduos sólidos na cidade de São Paulo (2013-2024), identificando um apagão de dados públicos a partir de 2021. Foram utilizadas técnicas de **Ciência de Dados e Machine Learning** para estimar o volume de resíduos não registrado e fornecer insights estratégicos para a ONG Limpa Brasil.

### Principal Desafio: A Lacuna de 2021
A partir de 2021, observou-se uma queda atípica e inconsistente nos dados oficiais de coleta. O projeto investiga se essa redução é real ou fruto da diminuição de investimentos em monitoramento pós-pandemia, utilizando modelagem preditiva para preencher esse "vazio" informativo.

---

## Tecnologias e Ferramentas
* **Linguagem:** Python
* **Manipulação de Dados:** Pandas, NumPy
* **Visualização:** Plotly, Matplotlib (Gráficos interativos e estáticos)
* **Machine Learning:** Regressão e Modelagem Preditiva para estimativa de volumes (2021-2025).
* **Deploy:** Streamlit (Dashboard interativo para apresentação de insights).

---

## Principais Insights e Metodologia

1.  **Engenharia de Dados (ETL):** Integração de bases históricas e tratamento de inconsistências em dados públicos.
2.  **Modelagem Preditiva:** Desenvolvimento de modelo para projetar o descarte de resíduos até 2025, mitigando a falta de transparência dos dados oficiais atuais.
3.  **Análise de Impacto:** * O volume acumulado desde 2013 ocuparia **53% da área de São Caetano do Sul**.
    * Identificação de que o **resíduo domiciliar** é o maior responsável pelo descarte irregular nas ruas, sugerindo falhas na infraestrutura de educação ambiental.
4.  **Conformidade:** Análise baseada nas diretrizes da **Política Nacional de Resíduos Sólidos (PNRS)**.

---

## Como Executar o Projeto
1. Clone o repositório: `git clone https://github.com/IIIgorMoura/analise-gestao-residuos-sp.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o Dashboard: `streamlit run analise.py`

---

## Publicações e Entregáveis
* **Artigo Científico:** Submetido à revista *Mix Sustentabilidade*.
* **Apresentação:** Pitch realizado para a diretoria da ONG Limpa Brasil.

---
