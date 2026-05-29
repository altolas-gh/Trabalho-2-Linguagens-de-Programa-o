"""
Dashboard de Análise de Segurança Cibernética - Brasil (2015–2024)
Projeto G2 — Tema 26
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="CyberSec Brasil Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Estado do tema ───────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ─── Paletas de cores por tema ────────────────────────────────────────────────
def get_theme():
    if st.session_state.dark_mode:
        return {
            "plotly_template": "plotly_dark",
            "plot_bg": "rgba(15,23,42,1)",
            "paper_bg": "rgba(0,0,0,0)",
            # CSS
            "page_bg": "#030712",
            "sidebar_bg": "#0f172a",
            "text_color": "#e2e8f0",
            "subtext_color": "#94a3b8",
            "card_bg": "linear-gradient(135deg, #1e3a5f, #0d2137)",
            "card_border": "#2563eb",
            "card_value": "#60a5fa",
            "section_title_color": "#60a5fa",
            "section_border": "#2563eb",
            "insight_bg": "#0f172a",
            "insight_text": "#cbd5e1",
            "hr_color": "#1e3a5f",
            "toggle_bg": "#1e3a5f",
            "toggle_border": "#2563eb",
            "toggle_text": "#93c5fd",
            "label": "☀️ Modo Claro",
        }
    else:
        return {
            "plotly_template": "plotly_white",
            "plot_bg": "rgba(248,250,252,1)",
            "paper_bg": "rgba(0,0,0,0)",
            # CSS
            "page_bg": "#f1f5f9",
            "sidebar_bg": "#ffffff",
            "text_color": "#0f172a",
            "subtext_color": "#475569",
            "card_bg": "linear-gradient(135deg, #dbeafe, #eff6ff)",
            "card_border": "#3b82f6",
            "card_value": "#1d4ed8",
            "section_title_color": "#1d4ed8",
            "section_border": "#3b82f6",
            "insight_bg": "#eff6ff",
            "insight_text": "#1e3a5f",
            "hr_color": "#cbd5e1",
            "toggle_bg": "#dbeafe",
            "toggle_border": "#3b82f6",
            "toggle_text": "#1d4ed8",
            "label": "🌙 Modo Escuro",
        }

T = get_theme()

# ─── CSS dinâmico ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* Fundo geral */
    .stApp {{ background-color: {T['page_bg']}; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {T['sidebar_bg']} !important;
    }}
    [data-testid="stSidebar"] * {{ color: {T['text_color']} !important; }}

    /* Textos gerais */
    .stMarkdown, .stText, p, span, label {{
        color: {T['text_color']};
    }}

    /* KPI cards */
    .metric-card {{
        background: {T['card_bg']};
        border: 1px solid {T['card_border']};
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        color: {T['text_color']};
    }}
    .metric-value {{ font-size: 2rem; font-weight: 700; color: {T['card_value']}; }}
    .metric-label {{ font-size: 0.85rem; color: {T['subtext_color']}; margin-top: 4px; }}
    .metric-sub   {{ font-size: 0.9rem; color: #f97316; font-weight: 600; }}

    /* Títulos de seção */
    .section-title {{
        font-size: 1.1rem; font-weight: 700;
        color: {T['section_title_color']};
        border-left: 4px solid {T['section_border']};
        padding-left: 10px; margin-bottom: 12px;
    }}

    /* Caixas de insight */
    .insight-box {{
        background-color: {T['insight_bg']};
        border-left: 4px solid #f97316;
        border-radius: 6px;
        padding: 14px 18px;
        color: {T['insight_text']};
        font-size: 0.9rem;
        line-height: 1.6;
    }}

    /* Separadores */
    hr {{ border-color: {T['hr_color']} !important; }}

    /* Botão toggle */
    .toggle-btn {{
        display: inline-block;
        background: {T['toggle_bg']};
        border: 1.5px solid {T['toggle_border']};
        color: {T['toggle_text']};
        border-radius: 8px;
        padding: 6px 16px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
    }}

    /* Títulos h1/h2/h3 */
    h1, h2, h3 {{ color: {T['text_color']} !important; }}

    /* Tabela */
    [data-testid="stDataFrame"] {{ background: {T['insight_bg']}; }}

    /* Tendência nos KPIs */
    .trend-up   {{ color: #ef4444; font-size: 0.8rem; font-weight: 700; }}
    .trend-down {{ color: #22c55e; font-size: 0.8rem; font-weight: 700; }}
    .trend-flat {{ color: #94a3b8; font-size: 0.8rem; }}

    /* Contador de registros */
    .record-counter {{
        background: {T['toggle_bg']};
        border: 1px solid {T['toggle_border']};
        border-radius: 8px;
        padding: 6px 16px;
        font-size: 0.82rem;
        color: {T['toggle_text']};
        display: inline-block;
        margin-bottom: 8px;
    }}
    .record-counter b {{ color: {T['card_value']}; }}
</style>
""", unsafe_allow_html=True)

# ─── Carregamento e persistência SQLite ───────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dados/simulacao_ciberseguranca_brasil.csv", parse_dates=["data"])
    df["ano"] = df["ano"].astype(int)
    df["mes"] = df["mes"].astype(int)
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    df.to_sql("incidentes", engine, if_exists="replace", index=False)
    return df

df_full = load_data()

# ─── Sidebar — Filtros + Toggle ───────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=60)
    st.title("🔎 Filtros")
    st.markdown("---")

    anos = sorted(df_full["ano"].unique())
    ano_sel = st.multiselect("📅 Ano", anos, default=anos)

    meses = list(range(1, 13))
    nomes_mes = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    mes_sel = st.multiselect("🗓️ Mês", meses, default=meses,
                              format_func=lambda x: nomes_mes[x - 1])

    regioes = sorted(df_full["regiao"].unique())
    reg_sel = st.multiselect("🗺️ Região", regioes, default=regioes)

    ufs = sorted(df_full[df_full["regiao"].isin(reg_sel)]["uf"].unique())
    uf_sel = st.multiselect("📍 Estado (UF)", ufs, default=ufs)

    setores = sorted(df_full["setor"].unique())
    set_sel = st.multiselect("🏢 Setor", setores, default=setores)

    ataques = sorted(df_full["tipo_ataque"].unique())
    atk_sel = st.multiselect("⚔️ Tipo de Ataque", ataques, default=ataques)

    criticidades = sorted(df_full["nivel_criticidade"].unique())
    crit_sel = st.multiselect("🚨 Nível de Criticidade", criticidades, default=criticidades)

    st.markdown("---")

    # ── Botão de tema ──
    if st.button(T["label"], key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.caption("Projeto G2 · Tema 26 · CyberSec Brasil")

# ─── Aplicar filtros ──────────────────────────────────────────────────────────
df = df_full[
    df_full["ano"].isin(ano_sel) &
    df_full["mes"].isin(mes_sel) &
    df_full["regiao"].isin(reg_sel) &
    df_full["uf"].isin(uf_sel) &
    df_full["setor"].isin(set_sel) &
    df_full["tipo_ataque"].isin(atk_sel) &
    df_full["nivel_criticidade"].isin(crit_sel)
]

# ─── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown("# 🛡️ Dashboard de Segurança Cibernética — Brasil")
st.markdown("**Análise de ataques digitais e incidentes de segurança (2015–2024)**  |  Projeto G2 · Tema 26")
st.markdown("---")

if df.empty:
    st.warning("⚠️ Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ─── Contador de registros ────────────────────────────────────────────────────
total_registros   = len(df_full)
filtrados         = len(df)
pct_filtro        = filtrados / total_registros * 100
st.markdown(
    f'<div class="record-counter">🗂️ Exibindo <b>{filtrados:,}</b> de <b>{total_registros:,}</b> registros '
    f'<span style="color:#94a3b8">({pct_filtro:.1f}% do total)</span></div>',
    unsafe_allow_html=True
)

# ─── KPIs — com indicador de tendência ───────────────────────────────────────
total_incidentes = int(df["incidentes"].sum())
impacto_total    = df["impacto_financeiro"].sum()
tempo_medio      = df["tempo_recuperacao"].mean()
ataque_principal = df.groupby("tipo_ataque")["incidentes"].sum().idxmax()
setor_principal  = df.groupby("setor")["incidentes"].sum().idxmax()
regiao_critica   = df.groupby("regiao")["incidentes"].sum().idxmax()

# Calcula tendência: compara último ano disponível com o penúltimo
def calc_trend(serie_col, anos_disponiveis):
    """Retorna (html_badge, variação_%) comparando último vs penúltimo ano."""
    anos_ord = sorted(anos_disponiveis)
    if len(anos_ord) < 2:
        return '<span class="trend-flat">—</span>', 0.0
    ult  = df[df["ano"] == anos_ord[-1]][serie_col].sum()
    pult = df[df["ano"] == anos_ord[-2]][serie_col].sum()
    if pult == 0:
        return '<span class="trend-flat">—</span>', 0.0
    var = (ult - pult) / pult * 100
    if var > 0:
        badge = f'<span class="trend-up">▲ {var:.1f}%</span>'
    elif var < 0:
        badge = f'<span class="trend-down">▼ {abs(var):.1f}%</span>'
    else:
        badge = '<span class="trend-flat">= 0%</span>'
    return badge, var

trend_inc,  _ = calc_trend("incidentes",        ano_sel)
trend_imp,  _ = calc_trend("impacto_financeiro", ano_sel)
trend_rec,  _ = calc_trend("tempo_recuperacao",  ano_sel)

col1, col2, col3, col4, col5, col6 = st.columns(6)

def kpi_card(col, icon, label, value, trend_badge="", sub=""):
    trend_html = f'<div style="margin-top:4px">{trend_badge}</div>' if trend_badge else ""
    col.markdown(f"""
    <div class="metric-card">
        <div style="font-size:1.6rem">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {trend_html}
        {'<div class="metric-sub">' + sub + '</div>' if sub else ''}
    </div>""", unsafe_allow_html=True)

kpi_card(col1, "📊", "Total de Incidentes",      f"{total_incidentes:,}".replace(",", "."), trend_inc)
kpi_card(col2, "💸", "Impacto Financeiro",       f"R$ {impacto_total/1e9:.2f}B",            trend_imp)
kpi_card(col3, "⏱️", "Tempo Médio Recuperação", f"{tempo_medio:.1f}h",                      trend_rec)
kpi_card(col4, "⚔️", "Ataque Predominante",     ataque_principal)
kpi_card(col5, "🏢", "Setor Mais Afetado",      setor_principal)
kpi_card(col6, "🗺️", "Região Crítica",          regiao_critica)

anos_legenda = sorted(ano_sel)
if len(anos_legenda) >= 2:
    st.caption(
        f"▲▼ Tendência: variação de {anos_legenda[-1]} em relação a {anos_legenda[-2]}. "
        "Vermelho = aumento (alerta) · Verde = redução (melhora)."
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─── Helper: layout padrão de figura ─────────────────────────────────────────
def fig_layout(fig, **kwargs):
    fig.update_layout(
        template=T["plotly_template"],
        paper_bgcolor=T["paper_bg"],
        plot_bgcolor=T["plot_bg"],
        **kwargs
    )
    return fig

# ─── Linha temporal ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Evolução Temporal dos Incidentes</div>', unsafe_allow_html=True)

col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    df_tempo = df.groupby(["ano", "tipo_ataque"])["incidentes"].sum().reset_index()
    fig_linha = px.line(
        df_tempo, x="ano", y="incidentes", color="tipo_ataque",
        markers=True, template=T["plotly_template"],
        labels={"ano": "Ano", "incidentes": "Incidentes", "tipo_ataque": "Tipo de Ataque"},
        title="Incidentes por Tipo de Ataque ao Longo dos Anos"
    )
    fig_layout(fig_linha,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(dtick=1)
    )
    st.plotly_chart(fig_linha, use_container_width=True)

with col_t2:
    df_ano = df.groupby("ano")["incidentes"].sum().reset_index()
    crescimento = ((df_ano["incidentes"].iloc[-1] - df_ano["incidentes"].iloc[0]) /
                   df_ano["incidentes"].iloc[0] * 100) if len(df_ano) > 1 else 0
    st.markdown(f"""
    <div class="insight-box">
    <b>🔍 Interpretação</b><br><br>
    A série temporal revela a <b>tendência de crescimento</b> dos ataques cibernéticos no Brasil
    entre {min(ano_sel)} e {max(ano_sel)}.<br><br>
    O crescimento acumulado no período selecionado foi de aproximadamente
    <b style="color:#f97316">{crescimento:.1f}%</b>.<br><br>
    Ataques de <b>Ransomware</b> e <b>Phishing</b> tendem a apresentar os maiores
    volumes, refletindo a sofisticação crescente das ameaças digitais.
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ─── Barras: Ataque e Setor ───────────────────────────────────────────────────
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown('<div class="section-title">⚔️ Frequência por Tipo de Ataque</div>', unsafe_allow_html=True)
    df_atk = df.groupby("tipo_ataque")["incidentes"].sum().sort_values(ascending=True).reset_index()
    fig_atk = px.bar(
        df_atk, x="incidentes", y="tipo_ataque", orientation="h",
        template=T["plotly_template"], color="incidentes",
        color_continuous_scale="Blues",
        labels={"incidentes": "Total de Incidentes", "tipo_ataque": "Tipo de Ataque"}
    )
    fig_layout(fig_atk, coloraxis_showscale=False)
    st.plotly_chart(fig_atk, use_container_width=True)

with col_b2:
    st.markdown('<div class="section-title">🏢 Incidentes por Setor</div>', unsafe_allow_html=True)
    df_set = df.groupby("setor")["incidentes"].sum().sort_values(ascending=True).reset_index()
    fig_set = px.bar(
        df_set, x="incidentes", y="setor", orientation="h",
        template=T["plotly_template"], color="incidentes",
        color_continuous_scale="Oranges",
        labels={"incidentes": "Total de Incidentes", "setor": "Setor"}
    )
    fig_layout(fig_set, coloraxis_showscale=False)
    st.plotly_chart(fig_set, use_container_width=True)

st.markdown("---")

# ─── Heatmap mensal ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🔥 Heatmap de Incidentes — Mês × Ano</div>', unsafe_allow_html=True)

df_heat  = df.groupby(["ano", "mes"])["incidentes"].sum().reset_index()
df_pivot = df_heat.pivot(index="mes", columns="ano", values="incidentes").fillna(0)

fig_heat = go.Figure(data=go.Heatmap(
    z=df_pivot.values,
    x=[str(c) for c in df_pivot.columns],
    y=nomes_mes[:len(df_pivot.index)],
    colorscale="YlOrRd",
    text=df_pivot.values.astype(int),
    texttemplate="%{text}",
    showscale=True
))
fig_layout(fig_heat, xaxis_title="Ano", yaxis_title="Mês", height=380)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("""
<div class="insight-box">
<b>🔍 Períodos Críticos:</b> O heatmap permite identificar concentrações mensais de ataques.
Meses com cores mais intensas indicam janelas de maior exposição — informação vital para
reforço preventivo de infraestrutura e alocação de equipes de resposta a incidentes.
</div>""", unsafe_allow_html=True)
st.markdown("---")

# ─── Dispersão impacto × incidentes ─────────────────────────────────────────
col_d1, col_d2 = st.columns([2, 1])

with col_d1:
    st.markdown('<div class="section-title">💸 Impacto Financeiro × Incidentes (por Setor)</div>', unsafe_allow_html=True)
    df_disp = df.groupby(["setor", "tipo_ataque"]).agg(
        incidentes=("incidentes", "sum"),
        impacto=("impacto_financeiro", "sum"),
        sistemas=("sistemas_afetados", "mean")
    ).reset_index()
    fig_disp = px.scatter(
        df_disp, x="incidentes", y="impacto", color="setor",
        size="sistemas", hover_name="tipo_ataque",
        template=T["plotly_template"],
        labels={"incidentes": "Total Incidentes", "impacto": "Impacto Financeiro (R$)", "setor": "Setor"},
        title="Correlação: Volume de Incidentes vs Prejuízo Financeiro"
    )
    fig_layout(fig_disp)
    st.plotly_chart(fig_disp, use_container_width=True)

with col_d2:
    st.markdown('<div class="section-title">🔑 Vulnerabilidades</div>', unsafe_allow_html=True)
    df_vuln = df.groupby("vulnerabilidade")["incidentes"].sum().sort_values(ascending=False).reset_index()
    fig_vuln = px.pie(
        df_vuln, names="vulnerabilidade", values="incidentes",
        template=T["plotly_template"], hole=0.45,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_layout(fig_vuln, showlegend=True, legend=dict(font=dict(size=11)))
    st.plotly_chart(fig_vuln, use_container_width=True)

st.markdown("---")

# ─── Comparação regional ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">🗺️ Comparação Regional</div>', unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)
with col_r1:
    df_reg = df.groupby("regiao").agg(
        incidentes=("incidentes","sum"),
        impacto=("impacto_financeiro","sum")
    ).reset_index()
    fig_reg = px.bar(
        df_reg.sort_values("incidentes", ascending=False),
        x="regiao", y="incidentes", color="impacto",
        template=T["plotly_template"], color_continuous_scale="Reds",
        labels={"regiao":"Região","incidentes":"Incidentes","impacto":"Impacto (R$)"},
        title="Incidentes e Impacto por Região"
    )
    fig_layout(fig_reg)
    st.plotly_chart(fig_reg, use_container_width=True)

with col_r2:
    df_uf = df.groupby("uf")["incidentes"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_uf = px.bar(
        df_uf, x="incidentes", y="uf", orientation="h",
        template=T["plotly_template"], color="incidentes", color_continuous_scale="Teal",
        labels={"uf":"Estado","incidentes":"Incidentes"},
        title="Top 10 Estados com Mais Incidentes"
    )
    fig_layout(fig_uf, coloraxis_showscale=False)
    st.plotly_chart(fig_uf, use_container_width=True)

st.markdown("---")

# ─── Análise de tempo de recuperação ─────────────────────────────────────────
st.markdown('<div class="section-title">⏱️ Tempo de Recuperação por Criticidade e Setor</div>', unsafe_allow_html=True)

col_rec1, col_rec2 = st.columns(2)
with col_rec1:
    df_crit = df.groupby("nivel_criticidade")["tempo_recuperacao"].mean().reset_index()
    ordem_crit = ["Baixo","Médio","Alto","Crítico"]
    df_crit["nivel_criticidade"] = pd.Categorical(df_crit["nivel_criticidade"], categories=ordem_crit, ordered=True)
    df_crit = df_crit.sort_values("nivel_criticidade")
    fig_crit = px.bar(
        df_crit, x="nivel_criticidade", y="tempo_recuperacao",
        color="nivel_criticidade", template=T["plotly_template"],
        color_discrete_map={"Baixo":"#22c55e","Médio":"#eab308","Alto":"#f97316","Crítico":"#ef4444"},
        labels={"nivel_criticidade":"Criticidade","tempo_recuperacao":"Tempo Médio (h)"},
        title="Tempo Médio de Recuperação por Nível de Criticidade"
    )
    fig_layout(fig_crit, showlegend=False)
    st.plotly_chart(fig_crit, use_container_width=True)

with col_rec2:
    df_rec = df.groupby("setor")["tempo_recuperacao"].mean().sort_values(ascending=False).reset_index()
    fig_rec = px.bar(
        df_rec, x="setor", y="tempo_recuperacao",
        template=T["plotly_template"], color="tempo_recuperacao", color_continuous_scale="Purples",
        labels={"setor":"Setor","tempo_recuperacao":"Tempo Médio (h)"},
        title="Tempo Médio de Recuperação por Setor"
    )
    fig_layout(fig_rec, coloraxis_showscale=False)
    st.plotly_chart(fig_rec, use_container_width=True)

st.markdown("---")

# ─── Tabela dinâmica ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Tabela Dinâmica — Exploração Detalhada</div>', unsafe_allow_html=True)

col_tab1, col_tab2 = st.columns([1, 3])
with col_tab1:
    agg_col = st.selectbox("Agrupar por:", ["setor","tipo_ataque","regiao","uf","vulnerabilidade","nivel_criticidade"])
    metrica  = st.selectbox("Métrica:", ["incidentes","impacto_financeiro","tempo_recuperacao","sistemas_afetados"])

with col_tab2:
    df_tab = df.groupby(agg_col).agg(
        total=(metrica, "sum"),
        media=(metrica, "mean"),
        max_val=(metrica, "max"),
        registros=("incidentes", "count")
    ).round(2).sort_values("total", ascending=False).reset_index()
    df_tab.columns = [agg_col.capitalize(), "Total", "Média", "Máximo", "Registros"]
    st.dataframe(df_tab, use_container_width=True, height=280)

st.markdown("---")

# ─── Conclusão executiva ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">📝 Conclusão Executiva</div>', unsafe_allow_html=True)

top3_ataques = df.groupby("tipo_ataque")["incidentes"].sum().sort_values(ascending=False).head(3).index.tolist()
top_vuln     = df.groupby("vulnerabilidade")["incidentes"].sum().idxmax()
pct_critico  = (df[df["nivel_criticidade"]=="Crítico"]["incidentes"].sum() / df["incidentes"].sum() * 100)

st.markdown(f"""
<div class="insight-box" style="border-left-color:#60a5fa; font-size:0.95rem; line-height:1.8">
<b>🛡️ Análise de Segurança Cibernética — Brasil ({min(ano_sel)}–{max(ano_sel)})</b><br><br>

O período analisado registrou <b style="color:#2563eb">{total_incidentes:,} incidentes</b> de segurança digital,
com impacto financeiro estimado em <b style="color:#f97316">R$ {impacto_total/1e6:.1f} milhões</b>
e tempo médio de recuperação de <b>{tempo_medio:.1f} horas</b>.<br><br>

<b>Principais Ameaças:</b> Os ataques mais frequentes foram
{', '.join(f'<b>{a}</b>' for a in top3_ataques)}, refletindo a diversificação
das estratégias utilizadas por agentes maliciosos.<br><br>

<b>Vulnerabilidade Predominante:</b> A principal falha explorada foi
<b style="color:#f97316">{top_vuln}</b>, indicando a necessidade urgente de
capacitação humana e políticas de autenticação mais robustas.<br><br>

<b>Setor Mais Exposto:</b> O setor de <b>{setor_principal}</b> concentrou o maior
volume de incidentes, enquanto a região <b>{regiao_critica}</b> apresentou
a maior frequência de ataques.<br><br>

<b style="color:#ef4444">⚠️ {pct_critico:.1f}%</b> dos incidentes foram classificados como nível
<b>Crítico</b>, demandando planos de resposta imediata, monitoramento contínuo e
investimento prioritário em infraestrutura de segurança.
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Dashboard desenvolvido com Streamlit + Plotly | Projeto G2 · Tema 26 | Dados simulados 2015–2024")
