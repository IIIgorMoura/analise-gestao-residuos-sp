# ♻️ Análise de Gestão de Resíduos Sólidos Urbanos em São Paulo
**Em parceria com o Instituto Limpa Brasil**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-4DABCF?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

## Visão Geral
Este projeto analisa o histórico de coleta de resíduos sólidos na cidade de São Paulo, identificando um apagão de dados públicos a partir de 2021. Foram utilizadas técnicas de **Ciência de Dados e Machine Learning** para estimar o volume de resíduos não registrado e fornecer insights estratégicos para o Instituto Limpa Brasil.

### Principal Desafio: A Lacuna de 2021
A partir de 2021, observou-se uma queda inconsistente nos dados oficiais de coleta. O projeto investiga se essa redução é real ou fruto de uma falha ou mudança de escopo da coleta de dados de acesso público, utilizando modelagem preditiva para fazer estimativas no período inconsistente e projeções para o futuro da coleta de RSU.

---

## Tecnologias e Ferramentas
* **Linguagem:** Python
* **Manipulação de Dados:** Pandas, NumPy
* **Visualização:** Plotly, Matplotlib
* **Machine Learning:** Modelagem Preditiva utilizando Prophet para estimativa de volumes (2021-2027).
* **Deploy:** Streamlit (Dashboard interativo para apresentação de insights).

---

## Principais Insights e Metodologia

1.  **Engenharia de Dados (ETL):** Integração de bases históricas e tratamento de inconsistências em dados públicos.
2.  **Modelagem Preditiva:** Desenvolvimento de modelo para projetar o descarte de resíduos até 2027, mitigando a falta de transparência dos dados oficiais atuais.
3.  **Comparação de Modelos:** Experimento com ARIMA, Random Forest e Prophet, utilizando RMSE (Raiz do Erro Quadrático Médio), MAE (Erro Médio Absoluto) e MAPE (Erro Percentual Absoluto Médio) como métricas de validação e seleção, com o Prophet apresentando o melhor desempenho.
4.  **Análise de Impacto:** O volume acumulado desde 2013 ocuparia **53% da área de São Caetano do Sul** e identificação de que o **resíduo domiciliar** é o maior responsável pelo descarte irregular nas ruas, sugerindo falhas na infraestrutura de educação ambiental.
5.  **Conformidade:** Análise baseada nas diretrizes da **Política Nacional de Resíduos Sólidos (PNRS)**.

---

## Como Executar o Projeto
1. Clone o repositório: `git clone https://github.com/IIIgorMoura/analise-gestao-residuos-sp.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o Dashboard: `streamlit run analise.py`

---

## Publicações e Entregáveis
* **Artigo Científico:** Publicação no Congresso SENAI.
* **Apresentação:** Pitch realizado para a diretoria do Instituto Limpa Brasil.

---
