"""
Messi Goals — Aesthetic Dashboard V2
Tema: Stadium Night · Modern Editorial Glass
Struktur: Linear (Flat) & Layout Berurutan (1 Grafik per Baris)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==============================================================================
# 1. SETUP KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="Messi · Goals Atlas V2",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 2. KONSTANTA DESAIN & WARNA (Stadium Night)
# ==============================================================================
INK        = "#0A0A0F"   # Latar belakang utama (near-black)
INK_2      = "#11111A"   # Latar belakang sekunder (sidebar & tooltip)
SURFACE    = "rgba(255,255,255,0.04)"  # Permukaan card transparan
BORDER     = "rgba(255,255,255,0.08)"  # Garis tepi card
TEXT       = "#F4F4F5"   # Warna teks utama (putih terang)
MUTED      = "#8A8A99"   # Warna teks sekunder (abu-abu)
ROSE       = "#F43F5E"   # Aksen merah/pink (untuk Home / elemen utama)
AMBER      = "#F59E0B"   # Aksen emas/kuning
CYAN       = "#22D3EE"   # Aksen biru muda (untuk Away)

# Palet warna untuk donut chart (dari kategori terbesar ke terkecil)
CATEGORICAL = ["#F43F5E", "#22D3EE", "#F59E0B", "#8B5CF6", "#34D399", "#F472B6"]

# Font utama yang digunakan
FONT = "Inter, ui-sans-serif, system-ui, sans-serif"

# ==============================================================================
# 3. INJEKSI CSS KUSTOM (Tema Premium & Efek Kaca)
# ==============================================================================
st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
  html, body, [class*="css"], .stApp {{
      font-family: {FONT};
      color: {TEXT};
  }}
  .stApp {{
      background:
        radial-gradient(1200px 600px at 85% -10%, rgba(244,63,94,0.18), transparent 60%),
        radial-gradient(900px 500px at -10% 10%, rgba(139,92,246,0.18), transparent 60%),
        radial-gradient(800px 400px at 50% 110%, rgba(34,211,238,0.12), transparent 60%),
        linear-gradient(180deg, {INK} 0%, {INK_2} 100%);
      background-attachment: fixed;
  }}
  [data-testid="stHeader"] {{ background: transparent; }}
  .block-container {{ padding-top: 1.2rem; padding-bottom: 4rem; max-width: 1400px; }}

  /* Kartu Banner Hero */
  .hero {{
      position: relative;
      padding: 56px 44px 48px 44px;
      border-radius: 28px;
      border: 1px solid {BORDER};
      background:
        radial-gradient(600px 240px at 90% 0%, rgba(244,63,94,0.18), transparent 70%),
        linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
      backdrop-filter: blur(20px);
      overflow: hidden;
      margin-bottom: 28px;
  }}
  .hero::before {{
      content: ""; position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
      background-size: 56px 56px;
      mask-image: radial-gradient(ellipse at 50% 0%, black 30%, transparent 80%);
      pointer-events: none;
  }}
  .hero-tag {{
      display: inline-flex; align-items: center; gap: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px; letter-spacing: .22em; text-transform: uppercase;
      color: {MUTED};
      padding: 6px 12px; border-radius: 999px;
      border: 1px solid {BORDER};
      background: rgba(255,255,255,0.03);
  }}
  .hero-tag .dot {{
      width: 6px; height: 6px; border-radius: 50%; background: {ROSE};
      box-shadow: 0 0 12px {ROSE};
  }}
  .hero h1 {{
      font-family: 'Space Grotesk', {FONT};
      font-size: clamp(2.4rem, 5.5vw, 4.5rem);
      font-weight: 700;
      letter-spacing: -0.035em;
      line-height: 0.98;
      margin: 18px 0 14px 0;
      background: linear-gradient(135deg, #FFFFFF 0%, #F4F4F5 40%, {ROSE} 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
  }}
  .hero h1 em {{
      font-family: 'Instrument Serif', 'Space Grotesk', serif;
      font-style: italic; font-weight: 400;
      color: {AMBER}; -webkit-text-fill-color: {AMBER};
  }}
  .hero p.lede {{
      max-width: 640px; color: {MUTED};
      font-size: 1.02rem; line-height: 1.6; margin: 0;
  }}

  /* Kartu KPI / Metrik */
  .kpi {{
      padding: 22px 22px 20px 22px;
      border-radius: 20px;
      border: 1px solid {BORDER};
      background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
      backdrop-filter: blur(14px);
      transition: transform .25s ease, border-color .25s ease;
      height: 100%;
  }}
  .kpi:hover {{ transform: translateY(-2px); border-color: rgba(244,63,94,0.4); }}
  .kpi .label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px; letter-spacing: .2em; text-transform: uppercase;
      color: {MUTED};
  }}
  .kpi .value {{
      font-family: 'Space Grotesk', {FONT};
      font-size: 2.6rem; font-weight: 600; letter-spacing: -0.03em;
      color: {TEXT}; margin-top: 6px; font-variant-numeric: tabular-nums;
  }}
  .kpi .sub {{ font-size: 12.5px; color: {MUTED}; margin-top: 4px; }}
  .kpi .accent {{ color: {ROSE}; }}

  /* Kepala Bagian (Section Header) */
  .section {{
      display: flex; align-items: baseline; gap: 14px;
      margin: 28px 0 14px 0;
  }}
  .section .num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px; letter-spacing: .22em; color: {ROSE}; text-transform: uppercase;
  }}
  .section .title {{
      font-family: 'Space Grotesk', {FONT};
      font-size: 1.25rem; font-weight: 600; letter-spacing: -0.02em; color: {TEXT};
  }}
  .section .rule {{
      flex: 1; height: 1px;
      background: linear-gradient(90deg, {BORDER}, transparent);
  }}

  /* Wadah Kartu Grafik */
  .card {{
      border: 1px solid {BORDER};
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      border-radius: 20px;
      padding: 18px 18px 8px 18px;
      backdrop-filter: blur(14px);
      margin-bottom: 24px;
  }}

  /* Kustomisasi Sidebar */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, rgba(10,10,15,0.85), rgba(17,17,26,0.85));
      backdrop-filter: blur(20px);
      border-right: 1px solid {BORDER};
  }}
  [data-testid="stSidebar"] * {{ color: {TEXT}; }}
  [data-testid="stSidebar"] h2 {{
      font-family: 'Space Grotesk', {FONT};
      font-size: 1.05rem; font-weight: 600;
      letter-spacing: .04em; text-transform: uppercase;
      color: {ROSE}; margin-bottom: 4px;
  }}
  [data-testid="stSidebar"] label {{ color: {MUTED} !important; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; }}

  /* Tabel Data */
  [data-testid="stDataFrame"] {{
      border: 1px solid {BORDER}; border-radius: 16px; overflow: hidden;
  }}

  /* Gaya elemen seleksi / input filter */
  div[data-baseweb="select"] > div {{
      background-color: #11111A !important;
      border-color: rgba(244,63,94,0.25) !important;
      color: #F4F4F5 !important;
      border-radius: 10px !important;
  }}
  div[data-baseweb="select"] input {{
      color: #F4F4F5 !important;
  }}
  ul[role="listbox"] {{
      background-color: #11111A !important;
      border: 1px solid rgba(244,63,94,0.25) !important;
      border-radius: 12px !important;
  }}
  li[role="option"] {{
      background-color: #11111A !important;
      color: #F4F4F5 !important;
  }}
  li[role="option"]:hover {{
      background-color: rgba(244,63,94,0.12) !important;
      color: #F4F4F5 !important;
  }}
  li[role="option"][aria-selected="true"] {{
      background-color: rgba(244,63,94,0.18) !important;
      color: #F4F4F5 !important;
  }}
  span[data-baseweb="tag"] {{
      background-color: rgba(244,63,94,0.15) !important;
      color: #F4F4F5 !important;
      border: 1px solid rgba(244,63,94,0.40) !important;
      border-radius: 6px !important;
  }}
  span[data-baseweb="tag"] span[data-baseweb="tag-action"] svg path {{
      fill: {ROSE} !important;
  }}

  /* Garis Pembatas */
  hr {{ border: none; height: 1px; background: linear-gradient(90deg, transparent, {BORDER}, transparent); margin: 28px 0; }}

  /* Footer */
  .footer {{
      margin-top: 60px; padding-top: 22px;
      border-top: 1px solid {BORDER};
      display: flex; justify-content: space-between; align-items: center;
      color: {MUTED}; font-size: 12px;
      font-family: 'JetBrains Mono', monospace; letter-spacing: .08em;
  }}

  /* Menyembunyikan menu bawaan Streamlit */
  #MainMenu, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. FUNGSI PEMBANTU (Helper Functions)
# ==============================================================================
def style_fig(fig, height=380, showlegend=False):
    """
    Menyelaraskan tema visual visualisasi Plotly agar serasi dengan CSS global (Dark Mode).
    """
    fig.update_layout(
        template="plotly_dark",
        height=height,
        font=dict(family=FONT, color=TEXT, size=11),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=showlegend,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                    font=dict(color=MUTED, size=11)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)",
                   tickfont=dict(color=MUTED, size=11), title=None),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)",
                   tickfont=dict(color=MUTED, size=11), title=None),
        hoverlabel=dict(bgcolor="#11111A", bordercolor=ROSE, font=dict(color=TEXT, family=FONT)),
    )
    return fig

def render_section_header(num: str, title: str):
    """
    Merender baris pemisah visual antar bagian dashboard.
    """
    st.markdown(
        f"<div class='section'><span class='num'>§ {num}</span>"
        f"<span class='title'>{title}</span><span class='rule'></span></div>",
        unsafe_allow_html=True,
    )

# ==============================================================================
# 5. DATA PIPELINE (Loading & Caching)
# ==============================================================================
@st.cache_data
def load_data(path: str = "messi_all_goals.xlsx") -> pd.DataFrame:
    """
    Memuat data mentah dari Excel dan melakukan normalisasi kolom.
    """
    df = pd.read_excel(path)
    df["date"] = pd.to_datetime(df["date"])

    # Normalisasi format musim ke "YYYY/YY"
    def _parse_season(val):
        if isinstance(val, str):
            return val.replace("-", "/")   # "2012-13" -> "2012/13"
        try:
            return pd.to_datetime(val).strftime("%Y/%m")  # datetime -> "2004/05"
        except Exception:
            return str(val)

    df["season"] = df["season"].apply(_parse_season)

    # Cast kolom kategori ke string
    for c in ("club", "competition", "venue", "goal_type",
              "player_position", "goal_minute_bucket", "assist_player"):
        if c in df.columns:
            df[c] = df[c].astype(str)

    return df

# ==============================================================================
# 6. PEMBACAAN DATA UTAMA
# ==============================================================================
df_master = load_data()

# ==============================================================================
# 7. FILTER SIDEBAR (Langsung di Alur Utama)
# ==============================================================================
with st.sidebar:
    st.markdown("## Filters")
    st.caption("Refine the dataset")

    seasons    = sorted(df_master["season"].unique())
    clubs      = sorted(df_master["club"].unique())
    comps      = sorted(df_master["competition"].unique())
    goal_types = sorted(df_master["goal_type"].unique())
    positions  = sorted(df_master["player_position"].unique())

    sel_seasons    = st.multiselect("Season", seasons, default=seasons)
    sel_clubs      = st.multiselect("Club", clubs, default=clubs)
    sel_comps      = st.multiselect("Competition", comps, default=comps)
    sel_goal_types = st.multiselect("Goal Type", goal_types, default=goal_types)
    sel_positions  = st.multiselect("Player Position", positions, default=positions)
    sel_venue      = st.radio("Venue", ["All", "Home", "Away"], horizontal=True)

    st.markdown("---")
    st.markdown(
        f"<div style='font-family:JetBrains Mono,monospace;font-size:11px;color:{MUTED};letter-spacing:.12em'>"
        f"DATASET · {len(df_master):,} GOALS<br/>2004 → 2024</div>",
        unsafe_allow_html=True,
    )

# Terapkan filter ke DataFrame utama
mask = (
    df_master["season"].isin(sel_seasons)
    & df_master["club"].isin(sel_clubs)
    & df_master["competition"].isin(sel_comps)
    & df_master["goal_type"].isin(sel_goal_types)
    & df_master["player_position"].isin(sel_positions)
)
if sel_venue != "All":
    mask &= df_master["venue"] == sel_venue

df = df_master[mask].copy()

# Hentikan proses jika hasil filter kosong
if df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter.")
    st.stop()

# ==============================================================================
# 8. HERO HEADER
# ==============================================================================
st.markdown(f"""
<div class="hero">
  <span class="hero-tag"><span class="dot"></span>STADIUM NIGHT · MESSI LEGACY · VOL. 10</span>
  <h1>Every goal,<br/>every <em>minute</em>, every stage.</h1>
  <p class="lede">An interactive atlas of {len(df_master):,} career goals scored by Lionel Messi —
  spanning two continents, four clubs, and two decades of impossible football.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 9. KPI METRIK UTAMA
# ==============================================================================
total_goals = len(df)
seasons_active = df["season"].nunique()
top_comp = df["competition"].value_counts().idxmax() if total_goals else "—"
top_assist = (
    df[df["assist_player"].str.lower() != "not applicable"]["assist_player"]
    .value_counts().idxmax() if total_goals else "—"
)
home_share = (df["venue"].eq("Home").mean() * 100) if total_goals else 0

c1, c2, c3, c4 = st.columns(4)
for col, label, value, sub in [
    (c1, "Total Goals",     f"{total_goals:,}",          "filtered dataset"),
    (c2, "Active Seasons",  f"{seasons_active}",   "across the timeline"),
    (c3, "Top Competition", f"{top_comp[:18]}",    "by goal count"),
    (c4, "Home Share",      f"{home_share:.0f}%",  f"top assist · {top_assist[:18]}"),
]:
    with col:
        st.markdown(
            f"<div class='kpi'><div class='label'>{label}</div>"
            f"<div class='value accent'>{value}</div>"
            f"<div class='sub'>{sub}</div></div>",
            unsafe_allow_html=True,
        )

# Garis pemisah setelah metrik
st.markdown("<hr/>", unsafe_allow_html=True)

# ==============================================================================
# 10. GRID GRAFIK - LAYOUT KOLOM (Opsi B: st.columns(2))
# ==============================================================================

# ------------------------------------------------------------------------------
# BARIS 1: Grafik 01 (Tren per Musim) & Grafik 02 (Gol per Klub)
# ------------------------------------------------------------# Grafik 01 (Tren per Musim)
render_section_header("01", "Goals across the seasons")
s = df.groupby(["season", "club"]).size().reset_index(name="goals").sort_values("season")
fig1 = px.line(
    s, x="season", y="goals", color="club", line_shape="spline",
    color_discrete_map={
        "FC Barcelona":        "#5C7CFA",
        "Inter Miami CF":      "#FF6B6B",
        "Paris Saint-Germain": "#20C997",
        "Argentina":           "#22D3EE",
    }
)
fig1.update_traces(mode="lines+markers", marker=dict(size=6))

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(style_fig(fig1, 360, showlegend=True), width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# Grafik 02 (Gol per Klub)
render_section_header("02", "Goals by club")
cl = df.groupby(["club", "venue"]).size().reset_index(name="goals")
club_totals = cl.groupby("club")["goals"].sum().reset_index().sort_values("goals", ascending=False)
cl["club"] = pd.Categorical(cl["club"], categories=club_totals["club"], ordered=True)
cl = cl.sort_values("club")

fig2 = px.bar(
    cl, x="goals", y="club", orientation="h",
    color="venue",
    color_discrete_map={"Home": ROSE, "Away": CYAN},
    text="goals"
)
fig2.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    textfont=dict(color=TEXT, size=11),
    marker_line_width=0
)
fig2.update_layout(yaxis=dict(autorange="reversed"))

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(style_fig(fig2, 360, showlegend=True), width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BARIS 2: Grafik 03 (Tipe Gol) & Grafik 04 (Rentang Menit)
# ------------------------------------------------------------------------------
# Grafik 03 (Distribusi Tipe Gol)
render_section_header("03", "Goal type distribution")
top_types  = df["goal_type"].value_counts().head(8).index
gt_filtered = df[df["goal_type"].isin(top_types)]
gt = gt_filtered.groupby(["goal_type", "club"]).size().reset_index(name="count")

type_totals = gt.groupby("goal_type")["count"].sum().reset_index().sort_values("count", ascending=False)
gt["goal_type"] = pd.Categorical(gt["goal_type"], categories=type_totals["goal_type"], ordered=True)
gt = gt.sort_values("goal_type")

fig3 = px.bar(
    gt, x="count", y="goal_type", orientation="h",
    color="club",
    color_discrete_map={
        "FC Barcelona":        "#5C7CFA",
        "Inter Miami CF":      "#FF6B6B",
        "Paris Saint-Germain": "#20C997",
        "Argentina":           "#22D3EE",
    },
    text="count"
)
fig3.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    textfont=dict(color=TEXT, size=11),
    marker_line_width=0
)
fig3.update_layout(yaxis=dict(autorange="reversed"))

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(style_fig(fig3, 380, showlegend=True), width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# Grafik 04 (Rentang Menit Gol)
render_section_header("04", "Goal timing / minute bucket")
mb = df.groupby(["goal_minute_bucket", "venue"]).size().reset_index(name="count")
bucket_order = ["0-15","16-30","31-45","46-60","61-75","76-90","91+"]
mb["goal_minute_bucket"] = pd.Categorical(mb["goal_minute_bucket"], categories=bucket_order, ordered=True)
mb = mb.sort_values("goal_minute_bucket")

fig4 = px.bar(
    mb, x="goal_minute_bucket", y="count",
    color="venue",
    color_discrete_map={"Home": ROSE, "Away": CYAN},
    text="count"
)
fig4.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    textfont=dict(color=TEXT, size=11),
    marker_line_width=0
)
fig4.update_layout(coloraxis_showscale=False)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(style_fig(fig4, 380, showlegend=True), width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BARIS 3: Grafik 05 (Home vs Away per Musim) & Grafik 06 (Donut Chart Posisi)
# ------------------------------------------------------------------------------
# Grafik 05 (Perbandingan Home/Away per Musim)
render_section_header("05", "Venue comparison (Home vs Away)")
ven = df.groupby(["season", "venue"]).size().reset_index(name="goals")
fig5 = px.bar(
    ven, x="season", y="goals",
    color="venue",
    barmode="group",
    color_discrete_map={"Home": ROSE, "Away": CYAN}
)
fig5.update_traces(marker_line_width=0)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(style_fig(fig5, 360, showlegend=True), width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# Grafik 06 (Donut Chart Posisi Pemain)
render_section_header("06", "Goals by player position")
pos = df["player_position"].value_counts().reset_index()
pos.columns = ["position", "goals"]

fig6 = go.Figure(go.Pie(
    labels=pos["position"],
    values=pos["goals"],
    hole=0.65,
    marker=dict(
        colors=CATEGORICAL,
        line=dict(color=INK, width=2)
    ),
    textinfo="label+percent",
    textfont=dict(color=TEXT, family=FONT, size=11),
    hovertemplate="<b>%{label}</b><br>%{value} goals (%{percent})<extra></extra>",
))
fig6.add_annotation(
    text=f"<b>{total_goals}</b><br><span style='font-size:11px;color:{MUTED}'>goals</span>",
    showarrow=False,
    font=dict(color=TEXT, family=FONT, size=20)
)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(style_fig(fig6, 360, showlegend=False), width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BARIS 4: Grafik 07 (Heatmap Musim vs Menit) & Grafik 08 (Assist Partner)
# ------------------------------------------------------------------------------
# Grafik 07 (Heatmap Musim vs Menit)
render_section_header("07", "Heatmap — season × minute")

# Kelompokkan data heatmap
hm = (df.groupby(["season", "goal_minute_bucket"]).size()
        .reset_index(name="goals")
        .pivot(index="season", columns="goal_minute_bucket", values="goals")
        .reindex(columns=["0-15","16-30","31-45","46-60","61-75","76-90","91+"])
        .fillna(0))

text_vals = np.where(hm.values == 0, "", hm.values.astype(int).astype(str))

fig7 = go.Figure(go.Heatmap(
    z=hm.values,
    x=hm.columns,
    y=hm.index,
    colorscale=[
        [0,    "#0F0A18"],
        [0.25, "#3B0F4A"],
        [0.5,  "#7C1D6F"],
        [0.75, "#F43F5E"],
        [1,    "#F59E0B"],
    ],
    hovertemplate="<b>%{y}</b> · %{x}<br>%{z} goals<extra></extra>",
    colorbar=dict(
        thickness=10,
        tickfont=dict(color=MUTED, size=10),
        outlinewidth=0,
        len=0.7
    ),
    text=text_vals,
    texttemplate="%{text}",
    textfont=dict(color="white", size=11, family=FONT),
))

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(style_fig(fig7, 460), width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# Grafik 08 (Assist Partner Terbaik)
render_section_header("08", "Top Assist Partners")
df_assist = df[df["assist_player"].str.lower() != "not applicable"]

if len(df_assist) > 0:
    top_assisters = df_assist["assist_player"].value_counts().head(15).index
    ap_grouped = df_assist[df_assist["assist_player"].isin(top_assisters)]
    ap = ap_grouped.groupby(["assist_player", "club"]).size().reset_index(name="jumlah_assist")

    player_totals = ap.groupby("assist_player")["jumlah_assist"].sum().reset_index().sort_values("jumlah_assist", ascending=False)
    ap["assist_player"] = pd.Categorical(ap["assist_player"], categories=player_totals["assist_player"], ordered=True)
    ap = ap.sort_values("assist_player")

    fig8 = px.bar(
        ap, x="jumlah_assist", y="assist_player", orientation="h",
        color="club",
        color_discrete_map={
            "FC Barcelona":        "#5C7CFA",
            "Inter Miami CF":      "#FF6B6B",
            "Paris Saint-Germain": "#20C997",
            "Argentina":           "#22D3EE",
        },
        labels={"jumlah_assist": "jumlah_assist", "assist_player": "assist_player"}
    )
    fig8.update_traces(marker_line_width=0)
    fig8.update_layout(yaxis=dict(autorange="reversed"))

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(style_fig(fig8, 460, showlegend=True), width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.info("No assist data available for the current selection.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 11. TABEL DATA LENGKAP (Lebar Penuh)
# ==============================================================================
render_section_header("09", "The complete record")
st.dataframe(
    df[["date","season","club","competition","venue","player_position",
       "goal_minute_bucket","goal_type","assist_player"]]
      .sort_values("date", ascending=False).reset_index(drop=True),
    width="stretch", height=420,
)

# ==============================================================================
# 12. FOOTER HALAMAN
# ==============================================================================
st.markdown(
    f"<div class='footer'>"
    f"<span>© MESSI · GOALS ATLAS V2</span>"
    f"<span>STADIUM NIGHT — DATA VISUALIZATION</span>"
    f"</div>",
    unsafe_allow_html=True,
)
