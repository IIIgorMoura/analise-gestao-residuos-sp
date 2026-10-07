import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_tags import st_tags

# Configurações iniciais
st.set_page_config(
    page_title="Dashboard de Residuos", page_icon="♻️", layout="wide"
)

# Carregar dados
df_soma = pd.read_excel("./DF/somas_total_2013_2024.xlsx")
df_tipos = pd.read_excel("./DF/tipo_residuos_total.xlsx")
df_soma_mensal = pd.read_excel("./DF/total_mensal_fixed.xlsx")
df_soma_mensal_estimativa = pd.read_excel(
    "./DF/total_mensal_fixed_ESTIMATIVA.xlsx"
)
df_previsoes_consolidado = pd.read_excel(
    "./DF/projecoes_consolidadas_2021_2027.xlsx"
)
df_previsao = pd.read_excel("./DF/previsoes_modelos.xlsx")
df_mensal = pd.read_excel("./DF/2013-2021.xlsx")

# Criar um filtro para retirar o total_geral para fazer somas
df_filtro = df_tipos[df_tipos["tipo_residuo"] != "total_geral"]


# Style
def aplicar_estilo():
  with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


aplicar_estilo()

# Lista para configuração
meses = [
    "jan",
    "fev",
    "mar",
    "abr",
    "mai",
    "jun",
    "jul",
    "ago",
    "set",
    "out",
    "nov",
    "dez",
]
meses_previcao = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]
meses_traducao = {
    "jan": "jan",
    "fev": "feb",
    "mar": "mar",
    "abr": "apr",
    "mai": "may",
    "jun": "jun",
    "jul": "jul",
    "ago": "aug",
    "set": "sep",
    "out": "oct",
    "nov": "nov",
    "dez": "dec",
}
cores = {
    "Domiciliar": "#0068C9",
    "Entulho Mecanizado": "#74B537",
    "Diversos": "#E15759",
    "Ecoponto": "#F28E2B",
    "Piscinões": "#9467BD",
    "Esgoto": "#FFC20A",
    "Córregos": "#8C564B",
    "Varricação Manual": "#E377C2",
    "Feira Livre": "#7F7F7F",
    "Coleta Seletiva": "#17BECF",
}
labels_map = {
    "domiciliar": "Domiciliar",
    "entulho_mecanizado": "Entulho Mecanizado",
    "diversos": "Diversos",
    "ecoponto": "Ecoponto",
    "piscinoes": "Piscinões",
    "esgoto": "Esgoto",
    "corregos": "Córregos",
    "varricao_manual": "Varricação Manual",
    "feira_livre": "Feira Livre",
    "coleta_seletiva": "Coleta Seletiva",
}

# Replace
df_filtro["tipo_residuo"] = df_filtro["tipo_residuo"].replace(labels_map)
df_tipos["tipo_residuo"] = df_tipos["tipo_residuo"].replace(labels_map)
df_mensal["tipo_residuo"] = df_mensal["tipo_residuo"].replace(labels_map)

# Sidebar
st.sidebar.header("Selecione os Filtros")

with st.sidebar.expander("Configurações de Tipos de Resíduo"):
  tipo_residuo = st.multiselect(
      "Tipos de resíduo",
      options=df_filtro.nlargest(10, "total_anos")["tipo_residuo"],
      default=df_filtro.nlargest(10, "total_anos")["tipo_residuo"],
      help="Selecione um ou mais tipos de resíduos para visualizar no gráfico.",
      key="tipo",
  )

with st.sidebar.expander("Configurações de Faixa de Tempo"):
  # ATUALIZAÇÃO REQUISITO 1: Limite alterado para 2027
  ano = st.slider(
      "Faixa de tempo em anos",
      min_value=2013,
      max_value=2027,
      value=(2013, 2027),
      help="Arraste para selecionar o intervalo de anos.",
  )

# Aplicar filtro do tipo de residuo e do ano entre colunas (verificando existência da coluna)
colunas_ano = [
    f"total_{a}"
    for a in range(ano[0], ano[1] + 1)
    if f"total_{a}" in df_tipos.columns
]
df_selecao_tipos = df_tipos.query(f"tipo_residuo in @tipo_residuo")[colunas_ano]
df_selecao_tipos_setor = df_tipos.query(f"tipo_residuo in @tipo_residuo")

# Restaurando as colunas perdidas
df_selecao_tipos["total_anos"] = (
    df_selecao_tipos.iloc[:, 1:].select_dtypes(include="number").sum(axis=1)
)
df_selecao_tipos["tipo_residuo"] = df_tipos["tipo_residuo"]

# Filtrar o df da soma pelo o tempo
df_selecao_soma = df_soma.query("@ano[0] <= ano <= @ano[1]")

# Ajustar o df da soma mensal (somente colunas existentes)
colunas_meses_anos = [
    f"{mes}/{i - 2000}"
    for i in range(ano[0], ano[1] + 1)
    for mes in meses
    if f"{mes}/{i - 2000}" in df_soma_mensal.columns
]
df_selecao_soma_mensal = df_soma_mensal[colunas_meses_anos]

df_selecao_soma_mensal_long = pd.melt(
    df_selecao_soma_mensal, var_name="meses/ano", value_name="total_geral"
)

# Ajustar o df da soma mensal de estimativa
colunas_meses_anos_estimativa = [
    f"{mes}/{i - 2000}"
    for i in range(ano[0], ano[1] + 1)
    for mes in meses
    if f"{mes}/{i - 2000}" in df_soma_mensal_estimativa.columns
]
df_selecao_soma_mensal_estimativa = df_soma_mensal_estimativa[
    colunas_meses_anos_estimativa
]

df_selecao_soma_mensal_estimativa_long = pd.melt(
    df_selecao_soma_mensal_estimativa,
    var_name="meses/ano",
    value_name="total_geral",
)

df_selecao_soma_mensal_estimativa_long["meses/ano"] = (
    df_selecao_soma_mensal_estimativa_long["meses/ano"].replace(
        meses_traducao, regex=True
    )
)
df_selecao_soma_mensal_estimativa_long["meses/ano"] = pd.to_datetime(
    df_selecao_soma_mensal_estimativa_long["meses/ano"], format="%b/%y"
)

df_selecao_soma_mensal_long["meses/ano"] = df_selecao_soma_mensal_long[
    "meses/ano"
].replace(meses_traducao, regex=True)
df_selecao_soma_mensal_long["meses/ano"] = pd.to_datetime(
    df_selecao_soma_mensal_long["meses/ano"], format="%b/%y"
)

# Filtrar df_previsao
coluna_ano_previsao = [
    f"{mes}/{i - 2000}"
    for i in range(ano[0], ano[1] + 1)
    for mes in meses_previcao
    if (i == 2020 and mes == "dec")
    or (
        2021 <= i <= 2027
        and (
            i < 2025
            or mes in [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jun",
                "jul",
                "aug",
                "sep",
                "oct",
                "nov",
                "dec",
            ]
        )
    )
]
coluna_ano_previsao_datetime = pd.to_datetime(
    coluna_ano_previsao, format="%b/%y"
)
df_selecao_previsao = df_previsao.query("ds in @coluna_ano_previsao_datetime")

# Ajustar df mensal
colunas_meses_anos_34 = [
    f"{mes}/{i - 2000}"
    for i in range(ano[0], ano[1] + 1)
    for mes in meses
    if f"{mes}/{i - 2000}" in df_mensal.columns
]
df_selecao_mensal = df_mensal.query(f"tipo_residuo in @tipo_residuo")[
    colunas_meses_anos_34
]
df_selecao_mensal["tipo_residuo"] = df_mensal["tipo_residuo"]

df_selecao_mensal.columns = df_selecao_mensal.columns.str.replace(
    r"(\w{3})/(\d{2})",
    lambda m: f"{meses_traducao[m.group(1)]}/{m.group(2)}",
    regex=True,
)

df_selecao_mensal_long = pd.melt(
    df_selecao_mensal,
    id_vars=["tipo_residuo"],
    var_name="mes_ano",
    value_name="total",
)

df_selecao_mensal_long["mes_ano"] = pd.to_datetime(
    df_selecao_mensal_long["mes_ano"], format="%b/%y"
)


# Funções para exibir
def Home():
  st.title("Análise da Gestão de Resíduos Sólidos Urbanos em SP de 2013 a 2027")
  total_coletado = df_selecao_soma["soma_total"].sum()
  st.metric(
      "Total coletado no período (Toneladas)",
      value=f"{total_coletado:,.0f}".replace(",", "."),
      border=True,
  )


def previsao():
  fig_linha = px.line(
      df_selecao_soma_mensal_long,
      x="meses/ano",
      y="total_geral",
      title=(
          "Evolução Temporal da Coleta Mensal de Resíduos Sólidos Urbanos em"
          " São Paulo (2013–2027)"
      ),
      labels={
          "total_geral": "Total Geral (Toneladas)",
          "meses/ano": "Tempo (Meses)",
      },
  )

  fig_linha.update_layout(
      xaxis=dict(
          dtick="M12",
          tickformat="%Y",
          showgrid=True,
          gridcolor="LightGray",
      ),
      yaxis=dict(
          showgrid=True,
          gridcolor="LightGray",
          tickformat=",.0f",
      ),
      template="plotly_white",
      separators=",.",
      margin=dict(l=50, r=50, t=80, b=50),
  )

  fig_linha.update_traces(
      hovertemplate=(
          "<b>Data:</b> %{x|%b/%Y}<br><b>Total Geral:</b> %{y:,.0f}"
          " t<extra></extra>"
      )
  )

  # -------------------------------------------------------------
  # ATUALIZAÇÃO REQUISITO 2: FILTRO DINÂMICO APLICADO EM TODAS AS FASES DO PROPHET
  # -------------------------------------------------------------
  df_prev_cons = df_previsoes_consolidado.copy()
  df_prev_cons["ds"] = pd.to_datetime(df_prev_cons["ds"])

  # Limites baseados no slider
  data_inicio = pd.to_datetime(f"{ano[0]}-01-01")
  data_fim = pd.to_datetime(f"{ano[1]}-12-31")

  # 1. Dados Históricos (2013-2020) filtrados pelo slider
  df_full_train = df_selecao_soma_mensal_estimativa_long[
      (df_selecao_soma_mensal_estimativa_long["meses/ano"] >= data_inicio)
      & (df_selecao_soma_mensal_estimativa_long["meses/ano"] <= data_fim)
      & (df_selecao_soma_mensal_estimativa_long["meses/ano"] <= "2020-12-01")
  ].sort_values(by="meses/ano")

  # 2. Estimativa Prophet (2021-2025) filtrada pelo slider
  est_mask = (
      (df_prev_cons["ds"] >= data_inicio)
      & (df_prev_cons["ds"] <= data_fim)
      & (df_prev_cons["ds"] >= "2021-01-01")
      & (df_prev_cons["ds"] <= "2025-12-01")
  )

  # 3. Projeção Prophet (2026-2027) filtrada pelo slider
  fut_mask = (
      (df_prev_cons["ds"] >= data_inicio)
      & (df_prev_cons["ds"] <= data_fim)
      & (df_prev_cons["ds"] >= "2026-01-01")
      & (df_prev_cons["ds"] <= "2027-12-01")
  )

  fig_linha_previcao = go.Figure()

  # FASE 1: Dados Históricos
  if not df_full_train.empty:
    fig_linha_previcao.add_trace(
        go.Scatter(
            x=df_full_train["meses/ano"],
            y=df_full_train["total_geral"],
            mode="lines",
            name="1. Dados Históricos (2013-2020)",
            line=dict(color="black", width=1.5),
            hovertemplate=(
                "<b>Data:</b> %{x|%b/%Y}<br><b>Histórico:</b> %{y:,.0f}"
                " t<extra></extra>"
            ),
        )
    )

  # FASE 2: Estimativa Prophet
  if est_mask.any():
    fig_linha_previcao.add_trace(
        go.Scatter(
            x=df_prev_cons.loc[est_mask, "ds"],
            y=df_prev_cons.loc[est_mask, "Previsao_Prophet"],
            mode="lines",
            name="2. Estimativa Prophet (2021-2025)",
            line=dict(color="#FF8C00", dash="dot", width=2.5),
            hovertemplate=(
                "<b>Data:</b> %{x|%b/%Y}<br><b>Estimativa:</b> %{y:,.0f}"
                " t<extra></extra>"
            ),
        )
    )

  # FASE 3: Projeção Prophet
  if fut_mask.any():
    fig_linha_previcao.add_trace(
        go.Scatter(
            x=df_prev_cons.loc[fut_mask, "ds"],
            y=df_prev_cons.loc[fut_mask, "Previsao_Prophet"],
            mode="lines",
            name="3. Projeção Prophet (2026-2027)",
            line=dict(color="#0068C9", dash="dot", width=2.5),
            hovertemplate=(
                "<b>Data:</b> %{x|%b/%Y}<br><b>Projeção:</b> %{y:,.0f}"
                " t<extra></extra>"
            ),
        )
    )

  # Linhas verticais condicionais ao intervalo visível
  if ano[0] <= 2021 <= ano[1]:
    fig_linha_previcao.add_vline(
        x="2021-01-01", line_dash="dot", line_color="gray", line_width=1.5
    )
  if ano[0] <= 2026 <= ano[1]:
    fig_linha_previcao.add_vline(
        x="2026-01-01", line_dash="dot", line_color="gray", line_width=1.5
    )

  fig_linha_previcao.update_layout(
      title=(
          "Coleta de RSU em SP: Dados Históricos, Estimativa e Projeção Prophet"
          " (2013–2027)"
      ),
      xaxis_title="Tempo (Meses)",
      yaxis_title="Total Geral (Toneladas)",
      template="plotly_white",
      hovermode="x unified",
      separators=",.",
      legend=dict(
          x=0.99,
          y=0.99,
          xanchor="right",
          yanchor="top",
          bgcolor="rgba(255, 255, 255, 0.8)",
          borderwidth=0,
      ),
      xaxis=dict(
          dtick="M12",
          tickformat="%Y",
          showgrid=True,
          gridcolor="LightGray",
      ),
      yaxis=dict(
          showgrid=True,
          gridcolor="LightGray",
          tickformat=",.0f",
      ),
      margin=dict(l=50, r=50, t=80, b=50),
  )

  st.plotly_chart(fig_linha, use_container_width=True)
  st.plotly_chart(fig_linha_previcao, use_container_width=True)

  # Métricas
  df_hist_complete = df_selecao_soma_mensal_estimativa_long
  df_2013 = df_hist_complete[df_hist_complete["meses/ano"].dt.year == 2013]
  media_2013 = df_2013["total_geral"].mean() if not df_2013.empty else 0

  df_2020 = df_hist_complete[df_hist_complete["meses/ano"].dt.year == 2020]
  media_2020 = df_2020["total_geral"].mean() if not df_2020.empty else 0

  mask_2027 = (df_prev_cons["ds"] >= "2027-01-01") & (
      df_prev_cons["ds"] <= "2027-12-01"
  )
  df_2027 = df_prev_cons.loc[mask_2027, "Previsao_Prophet"]
  media_2027_prophet = df_2027.mean() if not df_2027.empty else 0

  metric1, metric2, metric3 = st.columns(3)
  with metric1:
    st.metric(
        "Média Histórica Mensal em 2013 (Toneladas)",
        value=f"{media_2013:,.0f}".replace(",", "."),
        border=True,
    )
  with metric2:
    st.metric(
        "Média Histórica Mensal em 2020 (Toneladas)",
        value=f"{media_2020:,.0f}".replace(",", "."),
        border=True,
    )
  with metric3:
    st.metric(
        "Média Projetada Mensal em 2027 - Prophet (Toneladas)",
        value=f"{media_2027_prophet:,.0f}".replace(",", "."),
        border=True,
    )


def soma_tipo():
  df_soma_residuos = (
      df_selecao_mensal_long.groupby("tipo_residuo")["total"]
      .sum()
      .reset_index()
  )
  df_top_10_residuos = df_soma_residuos.nlargest(10, "total")

  df_mensal_top_10 = df_selecao_mensal_long[
      df_selecao_mensal_long["tipo_residuo"].isin(
          df_top_10_residuos["tipo_residuo"]
      )
  ]

  fig_linha_residuos = px.line(
      df_mensal_top_10,
      x="mes_ano",
      y="total",
      color="tipo_residuo",
      title="Top 10 Tipos de Resíduos Coletados de 2013 a 2020",
      labels={
          "mes_ano": "Tempo (Meses)",
          "total": "Total Coletado (Toneladas)",
          "tipo_residuo": "Tipo de Resíduo",
      },
      color_discrete_map=cores,
  )

  fig_linha_residuos.update_layout(
      xaxis=dict(
          dtick="M12",
          tickformat="%Y",
          showgrid=True,
          gridcolor="LightGray",
      ),
      yaxis=dict(
          showgrid=True,
          gridcolor="LightGray",
          tickformat=",.0f",
      ),
      template="plotly_white",
      separators=",.",
      margin=dict(l=50, r=50, t=80, b=50),
  )

  fig_linha_residuos.update_traces(
      hovertemplate=(
          "<b>Tipo:</b> %{fullData.name}<br><b>Data:</b>"
          " %{x|%b/%Y}<br><b>Total:</b> %{y:,.0f} t<extra></extra>"
      )
  )

  st.plotly_chart(fig_linha_residuos, use_container_width=True)


def tipo_residuo_graficos():
  fig_barras = px.bar(
      df_selecao_tipos.sort_values(by="total_anos", ascending=False),
      x="total_anos",
      y="tipo_residuo",
      color="tipo_residuo",
      title="Quantidade Total de Resíduos Coletados  no Período",
      color_discrete_map=cores,
      labels={
          "tipo_residuo": "Tipos de Resíduo",
          "total_anos": "Total Geral (Toneladas)",
      },
  )

  fig_barras.update_layout(
      xaxis=dict(
          showgrid=True,
          gridcolor="LightGray",
          dtick=1000000,
          tickformat=",.0f",
      ),
      yaxis=dict(showgrid=False),
      template="plotly_white",
      separators=",.",
      margin=dict(l=50, r=50, t=80, b=50),
  )

  fig_barras.update_traces(
      hovertemplate=(
          "<b>Tipo de Resíduo:</b> %{y}<br><b>Total:</b> %{x:,.0f}"
          " t<extra></extra>"
      )
  )

  st.plotly_chart(fig_barras, use_container_width=True)


def proporcao():
  select1, select2 = st.columns(2)
  with select1:
    ano_pie_1 = st.selectbox(
        "Selecione o ano do gráfico abaixo:",
        options=range(2013, 2021),
        index=0,
        key="pie1",
    )
  with select2:
    ano_pie_2 = st.selectbox(
        "Selecione o ano do gráfico abaixo:",
        options=[x for x in range(2013, 2021) if x != ano_pie_1],
        index=6,
        key="pie2",
    )

  setor1, setor2 = st.columns(2)
  with setor1:
    fig_pie1 = px.pie(
        df_selecao_tipos_setor.nlargest(5, f"total_{ano_pie_1}"),
        names="tipo_residuo",
        values=f"total_{ano_pie_1}",
        color="tipo_residuo",
        color_discrete_map=cores,
        title=f"Distribuição dos tipos de resíduo no ano de {ano_pie_1}",
    )

    fig_pie1.update_layout(separators=",.")

    fig_pie1.update_traces(
        hovertemplate=(
            "<b>Tipo de Resíduo:</b> %{label}<br><b>Total:</b> %{value:,.0f}"
            " t<br><b>Porcentagem:</b> %{percent}<extra></extra>"
        )
    )

    total_do_ano_1 = df_soma["soma_total"][df_soma["ano"] == ano_pie_1].iloc[0]

    st.plotly_chart(fig_pie1, use_container_width=True)
    st.metric(
        f"Total coletado no ano de {ano_pie_1} (Toneladas)",
        value=f"{total_do_ano_1:,.0f}".replace(",", "."),
        border=True,
    )

  with setor2:
    fig_pie2 = px.pie(
        df_selecao_tipos_setor.nlargest(5, f"total_{ano_pie_2}"),
        names="tipo_residuo",
        values=f"total_{ano_pie_2}",
        color="tipo_residuo",
        color_discrete_map=cores,
        title=f"Distribuição dos tipos de resíduo no ano de {ano_pie_2}",
    )

    fig_pie2.update_layout(separators=",.")

    fig_pie2.update_traces(
        hovertemplate=(
            "<b>Tipo de Resíduo:</b> %{label}<br><b>Total:</b> %{value:,.0f}"
            " t<br><b>Porcentagem:</b> %{percent}<extra></extra>"
        )
    )

    total_do_ano_2 = df_soma["soma_total"][df_soma["ano"] == ano_pie_2].iloc[0]

    st.plotly_chart(fig_pie2, use_container_width=True)
    st.metric(
        f"Total coletado no ano de {ano_pie_2} (Toneladas)",
        value=f"{total_do_ano_2:,.0f}".replace(",", "."),
        border=True,
    )


# Execução do Dashboard
Home()
previsao()
st.markdown("---")
proporcao()
st.markdown("---")
soma_tipo()
tipo_residuo_graficos()