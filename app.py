import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import time
import io

st.set_page_config(
    page_title="Affiliate Programs Monitor",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #f8f9fb; }
  [data-testid="stHeader"] { background: #ffffff; border-bottom: 1px solid #e5e7eb; }
  .block-container { padding-top: 2rem; padding-bottom: 3rem; }

  html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: #111827;
  }

  .app-header {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .app-title { font-size: 20px; font-weight: 700; color: #111827; margin-bottom: 2px; }
  .app-subtitle { font-size: 13px; color: #6b7280; }
  .live-block { text-align: right; }
  .live-dot-wrap { display: flex; align-items: center; gap: 6px; justify-content: flex-end; font-size: 13px; color: #16a34a; font-weight: 500; }
  .live-dot { width: 7px; height: 7px; border-radius: 50%; background: #16a34a; display: inline-block; }
  .last-scan-text { font-size: 11px; color: #9ca3af; margin-top: 3px; }

  [data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  [data-testid="stMetricLabel"] { color: #6b7280 !important; font-size: 11px !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.05em; }
  [data-testid="stMetricValue"] { color: #111827 !important; font-size: 24px !important; font-weight: 700 !important; }

  .section-title {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
    margin: 28px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e5e7eb;
  }

  .stButton > button {
    background: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: 500;
  }
  .stButton > button:hover { background: #1d4ed8; color: #ffffff; border: none; }

  [data-testid="stSelectbox"] > div > div {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    color: #111827;
  }

  .alert-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .alert-card.new { border-left: 4px solid #6d28d9; }
  .alert-card.verify { border-left: 4px solid #d97706; }
  .alert-card.risk { border-left: 4px solid #dc2626; }
  .alert-title { font-weight: 700; font-size: 14px; color: #111827; margin-bottom: 10px; }
  .alert-row { font-size: 13px; color: #6b7280; margin-bottom: 4px; }
  .alert-row strong { color: #111827; }
  .alert-action { font-size: 13px; font-weight: 500; margin-top: 10px; }
  .alert-action.new { color: #6d28d9; }
  .alert-action.verify { color: #d97706; }
  .alert-action.risk { color: #dc2626; }

  .log-box {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 16px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #1e293b;
    line-height: 1.9;
  }

  .step-item {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
  }
  .step-num {
    background: #eff6ff;
    color: #2563eb;
    font-weight: 700;
    font-size: 12px;
    padding: 3px 9px;
    border-radius: 5px;
    min-width: 32px;
    text-align: center;
  }
  .step-body-title { font-weight: 600; color: #111827; margin-bottom: 2px; font-size: 14px; }
  .step-body-desc { font-size: 13px; color: #6b7280; }

  /* Digest */
  .digest-header {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
  }
  .digest-title { font-size: 18px; font-weight: 700; color: #111827; }
  .digest-sub { font-size: 13px; color: #6b7280; margin-top: 4px; }

  .digest-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
  }
  .digest-card-title { font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 8px; }
  .digest-row { font-size: 13px; color: #6b7280; margin-bottom: 3px; }
  .digest-row strong { color: #111827; }

  .risk-card {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #92400e;
  }

  .rec-card {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #14532d;
  }

  .footer {
    margin-top: 48px;
    padding-top: 16px;
    border-top: 1px solid #e5e7eb;
    text-align: center;
    font-size: 12px;
    color: #9ca3af;
  }

  hr { border-color: #e5e7eb !important; }
  [data-testid="stTabs"] { margin-top: 8px; }
</style>
""", unsafe_allow_html=True)


# ── Data ──────────────────────────────────────────────────────────────────────
PROGRAM_NAMES = [
    "Bet365 Partners","888 Affiliates","LeoVegas Affiliates","Income Access Network",
    "Rizk Partners","Stake Affiliates","PlayAmo Partners","Fortune Affiliates",
    "Betsson Group Affiliates","22Bet Partners","Betwinner Affiliates","Coldbet Partners",
    "FoxSlots Partners","Rocketpot Affiliates","Bwin Affiliates","William Hill Partners",
    "Unibet Affiliates","PokerStars Affiliates","Betway Partners","Mr Green Affiliates",
    "Casumo Affiliates","Videoslots Partners","Casiplay Affiliates","Fastpay Partners",
    "N1 Partners","Slotty Vegas Affiliates","Wildz Affiliates","Dunder Affiliates",
    "CasinoRoom Partners","Kaboo Affiliates","Genesis Affiliates","OVO Casino Partners",
    "Vera&John Affiliates","Guts Affiliates","Betsafe Partners","NordicBet Affiliates",
    "Expekt Affiliates","Jetbull Partners","EasyBet Partners","SpinBet Affiliates",
    "MegaSlot Affiliates","CryptoLuck Partners","LuckyNova Partners","GrandWin Affiliates",
    "SilverPlay Partners","Winolot Affiliates","Casinado Partners","Odds96 Partners",
    "C24 Partners","Boomerang Partners","Partners1xbet","Parimatch Partners",
    "Mostbet Affiliates","Melbet Partners","PinUp Partners","1win Affiliates",
    "GGBet Partners","Vulkan Bet Affiliates","ICE Casino Partners","BC.Game Affiliates",
    "BitStarz Partners","FortuneJack Affiliates","mBit Partners","BetFury Affiliates",
    "CloudBet Partners","CryptoGames Partners","Rollbit Affiliates","Shuffle Affiliates",
    "JackBit Partners","NineCasino Affiliates","Vave Affiliates","Sportsbet.io Partners",
    "Rabona Affiliates","Oshi Affiliates","BetChain Partners","1xSlots Affiliates",
    "BetAndreas Partners","Sportaza Affiliates","Haz Casino Partners","20Bet Affiliates",
    "Playfina Affiliates","Legzo Partners","Turbo Casino Affiliates","Fresh Casino Partners",
    "Sol Casino Partners","Izzi Casino Affiliates","Cat Casino Partners","Gama Affiliates",
    "Selector Casino Partners","Brillx Affiliates","Riobet Partners","JVSpin Affiliates",
    "DrBet Partners","SpinAway Affiliates","Mystake Partners","Paripesa Affiliates",
    "MozzartBet Affiliates","Betmaster Partners","Betano Affiliates","Novibet Partners",
    "NetBet Partners","10Bet Affiliates","GalaBingo Affiliates","Tombola Partners",
    "BetVictor Affiliates","Coral Partners","Ladbrokes Affiliates","Paddy Power Partners",
    "Sky Bet Affiliates","Betfair Affiliates","Smarkets Partners","STS Affiliates",
    "Fortuna Partners","Tipsport Affiliates","Synot Affiliates","Tipico Partners",
    "Bettilt Affiliates","Betpas Partners","Mariobet Affiliates","Ngsbahis Partners",
    "Hilbet Partners","Piabet Affiliates","Goldenbahis Partners","Bahsegel Affiliates",
    "Casinomaxi Partners","Vdcasino Affiliates","Mobilbahis Partners","Superbahis Affiliates",
    "Tempobet Partners","Betboo Affiliates","Pragmatic Partners","Push Gaming Affiliates",
    "Nolimit City Affiliates","Yggdrasil Partners","Thunderkick Affiliates","ELK Studios Partners",
    "Quickspin Affiliates","Microgaming Partners","NetEnt Affiliates","Play n GO Partners",
    "Red Tiger Affiliates","Evolution Partners","Playtech Affiliates","NextGen Partners",
    "Betcris Affiliates","Coolbet Partners","NorgesBet Affiliates","Grosvenor Partners",
    "Sky Vegas Affiliates","Betdaq Affiliates","Colossus Bets Partners","BetConnect Affiliates",
    "Spreadex Affiliates","BoyleSports Partners","Quinnbet Affiliates","LiveScore Partners",
    "Midnite Affiliates","Caledonian Affiliates","Highlands Bet Partners","NetBet Affiliates",
    "Fansbet Affiliates","Rootz Affiliates","White Hat Gaming Affiliates","ProgressPlay Partners",
    "Nektan Affiliates","Cozy Games Partners","Relax Gaming Affiliates","Pariplay Partners",
    "Jumpman Partners","MrQ Partners","SpinGenie Affiliates","Slingo Partners",
    "Aspers Affiliates","Buzz Bingo Partners","Mecca Bingo Affiliates","Jackpotjoy Partners",
    "Heart Bingo Affiliates","Foxy Games Partners","Virgin Games Affiliates","888Ladies Partners",
    "Moon Games Affiliates","OddsMonkey Affiliates","Matched Betting Blog Partners",
    "Profit Accumulator Affiliates","OddsJam Partners","SharpSide Affiliates",
    "BetQL Affiliates","Action Network Partners","The Action Network Affiliates",
    "Sports Insights Partners","Pinnacle Affiliates","Betcris Partners","Betsson UA Affiliates",
    "Fonbet Affiliates","Liga Stavok Partners","Winline Affiliates","Leon Bet Partners",
    "Marathonbet Affiliates","Pari Affiliates","BetCity Partners","Olimp Affiliates",
    "1xBet Partners","Bwin UA Affiliates","Parimatch UA Partners","Favbet Affiliates",
    "Vbet Partners","FanSport Affiliates","GambetDC Partners","BetMGM Affiliates",
    "DraftKings Partners","FanDuel Affiliates","Caesars Affiliates","PointsBet Partners",
    "WynnBet Affiliates","Barstool Partners","theScore Affiliates","SI Sportsbook Partners",
    "MaximBet Affiliates","Fubo Sportsbook Partners","Unibet US Affiliates","Fox Bet Partners",
    "BallyBet Affiliates","Golden Nugget Partners","Hard Rock Affiliates","Rivers Casino Partners",
    "Rush Street Partners","SugarHouse Affiliates","SBK Partners","Sleeper Affiliates",
    "PrizePicks Partners","Underdog Fantasy Affiliates","Draft Partners","SuperDraft Affiliates",
    "OwnersBox Partners","Boom Fantasy Affiliates","Yahoo Fantasy Partners","ESPN Bet Affiliates",
    "Tipwin Partners","Sportingbet Affiliates","Winner Affiliates","Interwetten Partners",
    "Eurobet Affiliates","Snai Partners","Lottomatica Affiliates","Sisal Partners",
    "Planetwin Affiliates","Better Partners","Betflag Affiliates","BetFlag Partners",
    "Eurobet Partners","GoldBet Affiliates","Betclic Partners","Winamax Affiliates",
    "PMU Partners","France Pari Affiliates","NetBet FR Partners","JOA Partners",
    "Barriere Affiliates","Partouche Partners","Ladbrokes BE Affiliates","Circus Partners",
    "Napoleon Games Affiliates","Betfirst Partners","Golden Palace Affiliates",
    "Unibet BE Partners","Viggoslots Affiliates","Catena Media Partners","Better Collective Affiliates",
    "XLMedia Partners","Raketech Affiliates","Gambling.com Partners","AskGamblers Affiliates",
    "CasinoGuru Partners","Slotegrator Affiliates","SoftSwiss Partners","BGaming Affiliates",
    "Spinomenal Partners","KA Gaming Affiliates","Hacksaw Gaming Partners","NoLimit Affiliates",
    "Avatar UX Partners","Kalamba Games Affiliates","Triple Edge Partners","1spin4win Affiliates",
]

SOURCES_LIST = ["AffPapa","GPWA","Affiliate Guard Dog","AskGamblers","SBC News","Gambling Insider","Reddit","Trustpilot"]
GEO_LIST = ["EU","UK","CA","AU","US","SE","DE","FI","NO","UA","CIS","LATAM","APAC","Tier 1","Worldwide"]
LICENSE_LIST = ["MGA","UKGC","Curaçao","Gibraltar","Isle of Man","Kahnawake","Unknown"]
STATUS_WEIGHTS = ["New","New","To Verify","To Verify","Verified","Verified","Verified","Verified","Verified","Rejected"]
PRIORITY_LIST = ["High","High","Medium","Medium","Low"]
COMMISSION_LIST = ["RevShare 25-40%","RevShare 30-45%","CPA $50-150","CPA $100-200","Hybrid","RevShare 20-35%","RevShare 35-50%"]
NOTES_LIST = [
    "Verified program. Stable payouts.",
    "New listing — terms under review.",
    "Community-flagged for late payments.",
    "Strong Tier 1 traffic focus.",
    "Crypto-friendly. Fast onboarding.",
    "Mixed reviews. Monitor closely.",
    "High RevShare. No track record yet.",
    "Established network. Well-reviewed.",
    "Recently launched. License pending.",
    "Reputation confirmed. Recommended.",
    "Rapid growth in LATAM market.",
    "Pending license renewal. Risk flag.",
    "Top performer in Nordics.",
    "New management. Quality unclear.",
    "Strong affiliate community feedback.",
]

TODAY = "2026-06-12"
TODAY_DT = datetime(2026, 6, 12)


def generate_programs(n=500):
    random.seed(42)
    names = (PROGRAM_NAMES * ((n // len(PROGRAM_NAMES)) + 2))[:n]
    rows = []
    for i, name in enumerate(names):
        # Spread: mostly last 90 days, some today
        if i < 8:
            days_ago = 0
        elif i < 30:
            days_ago = random.randint(1, 7)
        else:
            days_ago = random.randint(1, 90)
        detected = (TODAY_DT - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        status = random.choice(STATUS_WEIGHTS)
        if days_ago == 0:
            status = "New"
        elif days_ago <= 7:
            status = random.choice(["New","To Verify"])
        geo_sample = random.sample(GEO_LIST, random.randint(1, 3))
        rows.append({
            "Name": name,
            "Date Detected": detected,
            "Source": random.choice(SOURCES_LIST),
            "GEO": ", ".join(geo_sample),
            "License": random.choice(LICENSE_LIST),
            "Commission": random.choice(COMMISSION_LIST),
            "Affiliate URL": name.lower().replace(" ","").replace("'","").replace("&","and") + ".com/affiliates",
            "Status": status,
            "Priority": random.choice(PRIORITY_LIST),
            "Notes": random.choice(NOTES_LIST),
        })
    return pd.DataFrame(rows)


NEW_POOL = [
    {"Name":"SpinBet Affiliates","Source":"SBC News","GEO":"EU, UA","License":"Curaçao","Commission":"RevShare 45%","Affiliate URL":"spinbet-affiliates.com/affiliates","Status":"New","Priority":"High","Notes":"High RevShare. No track record yet."},
    {"Name":"LuckyNova Partners","Source":"Reddit","GEO":"UA, EU","License":"Unknown","Commission":"CPA $120","Affiliate URL":"luckynova.io/affiliates","Status":"To Verify","Priority":"High","Notes":"License unconfirmed. Verify before engagement."},
    {"Name":"MegaSlot Affiliates","Source":"AffPapa","GEO":"EU, UA","License":"Curaçao","Commission":"Hybrid","Affiliate URL":"megaslot.io/affiliates","Status":"New","Priority":"Medium","Notes":"New launch. High bonus offers."},
    {"Name":"CryptoNova Partners","Source":"GPWA","GEO":"Worldwide","License":"Unknown","Commission":"RevShare 30%","Affiliate URL":"cryptonova.gg/affiliates","Status":"To Verify","Priority":"Medium","Notes":"Crypto-native. Community buzz. License unclear."},
    {"Name":"NovaSpin Affiliates","Source":"Affiliate Guard Dog","GEO":"EU","License":"MGA","Commission":"RevShare 35%","Affiliate URL":"novaspin.com/affiliates","Status":"New","Priority":"High","Notes":"Early detection. Solid MGA license."},
    {"Name":"StarAffiliates Network","Source":"SBC News","GEO":"Tier 1","License":"MGA","Commission":"RevShare 30-45%","Affiliate URL":"staraffiliates.com/partners","Status":"New","Priority":"High","Notes":"Announced at SBC Summit. Established team."},
    {"Name":"BetRocket Partners","Source":"AffPapa","GEO":"EU, CA","License":"Curaçao","Commission":"CPA $150","Affiliate URL":"betrocket.io/affiliates","Status":"To Verify","Priority":"Medium","Notes":"New CPA-focused program. Terms unclear."},
]

MONITORING_SOURCES = [
    {"Source":"AffPapa","Type":"Affiliate Directory","Monitors":"New listings, terms changes","Frequency":"Daily","Priority":"High"},
    {"Source":"GPWA","Type":"Affiliate Forum","Monitors":"New announcements, affiliate feedback","Frequency":"Daily","Priority":"High"},
    {"Source":"Affiliate Guard Dog","Type":"Watchdog Forum","Monitors":"Rogue programs, payment issues","Frequency":"3x/week","Priority":"High"},
    {"Source":"AskGamblers","Type":"Review Platform","Monitors":"New programs, complaint trends","Frequency":"Daily","Priority":"High"},
    {"Source":"SBC News","Type":"Industry News","Monitors":"New launches, partnerships","Frequency":"Daily","Priority":"High"},
    {"Source":"Gambling Insider","Type":"Industry News","Monitors":"Market launches, M&A activity","Frequency":"Daily","Priority":"Medium"},
    {"Source":"Reddit","Type":"Community Forum","Monitors":"Community buzz, warnings","Frequency":"Daily","Priority":"Medium"},
    {"Source":"Trustpilot","Type":"Review Platform","Monitors":"Reputation signals, complaints","Frequency":"Weekly","Priority":"Medium"},
]


# ── Session state ─────────────────────────────────────────────────────────────
if "programs" not in st.session_state:
    st.session_state.programs = generate_programs(500)
if "scan_log" not in st.session_state:
    st.session_state.scan_log = []
if "last_scan" not in st.session_state:
    st.session_state.last_scan = None


# ── Header ────────────────────────────────────────────────────────────────────
last_scan_text = st.session_state.last_scan.strftime("%d %b %Y, %H:%M") if st.session_state.last_scan else "Not yet run"
st.markdown(f"""
<div class="app-header">
  <div>
    <div class="app-title">📡 Affiliate Programs Monitor</div>
    <div class="app-subtitle">Affiliate intelligence platform for monitoring new iGaming partnership opportunities.</div>
  </div>
  <div class="live-block">
    <div class="live-dot-wrap"><span class="live-dot"></span> Live</div>
    <div class="last-scan-text">Last scan: {last_scan_text}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Monitor", "📋 Weekly CEO Digest"])


# ════════════════════════════════════════════════════════════
# TAB 1 — MONITOR
# ════════════════════════════════════════════════════════════
with tab1:

    # Metrics
    df = st.session_state.programs
    week_ago_str = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
    total = len(df)
    new_this_week = len(df[df["Date Detected"] >= week_ago_str])
    today_detected = len(df[df["Date Detected"] == TODAY])
    to_verify = len(df[df["Status"] == "To Verify"])
    verified = len(df[df["Status"] == "Verified"])

    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    c1.metric("Total Programs", total)
    c2.metric("New This Week", new_this_week, delta=f"+{new_this_week}")
    c3.metric("Detected Today", today_detected, delta=f"+{today_detected}")
    c4.metric("To Verify", to_verify)
    c5.metric("Verified", verified)
    c6.metric("Sources Monitored", len(MONITORING_SOURCES))
    c7.metric("Rejected", len(df[df["Status"] == "Rejected"]))

    st.markdown("<br>", unsafe_allow_html=True)

    # Scan
    st.markdown('<div class="section-title">Scan Controls</div>', unsafe_allow_html=True)
    col_btn, col_space = st.columns([2, 5])
    with col_btn:
        run_scan = st.button("🔍 Run Scan Now", use_container_width=True)

    if run_scan:
        with st.spinner("Scanning sources..."):
            time.sleep(1.5)
        existing = set(st.session_state.programs["Name"].tolist())
        available = [p for p in NEW_POOL if p["Name"] not in existing]
        if not available:
            available = NEW_POOL
        n_new = random.randint(3, 5)
        batch = random.sample(available, min(n_new, len(available)))
        scan_time = datetime.now()
        for p in batch:
            p = p.copy()
            p["Date Detected"] = TODAY
        new_df = pd.DataFrame([{**p, "Date Detected": TODAY} for p in batch])
        st.session_state.programs = pd.concat([st.session_state.programs, new_df], ignore_index=True)
        st.session_state.last_scan = scan_time
        log = [f"[{scan_time.strftime('%H:%M:%S')}] Scan started — {len(MONITORING_SOURCES)} sources active"]
        for src in ["AffPapa","GPWA","SBC News","Reddit","Affiliate Guard Dog"]:
            log.append(f"[{scan_time.strftime('%H:%M:%S')}]  Scanning {src}...")
        for p in batch:
            log.append(f"[{scan_time.strftime('%H:%M:%S')}]  DETECTED: {p['Name']} via {p['Source']} — {p['Status']}")
        log.append(f"[{scan_time.strftime('%H:%M:%S')}] Scan complete. {len(batch)} new affiliate programs added.")
        st.session_state.scan_log = log
        st.success(f"✅ Scan completed. {len(batch)} new affiliate programs detected.")
        st.rerun()

    if st.session_state.scan_log:
        st.markdown('<div class="section-title">Scan Log</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="log-box">{"<br>".join(st.session_state.scan_log)}</div>', unsafe_allow_html=True)

    # Database
    st.markdown('<div class="section-title">Affiliate Programs Database</div>', unsafe_allow_html=True)
    df = st.session_state.programs

    f1,f2,f3,f4,f5 = st.columns(5)
    with f1:
        search = st.text_input("🔍 Search by name", placeholder="e.g. Bet365")
    with f2:
        status_f = st.selectbox("Status", ["All"] + sorted(df["Status"].unique().tolist()))
    with f3:
        priority_f = st.selectbox("Priority", ["All","High","Medium","Low"])
    with f4:
        source_f = st.selectbox("Source", ["All"] + sorted(df["Source"].unique().tolist()))
    with f5:
        geo_options = sorted(set(g.strip() for geos in df["GEO"].str.split(",") for g in geos))
        geo_f = st.selectbox("GEO", ["All"] + geo_options)

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["Name"].str.contains(search, case=False, na=False)]
    if status_f != "All":
        filtered = filtered[filtered["Status"] == status_f]
    if priority_f != "All":
        filtered = filtered[filtered["Priority"] == priority_f]
    if source_f != "All":
        filtered = filtered[filtered["Source"] == source_f]
    if geo_f != "All":
        filtered = filtered[filtered["GEO"].str.contains(geo_f, case=False, na=False)]

    filtered_sorted = filtered.sort_values("Date Detected", ascending=False).reset_index(drop=True)

    row_count_col, export_col = st.columns([5,1])
    with row_count_col:
        st.markdown(f"<div style='font-size:13px;color:#6b7280;padding:6px 0;'>Showing <strong>{len(filtered_sorted)}</strong> of <strong>{len(df)}</strong> programs</div>", unsafe_allow_html=True)
    with export_col:
        buf = io.StringIO()
        filtered_sorted.to_csv(buf, index=False)
        st.download_button("⬇ Export CSV", buf.getvalue(), f"affiliate_programs_{TODAY}.csv", "text/csv", use_container_width=True)

    st.dataframe(
        filtered_sorted,
        use_container_width=True,
        height=500,
        column_config={
            "Name": st.column_config.TextColumn("Program Name", width="medium"),
            "Date Detected": st.column_config.DateColumn("Detected", format="DD MMM YYYY"),
            "Commission": st.column_config.TextColumn("Commission"),
            "Affiliate URL": st.column_config.TextColumn("URL"),
            "Notes": st.column_config.TextColumn("Notes", width="large"),
        },
        hide_index=True,
    )

    # Sources
    st.markdown('<div class="section-title">Monitoring Sources</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(MONITORING_SOURCES), use_container_width=True, hide_index=True, height=320)

    # Alerts
    st.markdown('<div class="section-title">Alert Examples</div>', unsafe_allow_html=True)
    a1,a2,a3 = st.columns(3)
    with a1:
        st.markdown("""
        <div class="alert-card new">
          <div class="alert-title">🟣 New Program Detected</div>
          <div class="alert-row"><strong>Program:</strong> SpinBet Affiliates</div>
          <div class="alert-row"><strong>Source:</strong> SBC News &nbsp;|&nbsp; <strong>GEO:</strong> EU, UA</div>
          <div class="alert-row"><strong>Commission:</strong> RevShare 45%</div>
          <div class="alert-row"><strong>Reason:</strong> New program. High RevShare. No track record.</div>
          <div class="alert-action new">→ Affiliate Manager to verify within 24h</div>
        </div>""", unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class="alert-card verify">
          <div class="alert-title">🟡 License Verification Required</div>
          <div class="alert-row"><strong>Program:</strong> LuckyNova Partners</div>
          <div class="alert-row"><strong>Source:</strong> Reddit &nbsp;|&nbsp; <strong>GEO:</strong> UA, EU</div>
          <div class="alert-row"><strong>License:</strong> Unknown</div>
          <div class="alert-row"><strong>Reason:</strong> Delayed payment reports. License unconfirmed.</div>
          <div class="alert-action verify">→ Verify licensing before engagement</div>
        </div>""", unsafe_allow_html=True)
    with a3:
        st.markdown("""
        <div class="alert-card risk">
          <div class="alert-title">🔴 Reputation Risk Flagged</div>
          <div class="alert-row"><strong>Program:</strong> Fortune Affiliates</div>
          <div class="alert-row"><strong>Source:</strong> Affiliate Guard Dog</div>
          <div class="alert-row"><strong>License:</strong> MGA</div>
          <div class="alert-row"><strong>Reason:</strong> Slow payment pattern over 3 months.</div>
          <div class="alert-action risk">→ Do not onboard until confirmed</div>
        </div>""", unsafe_allow_html=True)

    # Next steps
    st.markdown('<div class="section-title">Next Steps — Scaling the MVP</div>', unsafe_allow_html=True)
    steps = [
        ("01","Connect real scrapers / APIs","Apify or ParseHub for AffPapa, GPWA, SBC News. WhoisXML for new domains."),
        ("02","Add deduplication logic","Prevent same program appearing from multiple sources. Match by name + URL."),
        ("03","Set up scheduled scans","Automate daily scan at 09:00 via cron job or Make.com workflow."),
        ("04","Assign business owner","Affiliate Manager or SEO Head owns weekly verification process."),
        ("05","Add Slack / email notifications","Trigger alerts to #affiliate-monitoring on every new detection."),
        ("06","Build weekly digest for CEO","Auto-generate Monday morning summary. See Weekly CEO Digest tab."),
    ]
    sc1,sc2 = st.columns(2)
    for i,(num,title,desc) in enumerate(steps):
        with (sc1 if i%2==0 else sc2):
            st.markdown(f"""
            <div class="step-item">
              <div class="step-num">{num}</div>
              <div>
                <div class="step-body-title">{title}</div>
                <div class="step-body-desc">{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 2 — WEEKLY CEO DIGEST
# ════════════════════════════════════════════════════════════
with tab2:
    df = st.session_state.programs
    week_ago_str = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")

    new_this_week_df = df[df["Date Detected"] >= week_ago_str].copy()
    top5 = new_this_week_df.sort_values("Date Detected", ascending=False).head(5)
    risks = df[(df["Status"] == "To Verify") & (df["Priority"] == "High")].head(3)
    verified_this_week = new_this_week_df[new_this_week_df["Status"] == "Verified"]

    st.markdown(f"""
    <div class="digest-header">
      <div class="digest-title">📋 Weekly CEO Digest</div>
      <div class="digest-sub">Week of {(TODAY_DT - timedelta(days=6)).strftime('%d %b')} — {TODAY_DT.strftime('%d %b %Y')} &nbsp;·&nbsp; Auto-generated by PP Monitor</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:14px 20px; margin-bottom:20px; display:flex; gap:40px; align-items:center;">
      <div><span style="font-size:22px; font-weight:700; color:#15803d;">~15h</span><br><span style="font-size:12px; color:#166534;">Manual research avoided this week</span></div>
      <div><span style="font-size:22px; font-weight:700; color:#15803d;">{len(df)}</span><br><span style="font-size:12px; color:#166534;">Programs reviewed automatically</span></div>
      <div><span style="font-size:22px; font-weight:700; color:#15803d;">{len(MONITORING_SOURCES)}</span><br><span style="font-size:12px; color:#166534;">Sources monitored continuously</span></div>
      <div><span style="font-size:22px; font-weight:700; color:#15803d;">{len(new_this_week_df)}</span><br><span style="font-size:12px; color:#166534;">New programs detected this week</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Summary metrics
    d1,d2,d3,d4 = st.columns(4)
    d1.metric("New Programs This Week", len(new_this_week_df))
    d2.metric("High Priority — To Verify", len(risks))
    d3.metric("Verified This Week", len(verified_this_week))
    d4.metric("Sources Active", len(MONITORING_SOURCES))

    st.markdown("<br>", unsafe_allow_html=True)

    # Top 5
    st.markdown('<div class="section-title">Top 5 New Programs This Week</div>', unsafe_allow_html=True)
    if len(top5) == 0:
        st.info("No new programs detected this week. Run a scan to populate.")
    else:
        for _, row in top5.iterrows():
            st.markdown(f"""
            <div class="digest-card">
              <div class="digest-card-title">{row['Name']}</div>
              <div class="digest-row"><strong>Source:</strong> {row['Source']} &nbsp;|&nbsp; <strong>GEO:</strong> {row['GEO']} &nbsp;|&nbsp; <strong>Commission:</strong> {row['Commission']}</div>
              <div class="digest-row"><strong>License:</strong> {row['License']} &nbsp;|&nbsp; <strong>Status:</strong> {row['Status']} &nbsp;|&nbsp; <strong>Priority:</strong> {row['Priority']}</div>
              <div class="digest-row" style="margin-top:6px; color:#374151;"><strong>Notes:</strong> {row['Notes']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Risks
    st.markdown('<div class="section-title">Risks This Week</div>', unsafe_allow_html=True)
    if len(risks) == 0:
        st.success("No high-priority risks flagged this week.")
    else:
        for _, row in risks.iterrows():
            st.markdown(f"""
            <div class="risk-card">
              ⚠️ <strong>{row['Name']}</strong> — {row['Notes']} &nbsp;|&nbsp; Source: {row['Source']} &nbsp;|&nbsp; License: {row['License']}
            </div>
            """, unsafe_allow_html=True)

    # Recommendations
    st.markdown('<div class="section-title">Recommended Actions</div>', unsafe_allow_html=True)
    recs = [
        f"Affiliate Manager to verify {len(risks)} high-priority programs flagged this week.",
        f"Review {len(new_this_week_df[new_this_week_df['License']=='Unknown'])} programs with unknown license before engagement.",
        "Update verification status in database by Friday 15:00.",
        "Monitor SpinBet Affiliates and LuckyNova — community signals mixed.",
        "Schedule weekly scan every Monday at 09:00 to automate detection.",
    ]
    for rec in recs:
        st.markdown(f'<div class="rec-card">✅ {rec}</div>', unsafe_allow_html=True)

    # Export digest
    st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
    digest_df = pd.concat([
        top5[["Name","Source","GEO","Commission","License","Status","Priority","Notes"]],
    ])
    buf2 = io.StringIO()
    digest_df.to_csv(buf2, index=False)
    st.download_button("⬇ Export Digest CSV", buf2.getvalue(), f"ceo_digest_{TODAY}.csv", "text/csv")


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Prototype MVP. Built to validate monitoring logic before connecting live sources.<br>
  Sources: AffPapa · GPWA · Affiliate Guard Dog · AskGamblers · SBC News · Gambling Insider · Reddit · Trustpilot
</div>
""", unsafe_allow_html=True)
