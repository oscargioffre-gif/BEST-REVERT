import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
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
.hero-sub { font-size: 0.72rem; color: #334155; margin-top: 10px; letter-spacing: 0.15em; text-transform: uppercase; }
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
.stTextInput label { color: #334155 !important; font-size: 0.7rem !important; }
.stTextInput input::placeholder { color: #1e3a5f !important; }

/* Selectbox */
div[data-baseweb="select"] { background: #050508 !important; border-color: #0a1628 !important; border-radius: 8px !important; }
div[data-baseweb="select"] > div { background: #050508 !important; color: #e2e8f0 !important; }
div[data-baseweb="select"] span { color: #e2e8f0 !important; font-size: 0.88rem !important; }
div[data-baseweb="select"] input { color: #e2e8f0 !important; caret-color: #0099ff !important; }
div[data-baseweb="select"] svg { fill: #334155 !important; }
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
.pod-rank { font-size: 0.6rem; color: #334155; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 6px; }
.pod-ticker { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; }
.pod-score { font-size: 2.2rem; font-weight: 700; color: #0099ff; line-height: 1; margin: 4px 0; }
.pod-score sub { font-size: 0.8rem; color: #334155; }
.bar-bg { background: #0a1628; border-radius: 4px; height: 5px; margin: 8px 0; }
.bar-fill { border-radius: 4px; height: 5px; }
.pill { display: inline-block; background: #050a18; border: 1px solid #0a2040;
        border-radius: 5px; padding: 2px 7px; font-size: 0.65rem; color: #64748b; margin: 2px 2px 0 0; }
.pill b { color: #cbd5e1; }
.signal-sb { color: #0099ff; font-weight: 700; }
.signal-b  { color: #38bdf8; font-weight: 600; }
.signal-w  { color: #7dd3fc; }
.signal-wt { color: #ef4444; }
.exp-pos { color: #0099ff; } .exp-neg { color: #ef4444; }

/* captions */
small, .stCaption, [data-testid="stCaptionContainer"] { color: #334155 !important; font-size: 0.72rem !important; }
h3 { color: #f8fafc !important; font-size: 1rem !important; font-weight: 600 !important; }
[data-testid="stMetric"] { background: #050508; border: 1px solid #0a1628; border-radius: 10px; padding: 14px 18px; }
[data-testid="stMetricLabel"] { color: #334155 !important; font-size: 0.68rem !important; letter-spacing: 0.1em !important; }
[data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 1.3rem !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #0a1628; }
hr { border-color: #0a1628 !important; margin: 20px 0 !important; }
[data-testid="stExpander"] { background: #050508; border: 1px solid #0a1628; border-radius: 10px; }
[data-testid="stExpander"] summary { color: #64748b !important; font-size: 0.78rem !important; }
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
    """Try to resolve name/ISIN/ticker to a Yahoo Finance symbol."""
    raw = raw.strip()
    if not raw: return ""
    # ISIN pattern: 2 letters + 10 alphanumeric
    import re
    if re.match(r'^[A-Z]{2}[A-Z0-9]{10}$', raw.upper()):
        try:
            t = yf.Ticker(raw)
            info = t.get_info()
            sym = info.get("symbol","")
            if sym: return sym
        except: pass
    # Try as-is first
    try:
        t = yf.Ticker(raw)
        h = yf.download(raw, period="5d", progress=False, auto_adjust=True)
        if not h.empty: return raw.upper()
    except: pass
    # Try search via yfinance
    try:
        res = yf.Search(raw, max_results=1)
        quotes = res.quotes
        if quotes:
            return quotes[0].get("symbol","")
    except: pass
    return raw.upper()

@st.cache_data(ttl=600, show_spinner=False)
def analyse_ticker(ticker: str) -> dict | None:
    try:
        raw = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        if raw.empty or len(raw) < 30: return None
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        raw = raw[["Open","High","Low","Close","Volume"]].dropna()
        cl = raw["Close"]
        price       = float(cl.iloc[-1])
        rsi_val     = float(compute_rsi(cl).iloc[-1])
        atr_val     = float(compute_atr(raw).iloc[-1])
        atr_pct     = atr_val/price*100
        z           = float(compute_zscore(cl).iloc[-1])
        high52      = float(cl.rolling(252).max().iloc[-1])
        drop52      = (price - high52)/high52*100
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
            "Ticker":       ticker,
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
              <div style="margin-top:10px;font-size:0.72rem;color:#1e3a5f">
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
        ("📉 RSI min",           f"{df['RSI'].min():.1f}",             df.loc[df['RSI'].idxmin(),'Ticker']),
        ("📊 Z-Score min",       f"{df['Z-Score'].min():.2f}",         df.loc[df['Z-Score'].idxmin(),'Ticker']),
        ("🔻 Drop 52W max",      f"{df['Drop 52W %'].min():.1f}%",     df.loc[df['Drop 52W %'].idxmin(),'Ticker']),
        ("🔴 Streak neg max",    f"{int(df['Neg Days'].max())} gg",    df.loc[df['Neg Days'].idxmax(),'Ticker']),
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

    # ── METHODOLOGY ───────────────────────────────────────────────────────────
    with st.expander("📐 Metodologia Score"):
        st.markdown("""
**Reversion Score (0–100)** — 4 componenti da 0 a 25 punti ciascuno:

| Componente | Logica |
|---|---|
| **RSI (14)** | RSI < 30 = ipervenduto → score massimo |
| **Z-Score (20)** | Prezzo molto sotto la media mobile → alta tensione di ritorno |
| **Drop 52W %** | Distanza dai massimi annuali → potenziale di recupero |
| **Neg. Streak** | Giorni rossi consecutivi → catalizzatore inversione imminente |

**Segnali:** 🔵 STRONG BUY ≥70 · 🔵 BUY ≥50 · 🔵 WATCH ≥30 · 🔴 WAIT <30

**Expected Return** = −ZScore × ATR% × 0.5

**Confidence** = f(|ZScore|, RSI, Streak) — scala 10–99%
        """)

else:
    st.markdown("""
    <div style="text-align:center;padding:70px 20px">
      <div style="font-size:3.5rem;margin-bottom:20px;opacity:0.3">⚡</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#1e3a5f">
        Inserisci i ticker e premi GENERA CLASSIFICA
      </div>
      <div style="font-size:0.75rem;color:#0f1f35;margin-top:8px">
        Supporta ticker (ENI.MI / AAPL), ISIN e ricerca per nome
      </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("⚠️ Solo scopo educativo/informativo. Non costituisce consulenza finanziaria. Dati: Yahoo Finance.")
