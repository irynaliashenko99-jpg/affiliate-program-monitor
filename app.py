import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import time
import io
import math

st.set_page_config(
    page_title="Affiliate Intelligence Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}

html,body,[class*="css"],.stApp{
  font-family:'Inter',system-ui,sans-serif!important;
  background:#050505!important;
  color:#FFFFFF!important;
}
[data-testid="stAppViewContainer"]{background:#050505!important;}
[data-testid="stHeader"]{background:#050505!important;border-bottom:1px solid rgba(255,255,255,0.04);}
.block-container{padding:2rem 2.5rem 5rem!important;max-width:1440px!important;}
#MainMenu,footer,[data-testid="stDecoration"],[data-testid="stToolbar"]{display:none!important;visibility:hidden!important;}
section[data-testid="stSidebar"]{display:none!important;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{
  background:#0B0B0B!important;
  border:1px solid rgba(255,255,255,0.05)!important;
  border-radius:10px!important;
  padding:4px!important;
  gap:2px!important;
}
.stTabs [data-baseweb="tab-highlight"]{display:none!important;}
[data-testid="stTabs"] button{
  background:transparent!important;color:#52525B!important;
  border:none!important;border-radius:7px!important;
  font-size:13px!important;font-weight:500!important;
  padding:8px 18px!important;transition:all .2s!important;
}
[data-testid="stTabs"] button[aria-selected="true"]{
  background:rgba(139,92,246,0.12)!important;
  color:#A78BFA!important;
  border:1px solid rgba(139,92,246,0.2)!important;
}
[data-testid="stTabs"] button:hover{color:#FFFFFF!important;background:rgba(255,255,255,0.04)!important;}
[data-testid="stTabsContent"]{padding-top:28px!important;}

/* METRICS */
[data-testid="metric-container"]{
  background:#0B0B0B!important;
  border:1px solid rgba(255,255,255,0.06)!important;
  border-radius:12px!important;padding:18px 20px!important;
}
[data-testid="stMetricLabel"]{color:#52525B!important;font-size:10px!important;font-weight:600!important;text-transform:uppercase;letter-spacing:.1em;}
[data-testid="stMetricValue"]{color:#FFFFFF!important;font-size:26px!important;font-weight:700!important;letter-spacing:-.5px;}
[data-testid="stMetricDelta"]>div{font-size:11px!important;}

/* BUTTONS */
.stButton>button{
  background:linear-gradient(135deg,#7C3AED,#6D28D9)!important;
  color:#FFF!important;border:none!important;border-radius:8px!important;
  padding:10px 22px!important;font-size:13px!important;font-weight:500!important;
  box-shadow:0 0 24px rgba(124,58,237,.25)!important;transition:all .2s!important;
}
.stButton>button:hover{box-shadow:0 0 40px rgba(124,58,237,.45)!important;transform:translateY(-1px)!important;}

/* INPUTS */
[data-testid="stTextInput"] input{
  background:#0B0B0B!important;border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:8px!important;color:#FFF!important;font-size:13px!important;
}
[data-testid="stTextInput"] input:focus{border-color:rgba(139,92,246,.4)!important;}
[data-testid="stTextInput"] input::placeholder{color:#3F3F46!important;}
[data-testid="stSelectbox"]>div>div{
  background:#0B0B0B!important;border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:8px!important;color:#FFF!important;
}

/* DOWNLOAD BUTTON */
[data-testid="stDownloadButton"] button{
  background:rgba(255,255,255,0.04)!important;color:#71717A!important;
  border:1px solid rgba(255,255,255,0.07)!important;border-radius:8px!important;
  font-size:12px!important;box-shadow:none!important;
}
[data-testid="stDownloadButton"] button:hover{background:rgba(255,255,255,0.07)!important;color:#FFF!important;box-shadow:none!important;transform:none!important;}

/* SUCCESS/INFO */
[data-testid="stSuccess"]{background:rgba(34,197,94,.08)!important;border:1px solid rgba(34,197,94,.2)!important;border-radius:10px!important;color:#22C55E!important;}
[data-testid="stInfo"]{background:rgba(139,92,246,.08)!important;border:1px solid rgba(139,92,246,.2)!important;border-radius:10px!important;}

/* SECTION DIVIDER */
.sec{font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;
  margin:40px 0 18px;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.04);
  display:flex;align-items:center;gap:8px;}
.sec::before{content:'';display:inline-block;width:2px;height:11px;background:#7C3AED;border-radius:2px;}

hr{border-color:rgba(255,255,255,0.05)!important;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# DATA
# ══════════════════════════════════════════
PROGRAM_NAMES = [
    "Bet365 Partners","888 Affiliates","LeoVegas Affiliates","Income Access Network",
    "Rizk Partners","Stake Affiliates","PlayAmo Partners","Fortune Affiliates",
    "Betsson Group Affiliates","22Bet Partners","Betwinner Affiliates","Coldbet Partners",
    "FoxSlots Partners","Rocketpot Affiliates","Bwin Affiliates","William Hill Partners",
    "Unibet Affiliates","PokerStars Affiliates","Betway Partners","Mr Green Affiliates",
    "Casumo Affiliates","Videoslots Partners","Fastpay Partners","N1 Partners",
    "Wildz Affiliates","Dunder Affiliates","CasinoRoom Partners","Genesis Affiliates",
    "Vera John Affiliates","Guts Affiliates","Betsafe Partners","NordicBet Affiliates",
    "SpinBet Affiliates","MegaSlot Affiliates","CryptoLuck Partners","LuckyNova Partners",
    "GrandWin Affiliates","SilverPlay Partners","Odds96 Partners","C24 Partners",
    "Boomerang Partners","Partners1xbet","Parimatch Partners","Mostbet Affiliates",
    "Melbet Partners","PinUp Partners","1win Affiliates","GGBet Partners",
    "BC.Game Affiliates","BitStarz Partners","FortuneJack Affiliates","BetFury Affiliates",
    "CloudBet Partners","Rollbit Affiliates","JackBit Partners","NineCasino Affiliates",
    "Sportsbet.io Partners","Rabona Affiliates","BetChain Partners","1xSlots Affiliates",
    "Sportaza Affiliates","Haz Casino Partners","20Bet Affiliates","Playfina Affiliates",
    "Legzo Partners","Sol Casino Partners","Cat Casino Partners","Gama Affiliates",
    "JVSpin Affiliates","DrBet Partners","Mystake Partners","Paripesa Affiliates",
    "Betano Affiliates","Novibet Partners","NetBet Partners","BetVictor Affiliates",
    "Betfair Affiliates","Smarkets Partners","Fortuna Partners","Tipsport Affiliates",
    "Tipico Partners","Bettilt Affiliates","Betcris Affiliates","Coolbet Partners",
    "LiveScore Partners","Midnite Affiliates","Rootz Affiliates","MrQ Partners",
    "SpinGenie Affiliates","Jackpotjoy Partners","Virgin Games Affiliates","Pinnacle Affiliates",
    "1xBet Partners","Parimatch UA Partners","Favbet Affiliates","Vbet Partners",
    "BetMGM Affiliates","DraftKings Partners","FanDuel Affiliates","Caesars Affiliates",
    "PointsBet Partners","ESPN Bet Affiliates","Betclic Partners","Winamax Affiliates",
    "Better Collective Affiliates","Catena Media Partners","Raketech Affiliates","CasinoGuru Partners",
    "Hacksaw Gaming Partners","Push Gaming Affiliates","Evolution Partners","Playtech Affiliates",
    "Pragmatic Partners","NetEnt Affiliates","Red Tiger Affiliates","BGaming Affiliates",
    "Spinomenal Partners","KA Gaming Affiliates","Gamomat Partners","Wazdan Affiliates",
    "Betsoft Partners","PG Soft Affiliates","Spadegaming Partners","1spin4win Affiliates",
]

SOURCES_LIST = ["AffPapa","GPWA","Affiliate Guard Dog","AskGamblers","SBC News","Gambling Insider","Reddit","Trustpilot"]
GEO_LIST = ["EU","UK","CA","AU","US","SE","DE","FI","NO","UA","CIS","LATAM","APAC","Tier 1","Worldwide"]
LICENSE_LIST = ["MGA","UKGC","Curaçao","Gibraltar","Isle of Man","Kahnawake","Unknown"]
STATUS_W = ["New","New","To Verify","To Verify","Verified","Verified","Verified","Verified","Verified","Rejected"]
PRIORITY_L = ["High","High","Medium","Medium","Low"]
COMMISSION_L = ["RevShare 25-40%","RevShare 30-45%","CPA $50-150","CPA $100-200","Hybrid","RevShare 20-35%","RevShare 35-50%"]
NOTES_L = [
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
    "Pending license renewal.",
    "Top performer in Nordics.",
    "New management. Quality unclear.",
    "Strong affiliate community feedback.",
]
TODAY = "2026-06-12"
TODAY_DT = datetime(2026, 6, 12)

def risk_score(row):
    s = 10
    if row["License"] == "Unknown": s += 40
    if row["License"] == "Curaçao": s += 15
    if row["Status"] == "Rejected": s += 35
    if row["Status"] == "To Verify": s += 20
    if "late payment" in row["Notes"].lower() or "risk" in row["Notes"].lower(): s += 20
    if row["Priority"] == "High" and row["Status"] == "To Verify": s += 10
    return min(s, 99)

def opp_score(row):
    s = 30
    if row["Priority"] == "High": s += 30
    if row["Status"] == "Verified": s += 25
    if "Tier 1" in row["GEO"] or "Worldwide" in row["GEO"]: s += 10
    if "RevShare" in row["Commission"] and "45" in row["Commission"]: s += 8
    if "stable" in row["Notes"].lower() or "recommended" in row["Notes"].lower(): s += 10
    if row["Status"] == "New" and row["Priority"] == "High": s += 5
    return min(s, 99)

def generate_programs(n=500):
    random.seed(42)
    names = (PROGRAM_NAMES * ((n // len(PROGRAM_NAMES)) + 2))[:n]
    rows = []
    for i, name in enumerate(names):
        if i < 8: days_ago = 0
        elif i < 30: days_ago = random.randint(1, 7)
        else: days_ago = random.randint(1, 90)
        detected = (TODAY_DT - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        status = random.choice(STATUS_W)
        if days_ago == 0: status = "New"
        elif days_ago <= 7: status = random.choice(["New","To Verify"])
        geo = ", ".join(random.sample(GEO_LIST, random.randint(1,3)))
        license_ = random.choice(LICENSE_LIST)
        commission = random.choice(COMMISSION_L)
        notes = random.choice(NOTES_L)
        row = {
            "Name": name, "Date Detected": detected,
            "Source": random.choice(SOURCES_LIST), "GEO": geo,
            "License": license_, "Commission": commission,
            "Affiliate URL": name.lower().replace(" ","").replace("'","").replace("&","and")+".com/affiliates",
            "Status": status, "Priority": random.choice(PRIORITY_L), "Notes": notes,
        }
        row["Risk Score"] = risk_score(row)
        row["Opp Score"] = opp_score(row)
        rows.append(row)
    return pd.DataFrame(rows)

NEW_POOL = [
    {"Name":"SpinBet Affiliates","Source":"SBC News","GEO":"EU, UA","License":"Curaçao","Commission":"RevShare 45%","Affiliate URL":"spinbet-affiliates.com/affiliates","Status":"New","Priority":"High","Notes":"High RevShare. No track record yet."},
    {"Name":"LuckyNova Partners","Source":"Reddit","GEO":"UA, EU","License":"Unknown","Commission":"CPA $120","Affiliate URL":"luckynova.io/affiliates","Status":"To Verify","Priority":"High","Notes":"License unconfirmed. Verify before engagement."},
    {"Name":"NovaSpin Affiliates","Source":"Affiliate Guard Dog","GEO":"EU","License":"MGA","Commission":"RevShare 35%","Affiliate URL":"novaspin.com/affiliates","Status":"New","Priority":"High","Notes":"Early detection. Solid MGA license."},
    {"Name":"StarNet Affiliates","Source":"SBC News","GEO":"Tier 1","License":"MGA","Commission":"RevShare 30-45%","Affiliate URL":"starnet.com/partners","Status":"New","Priority":"High","Notes":"Announced at SBC Summit. Strong team."},
    {"Name":"BetRocket Partners","Source":"AffPapa","GEO":"EU, CA","License":"Curaçao","Commission":"CPA $150","Affiliate URL":"betrocket.io/affiliates","Status":"To Verify","Priority":"Medium","Notes":"New CPA-focused program. Terms unclear."},
    {"Name":"CryptoNova Partners","Source":"GPWA","GEO":"Worldwide","License":"Unknown","Commission":"RevShare 30%","Affiliate URL":"cryptonova.gg/affiliates","Status":"To Verify","Priority":"Medium","Notes":"Crypto-native. Community buzz. License unclear."},
]

MONITORING_SOURCES_DATA = [
    {"name":"AffPapa","type":"Affiliate Directory","found_week":12,"reliability":94,"last":"Today 09:00","status":"Active"},
    {"name":"GPWA","type":"Affiliate Forum","found_week":7,"reliability":89,"last":"Today 09:01","status":"Active"},
    {"name":"Affiliate Guard Dog","type":"Watchdog Forum","found_week":5,"reliability":92,"last":"Today 09:02","status":"Active"},
    {"name":"AskGamblers","type":"Review Platform","found_week":9,"reliability":87,"last":"Today 09:03","status":"Active"},
    {"name":"SBC News","type":"Industry News","found_week":11,"reliability":96,"last":"Today 09:04","status":"Active"},
    {"name":"Gambling Insider","type":"Industry News","found_week":6,"reliability":91,"last":"Today 09:05","status":"Active"},
    {"name":"Reddit","type":"Community Forum","found_week":8,"reliability":72,"last":"Today 09:06","status":"Active"},
    {"name":"Trustpilot","type":"Review Platform","found_week":3,"reliability":83,"last":"Jun 09","status":"Active"},
]

if "programs" not in st.session_state:
    st.session_state.programs = generate_programs(500)
    for p in NEW_POOL:
        p["Risk Score"] = risk_score({"License":p["License"],"Status":p["Status"],"Notes":p["Notes"],"Priority":p["Priority"],"GEO":p["GEO"],"Commission":p["Commission"]})
        p["Opp Score"] = opp_score({"Priority":p["Priority"],"Status":p["Status"],"GEO":p["GEO"],"Commission":p["Commission"],"Notes":p["Notes"]})
if "scan_log" not in st.session_state: st.session_state.scan_log = []
if "last_scan" not in st.session_state: st.session_state.last_scan = None
if "db_page" not in st.session_state: st.session_state.db_page = 0


# ══════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════
def status_badge(s):
    M = {
        "New":       ("rgba(139,92,246,.15)","#A78BFA","rgba(139,92,246,.25)"),
        "To Verify": ("rgba(245,158,11,.12)","#F59E0B","rgba(245,158,11,.2)"),
        "Verified":  ("rgba(34,197,94,.1)","#22C55E","rgba(34,197,94,.2)"),
        "Rejected":  ("rgba(239,68,68,.1)","#EF4444","rgba(239,68,68,.2)"),
    }
    bg,col,bdr = M.get(s, M["New"])
    return f'<span style="display:inline-block;font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;background:{bg};color:{col};border:1px solid {bdr};letter-spacing:.04em;">{s.upper()}</span>'

def risk_badge(score):
    if score >= 70: return f'<span style="color:#EF4444;font-weight:700;font-size:13px;">{score}<span style="color:#52525B;font-size:10px;font-weight:400;">/100</span></span>'
    if score >= 40: return f'<span style="color:#F59E0B;font-weight:700;font-size:13px;">{score}<span style="color:#52525B;font-size:10px;font-weight:400;">/100</span></span>'
    return f'<span style="color:#22C55E;font-weight:700;font-size:13px;">{score}<span style="color:#52525B;font-size:10px;font-weight:400;">/100</span></span>'

def opp_badge(score):
    if score >= 70: return f'<span style="color:#22C55E;font-weight:700;font-size:13px;">{score}<span style="color:#52525B;font-size:10px;font-weight:400;">/100</span></span>'
    if score >= 40: return f'<span style="color:#F59E0B;font-weight:700;font-size:13px;">{score}<span style="color:#52525B;font-size:10px;font-weight:400;">/100</span></span>'
    return f'<span style="color:#71717A;font-weight:700;font-size:13px;">{score}<span style="color:#52525B;font-size:10px;font-weight:400;">/100</span></span>'


# ══════════════════════════════════════════
# HERO
# ══════════════════════════════════════════
df = st.session_state.programs
week_ago = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
total = len(df)
new_wk = len(df[df["Date Detected"] >= week_ago])
today_n = len(df[df["Date Detected"] == TODAY])
to_verify = len(df[df["Status"] == "To Verify"])
verified = len(df[df["Status"] == "Verified"])
rejected = len(df[df["Status"] == "Rejected"])
high_risk = len(df[(df["Risk Score"] >= 70)])
opportunities = len(df[(df["Opp Score"] >= 70) & (df["Status"].isin(["New","To Verify"]))])
hours_saved = round(total * 0.06)
last_scan_txt = st.session_state.last_scan.strftime("%d %b %Y, %H:%M") if st.session_state.last_scan else "12 Jun 2026, 09:00"

st.markdown(f"""
<div style="background:linear-gradient(135deg,#0B0B0B 0%,#0D0B14 100%);
  border:1px solid rgba(139,92,246,0.12);border-radius:20px;
  padding:40px 48px;margin-bottom:32px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-80px;right:-80px;width:300px;height:300px;
    background:radial-gradient(circle,rgba(124,58,237,0.08) 0%,transparent 70%);pointer-events:none;"></div>
  <div style="position:absolute;bottom:-60px;left:200px;width:200px;height:200px;
    background:radial-gradient(circle,rgba(139,92,246,0.04) 0%,transparent 70%);pointer-events:none;"></div>

  <div style="display:flex;justify-content:space-between;align-items:flex-start;">
    <div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
        color:#7C3AED;margin-bottom:12px;">◈ AFFILIATE INTELLIGENCE PLATFORM</div>
      <div style="font-size:32px;font-weight:800;letter-spacing:-1px;color:#FFFFFF;margin-bottom:8px;
        background:linear-gradient(135deg,#FFFFFF 0%,#A78BFA 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        Real-time iGaming<br>Intelligence Dashboard</div>
      <div style="font-size:14px;color:#52525B;margin-top:8px;">
        Monitoring affiliate programs across the iGaming ecosystem</div>
    </div>
    <div style="text-align:right;">
      <div style="display:inline-flex;align-items:center;gap:7px;
        background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.2);
        border-radius:20px;padding:6px 14px;font-size:12px;font-weight:700;color:#22C55E;margin-bottom:8px;">
        <span style="width:7px;height:7px;border-radius:50%;background:#22C55E;
          box-shadow:0 0 8px #22C55E;display:inline-block;animation:none;"></span> LIVE
      </div>
      <div style="font-size:11px;color:#3F3F46;">Last scan: {last_scan_txt}</div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:32px;">
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
      border-radius:12px;padding:16px 20px;">
      <div style="font-size:28px;font-weight:800;color:#FFFFFF;letter-spacing:-1px;">{total}</div>
      <div style="font-size:11px;color:#52525B;margin-top:2px;text-transform:uppercase;letter-spacing:.06em;">Tracked programs</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
      border-radius:12px;padding:16px 20px;">
      <div style="font-size:28px;font-weight:800;color:#A78BFA;letter-spacing:-1px;">{new_wk}</div>
      <div style="font-size:11px;color:#52525B;margin-top:2px;text-transform:uppercase;letter-spacing:.06em;">New this week</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
      border-radius:12px;padding:16px 20px;">
      <div style="font-size:28px;font-weight:800;color:#22C55E;letter-spacing:-1px;">{opportunities}</div>
      <div style="font-size:11px;color:#52525B;margin-top:2px;text-transform:uppercase;letter-spacing:.06em;">Recommended opportunities</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
      border-radius:12px;padding:16px 20px;">
      <div style="font-size:28px;font-weight:800;color:#EF4444;letter-spacing:-1px;">{high_risk}</div>
      <div style="font-size:11px;color:#52525B;margin-top:2px;text-transform:uppercase;letter-spacing:.06em;">Critical risks flagged</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# TABS
# ══════════════════════════════════════════
tab1, tab2 = st.tabs(["◈  Intelligence Feed", "◈  Weekly CEO Digest"])


# ══════════════════════════════════════════════════════════
# TAB 1
# ══════════════════════════════════════════════════════════
with tab1:

    # EXECUTIVE SUMMARY CARDS
    st.markdown('<div class="sec">Executive Summary</div>', unsafe_allow_html=True)
    e1,e2,e3,e4 = st.columns(4)

    def exec_card(col, icon, val, val_color, label, sub, trend_label, trend_color, glow_color):
        col.markdown(f"""
        <div style="background:#0B0B0B;border:1px solid rgba(255,255,255,0.06);border-radius:14px;
          padding:24px;position:relative;overflow:hidden;transition:all .2s;
          box-shadow:0 0 0 0 {glow_color};">
          <div style="position:absolute;top:0;right:0;width:80px;height:80px;
            background:radial-gradient(circle,{glow_color} 0%,transparent 70%);opacity:.4;pointer-events:none;"></div>
          <div style="font-size:22px;margin-bottom:14px;">{icon}</div>
          <div style="font-size:38px;font-weight:800;color:{val_color};letter-spacing:-1.5px;margin-bottom:6px;">{val}</div>
          <div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:4px;">{label}</div>
          <div style="font-size:12px;color:#52525B;">{sub}</div>
          <div style="position:absolute;top:20px;right:18px;font-size:10px;font-weight:700;
            padding:3px 8px;border-radius:5px;background:rgba(255,255,255,0.05);color:{trend_color};">{trend_label}</div>
        </div>""", unsafe_allow_html=True)

    exec_card(e1,"🟢",opportunities,"#22C55E","Opportunities Detected","Programs worth review this week","↑ This week","#22C55E","rgba(34,197,94,0.1)")
    exec_card(e2,"🟡",to_verify,"#F59E0B","Requires Verification","Missing license information","Action needed","#F59E0B","rgba(245,158,11,0.1)")
    exec_card(e3,"🔴",high_risk,"#EF4444","Risk Alerts","Potential reputation issues","Critical","#EF4444","rgba(239,68,68,0.1)")
    exec_card(e4,"⚡",f"{hours_saved}h","#A78BFA","Research Hours Saved","Avoided manual work this week","Automated","#A78BFA","rgba(139,92,246,0.1)")

    # RECOMMENDED ACTIONS
    st.markdown('<div class="sec">Recommended Actions</div>', unsafe_allow_html=True)

    top_opps = df[(df["Opp Score"] >= 65) & (df["Status"].isin(["New","To Verify"]))].sort_values("Opp Score", ascending=False).head(6)

    if len(top_opps) > 0:
        cols = st.columns(3)
        for i, (_, row) in enumerate(top_opps.iterrows()):
            with cols[i % 3]:
                opp = row["Opp Score"]
                risk = row["Risk Score"]
                urgency = "Review within 24h" if row["Priority"] == "High" else "Review this week"
                urgency_color = "#EF4444" if row["Priority"] == "High" else "#F59E0B"
                geos = row["GEO"].split(", ")[:2]
                geo_chips = "".join([f'<span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(255,255,255,0.05);color:#71717A;margin-right:4px;">{g}</span>' for g in geos])

                st.markdown(f"""
                <div style="background:#0B0B0B;border:1px solid rgba(255,255,255,0.07);border-radius:14px;
                  padding:22px;margin-bottom:12px;position:relative;overflow:hidden;
                  border-top:2px solid rgba(139,92,246,0.4);">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">
                    <div>
                      <div style="font-size:15px;font-weight:700;color:#FFFFFF;margin-bottom:4px;">{row['Name']}</div>
                      <div style="font-size:11px;color:#52525B;">{row['Source']} · {row['Date Detected']}</div>
                    </div>
                    {status_badge(row['Status'])}
                  </div>
                  <div style="margin-bottom:14px;">{geo_chips}
                    <span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(255,255,255,0.05);color:#71717A;">{row['License']}</span>
                  </div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">
                    <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:10px 12px;">
                      <div style="font-size:9px;color:#3F3F46;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Opportunity</div>
                      {opp_badge(opp)}
                    </div>
                    <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:10px 12px;">
                      <div style="font-size:9px;color:#3F3F46;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Risk</div>
                      {risk_badge(risk)}
                    </div>
                  </div>
                  <div style="font-size:12px;color:#52525B;margin-bottom:12px;">{row['Commission']}</div>
                  <div style="font-size:11px;font-weight:600;color:{urgency_color};
                    background:rgba(255,255,255,0.03);border-radius:6px;padding:8px 12px;text-align:center;">
                    → {urgency}
                  </div>
                </div>""", unsafe_allow_html=True)

    # SCAN ENGINE
    st.markdown('<div class="sec">Monitoring Engine</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#0B0B0B;border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:24px 28px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div>
          <div style="font-size:15px;font-weight:600;color:#FFFFFF;margin-bottom:4px;">Automated Intelligence Scan</div>
          <div style="font-size:13px;color:#52525B;">Crawls 8 sources. Flags new affiliate programs and reputation risks in real time.</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns([1,2,1])
    with sc1:
        run_scan = st.button("◈  Run New Scan", use_container_width=True)

    if run_scan:
        pb = st.progress(0, text="Initializing...")
        srcs = ["AffPapa","GPWA","SBC News","Affiliate Guard Dog","AskGamblers","Trustpilot","Reddit","Gambling Insider"]
        for i, s in enumerate(srcs):
            time.sleep(0.25)
            pb.progress((i+1)/len(srcs), text=f"Scanning {s}...")
        time.sleep(0.2)
        pb.empty()

        existing = set(st.session_state.programs["Name"].tolist())
        avail = [p for p in NEW_POOL if p["Name"] not in existing] or NEW_POOL
        batch = random.sample(avail, min(random.randint(3,5), len(avail)))
        t = datetime.now()
        new_rows = []
        for p in batch:
            r = {**p, "Date Detected": TODAY}
            r["Risk Score"] = risk_score(r)
            r["Opp Score"] = opp_score(r)
            new_rows.append(r)
        st.session_state.programs = pd.concat([st.session_state.programs, pd.DataFrame(new_rows)], ignore_index=True)
        st.session_state.last_scan = t

        log = [f"[{t.strftime('%H:%M:%S')}] Scan initiated — 8 sources active"]
        for s in srcs:
            log.append(f"[{t.strftime('%H:%M:%S')}]  ↳ {s} — OK")
        for p in batch:
            log.append(f"[{t.strftime('%H:%M:%S')}]  ✓ {p['Name']} via {p['Source']} — {p['Status']}")
        log.append(f"[{t.strftime('%H:%M:%S')}] Scan complete — {len(batch)} programs detected")
        st.session_state.scan_log = log
        st.success(f"✅ Scan complete — {len(batch)} new affiliate programs detected.")
        st.rerun()

    if st.session_state.scan_log:
        st.markdown(f"""
        <div style="background:#030303;border:1px solid rgba(255,255,255,0.05);border-radius:10px;
          padding:16px 18px;margin-top:12px;font-family:'Courier New',monospace;
          font-size:12px;line-height:1.9;color:#22C55E;">
          {"<br>".join(st.session_state.scan_log)}
        </div>""", unsafe_allow_html=True)

    # PROGRAM CARDS VIEW (paginated)
    st.markdown('<div class="sec">Affiliate Programs Database</div>', unsafe_allow_html=True)
    df = st.session_state.programs

    f1,f2,f3,f4,f5 = st.columns(5)
    with f1: srch = st.text_input("Search", placeholder="Program name...")
    with f2: sf = st.selectbox("Status", ["All"] + sorted(df["Status"].unique().tolist()))
    with f3: pf = st.selectbox("Priority", ["All","High","Medium","Low"])
    with f4: srcf = st.selectbox("Source", ["All"] + sorted(df["Source"].unique().tolist()))
    with f5:
        geopts = sorted(set(g.strip() for geos in df["GEO"].str.split(",") for g in geos))
        gf = st.selectbox("GEO", ["All"] + geopts)

    filt = df.copy()
    if srch: filt = filt[filt["Name"].str.contains(srch, case=False, na=False)]
    if sf != "All": filt = filt[filt["Status"] == sf]
    if pf != "All": filt = filt[filt["Priority"] == pf]
    if srcf != "All": filt = filt[filt["Source"] == srcf]
    if gf != "All": filt = filt[filt["GEO"].str.contains(gf, case=False, na=False)]

    filt = filt.sort_values("Date Detected", ascending=False).reset_index(drop=True)
    RPP = 15
    total_pg = max(1, math.ceil(len(filt) / RPP))
    if st.session_state.db_page >= total_pg: st.session_state.db_page = 0

    r1,r2,r3,r4,r5 = st.columns([3,2,1,1,1])
    with r1:
        st.markdown(f"<div style='font-size:13px;color:#52525B;padding:8px 0;'>Showing <strong style='color:#A1A1AA;'>{len(filt)}</strong> of <strong style='color:#A1A1AA;'>{len(df)}</strong> — Page {st.session_state.db_page+1}/{total_pg}</div>", unsafe_allow_html=True)
    with r2:
        buf = io.StringIO(); filt.to_csv(buf, index=False)
        st.download_button("⬇ Export CSV", buf.getvalue(), f"affiliate_{TODAY}.csv", "text/csv", use_container_width=True)
    with r3:
        if st.button("◀", use_container_width=True) and st.session_state.db_page > 0:
            st.session_state.db_page -= 1; st.rerun()
    with r4:
        if st.button("▶", use_container_width=True) and st.session_state.db_page < total_pg - 1:
            st.session_state.db_page += 1; st.rerun()

    page_df = filt.iloc[st.session_state.db_page*RPP:(st.session_state.db_page+1)*RPP]

    # Custom HTML table
    rows_html = ""
    for i, (_, r) in enumerate(page_df.iterrows()):
        zebra = "background:rgba(255,255,255,0.012);" if i % 2 == 1 else ""
        risk_c = "#EF4444" if r["Risk Score"] >= 70 else ("#F59E0B" if r["Risk Score"] >= 40 else "#22C55E")
        opp_c = "#22C55E" if r["Opp Score"] >= 70 else ("#F59E0B" if r["Opp Score"] >= 40 else "#71717A")
        rows_html += f"""
        <tr style="border-bottom:1px solid rgba(255,255,255,0.04);{zebra}transition:background .15s;">
          <td style="padding:13px 16px;color:#FFFFFF;font-weight:500;font-size:13px;">{r['Name']}</td>
          <td style="padding:13px 16px;color:#71717A;font-size:12px;white-space:nowrap;">{r['Date Detected']}</td>
          <td style="padding:13px 16px;color:#71717A;font-size:12px;">{r['Source']}</td>
          <td style="padding:13px 16px;color:#71717A;font-size:12px;">{r['GEO']}</td>
          <td style="padding:13px 16px;color:#71717A;font-size:12px;">{r['License']}</td>
          <td style="padding:13px 16px;color:#71717A;font-size:12px;">{r['Commission']}</td>
          <td style="padding:13px 16px;">{status_badge(r['Status'])}</td>
          <td style="padding:13px 16px;font-size:12px;font-weight:700;color:{opp_c};">{r['Opp Score']}</td>
          <td style="padding:13px 16px;font-size:12px;font-weight:700;color:{risk_c};">{r['Risk Score']}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;border-radius:14px;border:1px solid rgba(255,255,255,0.07);margin-top:8px;">
      <table style="width:100%;border-collapse:collapse;background:#0B0B0B;">
        <thead>
          <tr style="background:#0D0D0D;border-bottom:1px solid rgba(255,255,255,0.07);">
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">Program</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;white-space:nowrap;">Detected</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">Source</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">GEO</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">License</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">Commission</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">Status</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">Opp ↑</th>
            <th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#3F3F46;">Risk ↑</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)

    # MONITORING SOURCES
    st.markdown('<div class="sec">Intelligence Sources</div>', unsafe_allow_html=True)
    sc = st.columns(4)
    for i, s in enumerate(MONITORING_SOURCES_DATA):
        with sc[i % 4]:
            rel = s["reliability"]
            rel_c = "#22C55E" if rel >= 90 else ("#F59E0B" if rel >= 75 else "#EF4444")
            st.markdown(f"""
            <div style="background:#0B0B0B;border:1px solid rgba(255,255,255,0.06);border-radius:12px;
              padding:20px;margin-bottom:12px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                <div style="font-size:14px;font-weight:700;color:#FFFFFF;">{s['name']}</div>
                <span style="font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;
                  background:rgba(34,197,94,0.1);color:#22C55E;border:1px solid rgba(34,197,94,0.2);">ACTIVE</span>
              </div>
              <div style="font-size:11px;color:#3F3F46;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;">{s['type']}</div>
              <div style="font-size:13px;color:#A1A1AA;margin-bottom:4px;">Found this week: <strong style="color:#FFFFFF;">{s['found_week']}</strong></div>
              <div style="font-size:13px;color:#A1A1AA;margin-bottom:4px;">Last scan: <strong style="color:#FFFFFF;">{s['last']}</strong></div>
              <div style="font-size:13px;color:#A1A1AA;margin-bottom:12px;">Reliability: <strong style="color:{rel_c};">{rel}%</strong></div>
              <div style="height:3px;background:rgba(255,255,255,0.05);border-radius:2px;">
                <div style="height:3px;background:{rel_c};border-radius:2px;width:{rel}%;opacity:0.6;"></div>
              </div>
            </div>""", unsafe_allow_html=True)
        if (i+1) % 4 == 0 and i+1 < len(MONITORING_SOURCES_DATA):
            sc = st.columns(4)

    # ALERT CENTER
    st.markdown('<div class="sec">Alert Center</div>', unsafe_allow_html=True)
    al1,al2,al3 = st.columns(3)
    alerts = [
        (al1,"rgba(139,92,246,0.08)","rgba(139,92,246,0.25)","rgba(139,92,246,0.4)","🟣","New Program Detected",
         "SpinBet Affiliates","SBC News","EU, UA","Curaçao","RevShare 45%",
         "New program. High RevShare with no established track record. Rapid growth signal.",
         "→ Affiliate Manager to verify terms and license within 24h","#A78BFA"),
        (al2,"rgba(245,158,11,0.06)","rgba(245,158,11,0.2)","rgba(245,158,11,0.35)","🟡","License Verification Required",
         "LuckyNova Partners","Reddit","UA, EU","Unknown","CPA $120",
         "Community reporting delayed payments. License cannot be confirmed from public sources.",
         "→ Verify licensing information before any engagement","#F59E0B"),
        (al3,"rgba(239,68,68,0.06)","rgba(239,68,68,0.2)","rgba(239,68,68,0.35)","🔴","Reputation Risk Flagged",
         "Fortune Affiliates","Affiliate Guard Dog","Worldwide","MGA","RevShare 25-40%",
         "Consistent slow payment pattern reported over 3 consecutive months in affiliate community.",
         "→ Do not onboard until reputation fully confirmed","#EF4444"),
    ]
    for col, bg, bdr, left_c, icon, title, prog, src, geo, lic, comm, reason, action, action_c in alerts:
        with col:
            col.markdown(f"""
            <div style="background:{bg};border:1px solid {bdr};border-left:4px solid {left_c};
              border-radius:12px;padding:22px;margin-bottom:8px;">
              <div style="font-size:18px;margin-bottom:10px;">{icon}</div>
              <div style="font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:12px;">{title}</div>
              <div style="font-size:13px;color:#71717A;margin-bottom:3px;"><strong style="color:#A1A1AA;">Program:</strong> {prog}</div>
              <div style="font-size:13px;color:#71717A;margin-bottom:3px;"><strong style="color:#A1A1AA;">Source:</strong> {src} &nbsp;|&nbsp; <strong style="color:#A1A1AA;">GEO:</strong> {geo}</div>
              <div style="font-size:13px;color:#71717A;margin-bottom:3px;"><strong style="color:#A1A1AA;">License:</strong> {lic} &nbsp;|&nbsp; <strong style="color:#A1A1AA;">Commission:</strong> {comm}</div>
              <div style="font-size:12px;color:#52525B;margin:12px 0;padding:10px 12px;
                background:rgba(255,255,255,0.03);border-radius:6px;">{reason}</div>
              <div style="font-size:12px;font-weight:600;color:{action_c};
                border-top:1px solid rgba(255,255,255,0.05);padding-top:12px;">{action}</div>
            </div>""", unsafe_allow_html=True)

    # NEXT STEPS
    st.markdown('<div class="sec">Scaling to Production</div>', unsafe_allow_html=True)
    steps = [
        ("01","Connect live scrapers","Apify for AffPapa, GPWA, SBC News. WhoisXML for new domain detection."),
        ("02","Deduplication layer","Prevent same program from multiple sources. Match by name + URL fingerprint."),
        ("03","Scheduled scans","Daily 09:00 via cron or Make.com. Zero manual triggers."),
        ("04","Assign business owner","Affiliate Manager owns verification. SLA: 48h per new program."),
        ("05","Slack / email alerts","Real-time push to #affiliate-intel on every High Priority detection."),
        ("06","Automated CEO Digest","Monday 09:00 auto-generated report. See CEO Digest tab."),
    ]
    ns1,ns2 = st.columns(2)
    for i,(n,t,d) in enumerate(steps):
        with (ns1 if i%2==0 else ns2):
            st.markdown(f"""
            <div style="background:#0B0B0B;border:1px solid rgba(255,255,255,0.06);border-radius:10px;
              padding:16px 20px;margin-bottom:8px;display:flex;align-items:flex-start;gap:14px;">
              <div style="background:rgba(139,92,246,0.12);color:#A78BFA;font-weight:700;font-size:11px;
                padding:4px 9px;border-radius:5px;min-width:32px;text-align:center;">{n}</div>
              <div>
                <div style="font-weight:600;color:#FFFFFF;font-size:13px;margin-bottom:3px;">{t}</div>
                <div style="font-size:12px;color:#52525B;">{d}</div>
              </div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 2 — CEO DIGEST
# ══════════════════════════════════════════════════════════
with tab2:
    df = st.session_state.programs
    wk = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
    new_wk_df = df[df["Date Detected"] >= wk].copy()
    top5 = new_wk_df.sort_values("Opp Score", ascending=False).head(5)
    risks_df = df[(df["Risk Score"] >= 70)].sort_values("Risk Score", ascending=False).head(5)
    verified_wk = new_wk_df[new_wk_df["Status"] == "Verified"]
    unk_lic = len(df[df["License"] == "Unknown"])

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0B0B0B,#0D0B14);
      border:1px solid rgba(139,92,246,0.15);border-radius:18px;padding:36px 40px;margin-bottom:28px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
        color:#7C3AED;margin-bottom:12px;">EXECUTIVE REPORT</div>
      <div style="font-size:26px;font-weight:800;color:#FFFFFF;letter-spacing:-.5px;margin-bottom:6px;">
        Weekly CEO Digest</div>
      <div style="font-size:13px;color:#52525B;">
        Week of {(TODAY_DT-timedelta(days=6)).strftime('%d %b')} — {TODAY_DT.strftime('%d %b %Y')} &nbsp;·&nbsp; Auto-generated by Affiliate Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:rgba(34,197,94,0.05);border:1px solid rgba(34,197,94,0.12);
      border-radius:14px;padding:22px 28px;display:flex;gap:48px;align-items:center;margin-bottom:28px;">
      <div><div style="font-size:32px;font-weight:800;color:#22C55E;letter-spacing:-1px;">~15h</div>
        <div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.08em;margin-top:2px;">Manual research avoided</div></div>
      <div><div style="font-size:32px;font-weight:800;color:#22C55E;letter-spacing:-1px;">{len(df)}</div>
        <div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.08em;margin-top:2px;">Programs reviewed automatically</div></div>
      <div><div style="font-size:32px;font-weight:800;color:#22C55E;letter-spacing:-1px;">{len(new_wk_df)}</div>
        <div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.08em;margin-top:2px;">New programs this week</div></div>
      <div><div style="font-size:32px;font-weight:800;color:#22C55E;letter-spacing:-1px;">{len(risks_df)}</div>
        <div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.08em;margin-top:2px;">Risk flags requiring action</div></div>
    </div>
    """, unsafe_allow_html=True)

    dc1,dc2,dc3,dc4 = st.columns(4)
    dc1.metric("New This Week", len(new_wk_df))
    dc2.metric("High Risk Flags", len(risks_df))
    dc3.metric("Verified This Week", len(verified_wk))
    dc4.metric("Unknown License", unk_lic)

    st.markdown("<br>", unsafe_allow_html=True)

    dg1, dg2 = st.columns([3,2])

    with dg1:
        st.markdown('<div class="sec">Top Opportunities This Week</div>', unsafe_allow_html=True)
        if len(top5) == 0:
            st.info("No programs detected this week. Run a scan.")
        else:
            for _, row in top5.iterrows():
                opp = row["Opp Score"]
                risk = row["Risk Score"]
                opp_c = "#22C55E" if opp >= 70 else "#F59E0B"
                risk_c = "#EF4444" if risk >= 70 else ("#F59E0B" if risk >= 40 else "#22C55E")
                st.markdown(f"""
                <div style="background:#0B0B0B;border:1px solid rgba(255,255,255,0.06);
                  border-radius:12px;padding:18px 20px;margin-bottom:10px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <div style="font-size:14px;font-weight:700;color:#FFFFFF;">{row['Name']}</div>
                    {status_badge(row['Status'])}
                  </div>
                  <div style="font-size:12px;color:#52525B;margin-bottom:8px;">
                    {row['Source']} · {row['GEO']} · {row['Commission']}
                  </div>
                  <div style="display:flex;gap:16px;">
                    <span style="font-size:12px;color:{opp_c};">Opp: <strong>{opp}/100</strong></span>
                    <span style="font-size:12px;color:{risk_c};">Risk: <strong>{risk}/100</strong></span>
                    <span style="font-size:12px;color:#52525B;">{row['License']}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    with dg2:
        st.markdown('<div class="sec">Risk Flags</div>', unsafe_allow_html=True)
        if len(risks_df) == 0:
            st.success("No critical risks this week.")
        else:
            for _, row in risks_df.iterrows():
                st.markdown(f"""
                <div style="background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.15);
                  border-left:3px solid #EF4444;border-radius:10px;padding:14px 16px;margin-bottom:8px;">
                  <div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:4px;">{row['Name']}</div>
                  <div style="font-size:12px;color:#71717A;">{row['Notes']}</div>
                  <div style="font-size:11px;color:#EF4444;margin-top:6px;font-weight:600;">Risk Score: {row['Risk Score']}/100</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec">Recommended Actions</div>', unsafe_allow_html=True)
        recs = [
            f"Verify {len(risks_df)} high-risk programs before engagement.",
            f"Review {unk_lic} programs with unknown license.",
            "Update all verification statuses by Friday 15:00.",
            "Run next scan Monday 09:00 to refresh intelligence.",
            "Assign Affiliate Manager as process owner.",
        ]
        for rec in recs:
            st.markdown(f"""
            <div style="background:rgba(34,197,94,0.04);border:1px solid rgba(34,197,94,0.1);
              border-radius:8px;padding:12px 16px;margin-bottom:6px;font-size:13px;color:#86EFAC;">
              ✅ {rec}
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec">Export</div>', unsafe_allow_html=True)
    ex1,ex2 = st.columns(2)
    with ex1:
        b1 = io.StringIO(); top5.to_csv(b1, index=False)
        st.download_button("⬇ Export Top Opportunities", b1.getvalue(), f"opportunities_{TODAY}.csv", "text/csv", use_container_width=True)
    with ex2:
        b2 = io.StringIO(); risks_df.to_csv(b2, index=False)
        st.download_button("⬇ Export Risk Flags", b2.getvalue(), f"risks_{TODAY}.csv", "text/csv", use_container_width=True)


# FOOTER
st.markdown(f"""
<div style="margin-top:60px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.04);
  display:flex;justify-content:space-between;align-items:center;">
  <div style="font-size:12px;color:#27272A;">© 2026 Affiliate Intelligence Platform</div>
  <div style="display:flex;gap:10px;">
    {"".join([f'<span style="font-size:10px;color:#3F3F46;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);padding:4px 10px;border-radius:5px;">{b}</span>' for b in ["MVP v1.0","Built in 48h","Budget <$200","Production Prototype"]])}
  </div>
</div>
""", unsafe_allow_html=True)
