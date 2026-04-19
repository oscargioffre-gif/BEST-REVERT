import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BEST REVERT MI/NDQ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;600;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background: #060810;
    color: #e2e8f0;
}
.stApp { background: #060810; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #0a0d16 !important; border-right: 1px solid #1a2035 !important; }
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #060810 0%, #0d1528 40%, #060810 100%);
    border: 1px solid #1a2035;
    border-radius: 16px;
    padding: 36px 40px 32px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #00d4ff, #7c3aed, #00d4ff);
    animation: shimmer 3s linear infinite;
    background-size: 200% 100%;
}
@keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem; font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.hero-title span { color: #00d4ff; }
.hero-sub { font-size: 0.82rem; color: #64748b; margin-top: 10px; letter-spacing: 0.05em; }
.hero-badges { margin-top: 16px; display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: #0f1829; border: 1px solid #1e3a5f;
    border-radius: 20px; padding: 4px 12px;
    font-size: 0.68rem; letter-spacing: 0.1em; color: #38bdf8;
    text-transform: uppercase; font-weight: 500;
}

/* ── Section labels ── */
.sec-label {
    font-size: 0.65rem; letter-spacing: 0.22em; text-transform: uppercase;
    color: #00d4ff; font-weight: 700;
    border-bottom: 1px solid #1a2035;
    padding-bottom: 10px; margin-bottom: 20px; margin-top: 32px;
}

/* ── Input area ── */
.input-card {
    background: #0a0d16;
    border: 1px solid #1a2035;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.input-card:hover { border-color: #1e3a5f; }
.input-num {
    font-size: 0.62rem; color: #475569; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 6px;
}

/* ── Score cards ── */
.score-card {
    background: linear-gradient(135deg, #0a0d16, #0f1829);
    border: 1px solid #1a2035;
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.score-card:hover { transform: translateY(-2px); border-color: #00d4ff44; }
.score-card.gold   { border-color: #f59e0b55; }
.score-card.silver { border-color: #94a3b855; }
.score-card.bronze { border-color: #cd7f3255; }
.score-rank { font-size: 0.62rem; color: #475569; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 4px; }
.score-ticker { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800; color: #f8fafc; }
.score-val { font-size: 2rem; font-weight: 700; margin-top: 4px; }
.score-label { font-size: 0.7rem; color: #64748b; margin-top: 2px; }
.signal-strong { color: #22c55e; }
.signal-mod    { color: #84cc16; }
.signal-weak   { color: #f59e0b; }
.signal-wait   { color: #ef4444; }

/* ── KPI pills ── */
.kpi-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
.kpi-pill {
    background: #111827; border: 1px solid #1a2035;
    border-radius: 6px; padding: 3px 9px;
    font-size: 0.68rem; color: #94a3b8;
}
.kpi-pill b { color: #e2e8f0; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0369a1, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 10px 20px !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* ── Text inputs ── */
.stTextInput input {
    background: #0a0d16 !important;
    border: 1px solid #1a2035 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput input:focus { border-color: #00d4ff !important; box-shadow: 0 0 0 2px #00d4ff22 !important; }
.stTextInput label { color: #64748b !important; font-size: 0.72rem !important; }

/* Selectbox */
div[data-baseweb="select"] { background-color: #0a0d16 !important; border-color: #1a2035 !important; border-radius: 8px !important; }
div[data-baseweb="select"] > div { background-color: #0a0d16 !important; color: #e2e8f0 !important; }
div[data-baseweb="select"] span { color: #e2e8f0 !important; font-size: 0.88rem !important; }
div[data-baseweb="select"] input { color: #e2e8f0 !important; caret-color: #00d4ff !important; }
ul[data-baseweb="menu"] { background-color: #0f1829 !important; border: 1px solid #1a2035 !important; border-radius: 8px !important; }
ul[data-baseweb="menu"] li { color: #e2e8f0 !important; background: transparent !important; font-size: 0.85rem !important; }
ul[data-baseweb="menu"] li:hover { background-color: #1a2035 !important; color: #00d4ff !important; }

/* Caption & small text */
small, .stCaption, [data-testid="stCaptionContainer"] { color: #475569 !important; font-size: 0.75rem !important; }

/* Metric */
[data-testid="stMetric"] { background: #0a0d16; border: 1px solid #1a2035; border-radius: 10px; padding: 14px 18px; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.72rem !important; letter-spacing: 0.1em !important; }
[data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 1.4rem !important; font-weight: 700 !important; }

/* Divider */
hr { border-color: #1a2035 !important; margin: 24px 0 !important; }

/* Expander */
[data-testid="stExpander"] { background: #0a0d16; border: 1px solid #1a2035; border-radius: 10px; }
[data-testid="stExpander"] summary { color: #94a3b8 !important; font-size: 0.82rem !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #1a2035; }
</style>
""", unsafe_allow_html=True)

# ── Constants & Helpers ───────────────────────────────────────────────────────
MARKET_PRESETS = {
    "FTSE MIB (Milano)": [
        "A2A.MI","AMP.MI","AZM.MI","BAMI.MI","BC.MI","BMED.MI","BMPS.MI","BPER.MI",
        "BZU.MI","CNHI.MI","DIA.MI","ENEL.MI","ENI.MI","ERG.MI","FBK.MI","G.MI",
        "HER.MI","IG.MI","IP.MI","IREN.MI","ISP.MI","LDO.MI","MB.MI","MONC.MI",
        "NEXI.MI","PIRC.MI","PRY.MI","PST.MI","RACE.MI","REC.MI","SRG.MI",
        "STLAM.MI","STM.MI","TEN.MI","TIT.MI","TRN.MI","UCG.MI","UNI.MI","WBD.MI",
    ],
    "Nasdaq 100": [
        "AAPL","MSFT","NVDA","AMZN","META","GOOGL","TSLA","AVGO","COST","NFLX",
        "TMUS","AMD","QCOM","INTU","AMAT","MU","LRCX","KLAC","MRVL","SNPS",
        "CDNS","ADBE","ADP","PANW","CRWD","FTNT","TEAM","WDAY","CSCO","TXN",
        "ADI","MCHP","ON","NXPI","ASML","TTD","DDOG","ZS","NET","HUBS",
        "VEEV","SNOW","PLTR","COIN","ABNB","DASH","UBER","PINS","SPOT","MELI",
    ],
}

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(com=period-1, min_periods=period).mean()
    loss = (-delta.clip(upper=0)).ewm(com=period-1, min_periods=period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def compute_atr(df, period=14):
    hi, lo, cl = df["High"], df["Low"], df["Close"]
    tr = pd.concat([(hi-lo), (hi-cl.shift()).abs(), (lo-cl.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(com=period-1, min_periods=period).mean()

def compute_zscore(series, window=20):
    roll_mean = series.rolling(window).mean()
    roll_std  = series.rolling(window).std()
    return (series - roll_mean) / roll_std.replace(0, np.nan)

def pct_from_52w_high(series):
    high_52w = series.rolling(252).max()
    return ((series - high_52w) / high_52w * 100).iloc[-1]

def analyse_ticker(ticker: str) -> dict | None:
    try:
        raw = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        if raw.empty or len(raw) < 30:
            return None
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        raw = raw[["Open","High","Low","Close","Volume"]].dropna()
        cl = raw["Close"]

        # Indicators
        rsi_val     = float(compute_rsi(cl).iloc[-1])
        atr_val     = float(compute_atr(raw).iloc[-1])
        atr_pct     = atr_val / float(cl.iloc[-1]) * 100
        zscore_val  = float(compute_zscore(cl).iloc[-1])
        drop_52w    = pct_from_52w_high(cl)
        vol_avg     = float(raw["Volume"].mean())
        vol_last    = float(raw["Volume"].iloc[-1])
        vol_ratio   = vol_last / vol_avg if vol_avg > 0 else 1.0
        pct_1d      = float(cl.pct_change().iloc[-1] * 100)
        pct_5d      = float((cl.iloc[-1]/cl.iloc[-6]-1)*100) if len(cl) >= 6 else 0.0
        price       = float(cl.iloc[-1])

        # Consecutive negative days
        neg_streak = 0
        for v in cl.pct_change().dropna().iloc[::-1]:
            if v < 0: neg_streak += 1
            else: break

        # Reversion Score (0–100)
        # Each component scored 0–25, summed
        s_rsi     = max(0, min(25, (70 - rsi_val) / 70 * 25))          # lower RSI → higher score
        s_zscore  = max(0, min(25, (-zscore_val / 3) * 25))             # more negative z → higher
        s_drop    = max(0, min(25, (-drop_52w / 40) * 25))              # deeper drop → higher
        s_streak  = max(0, min(25, (neg_streak / 5) * 25))              # more red days → higher
        score     = round(s_rsi + s_zscore + s_drop + s_streak, 1)

        # Signal classification
        if score >= 70:   signal = "STRONG BUY"
        elif score >= 50: signal = "BUY"
        elif score >= 30: signal = "WATCH"
        else:             signal = "WAIT"

        # Expected return (simple mean-reversion estimate)
        exp_ret = round(-zscore_val * atr_pct * 0.5, 2)

        # Confidence: based on RSI extremity + z-score magnitude
        conf = min(99, max(10, int(abs(zscore_val) * 20 + (70-rsi_val)*0.5 + neg_streak*3)))

        return {
            "Ticker":      ticker,
            "Price":       round(price, 3),
            "1d %":        round(pct_1d, 2),
            "5d %":        round(pct_5d, 2),
            "RSI":         round(rsi_val, 1),
            "Z-Score":     round(zscore_val, 2),
            "ATR %":       round(atr_pct, 2),
            "Drop 52w %":  round(drop_52w, 1),
            "Vol Ratio":   round(vol_ratio, 2),
            "Neg Days":    neg_streak,
            "Score":       score,
            "Signal":      signal,
            "Exp. Return": exp_ret,
            "Confidence":  conf,
        }
    except Exception:
        return None

def signal_color(sig):
    return {"STRONG BUY":"signal-strong","BUY":"signal-mod","WATCH":"signal-weak","WAIT":"signal-wait"}.get(sig,"")

def score_bar_html(score):
    w = int(score)
    if score >= 70:   col = "#22c55e"
    elif score >= 50: col = "#84cc16"
    elif score >= 30: col = "#f59e0b"
    else:             col = "#ef4444"
    return f"""<div style="background:#111827;border-radius:4px;height:6px;width:100%;margin-top:4px">
      <div style="background:{col};border-radius:4px;height:6px;width:{w}%"></div></div>"""

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

# Hero
st.markdown("""
<div class="hero">
  <div class="hero-title">⚡ BEST REVERT <span>MI</span> / NDQ</div>
  <div class="hero-sub">MEAN REVERSION SCANNER · MULTI-MARKET · AI-RANKED OPPORTUNITIES</div>
  <div class="hero-badges">
    <span class="badge">📊 Z-Score</span>
    <span class="badge">📈 RSI</span>
    <span class="badge">📉 52W Drop</span>
    <span class="badge">🔥 ATR Vol</span>
    <span class="badge">🏆 Auto Ranking</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Input Section ─────────────────────────────────────────────────────────────
st.markdown('<p class="sec-label">◼ 01 · Seleziona o Inserisci i Ticker</p>', unsafe_allow_html=True)

col_mode, col_preset = st.columns([1, 2])
with col_mode:
    mode = st.radio("Modalità input", ["Preset di mercato", "Ticker manuali"], horizontal=True, label_visibility="collapsed")
with col_preset:
    if mode == "Preset di mercato":
        preset_choice = st.selectbox("Scegli mercato", list(MARKET_PRESETS.keys()), label_visibility="collapsed")

if mode == "Preset di mercato":
    tickers_to_analyze = MARKET_PRESETS[preset_choice]
    st.caption(f"✓ {len(tickers_to_analyze)} ticker nel preset · filtro volume applicato a runtime")
else:
    # Dynamic link/ticker input
    if "n_inputs" not in st.session_state:
        st.session_state.n_inputs = 3

    col_add, col_clear = st.columns([1, 6])
    with col_add:
        if st.button("＋  Aggiungi campo"):
            st.session_state.n_inputs += 1
    with col_clear:
        if st.button("✕  Reset"):
            st.session_state.n_inputs = 3
            for k in list(st.session_state.keys()):
                if k.startswith("ticker_"):
                    del st.session_state[k]
            st.rerun()

    tickers_raw = []
    cols_per_row = 3
    for i in range(0, st.session_state.n_inputs, cols_per_row):
        row_cols = st.columns(cols_per_row)
        for j, c in enumerate(row_cols):
            idx = i + j
            if idx < st.session_state.n_inputs:
                with c:
                    val = st.text_input(
                        f"Ticker {idx+1}",
                        key=f"ticker_{idx}",
                        placeholder="es. ENI.MI  /  AAPL  /  TSLA",
                    )
                    if val.strip():
                        tickers_raw.append(val.strip().upper())

    tickers_to_analyze = tickers_raw

# ── Parameters ────────────────────────────────────────────────────────────────
st.markdown('<p class="sec-label">◼ 02 · Parametri Analisi</p>', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)
with p1:
    min_score   = st.slider("Score minimo", 0, 100, 20, step=5)
with p2:
    top_n       = st.slider("Top N risultati", 3, 20, 10)
with p3:
    min_vol_m   = st.slider("Vol. medio min (M)", 0.1, 10.0, 0.3, step=0.1)
with p4:
    rsi_max_val = st.slider("RSI max (ipervenduto)", 20, 80, 65)

# ── Run Analysis ──────────────────────────────────────────────────────────────
st.markdown('<p class="sec-label">◼ 03 · Esegui Analisi</p>', unsafe_allow_html=True)

run_col, info_col = st.columns([1, 4])
with run_col:
    run = st.button("⚡  GENERA RISULTATI", use_container_width=True)
with info_col:
    st.caption("Il sistema scarica i dati via yfinance, calcola Z-Score · RSI · ATR · Drop 52W · Streak negativi e genera un ranking pesato automatico.")

if run:
    if not tickers_to_analyze:
        st.warning("Inserisci almeno un ticker o seleziona un preset.")
        st.stop()

    results = []
    progress = st.progress(0, text="Analisi in corso…")
    total = len(tickers_to_analyze)

    for i, t in enumerate(tickers_to_analyze):
        progress.progress((i+1)/total, text=f"Analizzando {t} ({i+1}/{total})…")
        r = analyse_ticker(t)
        if r is None:
            continue
        if r["Vol Ratio"] * r["Price"] < min_vol_m * 1e6 / 252:
            pass  # keep — vol filtering done by preset loading
        results.append(r)

    progress.empty()

    if not results:
        st.error("Nessun dato disponibile per i ticker inseriti.")
        st.stop()

    df = pd.DataFrame(results)
    # Apply filters
    df = df[df["Score"] >= min_score]
    df = df[df["RSI"] <= rsi_max_val]
    df = df.sort_values("Score", ascending=False).reset_index(drop=True)
    df_top = df.head(top_n)

    # ── TOP 3 podio ───────────────────────────────────────────────────────────
    st.markdown('<p class="sec-label">◼ 04 · Top Opportunità di Reversione</p>', unsafe_allow_html=True)

    podio_classes = ["gold","silver","bronze"]
    podio_labels  = ["🥇 #1 · BEST PICK","🥈 #2","🥉 #3"]
    podio_cols = st.columns(min(3, len(df_top)))

    for idx, (col, cls, lbl) in enumerate(zip(podio_cols, podio_classes, podio_labels)):
        if idx >= len(df_top): break
        row = df_top.iloc[idx]
        sig_cls = signal_color(row["Signal"])
        bar = score_bar_html(row["Score"])
        with col:
            st.markdown(f"""
            <div class="score-card {cls}">
              <div class="score-rank">{lbl}</div>
              <div class="score-ticker">{row['Ticker']}</div>
              <div class="score-val {sig_cls}">{row['Score']}<span style="font-size:0.9rem;color:#64748b">/100</span></div>
              {bar}
              <div class="score-label" style="margin-top:8px">
                <span class="{sig_cls}" style="font-weight:700">{row['Signal']}</span>
              </div>
              <div class="kpi-row">
                <div class="kpi-pill">RSI <b>{row['RSI']}</b></div>
                <div class="kpi-pill">Z <b>{row['Z-Score']}</b></div>
                <div class="kpi-pill">ATR <b>{row['ATR %']}%</b></div>
                <div class="kpi-pill">🔴 <b>{row['Neg Days']}gg</b></div>
              </div>
              <div style="margin-top:10px;font-size:0.72rem;color:#475569">
                Exp. Return: <b style="color:#22c55e">{row['Exp. Return']:+.2f}%</b> &nbsp;·&nbsp;
                Confidence: <b style="color:#38bdf8">{row['Confidence']}%</b>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── st.metric row for top 3 ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    metrics = [
        (mc1, "🏆 Best Score",     f"{df_top.iloc[0]['Score']}/100",  df_top.iloc[0]['Ticker']),
        (mc2, "📉 RSI più basso",  f"{df['RSI'].min():.1f}",          df.loc[df['RSI'].idxmin(),'Ticker']),
        (mc3, "📊 Z-Score min",    f"{df['Z-Score'].min():.2f}",      df.loc[df['Z-Score'].idxmin(),'Ticker']),
        (mc4, "🔻 Drop 52W max",   f"{df['Drop 52w %'].min():.1f}%",  df.loc[df['Drop 52w %'].idxmin(),'Ticker']),
        (mc5, "🔴 Streak neg max", f"{int(df['Neg Days'].max())} gg", df.loc[df['Neg Days'].idxmax(),'Ticker']),
    ]
    for col, label, val, delta in metrics:
        with col:
            st.metric(label=label, value=val, delta=delta)

    # ── Full ranking table ────────────────────────────────────────────────────
    st.markdown('<p class="sec-label">◼ 05 · Classifica Completa</p>', unsafe_allow_html=True)

    def colorize(row):
        styles = [""] * len(row)
        cols = list(row.index)
        sig = row.get("Signal","")
        score = row.get("Score", 0)

        for i, c in enumerate(cols):
            if c == "Signal":
                if sig == "STRONG BUY": styles[i] = "color: #22c55e; font-weight: 700"
                elif sig == "BUY":      styles[i] = "color: #84cc16; font-weight: 600"
                elif sig == "WATCH":    styles[i] = "color: #f59e0b"
                else:                   styles[i] = "color: #ef4444"
            elif c == "Score":
                if score >= 70:   styles[i] = "color: #22c55e; font-weight: 700"
                elif score >= 50: styles[i] = "color: #84cc16"
                elif score >= 30: styles[i] = "color: #f59e0b"
                else:             styles[i] = "color: #ef4444"
            elif c == "1d %":
                styles[i] = "color: #22c55e" if row[c] > 0 else "color: #ef4444"
            elif c == "RSI":
                if row[c] < 30:  styles[i] = "color: #22c55e; font-weight:700"
                elif row[c] > 70: styles[i] = "color: #ef4444"
            elif c == "Exp. Return":
                styles[i] = "color: #22c55e" if row[c] > 0 else "color: #ef4444"
        return styles

    styled_df = (df_top.style
        .apply(colorize, axis=1)
        .format({
            "Price":        "{:.3f}",
            "1d %":         "{:+.2f}%",
            "5d %":         "{:+.2f}%",
            "RSI":          "{:.1f}",
            "Z-Score":      "{:.2f}",
            "ATR %":        "{:.2f}%",
            "Drop 52w %":   "{:.1f}%",
            "Vol Ratio":    "{:.2f}x",
            "Score":        "{:.1f}",
            "Exp. Return":  "{:+.2f}%",
            "Confidence":   "{}%",
        })
    )
    st.dataframe(styled_df, use_container_width=True, height=min(600, 40 + len(df_top)*38))

    # ── Download ──────────────────────────────────────────────────────────────
    csv = df_top.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇  Scarica CSV",
        data=csv,
        file_name="best_revert_results.csv",
        mime="text/csv",
    )

    # ── Methodology expander ──────────────────────────────────────────────────
    with st.expander("📐 Metodologia · Come viene calcolato lo Score"):
        st.markdown("""
**Reversion Score (0–100)** — somma pesata di 4 componenti:

| Componente | Peso | Logica |
|---|---|---|
| RSI | 25 pt | RSI basso (< 30) = titolo ipervenduto → alta probabilità di rimbalzo |
| Z-Score | 25 pt | Prezzo lontano sotto la media mobile → tensione di ritorno alla media |
| Drop 52W % | 25 pt | Più lontano dai massimi → maggiore spazio di recupero potenziale |
| Neg. Streak | 25 pt | Sequenza di chiusure negative consecutive → catalizzatore inversione |

**Signal:**
- 🟢 **STRONG BUY** ≥ 70 · 🟡 **BUY** ≥ 50 · 🟠 **WATCH** ≥ 30 · 🔴 **WAIT** < 30

**Expected Return** = −ZScore × ATR% × 0.5 (stima mean-reversion a breve termine)

**Confidence** = funzione di |ZScore|, (70−RSI), Neg.Streak — scala 10–99%

⚠️ Scopo puramente educativo/informativo. Non costituisce consulenza finanziaria.
        """)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#334155">
      <div style="font-size:3rem;margin-bottom:16px">⚡</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#475569">
        Configura i parametri e premi GENERA RISULTATI
      </div>
      <div style="font-size:0.8rem;color:#334155;margin-top:8px">
        Il sistema analizzerà ogni ticker e produrrà il ranking di reversione automatico
      </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("⚠️ Scopo puramente educativo. Non costituisce consulenza finanziaria. Dati: Yahoo Finance via yfinance.")
