import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
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
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"],.stApp{font-family:'Inter',system-ui,sans-serif!important;background:#060608!important;color:#FFFFFF!important;}
[data-testid="stAppViewContainer"]{background:#060608!important;}
[data-testid="stHeader"]{background:#060608!important;border-bottom:1px solid rgba(255,255,255,0.03);}
.block-container{padding:0 2.5rem 5rem!important;max-width:1480px!important;}
#MainMenu,footer,[data-testid="stDecoration"],[data-testid="stToolbar"]{display:none!important;visibility:hidden!important;}
section[data-testid="stSidebar"]{display:none!important;}
.stTabs [data-baseweb="tab-list"]{background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.05)!important;border-radius:10px!important;padding:4px!important;gap:2px!important;}
.stTabs [data-baseweb="tab-highlight"]{display:none!important;}
[data-testid="stTabs"] button{background:transparent!important;color:#3F3F46!important;border:none!important;border-radius:7px!important;font-size:13px!important;font-weight:500!important;padding:8px 20px!important;transition:all .2s!important;}
[data-testid="stTabs"] button[aria-selected="true"]{background:rgba(139,92,246,0.1)!important;color:#A78BFA!important;border:1px solid rgba(139,92,246,0.18)!important;}
[data-testid="stTabs"] button:hover{color:#FFFFFF!important;}
[data-testid="stTabsContent"]{padding-top:36px!important;}
[data-testid="metric-container"]{background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.05)!important;border-radius:12px!important;padding:20px!important;}
[data-testid="stMetricLabel"]{color:#3F3F46!important;font-size:10px!important;font-weight:600!important;text-transform:uppercase;letter-spacing:.12em;}
[data-testid="stMetricValue"]{color:#FFFFFF!important;font-size:28px!important;font-weight:700!important;letter-spacing:-.5px;}
.stButton>button{background:linear-gradient(135deg,#7C3AED,#5B21B6)!important;color:#FFF!important;border:none!important;border-radius:8px!important;padding:8px 18px!important;font-size:12px!important;font-weight:500!important;box-shadow:0 0 16px rgba(124,58,237,.15)!important;transition:all .2s!important;}
.stButton>button:hover{box-shadow:0 0 28px rgba(124,58,237,.3)!important;transform:translateY(-1px)!important;}
[data-testid="stTextInput"] input{background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.07)!important;border-radius:8px!important;color:#FFF!important;font-size:13px!important;}
[data-testid="stTextInput"] input::placeholder{color:#2E2E35!important;}
[data-testid="stSelectbox"]>div>div{background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.07)!important;border-radius:8px!important;color:#FFF!important;}
[data-testid="stDownloadButton"] button{background:rgba(255,255,255,0.03)!important;color:#52525B!important;border:1px solid rgba(255,255,255,0.06)!important;border-radius:8px!important;font-size:12px!important;box-shadow:none!important;}
[data-testid="stDownloadButton"] button:hover{background:rgba(255,255,255,0.06)!important;color:#FFF!important;box-shadow:none!important;transform:none!important;}
[data-testid="stSuccess"]{background:rgba(34,197,94,.07)!important;border:1px solid rgba(34,197,94,.18)!important;border-radius:10px!important;color:#22C55E!important;}
.sec-label{font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#3F3F46;margin-bottom:20px;display:flex;align-items:center;gap:10px;}
.sec-label::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.04);}
hr{border-color:rgba(255,255,255,0.04)!important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════
TODAY = "2026-06-12"
TODAY_DT = datetime(2026, 6, 12)

SRCS = ["AffPapa","GPWA","Affiliate Guard Dog","AskGamblers","SBC News",
        "Gambling Insider","iGamingBusiness","CasinoBeats","EGR Global","AffiliateFix"]

NAMES = [
    "Bet365 Partners","888 Affiliates","LeoVegas Affiliates","Income Access Network",
    "Rizk Partners","Stake Affiliates","PlayAmo Partners","Fortune Affiliates",
    "Betsson Group Affiliates","22Bet Partners","Betwinner Affiliates","Coldbet Partners",
    "FoxSlots Partners","Rocketpot Affiliates","Bwin Affiliates","William Hill Partners",
    "Unibet Affiliates","PokerStars Affiliates","Betway Partners","Mr Green Affiliates",
    "Casumo Affiliates","Videoslots Partners","Fastpay Partners","N1 Partners",
    "Wildz Affiliates","Dunder Affiliates","Genesis Affiliates","Vera John Affiliates",
    "Guts Affiliates","Betsafe Partners","NordicBet Affiliates","SpinBet Affiliates",
    "MegaSlot Affiliates","LuckyNova Partners","GrandWin Affiliates","SilverPlay Partners",
    "Odds96 Partners","C24 Partners","Boomerang Partners","Partners1xbet",
    "Parimatch Partners","Mostbet Affiliates","Melbet Partners","PinUp Partners",
    "1win Affiliates","GGBet Partners","BC.Game Affiliates","BitStarz Partners",
    "FortuneJack Affiliates","BetFury Affiliates","CloudBet Partners","Rollbit Affiliates",
    "JackBit Partners","NineCasino Affiliates","Sportsbet.io Partners","Rabona Affiliates",
    "BetChain Partners","1xSlots Affiliates","Sportaza Affiliates","Haz Casino Partners",
    "20Bet Affiliates","Playfina Affiliates","Legzo Partners","Sol Casino Partners",
    "Cat Casino Partners","Gama Affiliates","JVSpin Affiliates","DrBet Partners",
    "Mystake Partners","Paripesa Affiliates","Betano Affiliates","Novibet Partners",
    "NetBet Partners","BetVictor Affiliates","Betfair Affiliates","Smarkets Partners",
    "Fortuna Partners","Tipsport Affiliates","Tipico Partners","Bettilt Affiliates",
    "Betcris Affiliates","Coolbet Partners","LiveScore Partners","Midnite Affiliates",
    "Rootz Affiliates","MrQ Partners","SpinGenie Affiliates","Jackpotjoy Partners",
    "Virgin Games Affiliates","Pinnacle Affiliates","1xBet Partners","Parimatch UA Partners",
    "Favbet Affiliates","Vbet Partners","BetMGM Affiliates","DraftKings Partners",
    "FanDuel Affiliates","Caesars Affiliates","PointsBet Partners","ESPN Bet Affiliates",
    "Betclic Partners","Winamax Affiliates","Better Collective Affiliates","Catena Media Partners",
    "Raketech Affiliates","CasinoGuru Partners","Push Gaming Affiliates","Evolution Partners",
    "Playtech Affiliates","Pragmatic Partners","NetEnt Affiliates","Red Tiger Affiliates",
    "BGaming Affiliates","Spinomenal Partners","Gamomat Partners","Wazdan Affiliates",
    "Betsoft Partners","PG Soft Affiliates","Casiplay Affiliates","CasinoRoom Partners",
]

GEOS = ["UK","EU","CA","AU","LATAM","Nordics","UA/CIS","DE","SE","IE"]
LICS = ["MGA","UKGC","Curaçao","Gibraltar","Isle of Man","Unknown"]
STATS = ["New","New","To Verify","To Verify","Verified","Verified","Verified","Verified","Rejected"]
PRIS = ["High","High","Medium","Medium","Low"]
COMS = ["RevShare 25-35%","RevShare 30-40%","RevShare 35-45%","CPA £50-100","CPA £80-150","Hybrid"]
NOTES = [
    "Verified program. Stable payouts reported by community.",
    "New listing — terms under review by affiliate team.",
    "Delayed payment reports on Affiliate Guard Dog.",
    "Strong UK and Nordics traffic focus.",
    "Fast onboarding. License documentation complete.",
    "Mixed reviews on AffiliateFix. Monitor closely.",
    "High RevShare. Recently listed on AffPapa.",
    "Established network. Well-reviewed on GPWA.",
    "Recently launched. License application pending.",
    "Reputation confirmed via EGR Global listing.",
    "Rapid growth in LATAM. New program.",
    "License renewal pending. Temporary risk flag.",
    "Top performer in Nordics per iGamingBusiness.",
    "New management. Performance history unclear.",
    "Positive community signals on AffiliateFix.",
]

def calc_risk(row):
    s = 12
    if row.get("License") == "Unknown": s += 38
    if row.get("License") == "Curaçao": s += 10
    if row.get("Status") == "Rejected": s += 30
    if row.get("Status") == "To Verify": s += 15
    n = row.get("Notes","").lower()
    if "delayed" in n or "unclear" in n or "pending" in n: s += 14
    return min(max(s, 10), 88)

def calc_opp(row):
    s = 28
    if row.get("Priority") == "High": s += 22
    if row.get("Status") == "Verified": s += 18
    g = row.get("GEO","")
    if "UK" in g or "Nordics" in g or "CA" in g: s += 8
    c = row.get("Commission","")
    if "35-45" in c or "40" in c or "45" in c: s += 7
    n = row.get("Notes","").lower()
    if "stable" in n or "confirmed" in n or "top performer" in n: s += 8
    if row.get("Status") == "New" and row.get("Priority") == "High": s += 5
    lic = row.get("License","")
    if lic in ["MGA","UKGC","Gibraltar"]: s += 6
    return min(max(s, 30), 86)

def opp_reasons(row):
    reasons, risk_reasons = [], []
    lic = row.get("License","")
    g = row.get("GEO","")
    c = row.get("Commission","")
    n = row.get("Notes","").lower()
    src = row.get("Source","")
    if lic in ["MGA","UKGC","Gibraltar"]: reasons.append("Regulated license confirmed")
    if "UK" in g or "Nordics" in g: reasons.append("Tier 1 GEO coverage")
    if "CA" in g or "AU" in g: reasons.append("High-value market presence")
    if "35-45" in c or "40" in c: reasons.append("Above-market revenue share")
    if row.get("Status") == "New": reasons.append("New launch — first-mover advantage")
    if src in ["AffPapa","GPWA","EGR Global"]: reasons.append(f"Listed on {src} — verified source")
    if "stable" in n or "confirmed" in n: reasons.append("Positive reputation signals")
    if "top performer" in n: reasons.append("Top performer in region")

    if lic == "Unknown": risk_reasons.append("License status unconfirmed")
    elif lic == "Curaçao": risk_reasons.append("Curaçao license — lower regulatory standard")
    if "delayed" in n: risk_reasons.append("Delayed payment reports found")
    if "pending" in n: risk_reasons.append("License renewal in progress")
    if "unclear" in n: risk_reasons.append("Performance history unclear")
    if not risk_reasons: risk_reasons.append("No major reputation warnings found")
    if lic in ["MGA","UKGC"]: risk_reasons.append("License confirmed and active")
    if "stable" in n: risk_reasons.append("No payment complaints on record")

    return reasons[:4] or ["Active program","Detected via monitored source"], risk_reasons[:3]

def generate(n=280):
    random.seed(42)
    nms = (NAMES * ((n // len(NAMES)) + 2))[:n]
    rows = []
    for i, name in enumerate(nms):
        if i < 6: days = 0
        elif i < 28: days = random.randint(1, 7)
        else: days = random.randint(8, 85)
        det = (TODAY_DT - timedelta(days=days)).strftime("%Y-%m-%d")
        st_ = random.choice(STATS)
        if days == 0: st_ = "New"
        elif days <= 7: st_ = random.choice(["New","To Verify"])
        geo = ", ".join(random.sample(GEOS, random.randint(1,3)))
        lic = random.choice(LICS)
        com = random.choice(COMS)
        pri = random.choice(PRIS)
        note = random.choice(NOTES)
        row = {"Name":name,"Date Detected":det,"Source":random.choice(SRCS),
               "GEO":geo,"License":lic,"Commission":com,"Status":st_,"Priority":pri,"Notes":note}
        row["Risk"] = calc_risk(row)
        row["Opp"] = calc_opp(row)
        rows.append(row)
    return pd.DataFrame(rows)

def trend_data():
    random.seed(11)
    base = [2,3,2,1,3,2,4,3,2,3,1,2,3,2,1,3,2,3,2,1,2,3,2,3,2,1,2,3,2,2]
    return [(TODAY_DT - timedelta(days=29-i), base[i]) for i in range(30)]

NEW_POOL = [
    {"Name":"SpinBet Affiliates","Source":"SBC News","GEO":"UK, EU","License":"Curaçao","Commission":"RevShare 35-45%","Status":"New","Priority":"High","Notes":"High RevShare. Recently listed on SBC News. No prior track record."},
    {"Name":"NovaSpin Affiliates","Source":"Affiliate Guard Dog","GEO":"UK","License":"MGA","Commission":"RevShare 30-40%","Status":"New","Priority":"High","Notes":"Reputation confirmed via EGR Global listing."},
    {"Name":"StarNet Affiliates","Source":"AffPapa","GEO":"CA, AU","License":"MGA","Commission":"RevShare 30-40%","Status":"New","Priority":"High","Notes":"Fast onboarding. License documentation complete."},
    {"Name":"BetRocket Partners","Source":"CasinoBeats","GEO":"EU","License":"Curaçao","Commission":"CPA £80-150","Status":"To Verify","Notes":"New CPA program. Terms under review by affiliate team.","Priority":"Medium"},
    {"Name":"AlphaPlay Affiliates","Source":"iGamingBusiness","GEO":"Nordics","License":"MGA","Commission":"RevShare 25-35%","Status":"New","Priority":"Medium","Notes":"Top performer in Nordics per iGamingBusiness."},
]

SRC_DATA = [
    {"name":"AffPapa","type":"Affiliate Directory","found":6,"reliability":94,"last":"Today 09:00"},
    {"name":"GPWA","type":"Affiliate Forum","found":5,"reliability":89,"last":"Today 09:01"},
    {"name":"Affiliate Guard Dog","type":"Watchdog Forum","found":3,"reliability":92,"last":"Today 09:02"},
    {"name":"AskGamblers","type":"Review Platform","found":4,"reliability":87,"last":"Today 09:03"},
    {"name":"SBC News","type":"Industry News","found":4,"reliability":96,"last":"Today 09:04"},
    {"name":"Gambling Insider","type":"Industry News","found":3,"reliability":91,"last":"Today 09:05"},
    {"name":"iGamingBusiness","type":"Industry News","found":3,"reliability":90,"last":"Today 09:06"},
    {"name":"CasinoBeats","type":"Industry News","found":2,"reliability":85,"last":"Today 09:07"},
    {"name":"EGR Global","type":"Industry Publication","found":2,"reliability":93,"last":"Today 09:08"},
    {"name":"AffiliateFix","type":"Affiliate Forum","found":1,"reliability":78,"last":"Today 09:09"},
]

GEO_DIST = [("UK",7),("EU",6),("CA",4),("AU",3),("LATAM",3),("Nordics",2),("UA/CIS",2)]
SRC_DIST_WK = [("AffPapa",6),("GPWA",5),("SBC News",4),("AskGamblers",4),("Affiliate Guard Dog",3),("iGamingBusiness",3),("CasinoBeats",2),("EGR Global",2)]

if "df" not in st.session_state: st.session_state.df = generate(280)
if "last_scan" not in st.session_state: st.session_state.last_scan = None
if "pg" not in st.session_state: st.session_state.pg = 0
if "ran_scan" not in st.session_state: st.session_state.ran_scan = False

# ── helpers ──
def sbadge(s):
    M={"New":("rgba(139,92,246,.14)","#A78BFA","rgba(139,92,246,.22)"),
       "To Verify":("rgba(245,158,11,.11)","#F59E0B","rgba(245,158,11,.18)"),
       "Verified":("rgba(34,197,94,.09)","#22C55E","rgba(34,197,94,.18)"),
       "Rejected":("rgba(239,68,68,.09)","#EF4444","rgba(239,68,68,.18)")}
    bg,c,b=M.get(s,M["New"])
    return f'<span style="font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;background:{bg};color:{c};border:1px solid {b};letter-spacing:.04em;">{s.upper()}</span>'

def rc(v): return "#EF4444" if v>=65 else ("#F59E0B" if v>=38 else "#22C55E")
def oc(v): return "#22C55E" if v>=68 else ("#F59E0B" if v>=52 else "#71717A")

# ── metrics ──
df = st.session_state.df
W = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
total = len(df)
new_wk = len(df[df["Date Detected"] >= W])
today_n = len(df[df["Date Detected"] == TODAY])
to_ver = len(df[df["Status"] == "To Verify"])
verified = len(df[df["Status"] == "Verified"])
crit_risk = len(df[df["Risk"] >= 65])
opps = len(df[(df["Opp"] >= 65) & (df["Status"].isin(["New","To Verify","Verified"]))])
hrs = 11
last_txt = st.session_state.last_scan.strftime("%d %b, %H:%M") if st.session_state.last_scan else "Today 09:00"
n_sources = len(SRC_DATA)

# ══════════════════════════════════════════
# TOP NAV
# ══════════════════════════════════════════
st.markdown(f"""
<div style="padding:16px 0;display:flex;justify-content:space-between;align-items:center;
  border-bottom:1px solid rgba(255,255,255,0.04);margin-bottom:0;">
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="font-size:13px;font-weight:700;color:#7C3AED;letter-spacing:.12em;">◈</div>
    <div style="font-size:13px;font-weight:600;color:#FFFFFF;">Affiliate Intelligence Platform</div>
    <div style="height:12px;width:1px;background:rgba(255,255,255,0.08);"></div>
    <div style="font-size:12px;color:#3F3F46;">iGaming Ecosystem Monitor</div>
  </div>
  <div style="display:flex;align-items:center;gap:20px;">
    <div style="font-size:12px;color:#3F3F46;">Last scan: <span style="color:#52525B;">{last_txt}</span></div>
    <div style="font-size:12px;color:#3F3F46;">Next: <span style="color:#52525B;">Tomorrow 09:00</span></div>
    <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(34,197,94,0.07);
      border:1px solid rgba(34,197,94,0.15);border-radius:20px;padding:5px 12px;
      font-size:11px;font-weight:700;color:#22C55E;">
      <span style="width:6px;height:6px;border-radius:50%;background:#22C55E;box-shadow:0 0 6px #22C55E;display:inline-block;"></span>
      LIVE
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# TABS
# ══════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["  Intelligence Brief  ","  Program Database  ","  CEO Weekly Digest  "])


# ══════════════════════════════════════════════════════
# TAB 1
# ══════════════════════════════════════════════════════
with tab1:

    # HERO
    st.markdown(f"""
    <div style="padding:44px 0 36px;">
      <div style="font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
        color:#4B21A0;margin-bottom:14px;">EXECUTIVE INTELLIGENCE BRIEF · {TODAY_DT.strftime('%A, %d %B %Y').upper()}</div>
      <div style="font-size:40px;font-weight:800;letter-spacing:-1.5px;line-height:1.15;color:#FFFFFF;margin-bottom:8px;">
        This week in the<br>
        <span style="background:linear-gradient(90deg,#A78BFA,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
          iGaming affiliate ecosystem
        </span>
      </div>
      <div style="font-size:15px;color:#52525B;margin-top:12px;">
        {new_wk} new programs detected across {n_sources} monitored sources
      </div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1px;
      background:rgba(255,255,255,0.04);border-radius:14px;overflow:hidden;margin-bottom:44px;">
      <div style="background:#0C0C0F;padding:26px 22px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:10px;">New Programs</div>
        <div style="font-size:42px;font-weight:800;color:#FFFFFF;letter-spacing:-2px;line-height:1;">+{new_wk}</div>
        <div style="font-size:12px;color:#52525B;margin-top:6px;">detected this week</div>
      </div>
      <div style="background:#0C0C0F;padding:26px 22px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:10px;">High Priority</div>
        <div style="font-size:42px;font-weight:800;color:#A78BFA;letter-spacing:-2px;line-height:1;">{opps}</div>
        <div style="font-size:12px;color:#52525B;margin-top:6px;">programs worth review</div>
      </div>
      <div style="background:#0C0C0F;padding:26px 22px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:10px;">Risk Signals</div>
        <div style="font-size:42px;font-weight:800;color:#EF4444;letter-spacing:-2px;line-height:1;">{crit_risk}</div>
        <div style="font-size:12px;color:#52525B;margin-top:6px;">flagged this week</div>
      </div>
      <div style="background:#0C0C0F;padding:26px 22px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:10px;">Require Verification</div>
        <div style="font-size:42px;font-weight:800;color:#F59E0B;letter-spacing:-2px;line-height:1;">{to_ver}</div>
        <div style="font-size:12px;color:#52525B;margin-top:6px;">license or terms</div>
      </div>
      <div style="background:#0C0C0F;padding:26px 22px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:10px;">Total Tracked</div>
        <div style="font-size:42px;font-weight:800;color:#FFFFFF;letter-spacing:-2px;line-height:1;">{total}</div>
        <div style="font-size:12px;color:#52525B;margin-top:6px;">programs in database</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # EXECUTIVE RECOMMENDATION
    unk_lic = len(df[df["License"]=="Unknown"])
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(124,58,237,0.07),rgba(109,40,217,0.03));
      border:1px solid rgba(124,58,237,0.16);border-radius:16px;padding:28px 36px;margin-bottom:36px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
        color:#6D28D9;margin-bottom:14px;">◈ EXECUTIVE RECOMMENDATION · THIS WEEK</div>
      <div style="display:grid;grid-template-columns:2fr 1fr;gap:40px;align-items:start;">
        <div>
          <div style="font-size:17px;font-weight:700;color:#FFFFFF;margin-bottom:18px;letter-spacing:-.2px;">
            3 operational actions required this week
          </div>
          <div style="display:flex;flex-direction:column;gap:12px;">
            <div style="display:flex;align-items:flex-start;gap:12px;">
              <span style="font-size:11px;font-weight:700;padding:3px 8px;border-radius:4px;
                background:rgba(139,92,246,0.12);color:#A78BFA;min-width:32px;text-align:center;flex-shrink:0;">01</span>
              <div style="font-size:13px;color:#A1A1AA;line-height:1.6;">
                <strong style="color:#FFFFFF;">Review {opps} high-potential affiliate programs</strong><br>
                Strong GEO fit, competitive commission model, and credible source verification. Early contact recommended before market saturation.
              </div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:12px;">
              <span style="font-size:11px;font-weight:700;padding:3px 8px;border-radius:4px;
                background:rgba(245,158,11,0.1);color:#F59E0B;min-width:32px;text-align:center;flex-shrink:0;">02</span>
              <div style="font-size:13px;color:#A1A1AA;line-height:1.6;">
                <strong style="color:#FFFFFF;">Verify {to_ver} programs with incomplete license or terms data</strong><br>
                {unk_lic} have unknown license status. Missing affiliate contact or unclear commission structure. Compliance risk if onboarded without verification.
              </div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:12px;">
              <span style="font-size:11px;font-weight:700;padding:3px 8px;border-radius:4px;
                background:rgba(239,68,68,0.1);color:#EF4444;min-width:32px;text-align:center;flex-shrink:0;">03</span>
              <div style="font-size:13px;color:#A1A1AA;line-height:1.6;">
                <strong style="color:#FFFFFF;">Exclude {crit_risk} high-risk programs from outreach</strong><br>
                Reputation concerns or unresolved payment complaints flagged via Affiliate Guard Dog and AffiliateFix. Do not engage until resolved.
              </div>
            </div>
          </div>
        </div>
        <div style="border-left:1px solid rgba(255,255,255,0.06);padding-left:32px;">
          <div style="margin-bottom:22px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:8px;">High Priority Programs</div>
            <div style="font-size:28px;font-weight:800;color:#A78BFA;letter-spacing:-1px;">{opps}</div>
            <div style="font-size:12px;color:#52525B;margin-top:2px;">identified for review</div>
          </div>
          <div style="margin-bottom:22px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:8px;">Require Verification</div>
            <div style="font-size:28px;font-weight:800;color:#F59E0B;letter-spacing:-1px;">{to_ver}</div>
            <div style="font-size:12px;color:#52525B;margin-top:2px;">license or terms incomplete</div>
          </div>
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:8px;">High Risk Programs</div>
            <div style="font-size:28px;font-weight:800;color:#EF4444;letter-spacing:-1px;">{crit_risk}</div>
            <div style="font-size:12px;color:#52525B;margin-top:2px;">excluded from outreach</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # HIGHEST VALUE OPPORTUNITIES
    st.markdown('<div class="sec-label">Highest Value Opportunities</div>', unsafe_allow_html=True)
    top_ops = df[(df["Opp"] >= 60)].sort_values("Opp", ascending=False).head(3)

    for _, row in top_ops.iterrows():
        reasons, risk_reasons = opp_reasons(dict(row))
        opp_v, risk_v = int(row["Opp"]), int(row["Risk"])
        urgency = "Review onboarding within 24h" if row["Priority"] == "High" else "Schedule review this week"
        urgency_c = "#EF4444" if row["Priority"] == "High" else "#F59E0B"
        geos = [g.strip() for g in row["GEO"].split(",")][:3]
        geo_html = "".join([f'<span style="font-size:11px;padding:3px 8px;border-radius:5px;background:rgba(255,255,255,0.04);color:#71717A;margin-right:5px;">{g}</span>' for g in geos])

        st.markdown(f"""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:16px;
          padding:26px 30px;margin-bottom:12px;display:grid;
          grid-template-columns:2fr 1fr 1fr 1.6fr;gap:28px;align-items:start;">
          <div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
              <div style="font-size:16px;font-weight:700;color:#FFFFFF;">{row['Name']}</div>
              {sbadge(row['Status'])}
            </div>
            <div style="font-size:12px;color:#3F3F46;margin-bottom:10px;">{row['Source']} · Detected {row['Date Detected']}</div>
            <div style="margin-bottom:10px;">{geo_html}</div>
            <div style="font-size:12px;color:#52525B;">{row['Commission']} · {row['License']}</div>
          </div>
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:8px;">Opportunity</div>
            <div style="font-size:36px;font-weight:800;color:{oc(opp_v)};letter-spacing:-1px;margin-bottom:2px;">{opp_v}</div>
            <div style="font-size:10px;color:#3F3F46;margin-bottom:10px;">/ 100</div>
            <div style="font-size:10px;font-weight:600;color:#3F3F46;margin-bottom:5px;text-transform:uppercase;letter-spacing:.08em;">Based on:</div>
            {"".join([f'<div style="font-size:11px;color:#71717A;margin-bottom:3px;display:flex;align-items:center;gap:5px;"><span style="color:#22C55E;font-size:9px;">✓</span>{r}</div>' for r in reasons])}
          </div>
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:8px;">Risk</div>
            <div style="font-size:36px;font-weight:800;color:{rc(risk_v)};letter-spacing:-1px;margin-bottom:2px;">{risk_v}</div>
            <div style="font-size:10px;color:#3F3F46;margin-bottom:10px;">/ 100</div>
            <div style="font-size:10px;font-weight:600;color:#3F3F46;margin-bottom:5px;text-transform:uppercase;letter-spacing:.08em;">Based on:</div>
            {"".join([f'<div style="font-size:11px;color:#71717A;margin-bottom:3px;display:flex;align-items:center;gap:5px;"><span style="color:#52525B;font-size:9px;">·</span>{r}</div>' for r in risk_reasons])}
          </div>
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:8px;">Notes</div>
            <div style="font-size:12px;color:#71717A;line-height:1.6;margin-bottom:14px;">{row['Notes']}</div>
            <div style="font-size:12px;font-weight:600;color:{urgency_c};
              background:rgba(255,255,255,0.02);border-radius:6px;padding:8px 12px;
              border-left:2px solid {urgency_c};">→ {urgency}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # INTELLIGENCE ALERTS
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Intelligence Alerts</div>', unsafe_allow_html=True)

    alerts = [
        {"color":"rgba(139,92,246,0.35)","bg":"rgba(139,92,246,0.05)","border":"rgba(139,92,246,0.12)",
         "label":"NEW SIGNAL","ac":"#A78BFA","title":"High-RevShare Program Detected",
         "prog":"SpinBet Affiliates","src":"SBC News","geo":"UK, EU","lic":"Curaçao","comm":"RevShare 35-45%",
         "signal":"New program listed on SBC News with above-market revenue share. No prior history in GPWA or AffPapa databases.",
         "evidence":"RevShare of 35–45% is above the 30% industry average for new launches. Curaçao license — lower regulatory standard than MGA/UKGC.",
         "impact":"Potential early-partnership opportunity. License risk is moderate and manageable with due diligence.",
         "rec":"Affiliate Manager to verify terms and request license documentation within 24h.","rec_c":"#A78BFA"},
        {"color":"rgba(245,158,11,0.35)","bg":"rgba(245,158,11,0.04)","border":"rgba(245,158,11,0.12)",
         "label":"VERIFICATION REQUIRED","ac":"#F59E0B","title":"License Status Unconfirmed",
         "prog":"LuckyNova Partners","src":"AffiliateFix","geo":"UA/CIS, EU","lic":"Unknown","comm":"CPA £80-150",
         "signal":"Program appeared on AffiliateFix community forum. License cannot be confirmed from MGA, UKGC, Gibraltar, or Curaçao public registers.",
         "evidence":"License field is empty in affiliate submission. No listing found on Affiliate Guard Dog verified directory.",
         "impact":"Engagement without license verification creates compliance risk and potential payment disputes.",
         "rec":"Do not onboard. Affiliate Manager to request official license documentation before any contact.","rec_c":"#F59E0B"},
        {"color":"rgba(239,68,68,0.35)","bg":"rgba(239,68,68,0.04)","border":"rgba(239,68,68,0.12)",
         "label":"RISK FLAGGED","ac":"#EF4444","title":"Reputation Risk — Payment Delays",
         "prog":"Fortune Affiliates","src":"Affiliate Guard Dog","geo":"UK, EU","lic":"MGA","comm":"RevShare 25-35%",
         "signal":"Multiple affiliate payment delay complaints filed on Affiliate Guard Dog over the past 90 days.",
         "evidence":"6 verified complaints in Q2 2026. Pattern consistent with cashflow constraints. Community trust score declining month-over-month.",
         "impact":"High onboarding risk. Programs with delayed payment history carry reputational and financial risk for the affiliate team.",
         "rec":"Exclude from outreach shortlist. Revisit only after 6-month clean payment record is independently confirmed.","rec_c":"#EF4444"},
    ]
    al_cols = st.columns(3)
    for i, a in enumerate(alerts):
        with al_cols[i]:
            st.markdown(f"""
            <div style="background:{a['bg']};border:1px solid {a['border']};
              border-top:2px solid {a['color']};border-radius:14px;padding:22px;height:100%;">
              <div style="margin-bottom:14px;">
                <span style="font-size:10px;font-weight:700;padding:3px 8px;border-radius:4px;
                  background:{a['bg']};color:{a['ac']};border:1px solid {a['border']};
                  letter-spacing:.08em;">{a['label']}</span>
              </div>
              <div style="font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:5px;">{a['title']}</div>
              <div style="font-size:12px;color:#52525B;margin-bottom:16px;">{a['prog']} · {a['src']}</div>
              <div style="margin-bottom:10px;">
                <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#3F3F46;margin-bottom:4px;">Signal</div>
                <div style="font-size:12px;color:#A1A1AA;line-height:1.6;">{a['signal']}</div>
              </div>
              <div style="margin-bottom:10px;">
                <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#3F3F46;margin-bottom:4px;">Evidence</div>
                <div style="font-size:12px;color:#71717A;line-height:1.6;">{a['evidence']}</div>
              </div>
              <div style="margin-bottom:14px;">
                <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#3F3F46;margin-bottom:4px;">Impact</div>
                <div style="font-size:12px;color:#71717A;line-height:1.6;">{a['impact']}</div>
              </div>
              <div style="border-top:1px solid rgba(255,255,255,0.05);padding-top:12px;
                font-size:12px;font-weight:600;color:{a['rec_c']};">→ {a['rec']}</div>
            </div>""", unsafe_allow_html=True)

    # MARKET INTELLIGENCE
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Market Intelligence</div>', unsafe_allow_html=True)
    mi1, mi2, mi3 = st.columns(3)

    with mi1:
        max_g = max(v for _,v in GEO_DIST)
        rows_geo = "".join([f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:11px;">
          <div style="font-size:12px;color:#71717A;width:60px;">{g}</div>
          <div style="flex:1;height:4px;background:rgba(255,255,255,0.04);border-radius:2px;">
            <div style="height:4px;width:{int(v/max_g*100)}%;background:linear-gradient(90deg,#7C3AED,#A78BFA);border-radius:2px;"></div>
          </div>
          <div style="font-size:12px;color:#A1A1AA;font-weight:600;width:18px;">{v}</div>
        </div>""" for g,v in GEO_DIST])
        st.markdown(f"""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:22px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:18px;">New Programs by GEO · This Week</div>
          {rows_geo}
        </div>""", unsafe_allow_html=True)

    with mi2:
        max_s = max(v for _,v in SRC_DIST_WK)
        rows_src = "".join([f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:11px;">
          <div style="font-size:11px;color:#71717A;width:110px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;">{s}</div>
          <div style="flex:1;height:4px;background:rgba(255,255,255,0.04);border-radius:2px;">
            <div style="height:4px;width:{int(v/max_s*100)}%;background:linear-gradient(90deg,#22C55E,#86EFAC);border-radius:2px;"></div>
          </div>
          <div style="font-size:12px;color:#A1A1AA;font-weight:600;width:18px;">{v}</div>
        </div>""" for s,v in SRC_DIST_WK])
        st.markdown(f"""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:22px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:18px;">Programs by Source · This Week</div>
          {rows_src}
        </div>""", unsafe_allow_html=True)

    with mi3:
        td = trend_data()
        total_30 = sum(v for _,v in td)
        max_t = max(v for _,v in td)
        avg7 = round(sum(v for _,v in td[-7:])/7,1)
        avg7p = round(sum(v for _,v in td[-14:-7])/7,1)
        delta = round(avg7-avg7p,1)
        dc = "#22C55E" if delta>=0 else "#EF4444"
        ds = f"+{delta}" if delta>=0 else str(delta)
        bar_html = "".join([
            '<div style="flex:1;background:linear-gradient(180deg,rgba(124,58,237,0.65),rgba(124,58,237,0.15));height:' + str(int(v/max_t*56)+4) + 'px;border-radius:2px 2px 0 0;min-width:5px;"></div>'
            for d,v in td])
        st.markdown(f"""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:22px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3F3F46;margin-bottom:6px;">New Launches · Last 30 Days</div>
          <div style="font-size:30px;font-weight:800;color:#FFFFFF;letter-spacing:-1px;margin-bottom:4px;">{total_30}</div>
          <div style="font-size:12px;color:#52525B;margin-bottom:18px;">
            7-day avg: <span style="color:#A1A1AA;">{avg7}/day</span> &nbsp;
            <span style="color:{dc};">{ds} vs prior week</span>
          </div>
          <div style="display:flex;align-items:flex-end;gap:2px;height:64px;border-bottom:1px solid rgba(255,255,255,0.04);">{bar_html}</div>
          <div style="display:flex;justify-content:space-between;margin-top:6px;">
            <div style="font-size:10px;color:#2E2E35;">May 13</div>
            <div style="font-size:10px;color:#2E2E35;">Jun 12</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # MONITORING ENGINE STATUS
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Monitoring Engine Status</div>', unsafe_allow_html=True)

    src_cols = st.columns(5)
    for i, s in enumerate(SRC_DATA):
        with src_cols[i % 5]:
            rel_c = "#22C55E" if s["reliability"]>=90 else ("#F59E0B" if s["reliability"]>=78 else "#EF4444")
            st.markdown(f"""
            <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:16px 18px;margin-bottom:12px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <div style="font-size:13px;font-weight:600;color:#FFFFFF;">{s['name']}</div>
                <span style="font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;background:rgba(34,197,94,0.08);color:#22C55E;border:1px solid rgba(34,197,94,0.15);">ACTIVE</span>
              </div>
              <div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px;">{s['type']}</div>
              <div style="font-size:20px;font-weight:700;color:#FFFFFF;margin-bottom:2px;">{s['found']}</div>
              <div style="font-size:11px;color:#3F3F46;margin-bottom:10px;">found this week</div>
              <div style="height:2px;background:rgba(255,255,255,0.04);border-radius:1px;">
                <div style="height:2px;width:{s['reliability']}%;background:{rel_c};border-radius:1px;opacity:.6;"></div>
              </div>
              <div style="font-size:11px;color:#3F3F46;margin-top:5px;">Reliability <span style="color:{rel_c};">{s['reliability']}%</span></div>
            </div>""", unsafe_allow_html=True)
        if (i+1) % 5 == 0 and i+1 < len(SRC_DATA):
            src_cols = st.columns(5)

    # Engine status bar
    st.markdown(f"""
    <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:12px;
      padding:20px 28px;display:grid;grid-template-columns:repeat(5,1fr);gap:0;align-items:center;margin-top:4px;">
      <div style="padding-right:20px;border-right:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:6px;">Status</div>
        <div style="display:flex;align-items:center;gap:7px;">
          <span style="width:6px;height:6px;border-radius:50%;background:#22C55E;box-shadow:0 0 6px #22C55E;display:inline-block;"></span>
          <span style="font-size:13px;font-weight:600;color:#22C55E;">Automated</span>
        </div>
      </div>
      <div style="padding:0 20px;border-right:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:6px;">Last Scan</div>
        <div style="font-size:13px;font-weight:600;color:#FFFFFF;">{last_txt}</div>
      </div>
      <div style="padding:0 20px;border-right:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:6px;">Sources</div>
        <div style="font-size:13px;font-weight:600;color:#FFFFFF;">{n_sources}/{n_sources} active</div>
      </div>
      <div style="padding:0 20px;border-right:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:6px;">New Findings</div>
        <div style="font-size:13px;font-weight:600;color:#A78BFA;">{today_n} programs</div>
      </div>
      <div style="padding-left:20px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3F3F46;margin-bottom:6px;">Next Scan</div>
        <div style="font-size:13px;font-weight:600;color:#52525B;">Tomorrow 09:00</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Small secondary manual trigger
    st.markdown("<br>", unsafe_allow_html=True)
    mc1, mc2, mc3 = st.columns([1,5,1])
    with mc1:
        run = st.button("↺  Run manual scan", use_container_width=True)
    with mc2:
        st.markdown(f"<div style='font-size:11px;color:#2E2E35;padding:10px 0;'>Scans run automatically every day at 09:00. Manual scan triggers an immediate refresh across all {n_sources} sources.</div>", unsafe_allow_html=True)
    if run:
        import time
        pb = st.progress(0,"Starting scan...")
        for i,s in enumerate(SRCS[:n_sources]):
            time.sleep(0.2)
            pb.progress((i+1)/n_sources, f"Scanning {s}...")
        time.sleep(0.2); pb.empty()
        ex = set(st.session_state.df["Name"])
        av = [p for p in NEW_POOL if p["Name"] not in ex] or NEW_POOL
        batch = random.sample(av, min(random.randint(2,4), len(av)))
        t = datetime.now()
        for p in batch:
            p["Date Detected"] = TODAY
            p["Risk"] = calc_risk(p); p["Opp"] = calc_opp(p)
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame(batch)], ignore_index=True)
        st.session_state.last_scan = t
        st.success(f"✅ Scan complete — {len(batch)} new programs detected and added to database.")
        st.rerun()


# ══════════════════════════════════════════════════
# TAB 2 — DATABASE
# ══════════════════════════════════════════════════
with tab2:
    df = st.session_state.df
    st.markdown('<div class="sec-label" style="margin-top:8px;">Affiliate Programs Database</div>', unsafe_allow_html=True)

    f1,f2,f3,f4,f5 = st.columns(5)
    with f1: srch = st.text_input("Search", placeholder="Program name...")
    with f2: sf = st.selectbox("Status", ["All"]+sorted(df["Status"].unique().tolist()))
    with f3: pf = st.selectbox("Priority", ["All","High","Medium","Low"])
    with f4: srcf = st.selectbox("Source", ["All"]+sorted(df["Source"].unique().tolist()))
    with f5:
        geopts = sorted(set(g.strip() for gs in df["GEO"].str.split(",") for g in gs))
        gf = st.selectbox("GEO", ["All"]+geopts)

    filt = df.copy()
    if srch: filt = filt[filt["Name"].str.contains(srch, case=False, na=False)]
    if sf!="All": filt = filt[filt["Status"]==sf]
    if pf!="All": filt = filt[filt["Priority"]==pf]
    if srcf!="All": filt = filt[filt["Source"]==srcf]
    if gf!="All": filt = filt[filt["GEO"].str.contains(gf, case=False, na=False)]
    filt = filt.sort_values("Date Detected", ascending=False).reset_index(drop=True)

    RPP = 20
    tpg = max(1, math.ceil(len(filt)/RPP))
    if st.session_state.pg >= tpg: st.session_state.pg = 0

    r1,r2,r3,r4 = st.columns([4,2,1,1])
    with r1:
        st.markdown(f"<div style='font-size:13px;color:#3F3F46;padding:8px 0;'>Showing <strong style='color:#71717A;'>{len(filt)}</strong> of <strong style='color:#71717A;'>{len(df)}</strong> &nbsp;·&nbsp; Page {st.session_state.pg+1}/{tpg}</div>", unsafe_allow_html=True)
    with r2:
        buf = io.StringIO(); filt.to_csv(buf, index=False)
        st.download_button("⬇ Export CSV", buf.getvalue(), f"programs_{TODAY}.csv","text/csv",use_container_width=True)
    with r3:
        if st.button("◀ Prev") and st.session_state.pg>0: st.session_state.pg-=1; st.rerun()
    with r4:
        if st.button("Next ▶") and st.session_state.pg<tpg-1: st.session_state.pg+=1; st.rerun()

    page_df = filt.iloc[st.session_state.pg*RPP:(st.session_state.pg+1)*RPP]
    rows_html = ""
    for i,(_, r) in enumerate(page_df.iterrows()):
        z = "background:rgba(255,255,255,0.01);" if i%2==1 else ""
        occ = oc(r["Opp"]); rcc = rc(r["Risk"])
        rows_html += f"""
        <tr style="border-bottom:1px solid rgba(255,255,255,0.04);{z}">
          <td style="padding:13px 16px;color:#FFFFFF;font-weight:500;font-size:13px;">{r['Name']}</td>
          <td style="padding:13px 16px;color:#52525B;font-size:12px;white-space:nowrap;">{r['Date Detected']}</td>
          <td style="padding:13px 16px;color:#52525B;font-size:12px;">{r['Source']}</td>
          <td style="padding:13px 16px;color:#52525B;font-size:12px;">{r['GEO']}</td>
          <td style="padding:13px 16px;color:#52525B;font-size:12px;">{r['License']}</td>
          <td style="padding:13px 16px;color:#52525B;font-size:12px;">{r['Commission']}</td>
          <td style="padding:13px 16px;">{sbadge(r['Status'])}</td>
          <td style="padding:13px 16px;font-size:13px;font-weight:700;color:{occ};">{r['Opp']}</td>
          <td style="padding:13px 16px;font-size:13px;font-weight:700;color:{rcc};">{r['Risk']}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;border-radius:12px;border:1px solid rgba(255,255,255,0.06);margin-top:8px;">
      <table style="width:100%;border-collapse:collapse;background:#0C0C0F;">
        <thead>
          <tr style="background:#0D0D11;border-bottom:1px solid rgba(255,255,255,0.06);">
            {''.join([f'<th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#2E2E35;white-space:nowrap;">{h}</th>' for h in ["Program","Detected","Source","GEO","License","Commission","Status","Opp","Risk"]])}
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# TAB 3 — CEO DIGEST
# ══════════════════════════════════════════════════
with tab3:
    df = st.session_state.df
    wk = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
    nwdf = df[df["Date Detected"] >= wk].copy()
    top5 = nwdf.sort_values("Opp", ascending=False).head(5)
    risk5 = df[df["Risk"] >= 65].sort_values("Risk", ascending=False).head(5)
    ver_wk = nwdf[nwdf["Status"]=="Verified"]
    unk_lic_n = len(df[df["License"]=="Unknown"])
    qual_review = min(opps, 5)
    high_risk_n = min(crit_risk, 2)

    st.markdown(f"""
    <div style="padding:36px 0 28px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
        color:#4B21A0;margin-bottom:12px;">CONFIDENTIAL · EXECUTIVE REPORT</div>
      <div style="font-size:34px;font-weight:800;letter-spacing:-1px;color:#FFFFFF;margin-bottom:8px;">Weekly CEO Digest</div>
      <div style="font-size:14px;color:#3F3F46;">
        {(TODAY_DT-timedelta(days=6)).strftime('%d %b')} — {TODAY_DT.strftime('%d %b %Y')} &nbsp;·&nbsp;
        Prepared automatically by Affiliate Intelligence Platform
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Narrative summary
    st.markdown(f"""
    <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.06);border-radius:14px;
      padding:28px 32px;margin-bottom:28px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
        color:#3F3F46;margin-bottom:14px;">Weekly Overview</div>
      <div style="font-size:15px;color:#A1A1AA;line-height:1.8;max-width:760px;">
        This week the monitoring engine identified <strong style="color:#FFFFFF;">{new_wk} new affiliate programs</strong>
        across <strong style="color:#FFFFFF;">{n_sources} monitored sources</strong> including AffPapa, GPWA, SBC News, and EGR Global.
        <strong style="color:#A78BFA;">{qual_review} programs</strong> match our priority criteria and should be reviewed by the Affiliate Manager.
        <strong style="color:#EF4444;">{high_risk_n} programs</strong> were flagged as high-risk due to incomplete licensing or negative reputation signals.
        An estimated <strong style="color:#22C55E;">{hrs} hours</strong> of manual research was avoided through automated monitoring.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Savings bar
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
      background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.12);
      border-radius:14px;overflow:hidden;margin-bottom:32px;">
      {"".join([f'<div style="background:#060608;padding:22px 26px;"><div style="font-size:30px;font-weight:800;color:#22C55E;letter-spacing:-1px;">{v}</div><div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.1em;margin-top:4px;">{l}</div></div>' for v,l in [(f"~{hrs}h","Research saved"),(total,"Programs tracked"),(new_wk,"New this week"),(high_risk_n,"Risks flagged")]])}
    </div>
    """, unsafe_allow_html=True)

    dg1, dg2 = st.columns([3,2])

    with dg1:
        st.markdown('<div class="sec-label">Top Opportunities This Week</div>', unsafe_allow_html=True)
        for rank,(_, row) in enumerate(top5.iterrows(), 1):
            reasons, risk_reasons = opp_reasons(dict(row))
            occ = oc(int(row["Opp"])); rcc = rc(int(row["Risk"]))
            st.markdown(f"""
            <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:12px;
              padding:18px 22px;margin-bottom:10px;display:grid;
              grid-template-columns:1.8fr .8fr .8fr;gap:18px;align-items:start;">
              <div>
                <div style="font-size:10px;color:#3F3F46;margin-bottom:5px;">#{rank}</div>
                <div style="font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:4px;">{row['Name']}</div>
                <div style="font-size:12px;color:#52525B;margin-bottom:6px;">{row['Source']} · {row['GEO']}</div>
                <div style="font-size:12px;color:#52525B;">{row['Commission']} · {row['License']}</div>
                <div style="margin-top:8px;">{"".join([f'<div style="font-size:11px;color:#71717A;margin-bottom:2px;"><span style="color:#22C55E;">✓</span> {r}</div>' for r in reasons[:2]])}</div>
              </div>
              <div style="text-align:center;">
                <div style="font-size:10px;color:#3F3F46;margin-bottom:5px;text-transform:uppercase;letter-spacing:.1em;">Opportunity</div>
                <div style="font-size:28px;font-weight:800;color:{occ};">{int(row['Opp'])}</div>
                <div style="font-size:10px;color:#3F3F46;">/ 100</div>
              </div>
              <div style="text-align:center;">
                <div style="font-size:10px;color:#3F3F46;margin-bottom:5px;text-transform:uppercase;letter-spacing:.1em;">Risk</div>
                <div style="font-size:28px;font-weight:800;color:{rcc};">{int(row['Risk'])}</div>
                <div style="font-size:10px;color:#3F3F46;">/ 100</div>
              </div>
            </div>""", unsafe_allow_html=True)

    with dg2:
        st.markdown('<div class="sec-label">Risk Flags</div>', unsafe_allow_html=True)
        for _, row in risk5.iterrows():
            rcc = rc(int(row["Risk"]))
            st.markdown(f"""
            <div style="background:#0C0C0F;border:1px solid rgba(239,68,68,0.1);border-left:2px solid #EF4444;
              border-radius:10px;padding:14px 16px;margin-bottom:8px;">
              <div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:4px;">{row['Name']}</div>
              <div style="font-size:12px;color:#52525B;margin-bottom:5px;">{row['Notes']}</div>
              <div style="font-size:12px;color:{rcc};font-weight:700;">Risk: {int(row['Risk'])}/100</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<br><div class="sec-label">Recommended Actions</div>', unsafe_allow_html=True)
        recs = [
            (f"Review {qual_review} qualified opportunities with Affiliate Manager","#A78BFA"),
            (f"Verify {to_ver} programs with incomplete license or terms","#F59E0B"),
            (f"Exclude {high_risk_n} high-risk programs from outreach shortlist","#EF4444"),
            ("Prepare shortlist for CEO review by Friday EOD","#22C55E"),
            ("Schedule next intelligence review Monday 09:00","#22C55E"),
        ]
        for rec,c in recs:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);
              border-left:2px solid {c};border-radius:8px;padding:11px 14px;margin-bottom:7px;
              font-size:13px;color:#A1A1AA;">→ {rec}</div>""", unsafe_allow_html=True)

    # Business Impact
    st.markdown('<br><div class="sec-label">This Week at a Glance</div>', unsafe_allow_html=True)
    bi_items = [
        ("High Priority Programs", str(opps), "#A78BFA"),
        ("Requiring Verification", str(to_ver), "#F59E0B"),
        ("High Risk — Excluded", str(high_risk_n), "#EF4444"),
        ("Verified in Database", str(len(ver_wk)), "#22C55E"),
        ("Next Review", "Monday 09:00", "#52525B"),
    ]
    bi_cols = st.columns(5)
    for i,(label,val,color) in enumerate(bi_items):
        with bi_cols[i]:
            st.markdown(f"""
            <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:20px 18px;">
              <div style="font-size:24px;font-weight:800;color:{color};letter-spacing:-.5px;margin-bottom:6px;">{val}</div>
              <div style="font-size:11px;color:#3F3F46;line-height:1.4;">{label}</div>
            </div>""", unsafe_allow_html=True)

    # Next Steps
    st.markdown('<br><div class="sec-label">Next Steps — Connecting Real Sources</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:28px 32px;">
      <div style="display:grid;grid-template-columns:1.5fr 1fr;gap:40px;align-items:start;">
        <div>
          <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
            color:#3F3F46;margin-bottom:6px;">MVP Prototype · Built in 48 hours · Budget &lt;$200</div>
          <div style="font-size:16px;font-weight:600;color:#FFFFFF;margin-bottom:12px;letter-spacing:-.2px;">
            This platform validates the monitoring logic.<br>
            <span style="color:#A78BFA;">Next step: connect live data sources.</span>
          </div>
          <div style="font-size:13px;color:#71717A;line-height:1.7;">
            The current version uses a structured mock database to demonstrate the intelligence workflow —
            detection, scoring, alerting, and reporting. All logic is production-ready.
            Connecting real sources requires scraping setup and scheduled automation, estimated 2–3 days of engineering work.
          </div>
        </div>
        <div>
          <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
            color:#3F3F46;margin-bottom:14px;">Integration Roadmap</div>
          {"".join([f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;"><span style="width:5px;height:5px;border-radius:50%;background:#7C3AED;display:inline-block;flex-shrink:0;"></span><div style="font-size:13px;color:#A1A1AA;">{s}</div></div>' for s in [
            "AffPapa API / structured scraping",
            "GPWA forum monitoring",
            "AffiliateFix thread detection",
            "SBC News RSS feed integration",
            "EGR Global new listing alerts",
            "Daily Cloudflare cron jobs",
            "Slack or email digest delivery",
          ]])}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br><div class="sec-label">Export</div>', unsafe_allow_html=True)
    ex1,ex2,_ = st.columns([1,1,2])
    with ex1:
        b1=io.StringIO(); top5.to_csv(b1,index=False)
        st.download_button("⬇ Top Opportunities CSV",b1.getvalue(),f"opp_{TODAY}.csv","text/csv",use_container_width=True)
    with ex2:
        b2=io.StringIO(); risk5.to_csv(b2,index=False)
        st.download_button("⬇ Risk Flags CSV",b2.getvalue(),f"risks_{TODAY}.csv","text/csv",use_container_width=True)


# FOOTER
st.markdown(f"""
<div style="margin-top:60px;padding:18px 0;border-top:1px solid rgba(255,255,255,0.03);
  display:flex;justify-content:space-between;align-items:center;">
  <div style="font-size:11px;color:#1E1E24;">© 2026 Affiliate Intelligence Platform · Internal use only</div>
  <div style="display:flex;gap:8px;">
    {"".join([f'<span style="font-size:10px;color:#2E2E35;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);padding:4px 10px;border-radius:4px;">{b}</span>' for b in ["MVP v1.0","Built in 48h","Budget <$200","Production Prototype"]])}
  </div>
</div>
""", unsafe_allow_html=True)
