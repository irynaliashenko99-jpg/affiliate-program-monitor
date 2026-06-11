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
html,body,[class*="css"],.stApp{
  font-family:'Inter',system-ui,sans-serif!important;
  background:#060608!important;color:#FFFFFF!important;
}
[data-testid="stAppViewContainer"]{background:#060608!important;}
[data-testid="stHeader"]{background:#060608!important;border-bottom:1px solid rgba(255,255,255,0.03);}
.block-container{padding:0 2.5rem 5rem!important;max-width:1480px!important;}
#MainMenu,footer,[data-testid="stDecoration"],[data-testid="stToolbar"]{display:none!important;visibility:hidden!important;}
section[data-testid="stSidebar"]{display:none!important;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{
  background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.05)!important;
  border-radius:10px!important;padding:4px!important;gap:2px!important;
}
.stTabs [data-baseweb="tab-highlight"]{display:none!important;}
[data-testid="stTabs"] button{
  background:transparent!important;color:#3F3F46!important;border:none!important;
  border-radius:7px!important;font-size:13px!important;font-weight:500!important;
  padding:8px 20px!important;transition:all .2s!important;letter-spacing:.01em;
}
[data-testid="stTabs"] button[aria-selected="true"]{
  background:rgba(139,92,246,0.1)!important;color:#A78BFA!important;
  border:1px solid rgba(139,92,246,0.18)!important;
}
[data-testid="stTabs"] button:hover{color:#FFFFFF!important;}
[data-testid="stTabsContent"]{padding-top:36px!important;}

/* METRICS */
[data-testid="metric-container"]{
  background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.05)!important;
  border-radius:12px!important;padding:20px!important;
}
[data-testid="stMetricLabel"]{color:#3F3F46!important;font-size:10px!important;font-weight:600!important;text-transform:uppercase;letter-spacing:.12em;}
[data-testid="stMetricValue"]{color:#FFFFFF!important;font-size:28px!important;font-weight:700!important;letter-spacing:-.5px;}

/* BUTTONS */
.stButton>button{
  background:linear-gradient(135deg,#7C3AED,#5B21B6)!important;
  color:#FFF!important;border:none!important;border-radius:8px!important;
  padding:9px 20px!important;font-size:13px!important;font-weight:500!important;
  box-shadow:0 0 20px rgba(124,58,237,.2)!important;transition:all .2s!important;
}
.stButton>button:hover{box-shadow:0 0 36px rgba(124,58,237,.4)!important;transform:translateY(-1px)!important;}

/* INPUTS */
[data-testid="stTextInput"] input{
  background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.07)!important;
  border-radius:8px!important;color:#FFF!important;font-size:13px!important;
}
[data-testid="stTextInput"] input::placeholder{color:#2E2E35!important;}
[data-testid="stSelectbox"]>div>div{
  background:#0C0C0F!important;border:1px solid rgba(255,255,255,0.07)!important;
  border-radius:8px!important;color:#FFF!important;
}
[data-testid="stDownloadButton"] button{
  background:rgba(255,255,255,0.03)!important;color:#52525B!important;
  border:1px solid rgba(255,255,255,0.06)!important;border-radius:8px!important;
  font-size:12px!important;box-shadow:none!important;
}
[data-testid="stDownloadButton"] button:hover{background:rgba(255,255,255,0.06)!important;color:#FFF!important;box-shadow:none!important;transform:none!important;}
[data-testid="stSuccess"]{background:rgba(34,197,94,.07)!important;border:1px solid rgba(34,197,94,.18)!important;border-radius:10px!important;color:#22C55E!important;}

/* DIVIDERS */
.divider{height:1px;background:rgba(255,255,255,0.04);margin:40px 0;}
.sec-label{
  font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
  color:#3F3F46;margin-bottom:20px;display:flex;align-items:center;gap:10px;
}
.sec-label::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.04);}

hr{border-color:rgba(255,255,255,0.04)!important;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════
NAMES = [
    "Bet365 Partners","888 Affiliates","LeoVegas Affiliates","Income Access Network",
    "Rizk Partners","Stake Affiliates","PlayAmo Partners","Fortune Affiliates",
    "Betsson Group Affiliates","22Bet Partners","Betwinner Affiliates","Coldbet Partners",
    "FoxSlots Partners","Rocketpot Affiliates","Bwin Affiliates","William Hill Partners",
    "Unibet Affiliates","PokerStars Affiliates","Betway Partners","Mr Green Affiliates",
    "Casumo Affiliates","Videoslots Partners","Fastpay Partners","N1 Partners",
    "Wildz Affiliates","Dunder Affiliates","Genesis Affiliates","Vera John Affiliates",
    "Guts Affiliates","Betsafe Partners","NordicBet Affiliates","SpinBet Affiliates",
    "MegaSlot Affiliates","CryptoLuck Partners","LuckyNova Partners","GrandWin Affiliates",
    "SilverPlay Partners","Odds96 Partners","C24 Partners","Boomerang Partners",
    "Partners1xbet","Parimatch Partners","Mostbet Affiliates","Melbet Partners",
    "PinUp Partners","1win Affiliates","GGBet Partners","BC.Game Affiliates",
    "BitStarz Partners","FortuneJack Affiliates","BetFury Affiliates","CloudBet Partners",
    "Rollbit Affiliates","JackBit Partners","NineCasino Affiliates","Sportsbet.io Partners",
    "Rabona Affiliates","BetChain Partners","1xSlots Affiliates","Sportaza Affiliates",
    "Haz Casino Partners","20Bet Affiliates","Playfina Affiliates","Legzo Partners",
    "Sol Casino Partners","Cat Casino Partners","Gama Affiliates","JVSpin Affiliates",
    "DrBet Partners","Mystake Partners","Paripesa Affiliates","Betano Affiliates",
    "Novibet Partners","NetBet Partners","BetVictor Affiliates","Betfair Affiliates",
    "Smarkets Partners","Fortuna Partners","Tipsport Affiliates","Tipico Partners",
    "Bettilt Affiliates","Betcris Affiliates","Coolbet Partners","LiveScore Partners",
    "Midnite Affiliates","Rootz Affiliates","MrQ Partners","SpinGenie Affiliates",
    "Jackpotjoy Partners","Virgin Games Affiliates","Pinnacle Affiliates","1xBet Partners",
    "Parimatch UA Partners","Favbet Affiliates","Vbet Partners","BetMGM Affiliates",
    "DraftKings Partners","FanDuel Affiliates","Caesars Affiliates","PointsBet Partners",
    "ESPN Bet Affiliates","Betclic Partners","Winamax Affiliates","Better Collective Affiliates",
    "Catena Media Partners","Raketech Affiliates","CasinoGuru Partners","Hacksaw Gaming Partners",
    "Push Gaming Affiliates","Evolution Partners","Playtech Affiliates","Pragmatic Partners",
    "NetEnt Affiliates","Red Tiger Affiliates","BGaming Affiliates","Spinomenal Partners",
    "Gamomat Partners","Wazdan Affiliates","Betsoft Partners","PG Soft Affiliates",
    "Spadegaming Partners","1spin4win Affiliates","Casiplay Affiliates","CasinoRoom Partners",
]
SRCS = ["AffPapa","GPWA","Affiliate Guard Dog","AskGamblers","SBC News","Gambling Insider","Reddit","Trustpilot"]
GEOS = ["EU","UK","CA","AU","US","SE","DE","FI","NO","UA","CIS","LATAM","APAC","Tier 1","Worldwide"]
LICS = ["MGA","UKGC","Curaçao","Gibraltar","Isle of Man","Kahnawake","Unknown"]
STATS = ["New","New","To Verify","To Verify","Verified","Verified","Verified","Verified","Rejected"]
PRIS = ["High","High","Medium","Medium","Low"]
COMS = ["RevShare 25-40%","RevShare 30-45%","CPA $50-150","CPA $100-200","Hybrid","RevShare 20-35%","RevShare 35-50%"]
NOTES = [
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

def calc_risk(row):
    s = 10
    if row.get("License") == "Unknown": s += 40
    if row.get("License") == "Curaçao": s += 12
    if row.get("Status") == "Rejected": s += 35
    if row.get("Status") == "To Verify": s += 18
    n = row.get("Notes","").lower()
    if "late payment" in n or "risk" in n or "unclear" in n: s += 18
    return min(s, 99)

def calc_opp(row):
    s = 25
    if row.get("Priority") == "High": s += 28
    if row.get("Status") == "Verified": s += 22
    g = row.get("GEO","")
    if "Tier 1" in g or "Worldwide" in g: s += 10
    c = row.get("Commission","")
    if "45" in c or "50" in c: s += 8
    n = row.get("Notes","").lower()
    if "stable" in n or "recommended" in n or "top performer" in n: s += 10
    if row.get("Status") == "New" and row.get("Priority") == "High": s += 6
    return min(s, 99)

def opp_reasons(row):
    r = []
    g = row.get("GEO","")
    if "Tier 1" in g: r.append("Tier 1 GEO")
    if "Worldwide" in g: r.append("Global reach")
    c = row.get("Commission","")
    if "45" in c or "50" in c: r.append("High RevShare")
    if row.get("License") in ["MGA","UKGC"]: r.append("Regulated license")
    if row.get("Status") == "New": r.append("New launch — first-mover advantage")
    n = row.get("Notes","").lower()
    if "stable" in n: r.append("Stable payout history")
    if "top performer" in n: r.append("Top performer in region")
    if "community" in n and "feedback" in n: r.append("Positive community signals")
    return r[:4] if r else ["Active program","Detected via trusted source"]

def generate(n=500):
    random.seed(42)
    nms = (NAMES * ((n // len(NAMES)) + 2))[:n]
    rows = []
    for i, name in enumerate(nms):
        if i < 8: days = 0
        elif i < 35: days = random.randint(1, 7)
        else: days = random.randint(1, 90)
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
               "GEO":geo,"License":lic,"Commission":com,"Status":st_,
               "Priority":pri,"Notes":note}
        row["Risk"] = calc_risk(row)
        row["Opp"] = calc_opp(row)
        rows.append(row)
    return pd.DataFrame(rows)

# Trend data (mock 30 days)
def trend_data():
    random.seed(7)
    days = [(TODAY_DT - timedelta(days=29-i)) for i in range(30)]
    return [(d.strftime("%b %d"), random.randint(8,28)) for d in days]

GEO_DIST = [("US",34),("UK",22),("CA",12),("AU",9),("SE",7),("DE",6),("EU",5),("UA",4)]
SRC_DIST = [("AffPapa",22),("GPWA",14),("SBC News",11),("Reddit",8),("AskGamblers",7),("SBC News",5),("Trustpilot",3)]

if "df" not in st.session_state: st.session_state.df = generate(500)
if "scan_log" not in st.session_state: st.session_state.scan_log = []
if "last_scan" not in st.session_state: st.session_state.last_scan = None
if "pg" not in st.session_state: st.session_state.pg = 0

NEW_POOL = [
    {"Name":"SpinBet Affiliates","Source":"SBC News","GEO":"EU, UA","License":"Curaçao","Commission":"RevShare 45%","Status":"New","Priority":"High","Notes":"High RevShare. New launch. No track record yet."},
    {"Name":"LuckyNova Partners","Source":"Reddit","GEO":"UA, EU","License":"Unknown","Commission":"CPA $120","Status":"To Verify","Priority":"High","Notes":"License unconfirmed. Community flagged."},
    {"Name":"NovaSpin Affiliates","Source":"Affiliate Guard Dog","GEO":"EU","License":"MGA","Commission":"RevShare 35%","Status":"New","Priority":"High","Notes":"Early detection. Solid MGA license."},
    {"Name":"StarNet Affiliates","Source":"SBC News","GEO":"Tier 1","License":"MGA","Commission":"RevShare 30-45%","Status":"New","Priority":"High","Notes":"Announced at SBC Summit. Strong team."},
    {"Name":"BetRocket Partners","Source":"AffPapa","GEO":"EU, CA","License":"Curaçao","Commission":"CPA $150","Status":"To Verify","Priority":"Medium","Notes":"New CPA program. Terms under review."},
]

# ── helpers ──
def sbadge(s):
    M={"New":("rgba(139,92,246,.14)","#A78BFA","rgba(139,92,246,.22)"),
       "To Verify":("rgba(245,158,11,.11)","#F59E0B","rgba(245,158,11,.18)"),
       "Verified":("rgba(34,197,94,.09)","#22C55E","rgba(34,197,94,.18)"),
       "Rejected":("rgba(239,68,68,.09)","#EF4444","rgba(239,68,68,.18)")}
    bg,c,b=M.get(s,M["New"])
    return f'<span style="font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;background:{bg};color:{c};border:1px solid {b};letter-spacing:.04em;">{s.upper()}</span>'

def rc(score, hi=70, md=40):
    if score>=hi: return "#EF4444"
    if score>=md: return "#F59E0B"
    return "#22C55E"

def oc(score, hi=70, md=40):
    if score>=hi: return "#22C55E"
    if score>=md: return "#F59E0B"
    return "#71717A"


# ══════════════════════════════════════════
# COMPUTED METRICS
# ══════════════════════════════════════════
df = st.session_state.df
W = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
total = len(df)
new_wk = len(df[df["Date Detected"] >= W])
today_n = len(df[df["Date Detected"] == TODAY])
to_ver = len(df[df["Status"] == "To Verify"])
verified = len(df[df["Status"] == "Verified"])
rejected = len(df[df["Status"] == "Rejected"])
crit_risk = len(df[df["Risk"] >= 70])
opps = len(df[(df["Opp"] >= 65) & (df["Status"].isin(["New","To Verify","Verified"]))])
hrs = max(28, round(new_wk * 0.45 + total * 0.04))
last_txt = st.session_state.last_scan.strftime("%d %b, %H:%M") if st.session_state.last_scan else "Today 09:00"


# ══════════════════════════════════════════
# TOP NAV BAR
# ══════════════════════════════════════════
st.markdown(f"""
<div style="padding:16px 0 0;display:flex;justify-content:space-between;align-items:center;
  margin-bottom:0;border-bottom:1px solid rgba(255,255,255,0.04);padding-bottom:16px;">
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="font-size:13px;font-weight:700;color:#7C3AED;letter-spacing:.12em;">◈</div>
    <div style="font-size:13px;font-weight:600;color:#FFFFFF;">Affiliate Intelligence Platform</div>
    <div style="height:12px;width:1px;background:rgba(255,255,255,0.1);"></div>
    <div style="font-size:12px;color:#3F3F46;">iGaming Ecosystem Monitor</div>
  </div>
  <div style="display:flex;align-items:center;gap:20px;">
    <div style="font-size:12px;color:#3F3F46;">Last scan: <span style="color:#52525B;">{last_txt}</span></div>
    <div style="font-size:12px;color:#3F3F46;">Next scan: <span style="color:#52525B;">Tomorrow 09:00</span></div>
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
tab1, tab2, tab3 = st.tabs(["  Intelligence Brief  ", "  Program Database  ", "  CEO Weekly Digest  "])


# ══════════════════════════════════════════════════════════
# TAB 1 — INTELLIGENCE BRIEF
# ══════════════════════════════════════════════════════════
with tab1:

    # ── EXECUTIVE BRIEF HERO ──
    st.markdown(f"""
    <div style="padding:48px 0 40px;">
      <div style="font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
        color:#4B21A0;margin-bottom:16px;">EXECUTIVE INTELLIGENCE BRIEF · {TODAY_DT.strftime('%A, %d %B %Y').upper()}</div>
      <div style="font-size:42px;font-weight:800;letter-spacing:-1.5px;line-height:1.15;
        color:#FFFFFF;margin-bottom:8px;">
        This week in the<br>
        <span style="background:linear-gradient(90deg,#A78BFA,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">iGaming affiliate ecosystem</span>
      </div>
      <div style="font-size:15px;color:#52525B;margin-top:12px;font-weight:400;letter-spacing:.01em;">
        {new_wk} new programs detected across {len(SRCS)} monitored sources
      </div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1px;
      background:rgba(255,255,255,0.04);border-radius:14px;overflow:hidden;margin-bottom:52px;">
      <div style="background:#0C0C0F;padding:28px 24px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
          color:#3F3F46;margin-bottom:12px;">New Programs</div>
        <div style="font-size:44px;font-weight:800;color:#FFFFFF;letter-spacing:-2px;line-height:1;">+{new_wk}</div>
        <div style="font-size:12px;color:#52525B;margin-top:8px;">detected this week</div>
      </div>
      <div style="background:#0C0C0F;padding:28px 24px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
          color:#3F3F46;margin-bottom:12px;">Opportunities</div>
        <div style="font-size:44px;font-weight:800;color:#A78BFA;letter-spacing:-2px;line-height:1;">{opps}</div>
        <div style="font-size:12px;color:#52525B;margin-top:8px;">worth review</div>
      </div>
      <div style="background:#0C0C0F;padding:28px 24px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
          color:#3F3F46;margin-bottom:12px;">Risk Signals</div>
        <div style="font-size:44px;font-weight:800;color:#EF4444;letter-spacing:-2px;line-height:1;">{crit_risk}</div>
        <div style="font-size:12px;color:#52525B;margin-top:8px;">flagged this week</div>
      </div>
      <div style="background:#0C0C0F;padding:28px 24px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
          color:#3F3F46;margin-bottom:12px;">Require Verification</div>
        <div style="font-size:44px;font-weight:800;color:#F59E0B;letter-spacing:-2px;line-height:1;">{to_ver}</div>
        <div style="font-size:12px;color:#52525B;margin-top:8px;">license or terms</div>
      </div>
      <div style="background:#0C0C0F;padding:28px 24px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
          color:#3F3F46;margin-bottom:12px;">Hours Saved</div>
        <div style="font-size:44px;font-weight:800;color:#22C55E;letter-spacing:-2px;line-height:1;">{hrs}h</div>
        <div style="font-size:12px;color:#52525B;margin-top:8px;">research automated</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HIGHEST VALUE OPPORTUNITIES ──
    st.markdown('<div class="sec-label">Highest Value Opportunities</div>', unsafe_allow_html=True)

    top_ops = df[(df["Opp"] >= 60)].sort_values("Opp", ascending=False).head(5)

    for _, row in top_ops.iterrows():
        reasons = opp_reasons(dict(row))
        opp_v = row["Opp"]
        risk_v = row["Risk"]
        urgency = "Review onboarding within 24h" if row["Priority"] == "High" else "Schedule review this week"
        urgency_c = "#EF4444" if row["Priority"] == "High" else "#F59E0B"
        geos = [g.strip() for g in row["GEO"].split(",")][:3]
        geo_html = "".join([f'<span style="font-size:11px;padding:3px 8px;border-radius:5px;background:rgba(255,255,255,0.04);color:#71717A;margin-right:5px;">{g}</span>' for g in geos])

        st.markdown(f"""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:16px;
          padding:28px 32px;margin-bottom:12px;display:grid;
          grid-template-columns:2fr 1fr 1fr 1.5fr;gap:32px;align-items:start;">

          <div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
              <div style="font-size:17px;font-weight:700;color:#FFFFFF;">{row['Name']}</div>
              {sbadge(row['Status'])}
            </div>
            <div style="font-size:12px;color:#3F3F46;margin-bottom:10px;">{row['Source']} · Detected {row['Date Detected']}</div>
            <div style="margin-bottom:10px;">{geo_html}</div>
            <div style="font-size:12px;color:#52525B;">{row['Commission']} · {row['License']}</div>
          </div>

          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
              color:#3F3F46;margin-bottom:10px;">Opportunity Score</div>
            <div style="font-size:36px;font-weight:800;color:{oc(opp_v)};letter-spacing:-1px;">{opp_v}</div>
            <div style="font-size:11px;color:#3F3F46;margin-top:2px;">/ 100</div>
          </div>

          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
              color:#3F3F46;margin-bottom:10px;">Risk Score</div>
            <div style="font-size:36px;font-weight:800;color:{rc(risk_v)};letter-spacing:-1px;">{risk_v}</div>
            <div style="font-size:11px;color:#3F3F46;margin-top:2px;">/ 100</div>
          </div>

          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
              color:#3F3F46;margin-bottom:10px;">Supporting Signals</div>
            {"".join([f'<div style="font-size:12px;color:#A1A1AA;margin-bottom:5px;display:flex;align-items:center;gap:6px;"><span style="color:#22C55E;font-size:10px;">✓</span>{r}</div>' for r in reasons])}
            <div style="margin-top:14px;font-size:12px;font-weight:600;color:{urgency_c};
              background:rgba(255,255,255,0.02);border-radius:6px;padding:8px 12px;
              border-left:2px solid {urgency_c};">→ {urgency}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── ALERT CENTER ──
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Intelligence Alerts</div>', unsafe_allow_html=True)

    alerts = [
        {
            "color":"rgba(139,92,246,0.35)","bg":"rgba(139,92,246,0.06)","border":"rgba(139,92,246,0.12)",
            "icon":"◈","label":"NEW SIGNAL","ac":"#A78BFA",
            "title":"High-RevShare Program Detected",
            "prog":"SpinBet Affiliates","src":"SBC News","geo":"EU, UA","lic":"Curaçao","comm":"RevShare 45%",
            "signal":"New affiliate program announced via SBC News with above-market revenue share of 45%. First detected today.",
            "evidence":"High RevShare typically indicates aggressive market entry. No prior track record found in GPWA or AffPapa databases.",
            "impact":"Potential early-partnership opportunity before program reaches saturation.",
            "rec":"Affiliate Manager to verify terms and license documentation within 24h.",
            "rec_c":"#A78BFA",
        },
        {
            "color":"rgba(245,158,11,0.35)","bg":"rgba(245,158,11,0.05)","border":"rgba(245,158,11,0.12)",
            "icon":"⚠","label":"VERIFICATION REQUIRED","ac":"#F59E0B",
            "title":"License Information Unconfirmed",
            "prog":"LuckyNova Partners","src":"Reddit (r/gambling)","geo":"UA, EU","lic":"Unknown","comm":"CPA $120",
            "signal":"Program surfaced via Reddit community discussion. License cannot be confirmed from MGA, UKGC, or Curaçao public registers.",
            "evidence":"3 separate posts in r/gambling report delayed affiliate payments. Program not listed in Affiliate Guard Dog verified directory.",
            "impact":"Engagement without license verification creates compliance and payment risk.",
            "rec":"Do not onboard. Affiliate Manager to verify licensing status before any contact.",
            "rec_c":"#F59E0B",
        },
        {
            "color":"rgba(239,68,68,0.35)","bg":"rgba(239,68,68,0.05)","border":"rgba(239,68,68,0.12)",
            "icon":"✕","label":"RISK FLAGGED","ac":"#EF4444",
            "title":"Reputation Risk — Delayed Payments",
            "prog":"Fortune Affiliates","src":"Affiliate Guard Dog","geo":"Worldwide","lic":"MGA","comm":"RevShare 25-40%",
            "signal":"Multiple affiliate payment delay reports filed on Affiliate Guard Dog over a 90-day period.",
            "evidence":"7 verified complaints in the last quarter. Pattern consistent with cashflow issues. Community trust score declining.",
            "impact":"Partnership risk is high. Delayed affiliate payments indicate financial instability in the program.",
            "rec":"Remove from active consideration. Do not onboard until minimum 6-month clean payment record is confirmed.",
            "rec_c":"#EF4444",
        },
    ]

    al_cols = st.columns(3)
    for i, a in enumerate(alerts):
        with al_cols[i]:
            st.markdown(f"""
            <div style="background:{a['bg']};border:1px solid {a['border']};
              border-top:2px solid {a['color']};border-radius:14px;padding:24px;height:100%;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
                <span style="font-size:11px;font-weight:700;padding:3px 8px;border-radius:4px;
                  background:{a['bg']};color:{a['ac']};border:1px solid {a['border']};
                  letter-spacing:.08em;">{a['label']}</span>
              </div>
              <div style="font-size:15px;font-weight:700;color:#FFFFFF;margin-bottom:6px;">{a['title']}</div>
              <div style="font-size:12px;color:#52525B;margin-bottom:16px;">{a['prog']} · {a['src']}</div>

              <div style="margin-bottom:10px;">
                <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#3F3F46;margin-bottom:5px;">Signal</div>
                <div style="font-size:12px;color:#A1A1AA;line-height:1.6;">{a['signal']}</div>
              </div>
              <div style="margin-bottom:10px;">
                <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#3F3F46;margin-bottom:5px;">Evidence</div>
                <div style="font-size:12px;color:#71717A;line-height:1.6;">{a['evidence']}</div>
              </div>
              <div style="margin-bottom:14px;">
                <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#3F3F46;margin-bottom:5px;">Impact</div>
                <div style="font-size:12px;color:#71717A;line-height:1.6;">{a['impact']}</div>
              </div>
              <div style="border-top:1px solid rgba(255,255,255,0.05);padding-top:14px;
                font-size:12px;font-weight:600;color:{a['rec_c']};">→ {a['rec']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── MARKET INTELLIGENCE ──
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Market Intelligence</div>', unsafe_allow_html=True)

    mi1, mi2, mi3 = st.columns(3)

    with mi1:
        st.markdown("""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:24px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
            color:#3F3F46;margin-bottom:20px;">Programs by GEO · This Week</div>
        """, unsafe_allow_html=True)
        max_v = max(v for _,v in GEO_DIST)
        for geo, val in GEO_DIST:
            pct = int(val/max_v*100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:11px;">
              <div style="font-size:12px;color:#71717A;width:28px;text-align:right;">{geo}</div>
              <div style="flex:1;height:4px;background:rgba(255,255,255,0.04);border-radius:2px;">
                <div style="height:4px;width:{pct}%;background:linear-gradient(90deg,#7C3AED,#A78BFA);border-radius:2px;"></div>
              </div>
              <div style="font-size:12px;color:#A1A1AA;font-weight:600;width:22px;">{val}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with mi2:
        src_dist = df[df["Date Detected"] >= W]["Source"].value_counts().head(8)
        st.markdown("""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:24px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
            color:#3F3F46;margin-bottom:20px;">Programs by Source · This Week</div>
        """, unsafe_allow_html=True)
        if len(src_dist) > 0:
            max_s = src_dist.max()
            for src, cnt in src_dist.items():
                pct = int(cnt/max_s*100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:11px;">
                  <div style="font-size:11px;color:#71717A;width:100px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;">{src}</div>
                  <div style="flex:1;height:4px;background:rgba(255,255,255,0.04);border-radius:2px;">
                    <div style="height:4px;width:{pct}%;background:linear-gradient(90deg,#22C55E,#86EFAC);border-radius:2px;"></div>
                  </div>
                  <div style="font-size:12px;color:#A1A1AA;font-weight:600;width:22px;">{cnt}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with mi3:
        td = trend_data()
        max_t = max(v for _,v in td)
        # Sparkline using inline bar chart
        bar_html = "".join([
            f'<div title="{d}: {v}" style="flex:1;background:linear-gradient(180deg,rgba(124,58,237,0.7),rgba(124,58,237,0.2));height:{int(v/max_t*60)+4}px;border-radius:2px 2px 0 0;min-width:6px;"></div>'
            for d, v in td
        ])
        recent_avg = round(sum(v for _,v in td[-7:])/7,1)
        prev_avg = round(sum(v for _,v in td[-14:-7])/7,1)
        delta = round(recent_avg - prev_avg, 1)
        delta_c = "#22C55E" if delta >= 0 else "#EF4444"
        delta_s = f"+{delta}" if delta >= 0 else str(delta)
        st.markdown(f"""
        <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:24px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
            color:#3F3F46;margin-bottom:6px;">New Launches · Last 30 Days</div>
          <div style="font-size:28px;font-weight:800;color:#FFFFFF;letter-spacing:-1px;margin-bottom:4px;">{sum(v for _,v in td)}</div>
          <div style="font-size:12px;color:#52525B;margin-bottom:20px;">
            7-day avg: <span style="color:#A1A1AA;">{recent_avg}/day</span> &nbsp;
            <span style="color:{delta_c};">{delta_s} vs prev week</span>
          </div>
          <div style="display:flex;align-items:flex-end;gap:2px;height:68px;
            border-bottom:1px solid rgba(255,255,255,0.04);padding-bottom:0;">
            {bar_html}
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:6px;">
            <div style="font-size:10px;color:#2E2E35;">May 13</div>
            <div style="font-size:10px;color:#2E2E35;">Jun 12</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SCAN STATUS (no button — automation feel) ──
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Monitoring Engine Status</div>', unsafe_allow_html=True)

    src_cards = [
        ("AffPapa","Affiliate Directory",12,94),("GPWA","Affiliate Forum",7,89),
        ("Affiliate Guard Dog","Watchdog",5,92),("AskGamblers","Review Platform",9,87),
        ("SBC News","Industry News",11,96),("Gambling Insider","Industry News",6,91),
        ("Reddit","Community Forum",8,72),("Trustpilot","Review Platform",3,83),
    ]
    sc_cols = st.columns(4)
    for i, (name, typ, found, rel) in enumerate(src_cards):
        with sc_cols[i % 4]:
            rel_c = "#22C55E" if rel >= 90 else ("#F59E0B" if rel >= 75 else "#EF4444")
            st.markdown(f"""
            <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);
              border-radius:12px;padding:18px 20px;margin-bottom:12px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                <div>
                  <div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:2px;">{name}</div>
                  <div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.06em;">{typ}</div>
                </div>
                <span style="font-size:9px;font-weight:700;padding:2px 7px;border-radius:3px;
                  background:rgba(34,197,94,0.08);color:#22C55E;border:1px solid rgba(34,197,94,0.15);">ACTIVE</span>
              </div>
              <div style="font-size:22px;font-weight:700;color:#FFFFFF;margin-bottom:2px;">{found}</div>
              <div style="font-size:11px;color:#3F3F46;margin-bottom:12px;">programs found this week</div>
              <div style="height:2px;background:rgba(255,255,255,0.04);border-radius:1px;">
                <div style="height:2px;width:{rel}%;background:{rel_c};border-radius:1px;opacity:.7;"></div>
              </div>
              <div style="font-size:11px;color:#3F3F46;margin-top:6px;">Reliability <span style="color:{rel_c};">{rel}%</span></div>
            </div>""", unsafe_allow_html=True)
        if (i+1) % 4 == 0 and i+1 < len(src_cards):
            sc_cols = st.columns(4)

    # Manual scan (secondary, minimal)
    st.markdown('<br>', unsafe_allow_html=True)
    sc1,sc2,sc3 = st.columns([1,4,1])
    with sc1:
        run = st.button("◈  Force Scan", use_container_width=True)
    with sc2:
        st.markdown(f"<div style='font-size:12px;color:#3F3F46;padding:10px 0;'>Automated scans run daily at 09:00. Last: {last_txt} · Sources checked: 8 · New findings: {today_n}</div>", unsafe_allow_html=True)

    if run:
        import time
        pb = st.progress(0,"Initializing...")
        for i,s in enumerate(SRCS):
            time.sleep(0.22)
            pb.progress((i+1)/len(SRCS), f"Scanning {s}...")
        time.sleep(0.2); pb.empty()
        ex = set(st.session_state.df["Name"])
        av = [p for p in NEW_POOL if p["Name"] not in ex] or NEW_POOL
        batch = random.sample(av, min(random.randint(3,5), len(av)))
        t = datetime.now()
        for p in batch:
            p["Date Detected"] = TODAY
            p["Risk"] = calc_risk(p); p["Opp"] = calc_opp(p)
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame(batch)], ignore_index=True)
        st.session_state.last_scan = t
        st.success(f"✅ Scan complete — {len(batch)} new programs detected.")
        st.rerun()


# ══════════════════════════════════════════════════════════
# TAB 2 — DATABASE
# ══════════════════════════════════════════════════════════
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
        st.download_button("⬇ Export CSV", buf.getvalue(), f"programs_{TODAY}.csv", "text/csv", use_container_width=True)
    with r3:
        if st.button("◀ Prev") and st.session_state.pg > 0:
            st.session_state.pg -= 1; st.rerun()
    with r4:
        if st.button("Next ▶") and st.session_state.pg < tpg-1:
            st.session_state.pg += 1; st.rerun()

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
            {''.join([f'<th style="padding:11px 16px;text-align:left;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#2E2E35;white-space:nowrap;">{h}</th>' for h in ["Program","Detected","Source","GEO","License","Commission","Status","Opp ↑","Risk ↑"]])}
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 3 — CEO DIGEST
# ══════════════════════════════════════════════════════════
with tab3:
    df = st.session_state.df
    wk = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
    nwdf = df[df["Date Detected"] >= wk].copy()
    top5 = nwdf.sort_values("Opp", ascending=False).head(5)
    risk5 = df[df["Risk"] >= 65].sort_values("Risk", ascending=False).head(5)
    ver_wk = nwdf[nwdf["Status"] == "Verified"]
    unk = len(df[df["License"] == "Unknown"])

    st.markdown(f"""
    <div style="padding:40px 0 32px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
        color:#4B21A0;margin-bottom:14px;">CONFIDENTIAL · EXECUTIVE REPORT</div>
      <div style="font-size:36px;font-weight:800;letter-spacing:-1px;color:#FFFFFF;margin-bottom:8px;">
        Weekly CEO Digest</div>
      <div style="font-size:14px;color:#3F3F46;">
        {(TODAY_DT-timedelta(days=6)).strftime('%d %b')} — {TODAY_DT.strftime('%d %b %Y')} &nbsp;·&nbsp;
        Prepared by Affiliate Intelligence Platform
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Savings banner
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
      background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.12);
      border-radius:14px;overflow:hidden;margin-bottom:40px;">
      {"".join([f'<div style="background:#060608;padding:24px 28px;"><div style="font-size:32px;font-weight:800;color:#22C55E;letter-spacing:-1px;">{v}</div><div style="font-size:10px;color:#3F3F46;text-transform:uppercase;letter-spacing:.1em;margin-top:4px;">{l}</div></div>' for v,l in [("~15h","Research saved"),( len(df),"Programs tracked"),( len(nwdf),"New this week"),( len(risk5),"Risks flagged")]])}
    </div>
    """, unsafe_allow_html=True)

    dg1, dg2 = st.columns([3,2])

    with dg1:
        st.markdown('<div class="sec-label">Top Opportunities This Week</div>', unsafe_allow_html=True)
        for rank, (_, row) in enumerate(top5.iterrows(), 1):
            reasons = opp_reasons(dict(row))
            occ = oc(row["Opp"]); rcc = rc(row["Risk"])
            st.markdown(f"""
            <div style="background:#0C0C0F;border:1px solid rgba(255,255,255,0.05);border-radius:12px;
              padding:20px 24px;margin-bottom:10px;display:grid;
              grid-template-columns:1.8fr .8fr .8fr;gap:20px;align-items:start;">
              <div>
                <div style="font-size:10px;color:#3F3F46;margin-bottom:6px;">#{rank}</div>
                <div style="font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:5px;">{row['Name']}</div>
                <div style="font-size:12px;color:#52525B;margin-bottom:8px;">{row['Source']} · {row['GEO']} · {row['Commission']}</div>
                {"".join([f'<div style="font-size:11px;color:#71717A;margin-bottom:3px;"><span style="color:#22C55E;">✓</span> {r}</div>' for r in reasons[:3]])}
              </div>
              <div style="text-align:center;">
                <div style="font-size:10px;color:#3F3F46;margin-bottom:6px;text-transform:uppercase;letter-spacing:.1em;">Opportunity</div>
                <div style="font-size:30px;font-weight:800;color:{occ};">{row['Opp']}</div>
                <div style="font-size:10px;color:#3F3F46;">/ 100</div>
              </div>
              <div style="text-align:center;">
                <div style="font-size:10px;color:#3F3F46;margin-bottom:6px;text-transform:uppercase;letter-spacing:.1em;">Risk</div>
                <div style="font-size:30px;font-weight:800;color:{rcc};">{row['Risk']}</div>
                <div style="font-size:10px;color:#3F3F46;">/ 100</div>
              </div>
            </div>""", unsafe_allow_html=True)

    with dg2:
        st.markdown('<div class="sec-label">Risk Flags</div>', unsafe_allow_html=True)
        for _, row in risk5.iterrows():
            rcc = rc(row["Risk"])
            st.markdown(f"""
            <div style="background:#0C0C0F;border:1px solid rgba(239,68,68,0.12);
              border-left:2px solid #EF4444;border-radius:10px;padding:16px 18px;margin-bottom:8px;">
              <div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:4px;">{row['Name']}</div>
              <div style="font-size:12px;color:#52525B;margin-bottom:6px;">{row['Notes']}</div>
              <div style="font-size:12px;color:{rcc};font-weight:700;">Risk Score: {row['Risk']}/100</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<br><div class="sec-label">Recommended Actions</div>', unsafe_allow_html=True)
        recs = [
            (f"Verify {len(risk5)} high-risk programs before any engagement","#EF4444"),
            (f"Review {unk} programs with unknown license status","#F59E0B"),
            ("Update verification statuses by Friday 15:00","#A78BFA"),
            ("Assign Affiliate Manager as process owner","#22C55E"),
            ("Schedule next intelligence review for Monday 09:00","#22C55E"),
        ]
        for rec, c in recs:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);
              border-left:2px solid {c};border-radius:8px;padding:12px 16px;margin-bottom:7px;
              font-size:13px;color:#A1A1AA;">→ {rec}</div>""", unsafe_allow_html=True)

    # Export
    st.markdown('<br><div class="sec-label">Export</div>', unsafe_allow_html=True)
    ex1,ex2,_ = st.columns([1,1,2])
    with ex1:
        b1=io.StringIO(); top5.to_csv(b1,index=False)
        st.download_button("⬇ Top Opportunities CSV", b1.getvalue(), f"opp_{TODAY}.csv","text/csv",use_container_width=True)
    with ex2:
        b2=io.StringIO(); risk5.to_csv(b2,index=False)
        st.download_button("⬇ Risk Flags CSV", b2.getvalue(), f"risks_{TODAY}.csv","text/csv",use_container_width=True)


# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:64px;padding:20px 0;border-top:1px solid rgba(255,255,255,0.03);
  display:flex;justify-content:space-between;align-items:center;">
  <div style="font-size:11px;color:#1E1E24;">© 2026 Affiliate Intelligence Platform · Internal use only</div>
  <div style="display:flex;gap:8px;">
    {"".join([f'<span style="font-size:10px;color:#2E2E35;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);padding:4px 10px;border-radius:4px;">{b}</span>' for b in ["MVP v1.0","Built in 48h","Budget <$200","Production Prototype"]])}
  </div>
</div>
""", unsafe_allow_html=True)
