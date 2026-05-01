import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="BEST REVERT", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; background: #000000; color: #e2e8f0; }
.stApp { background: #000000; }

section[data-testid="stSidebar"] { background: #050508 !important; border-right: 1px solid #0f1520 !important; }
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* Hero */
.hero {
    background: linear-gradient(160deg, #000000 0%, #050a18 50%, #000000 100%);
    border: 1px solid #0a1628;
    border-radius: 16px; padding: 36px 40px 30px;
    margin-bottom: 28px; position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #0066ff, #00ccff, #0066ff);
    background-size: 200% 100%; animation: slide 3s linear infinite;
}
@keyframes slide { 0%{background-position:200% 0} 100%{background-position:-200% 0} }
.hero-title {
    font-family: 'Syne', sans-serif; font-size: 2.4rem; font-weight: 800;
    color: #ffffff; letter-spacing: -0.04em; line-height: 1;
}
.hero-title .accent { color: #0099ff; }
.hero-sub { font-size: 0.72rem; color: #7aa8c8; margin-top: 10px; letter-spacing: 0.15em; text-transform: uppercase; }
.hero-badges { margin-top: 18px; display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
    background: #050a18; border: 1px solid #0a2040;
    border-radius: 20px; padding: 4px 12px;
    font-size: 0.65rem; letter-spacing: 0.1em; color: #0099ff;
    text-transform: uppercase; font-weight: 500;
}

/* Section */
.sec { font-size: 0.62rem; letter-spacing: 0.25em; text-transform: uppercase; color: #0099ff;
       border-bottom: 1px solid #0a1628; padding-bottom: 10px; margin: 28px 0 18px; font-weight: 700; }

/* Input zone */
.input-zone { background: #050508; border: 1px solid #0a1628; border-radius: 12px; padding: 20px 24px; margin-bottom: 8px; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #003399 0%, #0066ff 100%) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important;
    font-weight: 500 !important; letter-spacing: 0.06em !important;
    padding: 10px 20px !important; transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }

/* Text input */
.stTextInput input {
    background: #050508 !important; border: 1px solid #0a1628 !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.88rem !important;
}
.stTextInput input:focus { border-color: #0066ff !important; box-shadow: 0 0 0 2px #0066ff22 !important; }
.stTextInput label { color: #7aa8c8 !important; font-size: 0.7rem !important; }
.stTextInput input::placeholder { color: #2a5a8a !important; }

/* Selectbox */
div[data-baseweb="select"] { background: #050508 !important; border-color: #0a1628 !important; border-radius: 8px !important; }
div[data-baseweb="select"] > div { background: #050508 !important; color: #e2e8f0 !important; }
div[data-baseweb="select"] span { color: #e2e8f0 !important; font-size: 0.88rem !important; }
div[data-baseweb="select"] input { color: #e2e8f0 !important; caret-color: #0099ff !important; }
div[data-baseweb="select"] svg { fill: #7aa8c8 !important; }
ul[data-baseweb="menu"] { background: #050a18 !important; border: 1px solid #0a1628 !important; border-radius: 8px !important; }
ul[data-baseweb="menu"] li { color: #cbd5e1 !important; font-size: 0.82rem !important; }
ul[data-baseweb="menu"] li:hover { background: #0a1628 !important; color: #0099ff !important; }

/* Podium cards */
.pod {
    background: #050508; border: 1px solid #0a1628;
    border-radius: 14px; padding: 22px 20px;
    transition: transform 0.2s, border-color 0.2s;
}
.pod:hover { transform: translateY(-3px); }
.pod.p1 { border-color: #0066ff44; background: linear-gradient(160deg,#050a18,#050508); }
.pod.p2 { border-color: #0044aa33; }
.pod.p3 { border-color: #0033882a; }
.pod-rank { font-size: 0.6rem; color: #7aa8c8; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 6px; }
.pod-ticker { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; }
.pod-score { font-size: 2.2rem; font-weight: 700; color: #0099ff; line-height: 1; margin: 4px 0; }
.pod-score sub { font-size: 0.8rem; color: #7aa8c8; }
.bar-bg { background: #0a1628; border-radius: 4px; height: 5px; margin: 8px 0; }
.bar-fill { border-radius: 4px; height: 5px; }
.pill { display: inline-block; background: #050a18; border: 1px solid #0a2040;
        border-radius: 5px; padding: 2px 7px; font-size: 0.65rem; color: #94b8cc; margin: 2px 2px 0 0; }
.pill b { color: #cbd5e1; }
.signal-sb { color: #0099ff; font-weight: 700; }
.signal-b  { color: #38bdf8; font-weight: 600; }
.signal-w  { color: #7dd3fc; }
.signal-wt { color: #ef4444; }
.exp-pos { color: #0099ff; } .exp-neg { color: #ef4444; }

/* captions */
small, .stCaption, [data-testid="stCaptionContainer"] { color: #7aa8c8 !important; font-size: 0.72rem !important; }
h3 { color: #f8fafc !important; font-size: 1rem !important; font-weight: 600 !important; }
[data-testid="stMetric"] { background: #050508; border: 1px solid #0a1628; border-radius: 10px; padding: 14px 18px; }
[data-testid="stMetricLabel"] { color: #94b8cc !important; font-size: 0.68rem !important; letter-spacing: 0.1em !important; }
[data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 1.3rem !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #0a1628; }
/* Force readable text in all table cells via iframe */
iframe[title="st.dataframe"] { background: #050508 !important; }
hr { border-color: #0a1628 !important; margin: 20px 0 !important; }
[data-testid="stExpander"] { background: #050508 !important; border: 1px solid #0a1628 !important; border-radius: 10px !important; }
[data-testid="stExpander"] summary { color: #94a3b8 !important; font-size: 0.82rem !important; font-weight:600 !important; }
[data-testid="stExpander"] summary:hover { color: #0099ff !important; }
/* Force all markdown text to be white */
[data-testid="stExpander"] p,
[data-testid="stExpander"] li,
[data-testid="stExpander"] span,
[data-testid="stExpander"] div { color: #e2e8f0 !important; }
[data-testid="stExpander"] strong { color: #f8fafc !important; font-weight: 700 !important; }
[data-testid="stExpander"] table { border-collapse: collapse !important; width: 100% !important; }
[data-testid="stExpander"] th { background: #000 !important; color: #94b8cc !important; padding: 8px 12px !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; border-bottom: 1px solid #0a1628 !important; }
[data-testid="stExpander"] td { color: #cbd5e1 !important; padding: 8px 12px !important; border-bottom: 1px solid #050a18 !important; font-size: 0.82rem !important; }
[data-testid="stExpander"] tr:hover td { background: #050a18 !important; }
/* General markdown text fix */
.stMarkdown p, .stMarkdown li, .stMarkdown span { color: #e2e8f0 !important; }
.stMarkdown strong, .stMarkdown b { color: #f8fafc !important; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color: #f8fafc !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def compute_rsi(s, p=14):
    d = s.diff()
    g = d.clip(lower=0).ewm(com=p-1, min_periods=p).mean()
    l = (-d.clip(upper=0)).ewm(com=p-1, min_periods=p).mean()
    return 100 - (100/(1+g/l.replace(0,np.nan)))

def compute_atr(df, p=14):
    hi,lo,cl = df["High"],df["Low"],df["Close"]
    tr = pd.concat([(hi-lo),(hi-cl.shift()).abs(),(lo-cl.shift()).abs()],axis=1).max(axis=1)
    return tr.ewm(com=p-1, min_periods=p).mean()

def compute_zscore(s, w=20):
    m = s.rolling(w).mean(); sd = s.rolling(w).std()
    return (s-m)/sd.replace(0,np.nan)

def neg_streak(pct):
    n = 0
    for v in pct.dropna().iloc[::-1]:
        if v < 0: n += 1
        else: break
    return n

def resolve_ticker(raw: str) -> str:
    """Resolve ISIN / name / ticker to a clean Yahoo Finance symbol."""
    import re
    raw = raw.strip()
    if not raw: return ""

    candidate = raw.upper()

    # 1. ISIN pattern (2 letters + 10 alphanumeric) — use yf.Search first
    if re.match(r'^[A-Z]{2}[A-Z0-9]{10}$', candidate):
        # Try yf.Search which handles ISINs well
        try:
            res = yf.Search(candidate, max_results=3)
            for q in res.quotes:
                sym = q.get("symbol","")
                # Prefer symbols that don't look like ISINs
                if sym and not re.match(r'^[A-Z]{2}[A-Z0-9]{10}$', sym):
                    return sym
        except: pass
        # Fallback: try as direct ticker
        try:
            h = yf.download(candidate, period="5d", progress=False, auto_adjust=True)
            if not h.empty:
                # Get real symbol from ticker info
                info = yf.Ticker(candidate).get_info()
                sym = info.get("symbol", candidate)
                if sym and not re.match(r'^[A-Z]{2}[A-Z0-9]{10}$', sym):
                    return sym
        except: pass
        return candidate  # last resort, will show error later

    # 2. Try as-is (normal ticker like AAPL, ENI.MI)
    try:
        h = yf.download(candidate, period="5d", progress=False, auto_adjust=True)
        if not h.empty: return candidate
    except: pass

    # 3. Search by name
    try:
        res = yf.Search(raw, max_results=1)
        if res.quotes:
            sym = res.quotes[0].get("symbol","")
            if sym: return sym
    except: pass

    return candidate

def analyse_ticker(ticker: str) -> dict | None:
    try:
        end_date = datetime.date.today() + datetime.timedelta(days=1)
        start_date = end_date - datetime.timedelta(days=400)
        raw = yf.download(ticker, start=start_date.isoformat(), end=end_date.isoformat(),
                          interval="1d", progress=False, auto_adjust=True)
        if raw.empty or len(raw) < 30: return None
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        raw = raw[["Open","High","Low","Close","Volume"]].dropna()
        cl = raw["Close"]
        price       = float(cl.iloc[-1])
        # Resolve display symbol — never show ISIN
        import re as _re
        display_sym = ticker
        if _re.match(r'^[A-Z]{2}[A-Z0-9]{10}$', ticker.upper()):
            try:
                info = yf.Ticker(ticker).get_info()
                sym = info.get("symbol", ticker)
                if sym and not _re.match(r'^[A-Z]{2}[A-Z0-9]{10}$', sym):
                    display_sym = sym
            except: pass
        rsi_val     = float(compute_rsi(cl).iloc[-1])
        atr_val     = float(compute_atr(raw).iloc[-1])
        atr_pct     = atr_val/price*100
        z           = float(compute_zscore(cl).iloc[-1])
        high52      = float(cl.expanding().max().iloc[-1])  # use all available history
        drop52      = (price - high52)/high52*100 if high52 > 0 else 0.0
        vol_avg     = float(raw["Volume"].mean())
        vol_last    = float(raw["Volume"].iloc[-1])
        vol_ratio   = vol_last/vol_avg if vol_avg>0 else 1.0
        pct1d       = float(cl.pct_change().iloc[-1]*100)
        pct5d       = float((cl.iloc[-1]/cl.iloc[-6]-1)*100) if len(cl)>=6 else 0.0
        streak      = neg_streak(cl.pct_change())
        # Mean-reversion stats (from RevertMI/NDQ logic)
        pct_s = cl.pct_change()*100
        streaks_list = []
        cnt = 0
        for v in pct_s.dropna():
            if v < 0: cnt += 1
            elif v > 0 and cnt > 0: streaks_list.append(cnt); cnt = 0
            else: cnt = 0
        avg_streak = round(float(np.mean(streaks_list)),2) if streaks_list else 0.0

        # Score components (0-25 each)
        s_rsi    = max(0, min(25, (70-rsi_val)/70*25))
        s_z      = max(0, min(25, (-z/3)*25))
        s_drop   = max(0, min(25, (-drop52/40)*25))
        s_streak = max(0, min(25, (streak/5)*25))
        score    = round(s_rsi+s_z+s_drop+s_streak, 1)

        if score>=70:   signal="STRONG BUY"
        elif score>=50: signal="BUY"
        elif score>=30: signal="WATCH"
        else:           signal="WAIT"

        exp_ret  = round(-z*atr_pct*0.5, 2)
        conf     = min(99, max(10, int(abs(z)*20+(70-rsi_val)*0.5+streak*3)))

        return {
            "Ticker":       display_sym,
            "Price":        round(price, 3),
            "1d %":         round(pct1d, 2),
            "5d %":         round(pct5d, 2),
            "RSI":          round(rsi_val, 1),
            "Z-Score":      round(z, 2),
            "ATR %":        round(atr_pct, 2),
            "Drop 52W %":   round(drop52, 1),
            "Vol Ratio":    round(vol_ratio, 2),
            "Neg Days":     streak,
            "Avg Streak":   avg_streak,
            "Score":        score,
            "Signal":       signal,
            "Exp. Return":  exp_ret,
            "Confidence %": conf,
            "_vol_avg":     vol_avg,
        }
    except Exception:
        return None

def score_bar(score):
    if score>=70: c="#0099ff"
    elif score>=50: c="#38bdf8"
    elif score>=30: c="#7dd3fc"
    else: c="#ef4444"
    return f'<div class="bar-bg"><div class="bar-fill" style="width:{int(score)}%;background:{c}"></div></div>'

def sig_cls(s):
    return {"STRONG BUY":"signal-sb","BUY":"signal-b","WATCH":"signal-w","WAIT":"signal-wt"}.get(s,"")

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">⚡ BEST REVERT <span class="accent">MI / NDQ</span></div>
  <div class="hero-sub">Mean Reversion Scanner · Auto-Ranking · Multi-Market</div>
  <div class="hero-badges">
    <span class="badge">Z-Score</span><span class="badge">RSI (14)</span>
    <span class="badge">52W Drop</span><span class="badge">ATR Vol</span>
    <span class="badge">Neg Streak</span><span class="badge">Avg Streak</span>
    <span class="badge">Exp. Return</span><span class="badge">Confidence</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="sec">◼ 01 · Inserisci Ticker / ISIN / Nome</p>', unsafe_allow_html=True)
st.caption("Inserisci ticker (ENI.MI, AAPL), ISIN oppure nome del titolo. L'app risolve automaticamente il simbolo.")

if "n_inputs" not in st.session_state:
    st.session_state.n_inputs = 5

col_add, col_rst, col_sp = st.columns([1,1,5])
with col_add:
    if st.button("＋ Aggiungi"):
        st.session_state.n_inputs += 1
with col_rst:
    if st.button("✕ Reset"):
        st.session_state.n_inputs = 5
        for k in list(st.session_state.keys()):
            if k.startswith("ti_"): del st.session_state[k]
        st.rerun()

cols_per_row = 4
for i in range(0, st.session_state.n_inputs, cols_per_row):
    row = st.columns(cols_per_row)
    for j, c in enumerate(row):
        idx = i+j
        if idx < st.session_state.n_inputs:
            with c:
                st.text_input(
                    f"#{idx+1}",
                    key=f"ti_{idx}",
                    placeholder="ENI.MI · AAPL · IT0003128367",
                    label_visibility="visible"
                )

# Collect non-empty inputs
raw_inputs = [st.session_state.get(f"ti_{i}","").strip() for i in range(st.session_state.n_inputs)]
raw_inputs = [r for r in raw_inputs if r]

# ── RUN ───────────────────────────────────────────────────────────────────────
st.markdown('<p class="sec">◼ 02 · Analisi</p>', unsafe_allow_html=True)

run_c, info_c = st.columns([1,5])
with run_c:
    run = st.button("⚡  GENERA CLASSIFICA", use_container_width=True)
with info_c:
    st.caption("Scarica dati real-time · Calcola Z-Score, RSI, ATR, Drop 52W, Streak · Genera ranking pesato automatico")

if run:
    if not raw_inputs:
        st.warning("⚠️ Inserisci almeno un ticker nel campo sopra.")
        st.stop()

    # Resolve tickers
    resolved = {}
    with st.spinner("🔍 Risoluzione simboli…"):
        for raw in raw_inputs:
            sym = resolve_ticker(raw)
            if sym:
                resolved[raw] = sym

    if not resolved:
        st.error("Nessun ticker valido trovato.")
        st.stop()

    # Show resolved mapping if any differ
    diffs = {k:v for k,v in resolved.items() if k.upper() != v}
    if diffs:
        st.caption("Simboli risolti: " + "  ·  ".join(f"{k} → **{v}**" for k,v in diffs.items()))

    # Analyse
    results = []
    prog = st.progress(0, text="Analisi in corso…")
    tickers_list = list(resolved.values())
    for i, t in enumerate(tickers_list):
        prog.progress((i+1)/len(tickers_list), text=f"Analizzando {t}…")
        r = analyse_ticker(t)
        if r: results.append(r)
    prog.empty()

    if not results:
        st.error("Nessun dato disponibile per i ticker inseriti.")
        st.stop()

    df = pd.DataFrame(results).sort_values("Score", ascending=False).reset_index(drop=True)

    _now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.caption(f"🕐 Analisi eseguita: **{_now}** · Dati real-time da Yahoo Finance · Nessuna cache")

    # ── PODIUM ────────────────────────────────────────────────────────────────
    st.markdown('<p class="sec">◼ 03 · Classifica Inversione</p>', unsafe_allow_html=True)
    st.caption("Ordine: probabilità di inversione rialzista per primo — basato su Score composito pesato")

    podium_labels = ["🥇 #1 · PRIMA INVERSIONE ATTESA","🥈 #2","🥉 #3"]
    podium_cls    = ["p1","p2","p3"]
    n_pod = min(3, len(df))
    pod_cols = st.columns(n_pod)

    for idx in range(n_pod):
        row = df.iloc[idx]
        sc  = sig_cls(row["Signal"])
        with pod_cols[idx]:
            exp_cls = "exp-pos" if row["Exp. Return"] > 0 else "exp-neg"
            st.markdown(f"""
            <div class="pod {podium_cls[idx]}">
              <div class="pod-rank">{podium_labels[idx]}</div>
              <div class="pod-ticker">{row['Ticker']}</div>
              <div class="pod-score">{row['Score']}<sub>/100</sub></div>
              {score_bar(row['Score'])}
              <div style="margin:6px 0 10px">
                <span class="{sc}" style="font-size:0.82rem;letter-spacing:0.08em">{row['Signal']}</span>
              </div>
              <div class="pill">RSI <b>{row['RSI']}</b></div>
              <div class="pill">Z <b>{row['Z-Score']}</b></div>
              <div class="pill">ATR <b>{row['ATR %']}%</b></div>
              <div class="pill">🔴 <b>{row['Neg Days']}gg</b></div>
              <div class="pill">Avg streak <b>{row['Avg Streak']}</b></div>
              <div class="pill">52W <b>{row['Drop 52W %']}%</b></div>
              <br>
              <div style="margin-top:10px;font-size:0.72rem;color:#7aa8c8">
                Exp.Return <span class="{exp_cls}" style="font-weight:700">{row['Exp. Return']:+.2f}%</span>
                &nbsp;·&nbsp; Conf. <b style="color:#0066ff">{row['Confidence %']}%</b>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── METRICS ───────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    mc = st.columns(min(5, len(df)))
    kpis = [
        ("⚡ Score più alto",    f"{df.iloc[0]['Score']}/100",         df.iloc[0]['Ticker']),
        ("📉 RSI min",           f"{df['RSI'].min():.1f}",             df.loc[df['RSI'].dropna().idxmin(),'Ticker'] if df['RSI'].notna().any() else "—"),
        ("📊 Z-Score min",       f"{df['Z-Score'].min():.2f}",         df.loc[df['Z-Score'].dropna().idxmin(),'Ticker'] if df['Z-Score'].notna().any() else "—"),
        ("🔻 Drop 52W max",      f"{df['Drop 52W %'].min():.1f}%",     df.loc[df['Drop 52W %'].dropna().idxmin(),'Ticker'] if df['Drop 52W %'].notna().any() else "—"),
        ("🔴 Streak neg max",    f"{int(df['Neg Days'].max())} gg",    df.loc[df['Neg Days'].dropna().idxmax(),'Ticker'] if df['Neg Days'].notna().any() else "—"),
    ]
    for i, (col, (label, val, delta)) in enumerate(zip(mc, kpis[:len(mc)])):
        with col:
            st.metric(label=label, value=val, delta=delta)

    # ── FULL TABLE ────────────────────────────────────────────────────────────
    st.markdown('<p class="sec">◼ 04 · Tabella Comparativa Completa</p>', unsafe_allow_html=True)

    disp_cols = ["Ticker","Price","1d %","5d %","RSI","Z-Score","ATR %",
                 "Drop 52W %","Neg Days","Avg Streak","Score","Signal","Exp. Return","Confidence %"]
    df_disp = df[disp_cols].copy()

    def colorize(row):
        styles = [""] * len(row)
        cols = list(row.index)
        for i, c in enumerate(cols):
            v = row[c]
            if c == "Signal":
                if v == "STRONG BUY": styles[i] = "color:#0099ff;font-weight:700"
                elif v == "BUY":      styles[i] = "color:#38bdf8;font-weight:600"
                elif v == "WATCH":    styles[i] = "color:#7dd3fc"
                else:                 styles[i] = "color:#ef4444"
            elif c == "Score":
                if v >= 70:   styles[i] = "color:#0099ff;font-weight:700"
                elif v >= 50: styles[i] = "color:#38bdf8"
                elif v >= 30: styles[i] = "color:#7dd3fc"
                else:         styles[i] = "color:#ef4444"
            elif c in ("1d %","5d %","Exp. Return"):
                styles[i] = "color:#0099ff" if v > 0 else "color:#ef4444"
            elif c == "RSI":
                if v < 30:  styles[i] = "color:#0099ff;font-weight:700"
                elif v > 70: styles[i] = "color:#ef4444"
            elif c == "Z-Score":
                styles[i] = "color:#0099ff" if v < -1 else ("color:#ef4444" if v > 1 else "")
        return styles

    styled = (df_disp.style
        .apply(colorize, axis=1)
        .format({
            "Price":       "{:.3f}",
            "1d %":        "{:+.2f}%",
            "5d %":        "{:+.2f}%",
            "RSI":         "{:.1f}",
            "Z-Score":     "{:.2f}",
            "ATR %":       "{:.2f}%",
            "Drop 52W %":  "{:.1f}%",
            "Vol Ratio":   "{:.2f}x",
            "Score":       "{:.1f}",
            "Exp. Return": "{:+.2f}%",
            "Confidence %": "{}%",
            "Avg Streak":  "{:.2f}",
        })
    )
    st.dataframe(styled, use_container_width=True, height=min(600, 60 + len(df_disp)*38))

    # ── DOWNLOAD ──────────────────────────────────────────────────────────────
    csv = df_disp.to_csv(index=False).encode("utf-8")
    st.download_button("⬇  Scarica CSV", data=csv, file_name="best_revert.csv", mime="text/csv")

    # ── SHARE / EXPORT ────────────────────────────────────────────────────────
    st.markdown('<p class="sec">◼ 05 · Condividi Risultati</p>', unsafe_allow_html=True)

    # Build share text
    share_lines = ["⚡ BEST REVERT MI/NDQ — Top Picks\n"]
    for i, row in df.head(5).iterrows():
        share_lines.append(
            f"#{i+1} {row['Ticker']} | Score {row['Score']}/100 | {row['Signal']} | "
            f"RSI {row['RSI']} | Z {row['Z-Score']} | Exp.Ret {row['Exp. Return']:+.2f}%"
        )
    share_lines.append("\nAnalisi Mean Reversion — Solo scopo educativo.")
    share_text = "\n".join(share_lines)

    import urllib.parse
    wa_url  = "https://api.whatsapp.com/send?text=" + urllib.parse.quote(share_text)
    tg_url  = "https://t.me/share/url?url=https://share.streamlit.io&text=" + urllib.parse.quote(share_text)
    mail_url = "mailto:?subject=" + urllib.parse.quote("BEST REVERT — Top Picks") + "&body=" + urllib.parse.quote(share_text)
    tw_url  = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text[:280])

    sh1, sh2, sh3, sh4, sh5 = st.columns(5)

    with sh1:
        st.markdown(f"""<a href="{wa_url}" target="_blank" style="
            display:block;text-align:center;background:#25D366;color:#fff;
            border-radius:8px;padding:10px 0;font-family:'JetBrains Mono',monospace;
            font-size:0.78rem;font-weight:600;text-decoration:none;letter-spacing:0.05em">
            📱 WhatsApp</a>""", unsafe_allow_html=True)
    with sh2:
        st.markdown(f"""<a href="{tg_url}" target="_blank" style="
            display:block;text-align:center;background:#229ED9;color:#fff;
            border-radius:8px;padding:10px 0;font-family:'JetBrains Mono',monospace;
            font-size:0.78rem;font-weight:600;text-decoration:none;letter-spacing:0.05em">
            ✈️ Telegram</a>""", unsafe_allow_html=True)
    with sh3:
        st.markdown(f"""<a href="{mail_url}" style="
            display:block;text-align:center;background:#0066ff;color:#fff;
            border-radius:8px;padding:10px 0;font-family:'JetBrains Mono',monospace;
            font-size:0.78rem;font-weight:600;text-decoration:none;letter-spacing:0.05em">
            📧 Email</a>""", unsafe_allow_html=True)
    with sh4:
        st.markdown(f"""<a href="{tw_url}" target="_blank" style="
            display:block;text-align:center;background:#1DA1F2;color:#fff;
            border-radius:8px;padding:10px 0;font-family:'JetBrains Mono',monospace;
            font-size:0.78rem;font-weight:600;text-decoration:none;letter-spacing:0.05em">
            🐦 Twitter/X</a>""", unsafe_allow_html=True)
    with sh5:
        # Copy to clipboard button
        st.markdown(f"""
        <button onclick="navigator.clipboard.writeText({repr(share_text)}).then(()=>{{this.textContent='✓ Copiato!';setTimeout(()=>this.textContent='📋 Copia Testo',2000)}})"
          style="width:100%;background:#050a18;border:1px solid #0a2040;color:#0099ff;
                 border-radius:8px;padding:10px 0;font-family:'JetBrains Mono',monospace;
                 font-size:0.78rem;font-weight:600;cursor:pointer;letter-spacing:0.05em">
          📋 Copia Testo</button>""", unsafe_allow_html=True)

    # Screenshot export via html2canvas
    st.markdown("<br>", unsafe_allow_html=True)
    import streamlit.components.v1 as components
    components.html(f"""
    <html><head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
      * {{ box-sizing:border-box; margin:0; padding:0; }}
      body {{ background:#000; font-family:'JetBrains Mono',monospace; padding:8px; }}
      #card {{
        background:#050508; border:1px solid #0a1628; border-radius:14px;
        padding:24px 28px; color:#e2e8f0;
      }}
      #card h2 {{ font-size:1.1rem; color:#0099ff; margin-bottom:16px; letter-spacing:0.1em; }}
      table {{ width:100%; border-collapse:collapse; font-size:0.75rem; }}
      th {{ background:#000; color:#94b8cc; padding:6px 8px; text-align:left;
            font-size:0.62rem; letter-spacing:0.1em; text-transform:uppercase;
            border-bottom:1px solid #0a1628; }}
      td {{ padding:6px 8px; border-bottom:1px solid #050a18; color:#e2e8f0; }}
      .sb {{ color:#0099ff; font-weight:700; }}
      .b  {{ color:#38bdf8; }} .w {{ color:#7dd3fc; }} .wt {{ color:#ef4444; }}
      .pos {{ color:#0099ff; }} .neg {{ color:#ef4444; }}
      #btn {{
        margin-top:14px; width:100%;
        background:linear-gradient(135deg,#003399,#0066ff);
        color:#fff; border:none; border-radius:8px; padding:11px;
        font-family:'JetBrains Mono',monospace; font-size:0.78rem;
        font-weight:600; cursor:pointer; letter-spacing:0.06em;
      }}
      #btn:hover {{ opacity:0.85; }}
      #status {{ text-align:center; color:#7aa8c8; font-size:0.7rem; margin-top:8px; }}
    </style></head>
    <body>
    <div id="card">
      <h2>⚡ BEST REVERT MI/NDQ — Classifica</h2>
      <table>
        <thead><tr>
          <th>#</th><th>Ticker</th><th>Score</th><th>Signal</th>
          <th>RSI</th><th>Z-Score</th><th>Exp.Ret</th><th>Conf.</th>
        </tr></thead>
        <tbody>
          {"".join(
            f'<tr><td>{i+1}</td><td><b>{r["Ticker"]}</b></td>'
            f'<td class="{"sb" if r["Score"]>=70 else "b" if r["Score"]>=50 else "w" if r["Score"]>=30 else "wt"}">{r["Score"]}</td>'
            f'<td class="{"sb" if r["Signal"]=="STRONG BUY" else "b" if r["Signal"]=="BUY" else "w" if r["Signal"]=="WATCH" else "wt"}">{r["Signal"]}</td>'
            f'<td>{r["RSI"]}</td><td>{r["Z-Score"]}</td>'
            f'<td class="{"pos" if r["Exp. Return"]>0 else "neg"}">{r["Exp. Return"]:+.2f}%</td>'
            f'<td>{r["Confidence %"]}%</td></tr>'
            for i,r in df.head(10).iterrows()
          )}
        </tbody>
      </table>
    </div>
    <button id="btn" onclick="captureAndDownload()">📸 Salva come JPEG</button>
    <div id="status"></div>
    <script>
    function captureAndDownload() {{
      var btn = document.getElementById("btn");
      var status = document.getElementById("status");
      btn.textContent = "⏳ Generando immagine…";
      btn.disabled = true;
      html2canvas(document.getElementById("card"), {{
        backgroundColor: "#050508", scale: 2,
        logging: false, useCORS: true
      }}).then(function(canvas) {{
        var link = document.createElement("a");
        link.download = "best_revert_classifica.jpg";
        link.href = canvas.toDataURL("image/jpeg", 0.95);
        link.click();
        btn.textContent = "✓ Download avviato!";
        status.textContent = "Immagine salvata come best_revert_classifica.jpg";
        setTimeout(() => {{ btn.textContent = "📸 Salva come JPEG"; btn.disabled = false; }}, 3000);
      }});
    }}
    </script>
    </body></html>
    """, height=420, scrolling=False)

    # ── METHODOLOGY ───────────────────────────────────────────────────────────
    with st.expander("📐 Legenda & Metodologia — clicca per espandere"):
        st.markdown("""
<style>
.leg-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:16px 0; }
.leg-card {
    background:#000; border:1px solid #0a1628; border-radius:10px;
    padding:14px 18px;
}
.leg-card:hover { border-color:#0a2040; }
.leg-title { font-size:0.65rem; letter-spacing:0.15em; text-transform:uppercase; color:#0099ff; margin-bottom:6px; font-weight:700; }
.leg-name  { font-size:1rem; font-weight:700; color:#f8fafc; margin-bottom:4px; font-family:'JetBrains Mono',monospace; }
.leg-desc  { font-size:0.78rem; color:#94a3b8; line-height:1.55; }
.leg-desc b { color:#e2e8f0; }
.sig-row { display:flex; gap:8px; flex-wrap:wrap; margin:14px 0; }
.sig-pill {
    border-radius:20px; padding:5px 14px;
    font-size:0.72rem; font-weight:700; letter-spacing:0.08em;
    font-family:'JetBrains Mono',monospace;
}
.formula-box {
    background:#000; border:1px solid #0a1628; border-radius:10px;
    padding:14px 18px; margin:10px 0; font-family:'JetBrains Mono',monospace;
}
.formula-box .f-label { font-size:0.62rem; color:#94b8cc; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:4px; }
.formula-box .f-val   { font-size:0.88rem; color:#38bdf8; font-weight:600; }
.formula-box .f-exp   { font-size:0.72rem; color:#94b8cc; margin-top:4px; }
.col-table { width:100%; border-collapse:collapse; font-family:'JetBrains Mono',monospace; font-size:0.78rem; margin:12px 0; }
.col-table th { background:#000; color:#94b8cc; padding:7px 10px; text-align:left; font-size:0.62rem; letter-spacing:0.1em; text-transform:uppercase; border-bottom:1px solid #0a1628; }
.col-table td { color:#cbd5e1; padding:7px 10px; border-bottom:1px solid #050a18; }
.col-table td:first-child { color:#e2e8f0; font-weight:600; }
.col-table tr:hover td { background:#050a18; }
</style>

<div style="font-family:'JetBrains Mono',monospace;">

<div style="font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#0099ff;margin-bottom:16px;font-weight:700">
  ◼ SIGNIFICATO COLONNE
</div>

<table class="col-table">
<tr><th>Colonna</th><th>Significato</th><th>Interpretazione</th></tr>
<tr><td>Price</td><td>Prezzo di chiusura attuale</td><td>Prezzo ultimo giorno disponibile</td></tr>
<tr><td>1d %</td><td>Variazione % giornaliera</td><td style="color:#0099ff">🔵 Positivo = rialzo · <span style="color:#ef4444">🔴 Negativo = ribasso</span></td></tr>
<tr><td>5d %</td><td>Performance ultimi 5 giorni</td><td>Trend di breve periodo</td></tr>
<tr><td>RSI (14)</td><td>Relative Strength Index</td><td><b style="color:#0099ff">&lt;30 = ipervenduto (segnale buy)</b> · &gt;70 = ipercomprato</td></tr>
<tr><td>Z-Score</td><td>Distanza dalla media mobile (20gg)</td><td><b style="color:#0099ff">&lt;−1.5 = molto sotto la media → forte pressione di ritorno</b></td></tr>
<tr><td>ATR %</td><td>Average True Range in %</td><td>Volatilità media giornaliera del titolo</td></tr>
<tr><td>Drop 52W %</td><td>Distanza dal massimo annuale</td><td><b style="color:#0099ff">−30% = titolo è 30% sotto i massimi dell'anno</b></td></tr>
<tr><td>Neg Days</td><td>Giorni negativi consecutivi</td><td>Quante chiusure rosse di fila — più alto = più probabile rimbalzo</td></tr>
<tr><td>Avg Streak</td><td>Media storica streak negative</td><td>Statisticamente, dopo questi giorni rossi il titolo rimbalza</td></tr>
<tr><td>Score</td><td>Punteggio di reversione 0–100</td><td><b style="color:#0099ff">Più alto = più probabile inversione rialzista imminente</b></td></tr>
<tr><td>Signal</td><td>Classificazione finale</td><td>STRONG BUY / BUY / WATCH / WAIT</td></tr>
<tr><td>Exp. Return</td><td>Rendimento atteso stimato %</td><td>Stima statistica del rimbalzo potenziale</td></tr>
<tr><td>Confidence %</td><td>Livello di confidenza</td><td>Forza del segnale — più alto = segnale più robusto</td></tr>
</table>

<div style="font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#0099ff;margin:20px 0 12px;font-weight:700">
  ◼ SEGNALI
</div>
<div class="sig-row">
  <span class="sig-pill" style="background:#001a4d;border:1px solid #0066ff;color:#0099ff">⚡ STRONG BUY ≥70</span>
  <span class="sig-pill" style="background:#001233;border:1px solid #0044aa;color:#38bdf8">▲ BUY ≥50</span>
  <span class="sig-pill" style="background:#000d24;border:1px solid #002266;color:#7dd3fc">◎ WATCH ≥30</span>
  <span class="sig-pill" style="background:#1a0000;border:1px solid #660000;color:#ef4444">✕ WAIT &lt;30</span>
</div>
<div style="font-size:0.72rem;color:#94b8cc;margin-top:6px">
  Un segnale STRONG BUY indica che il titolo è statisticamente in una zona di ipervenduto estremo su più indicatori contemporaneamente.
</div>

<div style="font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#0099ff;margin:20px 0 12px;font-weight:700">
  ◼ CALCOLO SCORE (0–100)
</div>
<div class="leg-grid">
  <div class="leg-card">
    <div class="leg-title">RSI · 25 pt max</div>
    <div class="leg-name">Relative Strength Index</div>
    <div class="leg-desc">Misura se un titolo è <b>ipervenduto</b>. RSI &lt; 30 è il segnale classico di inversione. Più basso l'RSI, più punti.</div>
  </div>
  <div class="leg-card">
    <div class="leg-title">Z-SCORE · 25 pt max</div>
    <div class="leg-name">Distanza dalla Media</div>
    <div class="leg-desc">Quanto è lontano il prezzo dalla <b>media mobile a 20 giorni</b>. Z &lt; −2 significa che il titolo è statisticamente anomalo verso il basso.</div>
  </div>
  <div class="leg-card">
    <div class="leg-title">DROP 52W · 25 pt max</div>
    <div class="leg-name">Calo dal Massimo Annuale</div>
    <div class="leg-desc">Distanza percentuale dal <b>massimo degli ultimi 12 mesi</b>. Un calo del −40% genera il punteggio massimo.</div>
  </div>
  <div class="leg-card">
    <div class="leg-title">NEG STREAK · 25 pt max</div>
    <div class="leg-name">Giorni Rossi Consecutivi</div>
    <div class="leg-desc">Quanti giorni di chiusura <b>negativa di fila</b>. 5+ giorni rossi consecutivi = massimo score: storicamente il rimbalzo è imminente.</div>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
  <div class="formula-box">
    <div class="f-label">Formula Expected Return</div>
    <div class="f-val">−ZScore × ATR% × 0.5</div>
    <div class="f-exp">Stima del rimbalzo atteso in % basata sulla volatilità e distanza dalla media</div>
  </div>
  <div class="formula-box">
    <div class="f-label">Formula Confidence</div>
    <div class="f-val">f(|Z|, RSI, Streak) · 10–99%</div>
    <div class="f-exp">Forza complessiva del segnale. 99% = tutti gli indicatori allineati</div>
  </div>
</div>

<div style="margin-top:14px;font-size:0.68rem;color:#7aa8c8;border-top:1px solid #0a1628;padding-top:10px">
  ⚠️ Scopo puramente educativo/informativo. Non costituisce consulenza finanziaria.
</div>
</div>
""", unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:70px 20px">
      <div style="font-size:3.5rem;margin-bottom:20px;opacity:0.3">⚡</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#7aa8c8">
        Inserisci i ticker e premi GENERA CLASSIFICA
      </div>
      <div style="font-size:0.75rem;color:#4a7a9b;margin-top:8px">
        Supporta ticker (ENI.MI / AAPL), ISIN e ricerca per nome
      </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
# Ensure config.toml is present for dark theme
st.caption("⚠️ Solo scopo educativo/informativo. Non costituisce consulenza finanziaria. Dati: Yahoo Finance.")
