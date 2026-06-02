"""
Messi Goals — Aesthetic Dashboard
Theme: Stadium Night · Modern Editorial Glass
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. PAGE & CONFIGURATION SETUP (PENGATURAN HALAMAN Halaman)
# ==============================================================================

# Mengonfigurasi properti dasar aplikasi web Streamlit.
# Fungsi ini wajib dipanggil sebagai perintah Streamlit pertama pada script.
st.set_page_config(
    page_title="Messi · Goals Atlas",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 2. DESIGN SYSTEM & CONSTANTS (TOKEN DESAIN)
# Menjaga konsistensi warna, gradien, dan tipografi di seluruh komponen visual.
# ==============================================================================

INK        = "#0A0A0F"   # Latar belakang gelap utama (near-black)
INK_2      = "#11111A"   # Latar belakang gelap sekunder
SURFACE    = "rgba(255,255,255,0.04)" # Permukaan card semi-transparan (glassmorphism)
BORDER     = "rgba(255,255,255,0.08)"  # Warna border tipis transparan
TEXT       = "#F4F4F5"   # Warna teks utama yang terang dan kontras
MUTED      = "#8A8A99"   # Warna teks sekunder/redup
ROSE       = "#F43F5E"   # Aksen warna pink/merah (Barcelona)
AMBER      = "#F59E0B"   # Aksen warna emas/kuning (Golden Ballon d'Or)
CYAN       = "#22D3EE"   # Aksen warna biru muda (Argentina)
VIOLET     = "#8B5CF6"
MINT       = "#34D399"

# Sekuensial gradien untuk chart Plotly (transisi magenta ke kuning amber premium)
SEQ        = ["#1E1B2E", "#3B0F4A", "#7C1D6F", "#C2185B", "#F43F5E", "#F59E0B", "#FCD34D"]
CATEGORICAL = ["#F43F5E", "#22D3EE", "#F59E0B", "#8B5CF6", "#34D399", "#F472B6"]

# Font keluarga utama
FONT = "Inter, ui-sans-serif, system-ui, sans-serif"

# ==============================================================================
# 3. HELPER FUNCTIONS & STYLING (FUNGSI PEMBANTU & TAMPILAN)
# ==============================================================================

def inject_global_css():
    """
    Menyuntikkan kode CSS kustom ke dalam Streamlit.
    Digunakan untuk mendefinisikan latar belakang gradien dinamis pada aplikasi, 
    gaya kartu kpi dinamis saat di-hover, mask grid bergaya stadium, 
    serta kustomisasi sidebar dan scrollbar agar bertema premium editorial.
    """
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
    
      /* HERO */
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
          font-size: clamp(2.8rem, 6.6vw, 5.6rem);
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
    
      /* KPI cards */
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
    
      /* Section heads */
      .section {{
          display: flex; align-items: baseline; gap: 14px;
          margin: 36px 0 14px 0;
      }}
      .section .num {{
          font-family: 'JetBrains Mono', monospace;
          font-size: 11px; letter-spacing: .22em; color: {ROSE}; text-transform: uppercase;
      }}
      .section .title {{
          font-family: 'Space Grotesk', {FONT};
          font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; color: {TEXT};
      }}
      .section .rule {{
          flex: 1; height: 1px;
          background: linear-gradient(90deg, {BORDER}, transparent);
      }}
    
      /* Chart card wrap */
      .card {{
          border: 1px solid {BORDER};
          background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
          border-radius: 20px;
          padding: 18px 18px 8px 18px;
          backdrop-filter: blur(14px);
      }}
    
      /* Sidebar */
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
    
      /* Dataframe */
      [data-testid="stDataFrame"] {{
          border: 1px solid {BORDER}; border-radius: 16px; overflow: hidden;
      }}
    
      /* Divider */
      hr {{ border: none; height: 1px; background: linear-gradient(90deg, transparent, {BORDER}, transparent); margin: 28px 0; }}
    
      /* Footer */
      .footer {{
          margin-top: 60px; padding-top: 22px;
          border-top: 1px solid {BORDER};
          display: flex; justify-content: space-between; align-items: center;
          color: {MUTED}; font-size: 12px;
          font-family: 'JetBrains Mono', monospace; letter-spacing: .08em;
      }}
    
      /* Hide Streamlit chrome */
      #MainMenu, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

def style_fig(fig, height=380, showlegend=False):
    """
    Menyelaraskan tema visual visualisasi Plotly agar serasi dengan CSS global (Dark Mode).
    Mengatur warna latar belakang menjadi transparan, font kustom, serta warna garis grid.
    """
    fig.update_layout(
        template="plotly_dark",
        height=height,
        font=dict(family=FONT, color=TEXT, size=12),
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
    Menampilkan nomor bab kustom (misal: § 01) diikuti oleh judul bagian.
    """
    st.markdown(
        f"<div class='section'><span class='num'>§ {num}</span>"
        f"<span class='title'>{title}</span><span class='rule'></span></div>",
        unsafe_allow_html=True,
    )

# ==============================================================================
# 4. DATA PIPELINE (LOADING & CACHING)
# ==============================================================================

@st.cache_data
def load_data(path: str = "messi_all_goals.xlsx") -> pd.DataFrame:
    """
    Memuat data mentah dari Excel dan melakukan preprocessing.
    Menggunakan mekanisme cache Streamlit agar data tidak dimuat ulang 
    setiap kali user mengubah filter widget (meningkatkan performa secara dramatis).
    """
    df = pd.read_excel(path)
    df["date"] = pd.to_datetime(df["date"])
    
    # Normalisasi format musim:
    # Baris data lama memiliki format objek datetime (misal: datetime(2004,5,1) -> musim "2004-05").
    # Data baru berupa string plain ("2012-13"). Semua disamakan menjadi format "YYYY/YY" dengan "/" 
    # agar Plotly tidak salah menginterpretasikannya sebagai tipe tanggal berkala (yang mematahkan grafik).
    def _parse_season(val):
        if isinstance(val, str):
            return val.replace("-", "/")   # "2012-13" → "2012/13"
        try:
            return pd.to_datetime(val).strftime("%Y/%m")  # datetime(2004,5,1) → "2004/05"
        except Exception:
            return str(val)
            
    df["season"] = df["season"].apply(_parse_season)
    
    # Cast kolom kategori ke string untuk mencegah inkonsistensi tipe data saat plotting
    for c in ("club", "competition", "venue", "goal_type",
              "player_position", "goal_minute_bucket", "assist_player"):
        if c in df.columns:
            df[c] = df[c].astype(str)
            
    return df

# ==============================================================================
# 5. USER INTERFACE COMPONENTS (MODUL UI/TAMPILAN)
# ==============================================================================

def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Merender sidebar navigasi filter dan mengembalikan dataset yang telah difilter.
    """
    with st.sidebar:
        st.markdown("## Filters")
        st.caption("Refine the dataset")

        # Mengambil opsi unik untuk filter pilihan
        seasons = sorted(df["season"].unique())
        clubs   = sorted(df["club"].unique())
        comps   = sorted(df["competition"].unique())

        # Widget pilihan filter interaktif
        sel_seasons = st.multiselect("Season", seasons, default=seasons)
        sel_clubs   = st.multiselect("Club", clubs, default=clubs)
        sel_comps   = st.multiselect("Competition", comps, default=comps)
        sel_venue   = st.radio("Venue", ["All", "Home", "Away"], horizontal=True)

        st.markdown("---")
        # Informasi total dataset mentah
        st.markdown(
            f"<div style='font-family:JetBrains Mono,monospace;font-size:11px;color:{MUTED};letter-spacing:.12em'>"
            f"DATASET · {len(df):,} GOALS<br/>2004 → 2024</div>",
            unsafe_allow_html=True,
        )

    # Melakukan pemotongan baris data berdasarkan filter yang dipilih user
    mask = (
        df["season"].isin(sel_seasons)
        & df["club"].isin(sel_clubs)
        & df["competition"].isin(sel_comps)
    )
    if sel_venue != "All":
        mask &= df["venue"] == sel_venue
        
    return df[mask].copy()

def render_hero(total_goals: int):
    """
    Merender Hero Header Section (banner atas) yang menyapa pengguna dengan ringkasan deskripsi.
    """
    st.markdown(f"""
    <div class="hero">
      <span class="hero-tag"><span class="dot"></span>STADIUM NIGHT · MESSI LEGACY · VOL. 10</span>
      <h1>Every goal,<br/>every <em>minute</em>, every stage.</h1>
      <p class="lede">An interactive atlas of {total_goals:,} career goals scored by Lionel Messi —
      spanning two continents, four clubs, and two decades of impossible football.</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpis(d: pd.DataFrame):
    """
    Menghitung dan menampilkan metrik utama (KPI) pada grid 4 kolom teratas.
    """
    total = len(d)
    seasons_active = d["season"].nunique()
    top_comp = d["competition"].value_counts().idxmax() if total else "—"
    top_assist = (
        d[d["assist_player"].str.lower() != "not applicable"]["assist_player"]
        .value_counts().idxmax() if total else "—"
    )
    home_share = (d["venue"].eq("Home").mean() * 100) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    # Merender setiap card KPI menggunakan blok kode HTML div kustom
    for col, label, value, sub in [
        (c1, "Total Goals",     f"{total:,}",          "filtered dataset"),
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

def render_seasons_and_clubs(d: pd.DataFrame):
    """
    Bagian 1: Visualisasi Tren Gol per Musim (Line Spline Chart) 
    dan Distribusi Gol berdasarkan Klub (Horizontal Bar Chart).
    """
    render_section_header("01", "Goals across the seasons")
    left, right = st.columns([2, 1])

    with left:
        # Menghitung agregat gol per musim untuk grafik deret waktu
        s = d.groupby("season").size().reset_index(name="goals").sort_values("season")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=s["season"], y=s["goals"], mode="lines",
            line=dict(color=ROSE, width=3, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(244,63,94,0.12)",
            hovertemplate="<b>%{x}</b><br>%{y} goals<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=s["season"], y=s["goals"], mode="markers",
            marker=dict(color=AMBER, size=8, line=dict(color=INK, width=2)),
            hoverinfo="skip",
        ))
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.plotly_chart(style_fig(fig, 360), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        # Menghitung jumlah gol untuk setiap klub yang dibela
        cl = d["club"].value_counts().reset_index()
        cl.columns = ["club", "goals"]
        fig = px.bar(cl, x="goals", y="club", orientation="h",
                     color="goals", color_continuous_scale=SEQ, text="goals")
        fig.update_traces(texttemplate="%{text}", textposition="outside",
                          textfont=dict(color=TEXT, size=11),
                          marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.plotly_chart(style_fig(fig, 360), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_goal_anatomy(d: pd.DataFrame):
    """
    Bagian 2: Visualisasi Metode Pencetakan Gol (Tipe Gol) dan Rentang Waktu (Minute Buckets).
    """
    render_section_header("02", "The anatomy of a goal")
    left, right = st.columns(2)

    with left:
        # 8 Tipe gol terbanyak
        gt = d["goal_type"].value_counts().head(8).reset_index()
        gt.columns = ["goal_type", "count"]
        fig = px.bar(gt, x="count", y="goal_type", orientation="h",
                     color="count", color_continuous_scale=SEQ, text="count")
        fig.update_traces(texttemplate="%{text}", textposition="outside",
                          textfont=dict(color=TEXT, size=11), marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.plotly_chart(style_fig(fig, 380), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        # Pengelompokan menit gol berdasarkan interval 15 menit
        bucket_order = ["0-15","16-30","31-45","46-60","61-75","76-90","91+"]
        mb = d["goal_minute_bucket"].value_counts().reindex(bucket_order, fill_value=0).reset_index()
        mb.columns = ["bucket", "count"]
        fig = px.bar(mb, x="bucket", y="count",
                     color="count", color_continuous_scale=SEQ, text="count")
        fig.update_traces(texttemplate="%{text}", textposition="outside",
                          textfont=dict(color=TEXT, size=11), marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.plotly_chart(style_fig(fig, 380), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_geography_and_rhythm(d: pd.DataFrame, total_goals_filtered: int):
    """
    Bagian 3: Visualisasi Distribusi Laga Home/Away dan Proporsi Posisi Bermain Messi.
    """
    render_section_header("03", "Geography & rhythm")
    left, right = st.columns(2)

    with left:
        # Pembagian gol kandang (Home) vs tandang (Away) per musim
        ven = d.groupby(["season", "venue"]).size().reset_index(name="goals")
        fig = px.bar(ven, x="season", y="goals", color="venue", barmode="group",
                     color_discrete_map={"Home": ROSE, "Away": CYAN})
        fig.update_traces(marker_line_width=0)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.plotly_chart(style_fig(fig, 360, showlegend=True), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        # Donut Chart untuk persentase gol berdasarkan posisi pemain di lapangan
        pos = d["player_position"].value_counts().reset_index()
        pos.columns = ["position", "goals"]
        fig = go.Figure(go.Pie(
            labels=pos["position"], values=pos["goals"], hole=0.65,
            marker=dict(colors=CATEGORICAL, line=dict(color=INK, width=2)),
            textinfo="label+percent", textfont=dict(color=TEXT, family=FONT, size=12),
            hovertemplate="<b>%{label}</b><br>%{value} goals (%{percent})<extra></extra>",
        ))
        # Menambahkan angka statistik di pusat lubang Donut Chart
        fig.add_annotation(text=f"<b>{total_goals_filtered}</b><br><span style='font-size:11px;color:{MUTED}'>goals</span>",
                           showarrow=False, font=dict(color=TEXT, family=FONT, size=22))
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.plotly_chart(style_fig(fig, 360, showlegend=False), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_season_minute_heatmap(d: pd.DataFrame):
    """
    Bagian 4: Heatmap Kerapatan Gol berdasarkan Persilangan Musim x Menit Pertandingan.
    """
    render_section_header("04", "The heatmap — season × minute")
    
    # Pivot tabel gol untuk mendistribusikan jumlah gol ke baris Musim dan kolom Menit
    hm = (d.groupby(["season", "goal_minute_bucket"]).size()
            .reset_index(name="goals")
            .pivot(index="season", columns="goal_minute_bucket", values="goals")
            .reindex(columns=["0-15","16-30","31-45","46-60","61-75","76-90","91+"])
            .fillna(0))
            
    fig = go.Figure(go.Heatmap(
        z=hm.values, x=hm.columns, y=hm.index,
        colorscale=[[0, "#0F0A18"], [0.25, "#3B0F4A"], [0.5, "#7C1D6F"],
                    [0.75, "#F43F5E"], [1, "#F59E0B"]],
        hovertemplate="<b>%{y}</b> · %{x}<br>%{z} goals<extra></extra>",
        colorbar=dict(thickness=10, tickfont=dict(color=MUTED, size=10),
                      outlinewidth=0, len=0.7),
    ))
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(style_fig(fig, 460), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_closest_collaborators(d: pd.DataFrame):
    """
    Bagian 5: Grafik Horizontal Bar untuk Pemain Penyumbang Assist Terbanyak.
    """
    render_section_header("05", "Closest collaborators")
    
    # Filter out goals where there is no assist record (e.g. Solo/Penalty/Not Applicable)
    ap = (d[d["assist_player"].str.lower() != "not applicable"]
            ["assist_player"].value_counts().head(12).reset_index())
    ap.columns = ["assist_player", "assists"]
    
    fig = px.bar(ap, x="assists", y="assist_player", orientation="h",
                 color="assists", color_continuous_scale=SEQ, text="assists")
    fig.update_traces(texttemplate="%{text}", textposition="outside",
                      textfont=dict(color=TEXT, size=11), marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(style_fig(fig, 460), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_complete_records_table(d: pd.DataFrame):
    """
    Bagian 6: Tabel Data Utama yang Menampilkan Seluruh Record Gol secara Interaktif.
    """
    render_section_header("06", "The complete record")
    st.dataframe(
        d[["date","season","club","competition","venue","player_position",
           "goal_minute_bucket","goal_type","assist_player"]]
          .sort_values("date", ascending=False).reset_index(drop=True),
        use_container_width=True, height=420,
    )

def render_footer():
    """
    Merender HTML kustom untuk footer hak cipta di bagian bawah halaman.
    """
    st.markdown(
        f"<div class='footer'>"
        f"<span>© MESSI · GOALS ATLAS</span>"
        f"<span>STADIUM NIGHT — DATA VISUALIZATION</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

# ==============================================================================
# 6. APPLICATION ENTRY POINT (FUNGSI UTAMA / MAIN)
# ==============================================================================

def main():
    """
    Alur eksekusi terstruktur aplikasi dashboard.
    """
    # 1. Suntikkan CSS kustom
    inject_global_css()
    
    # 2. Muat dataset ter-caching
    df = load_data()
    
    # 3. Render sidebar dan dapatkan data terfilter
    filtered_df = render_sidebar(df)
    
    # 4. Render Layout Dashboard
    render_hero(len(df)) # Tampilkan total gol keseluruhan di Hero
    render_kpis(filtered_df)
    render_seasons_and_clubs(filtered_df)
    render_goal_anatomy(filtered_df)
    render_geography_and_rhythm(filtered_df, len(filtered_df))
    render_season_minute_heatmap(filtered_df)
    render_closest_collaborators(filtered_df)
    render_complete_records_table(filtered_df)
    render_footer()

if __name__ == "__main__":
    main()
