import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Crescimento de Redes Sociais", layout="wide")
st.title("📱 Crescimento de Redes Sociais — Últimos 7 dias")

# -------------------------------------------------------
# 👇 Troque pela URL raw do seu CSV no GitHub
# Exemplo: https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/redes_sociais_7dias.csv
# -------------------------------------------------------
CSV_URL = "https://raw.githubusercontent.com/sablewin22/Grafico-Redes-Sociais/refs/heads/main/redes_sociais_7dias.csv"

@st.cache_data
def carregar_dados(url):
    return pd.read_csv(url, parse_dates=["data"])

df = carregar_dados(CSV_URL)

redes = ["instagram", "tiktok", "youtube", "twitter", "linkedin"]
cores = {
    "instagram": "#E1306C",
    "tiktok":    "#010101",
    "youtube":   "#FF0000",
    "twitter":   "#1DA1F2",
    "linkedin":  "#0077B5",
}

# --- Métricas de crescimento ---
st.subheader("Crescimento no período")
cols = st.columns(5)
for i, rede in enumerate(redes):
    inicio = df[rede].iloc[0]
    fim    = df[rede].iloc[-1]
    pct    = ((fim - inicio) / inicio) * 100
    cols[i].metric(rede.capitalize(), f"{fim:,.0f}", f"+{pct:.1f}%")

st.divider()

# --- Gráfico de linhas ---
df_long = df.melt(id_vars="data", value_vars=redes, var_name="rede", value_name="seguidores")
fig = px.line(
    df_long, x="data", y="seguidores", color="rede", markers=True,
    color_discrete_map=cores,
    labels={"data": "Data", "seguidores": "Seguidores", "rede": "Rede Social"},
    title="Evolução de seguidores por rede social",
)
fig.update_traces(line_width=2.5, marker_size=7)
fig.update_layout(hovermode="x unified", legend_title_text="",
                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Gráfico de barras: crescimento absoluto ---
st.subheader("Crescimento absoluto no período")
crescimento = {r: int(df[r].iloc[-1] - df[r].iloc[0]) for r in redes}
fig2 = go.Figure(go.Bar(
    x=list(crescimento.keys()), y=list(crescimento.values()),
    marker_color=[cores[r] for r in crescimento],
    text=[f"+{v:,}" for v in crescimento.values()], textposition="outside",
))
fig2.update_layout(yaxis_title="Novos seguidores", showlegend=False,
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig2, use_container_width=True)
