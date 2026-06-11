import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import time
import io
import math

st.set_page_config(
    page_title="Affiliate Intelligence Platform",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
  background: #0A0A0A !important;
  color: #FFFFFF !important;
}

[data-testid="stAppViewContainer"] { background: #0A0A0A !important; }
[data-testid="stHeader"] { background: #0A0A0A !important; border-bottom: 1px solid rgba(255,255,255,0.06); }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1400px !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── TABS ── */
[data-testid="stTabs"] button {
  background: transparent !important;
  color: #A1A1AA !important;
  border: none !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  padding: 10px 20px !important;
  border-radius: 8px !important;
  transition: all 0.2s !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  background: rgba(124,58,237,0.15) !important;
  color: #A78BFA !important;
  border: 1px solid rgba(124,58,237,0.3) !important;
}
[data-testid="stTabs"] button:hover { color: #FFFFFF !important; background: rgba(255,255,255,0.05) !important; }
[data-testid="stTabsContent"] { padding-top: 24px !important; }
.stTabs [data-baseweb="tab-list"] {
  background: #111111 !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 10px !important;
  padding: 4px !important;
  gap: 4px !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
  background: #111111 !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important;
  padding: 20px !important;
  backdrop-filter: blur(12px);
  transition: border-color 0.2s, transform 0.2s;
}
[data-testid="metric-container"]:hover {
  border-color: rgba(124,58,237,0.3) !important;
  transform: translateY(-1px);
}
[data-testid="stMetricLabel"] { color: #A1A1AA !important; font-size: 11px !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 28px !important; font-weight: 700 !important; letter-spacing: -0.5px; }
[data-testid="stMetricDelta"] > div { font-size: 12px !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 10px 24px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  font-family: 'Inter', sans-serif !important;
  box-shadow: 0 0 20px rgba(124,58,237,0.3) !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  box-shadow: 0 0 32px rgba(124,58,237,0.5) !important;
  transform: translateY(-1px) !important;
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input {
  background: #111111 !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 8px !important;
  color: #FFFFFF !important;
  font-size: 14px !important;
  padding: 10px 14px !important;
}
[data-testid="stTextInput"] input:focus { border-color: rgba(124,58,237,0.5) !important; outline: none !important; }
[data-testid="stTextInput"] input::placeholder { color: #4B4B5A !important; }

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
  background: #111111 !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 8px !important;
  color: #FFFFFF !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}
.dvn-scroller { background: #111111 !important; }
[data-testid="stDataFrame"] th {
  background: #1A1A1A !important;
  color: #A1A1AA !important;
  font-size: 11px !important;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
[data-testid="stDataFrame"] td { color: #E4E4E7 !important; font-size: 13px !important; }

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
  background: rgba(255,255,255,0.05) !important;
  color: #A1A1AA !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  box-shadow: none !important;
}
[data-testid="stDownloadButton"] button:hover {
  background: rgba(255,255,255,0.08) !important;
  color: #FFFFFF !important;
  box-shadow: none !important;
  transform: none !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] { color: #7C3AED !important; }

/* ── SUCCESS ── */
[data-testid="stSuccess"] {
  background: rgba(34,197,94,0.1) !important;
  border: 1px solid rgba(34,197,94,0.3) !important;
  border-radius: 10px !important;
  color: #22C55E !important;
}

/* ── SECTION TITLE ── */
.section-title {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #52525B;
  margin: 36px 0 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex;
  align-items: center;
  gap: 8px;
}
.section-title::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 12px;
  background: #7C3AED;
  border-radius: 2px;
}

/* ── HERO ── */
.hero-wrap {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 28px 36px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}
.hero-wrap::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(124,58,237,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.hero-title {
  font-size: 24px;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: -0.5px;
  margin-bottom: 6px;
}
.hero-sub { font-size: 14px; color: #71717A; }
.live-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(34,197,94,0.08);
  border: 1px solid rgba(34,197,94,0.2);
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #22C55E;
  margin-bottom: 6px;
}
.live-pulse {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #22C55E;
  box-shadow: 0 0 6px #22C55E;
  animation: livepulse 1.8s ease-in-out infinite;
}
@keyframes livepulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
.last-scan-lbl { font-size: 11px; color: #52525B; text-align: right; }

/* ── EXEC SUMMARY CARDS ── */
.exec-card {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 22px 24px;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
}
.exec-card:hover { border-color: rgba(124,58,237,0.25); transform: translateY(-2px); }
.exec-card-icon { font-size: 20px; margin-bottom: 12px; }
.exec-card-val { font-size: 36px; font-weight: 800; letter-spacing: -1.5px; margin-bottom: 4px; }
.exec-card-label { font-size: 12px; color: #71717A; font-weight: 500; }
.exec-card-trend { position: absolute; top: 20px; right: 20px; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 5px; }
.trend-up { background: rgba(34,197,94,0.12); color: #22C55E; }
.trend-warn { background: rgba(245,158,11,0.12); color: #F59E0B; }
.trend-danger { background: rgba(239,68,68,0.12); color: #EF4444; }

/* ── SCAN ENGINE ── */
.scan-engine-card {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 24px 28px;
}
.scan-engine-title { font-size: 16px; font-weight: 600; color: #FFFFFF; margin-bottom: 4px; }
.scan-engine-sub { font-size: 13px; color: #71717A; margin-bottom: 20px; }
.log-box {
  background: #0D0D0D;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px;
  padding: 16px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.9;
  color: #22C55E;
  margin-top: 16px;
}

/* ── HIGH PRIORITY TABLE ── */
.priority-card {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 8px;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  align-items: center;
  gap: 12px;
  transition: background 0.15s;
}
.priority-card:hover { background: rgba(255,255,255,0.03); }
.priority-name { font-weight: 600; font-size: 14px; color: #FFFFFF; }
.priority-source { font-size: 12px; color: #71717A; }
.badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  white-space: nowrap;
}
.badge-new { background: rgba(124,58,237,0.15); color: #A78BFA; border: 1px solid rgba(124,58,237,0.25); }
.badge-verify { background: rgba(245,158,11,0.12); color: #F59E0B; border: 1px solid rgba(245,158,11,0.2); }
.badge-verified { background: rgba(34,197,94,0.1); color: #22C55E; border: 1px solid rgba(34,197,94,0.2); }
.badge-rejected { background: rgba(239,68,68,0.1); color: #EF4444; border: 1px solid rgba(239,68,68,0.2); }
.risk-high { color: #EF4444; font-size: 12px; font-weight: 600; }
.risk-med { color: #F59E0B; font-size: 12px; font-weight: 600; }
.risk-low { color: #22C55E; font-size: 12px; font-weight: 600; }

/* ── SOURCE CARDS ── */
.source-card {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 18px 20px;
  transition: border-color 0.2s;
}
.source-card:hover { border-color: rgba(124,58,237,0.3); }
.source-name { font-size: 14px; font-weight: 600; color: #FFFFFF; margin-bottom: 4px; }
.source-type { font-size: 11px; color: #52525B; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 12px; }
.source-row { font-size: 12px; color: #71717A; margin-bottom: 3px; }
.source-row span { color: #A1A1AA; }

/* ── ALERT CARDS ── */
.alert-card {
  border-radius: 12px;
  padding: 20px 22px;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}
.alert-card-purple { background: rgba(124,58,237,0.08); border: 1px solid rgba(124,58,237,0.2); }
.alert-card-amber { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); }
.alert-card-red { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); }
.alert-icon { font-size: 20px; margin-bottom: 10px; }
.alert-title { font-size: 14px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px; }
.alert-row { font-size: 13px; color: #71717A; margin-bottom: 4px; }
.alert-row strong { color: #D4D4D8; }
.alert-action { font-size: 13px; font-weight: 500; margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06); }
.action-purple { color: #A78BFA; }
.action-amber { color: #F59E0B; }
.action-red { color: #EF4444; }

/* ── DIGEST ── */
.digest-hero {
  background: linear-gradient(135deg, rgba(124,58,237,0.1) 0%, rgba(109,40,217,0.05) 100%);
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 16px;
  padding: 28px 32px;
  margin-bottom: 24px;
}
.digest-title { font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px; }
.digest-sub { font-size: 13px; color: #71717A; }

.savings-bar {
  background: rgba(34,197,94,0.06);
  border: 1px solid rgba(34,197,94,0.15);
  border-radius: 12px;
  padding: 18px 24px;
  display: flex;
  gap: 48px;
  align-items: center;
  margin-bottom: 24px;
}
.savings-item-val { font-size: 28px; font-weight: 800; color: #22C55E; letter-spacing: -1px; }
.savings-item-lbl { font-size: 11px; color: #52525B; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px; }

.digest-opp-card {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 18px 22px;
  margin-bottom: 10px;
  transition: border-color 0.2s;
}
.digest-opp-card:hover { border-color: rgba(124,58,237,0.25); }
.digest-opp-name { font-size: 15px; font-weight: 600; color: #FFFFFF; margin-bottom: 8px; }
.digest-opp-row { font-size: 13px; color: #71717A; margin-bottom: 3px; }
.digest-opp-row strong { color: #A1A1AA; }

.risk-flag-card {
  background: rgba(239,68,68,0.06);
  border: 1px solid rgba(239,68,68,0.15);
  border-radius: 10px;
  padding: 14px 18px;
  margin-bottom: 8px;
  font-size: 13px;
  color: #FCA5A5;
}
.rec-card {
  background: rgba(34,197,94,0.05);
  border: 1px solid rgba(34,197,94,0.12);
  border-radius: 10px;
  padding: 14px 18px;
  margin-bottom: 8px;
  font-size: 13px;
  color: #86EFAC;
}

/* ── STEP ITEMS ── */
.step-item {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 8px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
}
.step-num {
  background: rgba(124,58,237,0.15);
  color: #A78BFA;
  font-weight: 700;
  font-size: 11px;
  padding: 4px 9px;
  border-radius: 5px;
  min-width: 34px;
  text-align: center;
}
.step-title { font-weight: 600; color: #FFFFFF; font-size: 14px; margin-bottom: 2px; }
.step-desc { font-size: 13px; color: #71717A; }

/* ── TABLE HEADER ── */
.tbl-header {
  background: #111111;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  padding: 14px 18px;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  gap: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #52525B;
  margin-bottom: 6px;
}

/* ── FOOTER ── */
.app-footer {
  margin-top: 60px;
  padding: 24px 0;
  border-top: 1px solid rgba(255,255,255,0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.footer-left { font-size: 12px; color: #3F3F46; }
.footer-right { display: flex; gap: 20px; }
.footer-badge {
  font-size: 11px;
  color: #52525B;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  padding: 4px 10px;
  border-radius: 5px;
}

/* ── PAGINATION ── */
.page-info { font-size: 13px; color: #71717A; padding: 8px 0; }

hr { border-color: rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════ DATA ════════════════════════
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
    "Midnite Affiliates","Fansbet Affiliates","Rootz Affiliates","White Hat Gaming Affiliates",
    "ProgressPlay Partners","Nektan Affiliates","Cozy Games Partners","Relax Gaming Affiliates",
    "Pariplay Partners","Jumpman Partners","MrQ Partners","SpinGenie Affiliates",
    "Slingo Partners","Aspers Affiliates","Buzz Bingo Partners","Mecca Bingo Affiliates",
    "Jackpotjoy Partners","Heart Bingo Affiliates","Foxy Games Partners","Virgin Games Affiliates",
    "888Ladies Partners","Moon Games Affiliates","OddsMonkey Affiliates","Profit Accumulator Affiliates",
    "Pinnacle Affiliates","Betcris Partners","Betsson UA Affiliates","Fonbet Affiliates",
    "Liga Stavok Partners","Winline Affiliates","Leon Bet Partners","Marathonbet Affiliates",
    "Pari Affiliates","BetCity Partners","Olimp Affiliates","1xBet Partners",
    "Bwin UA Affiliates","Parimatch UA Partners","Favbet Affiliates","Vbet Partners",
    "FanSport Affiliates","BetMGM Affiliates","DraftKings Partners","FanDuel Affiliates",
    "Caesars Affiliates","PointsBet Partners","WynnBet Affiliates","Barstool Partners",
    "theScore Affiliates","Fox Bet Partners","BallyBet Affiliates","Golden Nugget Partners",
    "Hard Rock Affiliates","Rivers Casino Partners","Rush Street Partners","SugarHouse Affiliates",
    "ESPN Bet Affiliates","Tipwin Partners","Sportingbet Affiliates","Winner Affiliates",
    "Interwetten Partners","Eurobet Affiliates","Snai Partners","Lottomatica Affiliates",
    "Sisal Partners","Planetwin Affiliates","Better Partners","Betclic Partners",
    "Winamax Affiliates","PMU Partners","France Pari Affiliates","NetBet FR Partners",
    "JOA Partners","Barriere Affiliates","Partouche Partners","Ladbrokes BE Affiliates",
    "Circus Partners","Napoleon Games Affiliates","Betfirst Partners","Golden Palace Affiliates",
    "Unibet BE Partners","Viggoslots Affiliates","Catena Media Partners","Better Collective Affiliates",
    "XLMedia Partners","Raketech Affiliates","Gambling.com Partners","AskGamblers Affiliates",
    "CasinoGuru Partners","Slotegrator Affiliates","SoftSwiss Partners","BGaming Affiliates",
    "Spinomenal Partners","KA Gaming Affiliates","Hacksaw Gaming Partners","Avatar UX Partners",
    "Kalamba Games Affiliates","Triple Edge Partners","1spin4win Affiliates","Gamomat Partners",
    "Nolimit Partners","ReelPlay Affiliates","Stakelogic Partners","Booongo Affiliates",
    "Endorphina Partners","Wazdan Affiliates","Elk Studios Partners","Thunderspin Affiliates",
    "Betsoft Partners","Habanero Affiliates","GameArt Partners","PG Soft Affiliates",
    "Spadegaming Partners","CQ9 Affiliates","JDB Affiliates","FC Affiliates",
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
        if i < 8: days_ago = 0
        elif i < 30: days_ago = random.randint(1, 7)
        else: days_ago = random.randint(1, 90)
        detected = (TODAY_DT - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        status = random.choice(STATUS_WEIGHTS)
        if days_ago == 0: status = "New"
        elif days_ago <= 7: status = random.choice(["New","To Verify"])
        geo_sample = random.sample(GEO_LIST, random.randint(1,3))
        rows.append({
            "Name": name,
            "Date Detected": detected,
            "Source": random.choice(SOURCES_LIST),
            "GEO": ", ".join(geo_sample),
            "License": random.choice(LICENSE_LIST),
            "Commission": random.choice(COMMISSION_LIST),
            "Affiliate URL": name.lower().replace(" ","").replace("'","").replace("&","and")+".com/affiliates",
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
    {"Name":"StarAffiliates Network","Source":"SBC News","GEO":"Tier 1","License":"MGA","Commission":"RevShare 30-45%","Affiliate URL":"staraffiliates.com/partners","Status":"New","Priority":"High","Notes":"Announced at SBC Summit."},
    {"Name":"BetRocket Partners","Source":"AffPapa","GEO":"EU, CA","License":"Curaçao","Commission":"CPA $150","Affiliate URL":"betrocket.io/affiliates","Status":"To Verify","Priority":"Medium","Notes":"New CPA-focused program. Terms unclear."},
]

MONITORING_SOURCES = [
    {"Source":"AffPapa","Type":"Affiliate Directory","Monitors":"New listings, terms changes","Frequency":"Daily","Priority":"High","Last Checked":"Today 09:00"},
    {"Source":"GPWA","Type":"Affiliate Forum","Monitors":"Announcements, affiliate feedback","Frequency":"Daily","Priority":"High","Last Checked":"Today 09:01"},
    {"Source":"Affiliate Guard Dog","Type":"Watchdog Forum","Monitors":"Rogue programs, payment issues","Frequency":"3x/week","Priority":"High","Last Checked":"Today 09:02"},
    {"Source":"AskGamblers","Type":"Review Platform","Monitors":"New programs, complaints","Frequency":"Daily","Priority":"High","Last Checked":"Today 09:03"},
    {"Source":"SBC News","Type":"Industry News","Monitors":"New launches, partnerships","Frequency":"Daily","Priority":"High","Last Checked":"Today 09:04"},
    {"Source":"Gambling Insider","Type":"Industry News","Monitors":"Market launches, M&A","Frequency":"Daily","Priority":"Medium","Last Checked":"Today 09:05"},
    {"Source":"Reddit","Type":"Community Forum","Monitors":"Community buzz, warnings","Frequency":"Daily","Priority":"Medium","Last Checked":"Today 09:06"},
    {"Source":"Trustpilot","Type":"Review Platform","Monitors":"Reputation signals","Frequency":"Weekly","Priority":"Medium","Last Checked":"Jun 09"},
]

SOURCE_ICONS = {"AffPapa":"🔗","GPWA":"📋","Affiliate Guard Dog":"🛡","AskGamblers":"🎰",
                "SBC News":"📰","Gambling Insider":"📊","Reddit":"💬","Trustpilot":"⭐"}

# ── Session state
if "programs" not in st.session_state:
    st.session_state.programs = generate_programs(500)
if "scan_log" not in st.session_state:
    st.session_state.scan_log = []
if "last_scan" not in st.session_state:
    st.session_state.last_scan = None
if "page" not in st.session_state:
    st.session_state.page = 0


# ════════════════════════ HERO ════════════════════════
last_scan_text = st.session_state.last_scan.strftime("%d %b %Y, %H:%M") if st.session_state.last_scan else "12 Jun 2026, 09:00"
st.markdown(f"""
<div class="hero-wrap">
  <div>
    <div class="hero-title">Affiliate Intelligence Platform</div>
    <div class="hero-sub">Real-time monitoring of affiliate programs across the iGaming ecosystem.</div>
  </div>
  <div style="text-align:right;">
    <div class="live-badge"><span class="live-pulse"></span> LIVE</div>
    <div class="last-scan-lbl">Last scan: {last_scan_text}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════ TABS ════════════════════════
tab1, tab2 = st.tabs(["📊  Monitor", "📋  Weekly CEO Digest"])


# ═══════════════════════════════════════════
# TAB 1
# ═══════════════════════════════════════════
with tab1:
    df = st.session_state.programs
    week_ago_str = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
    total = len(df)
    new_this_week = len(df[df["Date Detected"] >= week_ago_str])
    today_detected = len(df[df["Date Detected"] == TODAY])
    to_verify = len(df[df["Status"] == "To Verify"])
    verified = len(df[df["Status"] == "Verified"])
    rejected = len(df[df["Status"] == "Rejected"])
    high_risk = len(df[(df["Status"].isin(["To Verify","Rejected"])) & (df["Priority"] == "High")])
    hours_saved = round(total * 0.06)

    # ── Executive Summary
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
    e1,e2,e3,e4 = st.columns(4)
    with e1:
        st.markdown(f"""
        <div class="exec-card">
          <div class="exec-card-icon">🆕</div>
          <div class="exec-card-trend trend-up">↑ +{new_this_week}</div>
          <div class="exec-card-val" style="color:#A78BFA;">{new_this_week}</div>
          <div class="exec-card-label">New Programs This Week</div>
        </div>""", unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
        <div class="exec-card">
          <div class="exec-card-icon">⚠️</div>
          <div class="exec-card-trend trend-warn">Needs action</div>
          <div class="exec-card-val" style="color:#F59E0B;">{to_verify}</div>
          <div class="exec-card-label">Programs Requiring Verification</div>
        </div>""", unsafe_allow_html=True)
    with e3:
        st.markdown(f"""
        <div class="exec-card">
          <div class="exec-card-icon">🚨</div>
          <div class="exec-card-trend trend-danger">High priority</div>
          <div class="exec-card-val" style="color:#EF4444;">{high_risk}</div>
          <div class="exec-card-label">High Risk Programs</div>
        </div>""", unsafe_allow_html=True)
    with e4:
        st.markdown(f"""
        <div class="exec-card">
          <div class="exec-card-icon">⏱️</div>
          <div class="exec-card-trend trend-up">This week</div>
          <div class="exec-card-val" style="color:#22C55E;">{hours_saved}h</div>
          <div class="exec-card-label">Estimated Research Hours Saved</div>
        </div>""", unsafe_allow_html=True)

    # ── KPI Dashboard
    st.markdown('<div class="section-title">KPI Dashboard</div>', unsafe_allow_html=True)
    k1,k2,k3,k4,k5,k6,k7 = st.columns(7)
    k1.metric("Total Programs", total)
    k2.metric("New This Week", new_this_week, delta=f"+{new_this_week}")
    k3.metric("Detected Today", today_detected, delta=f"+{today_detected}")
    k4.metric("To Verify", to_verify)
    k5.metric("Verified", verified)
    k6.metric("Rejected", rejected)
    k7.metric("Sources Active", len(MONITORING_SOURCES))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Scan Engine
    st.markdown('<div class="section-title">Monitoring Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="scan-engine-card">', unsafe_allow_html=True)
    sc1, sc2 = st.columns([3,2])
    with sc1:
        st.markdown('<div class="scan-engine-title">Monitoring Engine</div>', unsafe_allow_html=True)
        st.markdown('<div class="scan-engine-sub">Automated scan across 8 iGaming intelligence sources. Detects new affiliate programs and flags risks in real time.</div>', unsafe_allow_html=True)
    with sc2:
        run_scan = st.button("🔍  Run New Scan", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if run_scan:
        progress_bar = st.progress(0, text="Initializing scan...")
        steps = ["AffPapa","GPWA","SBC News","Affiliate Guard Dog","AskGamblers","Trustpilot","Reddit","Gambling Insider"]
        for i, src in enumerate(steps):
            time.sleep(0.3)
            progress_bar.progress((i+1)/len(steps), text=f"Scanning {src}...")
        time.sleep(0.3)
        progress_bar.empty()

        existing = set(st.session_state.programs["Name"].tolist())
        available = [p for p in NEW_POOL if p["Name"] not in existing] or NEW_POOL
        n_new = random.randint(3,5)
        batch = random.sample(available, min(n_new, len(available)))
        scan_time = datetime.now()
        new_df = pd.DataFrame([{**p, "Date Detected": TODAY} for p in batch])
        st.session_state.programs = pd.concat([st.session_state.programs, new_df], ignore_index=True)
        st.session_state.last_scan = scan_time

        log = [f"[{scan_time.strftime('%H:%M:%S')}] Scan initiated — {len(MONITORING_SOURCES)} sources active"]
        for src in steps:
            log.append(f"[{scan_time.strftime('%H:%M:%S')}]  ↳ {src} — OK")
        for p in batch:
            log.append(f"[{scan_time.strftime('%H:%M:%S')}]  ✓ DETECTED: {p['Name']} via {p['Source']} — {p['Status']}")
        log.append(f"[{scan_time.strftime('%H:%M:%S')}] ✅ Scan complete — {len(batch)} new programs detected")
        st.session_state.scan_log = log
        st.success(f"✅ Scan completed — {len(batch)} new affiliate programs detected.")
        st.rerun()

    if st.session_state.scan_log:
        st.markdown(f'<div class="log-box">{"<br>".join(st.session_state.scan_log)}</div>', unsafe_allow_html=True)

    # ── High Priority Discoveries
    st.markdown('<div class="section-title">High Priority Discoveries</div>', unsafe_allow_html=True)
    df = st.session_state.programs
    high_prio = df[df["Priority"] == "High"].sort_values("Date Detected", ascending=False).head(10)

    def status_badge(s):
        if s == "New": return '<span class="badge badge-new">New</span>'
        if s == "To Verify": return '<span class="badge badge-verify">To Verify</span>'
        if s == "Verified": return '<span class="badge badge-verified">Verified</span>'
        return '<span class="badge badge-rejected">Rejected</span>'

    def risk_label(row):
        if row["License"] == "Unknown" or row["Status"] == "Rejected":
            return '<span class="risk-high">HIGH</span>'
        if row["Status"] == "To Verify":
            return '<span class="risk-med">MEDIUM</span>'
        return '<span class="risk-low">LOW</span>'

    st.markdown("""
    <div class="tbl-header">
      <div>Program</div><div>Source</div><div>GEO</div><div>Commission</div><div>Status</div><div>Risk</div>
    </div>""", unsafe_allow_html=True)

    for _, row in high_prio.iterrows():
        st.markdown(f"""
        <div class="priority-card">
          <div><div class="priority-name">{row['Name']}</div><div class="priority-source">{row['Date Detected']}</div></div>
          <div style="font-size:12px;color:#A1A1AA;">{row['Source']}</div>
          <div style="font-size:12px;color:#A1A1AA;">{row['GEO']}</div>
          <div style="font-size:12px;color:#A1A1AA;">{row['Commission']}</div>
          <div>{status_badge(row['Status'])}</div>
          <div>{risk_label(row)}</div>
        </div>""", unsafe_allow_html=True)

    # ── Full Database
    st.markdown('<div class="section-title">Affiliate Programs Database</div>', unsafe_allow_html=True)
    df = st.session_state.programs

    f1,f2,f3,f4,f5 = st.columns(5)
    with f1: search = st.text_input("Search", placeholder="Program name...")
    with f2: status_f = st.selectbox("Status", ["All"] + sorted(df["Status"].unique().tolist()))
    with f3: priority_f = st.selectbox("Priority", ["All","High","Medium","Low"])
    with f4: source_f = st.selectbox("Source", ["All"] + sorted(df["Source"].unique().tolist()))
    with f5:
        geo_opts = sorted(set(g.strip() for geos in df["GEO"].str.split(",") for g in geos))
        geo_f = st.selectbox("GEO", ["All"] + geo_opts)

    filtered = df.copy()
    if search: filtered = filtered[filtered["Name"].str.contains(search, case=False, na=False)]
    if status_f != "All": filtered = filtered[filtered["Status"] == status_f]
    if priority_f != "All": filtered = filtered[filtered["Priority"] == priority_f]
    if source_f != "All": filtered = filtered[filtered["Source"] == source_f]
    if geo_f != "All": filtered = filtered[filtered["GEO"].str.contains(geo_f, case=False, na=False)]

    filtered_sorted = filtered.sort_values("Date Detected", ascending=False).reset_index(drop=True)

    rows_per_page = 20
    total_pages = max(1, math.ceil(len(filtered_sorted) / rows_per_page))
    if st.session_state.page >= total_pages:
        st.session_state.page = 0

    rc, ec, pc1, pc2, pc3 = st.columns([3,2,1,1,1])
    with rc:
        st.markdown(f"<div class='page-info'>Showing <strong>{len(filtered_sorted)}</strong> of <strong>{len(df)}</strong> programs — Page {st.session_state.page+1} / {total_pages}</div>", unsafe_allow_html=True)
    with ec:
        buf = io.StringIO()
        filtered_sorted.to_csv(buf, index=False)
        st.download_button("⬇ Export CSV", buf.getvalue(), f"affiliate_programs_{TODAY}.csv", "text/csv", use_container_width=True)
    with pc1:
        if st.button("◀ Prev") and st.session_state.page > 0:
            st.session_state.page -= 1
            st.rerun()
    with pc2:
        if st.button("Next ▶") and st.session_state.page < total_pages - 1:
            st.session_state.page += 1
            st.rerun()

    page_df = filtered_sorted.iloc[st.session_state.page*rows_per_page:(st.session_state.page+1)*rows_per_page].copy()

    def badge_html(s):
        if s == "New":       return '<span style="display:inline-block;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;background:rgba(124,58,237,0.15);color:#A78BFA;border:1px solid rgba(124,58,237,0.25);">New</span>'
        if s == "To Verify": return '<span style="display:inline-block;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;background:rgba(245,158,11,0.12);color:#F59E0B;border:1px solid rgba(245,158,11,0.2);">To Verify</span>'
        if s == "Verified":  return '<span style="display:inline-block;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;background:rgba(34,197,94,0.1);color:#22C55E;border:1px solid rgba(34,197,94,0.2);">Verified</span>'
        return                       '<span style="display:inline-block;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;background:rgba(239,68,68,0.1);color:#EF4444;border:1px solid rgba(239,68,68,0.2);">Rejected</span>'

    def priority_html(p):
        if p == "High":   return '<span style="color:#EF4444;font-size:12px;font-weight:600;">High</span>'
        if p == "Medium": return '<span style="color:#F59E0B;font-size:12px;font-weight:600;">Medium</span>'
        return                    '<span style="color:#71717A;font-size:12px;font-weight:600;">Low</span>'

    rows_html = ""
    for _, r in page_df.iterrows():
        rows_html += f"""
        <tr>
          <td style="padding:12px 14px;color:#FFFFFF;font-weight:500;font-size:13px;">{r['Name']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:13px;">{r['Date Detected']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:13px;">{r['Source']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:13px;">{r['GEO']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:13px;">{r['License']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:13px;">{r['Commission']}</td>
          <td style="padding:12px 14px;">{badge_html(r['Status'])}</td>
          <td style="padding:12px 14px;">{priority_html(r['Priority'])}</td>
          <td style="padding:12px 14px;color:#52525B;font-size:12px;max-width:200px;">{r['Notes']}</td>
        </tr>"""

    table_html = f"""
    <div style="overflow-x:auto;border-radius:12px;border:1px solid rgba(255,255,255,0.08);">
      <table style="width:100%;border-collapse:collapse;background:#111111;">
        <thead>
          <tr style="background:#18181B;border-bottom:1px solid rgba(255,255,255,0.08);">
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">Program</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">Detected</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">Source</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">GEO</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">License</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">Commission</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">Status</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">Priority</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">Notes</th>
          </tr>
        </thead>
        <tbody>
          {''.join(['<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">' + r[4:] if i % 2 == 1 else r for i, r in enumerate(rows_html.strip().split('<tr>')[1:])])}
        </tbody>
      </table>
    </div>"""

    # Simpler, more reliable render
    rows_final = ""
    for i, (_, r) in enumerate(page_df.iterrows()):
        bg = "background:rgba(255,255,255,0.015);" if i % 2 == 1 else ""
        rows_final += f"""<tr style="border-bottom:1px solid rgba(255,255,255,0.04);{bg}">
          <td style="padding:12px 14px;color:#FFFFFF;font-weight:500;font-size:13px;">{r['Name']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:12px;white-space:nowrap;">{r['Date Detected']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:12px;">{r['Source']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:12px;">{r['GEO']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:12px;">{r['License']}</td>
          <td style="padding:12px 14px;color:#A1A1AA;font-size:12px;">{r['Commission']}</td>
          <td style="padding:12px 14px;">{badge_html(r['Status'])}</td>
          <td style="padding:12px 14px;">{priority_html(r['Priority'])}</td>
          <td style="padding:12px 14px;color:#52525B;font-size:12px;">{r['Notes']}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin-top:8px;">
      <table style="width:100%;border-collapse:collapse;background:#111111;">
        <thead>
          <tr style="background:#18181B;border-bottom:1px solid rgba(255,255,255,0.08);">
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">Program</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;white-space:nowrap;">Detected</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">Source</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">GEO</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">License</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">Commission</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">Status</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">Priority</th>
            <th style="padding:11px 14px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#52525B;">Notes</th>
          </tr>
        </thead>
        <tbody>{rows_final}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    # ── Monitoring Sources
    st.markdown('<div class="section-title">Monitoring Sources</div>', unsafe_allow_html=True)
    src_cols = st.columns(4)
    for i, src in enumerate(MONITORING_SOURCES):
        with src_cols[i % 4]:
            icon = SOURCE_ICONS.get(src["Source"], "🔗")
            prio_color = "#22C55E" if src["Priority"] == "High" else "#F59E0B"
            st.markdown(f"""
            <div class="source-card">
              <div style="font-size:22px;margin-bottom:8px;">{icon}</div>
              <div class="source-name">{src['Source']}</div>
              <div class="source-type">{src['Type']}</div>
              <div class="source-row">Monitors: <span>{src['Monitors']}</span></div>
              <div class="source-row">Frequency: <span>{src['Frequency']}</span></div>
              <div class="source-row">Priority: <span style="color:{prio_color};font-weight:600;">{src['Priority']}</span></div>
              <div class="source-row">Last checked: <span>{src['Last Checked']}</span></div>
            </div>""", unsafe_allow_html=True)
        if (i+1) % 4 == 0 and i+1 < len(MONITORING_SOURCES):
            src_cols = st.columns(4)

    # ── Alert Center
    st.markdown('<div class="section-title">Alert Center</div>', unsafe_allow_html=True)
    al1,al2,al3 = st.columns(3)
    with al1:
        st.markdown("""
        <div class="alert-card alert-card-purple">
          <div class="alert-icon">🟣</div>
          <div class="alert-title">New Program Detected</div>
          <div class="alert-row"><strong>Program:</strong> SpinBet Affiliates</div>
          <div class="alert-row"><strong>Source:</strong> SBC News &nbsp;|&nbsp; <strong>GEO:</strong> EU, UA</div>
          <div class="alert-row"><strong>Commission:</strong> RevShare 45%</div>
          <div class="alert-row"><strong>License:</strong> Curaçao</div>
          <div class="alert-row"><strong>Signal:</strong> High RevShare. No established track record.</div>
          <div class="alert-action action-purple">→ Affiliate Manager to verify within 24h</div>
        </div>""", unsafe_allow_html=True)
    with al2:
        st.markdown("""
        <div class="alert-card alert-card-amber">
          <div class="alert-icon">🟡</div>
          <div class="alert-title">License Verification Required</div>
          <div class="alert-row"><strong>Program:</strong> LuckyNova Partners</div>
          <div class="alert-row"><strong>Source:</strong> Reddit &nbsp;|&nbsp; <strong>GEO:</strong> UA, EU</div>
          <div class="alert-row"><strong>License:</strong> Unknown</div>
          <div class="alert-row"><strong>Signal:</strong> Delayed payment reports in affiliate community.</div>
          <div class="alert-row"><strong>Risk:</strong> High</div>
          <div class="alert-action action-amber">→ Verify licensing before any engagement</div>
        </div>""", unsafe_allow_html=True)
    with al3:
        st.markdown("""
        <div class="alert-card alert-card-red">
          <div class="alert-icon">🔴</div>
          <div class="alert-title">Reputation Risk Flagged</div>
          <div class="alert-row"><strong>Program:</strong> Fortune Affiliates</div>
          <div class="alert-row"><strong>Source:</strong> Affiliate Guard Dog</div>
          <div class="alert-row"><strong>License:</strong> MGA</div>
          <div class="alert-row"><strong>Signal:</strong> Consistent slow payment pattern — 3 months.</div>
          <div class="alert-row"><strong>Risk:</strong> High</div>
          <div class="alert-action action-red">→ Do not onboard until reputation confirmed</div>
        </div>""", unsafe_allow_html=True)

    # ── Next Steps
    st.markdown('<div class="section-title">Next Steps — Scaling to Production</div>', unsafe_allow_html=True)
    steps = [
        ("01","Connect live scrapers / APIs","Apify or ParseHub for AffPapa, GPWA, SBC News. WhoisXML API for new domain detection."),
        ("02","Add deduplication logic","Prevent same program appearing from multiple sources. Match by name + URL fingerprint."),
        ("03","Set up scheduled scans","Automate daily scan at 09:00 via cron job or Make.com. Zero manual trigger needed."),
        ("04","Assign business owner","Affiliate Manager or SEO Head owns weekly verification. Clear SLA: 48h per new program."),
        ("05","Add Slack / email alerts","Trigger real-time alerts to #affiliate-intel on every High Priority detection."),
        ("06","Build automated CEO Digest","Auto-generate Monday morning summary. Already prototyped in CEO Digest tab."),
    ]
    st1,st2 = st.columns(2)
    for i,(num,title,desc) in enumerate(steps):
        with (st1 if i%2==0 else st2):
            st.markdown(f"""
            <div class="step-item">
              <div class="step-num">{num}</div>
              <div><div class="step-title">{title}</div><div class="step-desc">{desc}</div></div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# TAB 2 — CEO DIGEST
# ═══════════════════════════════════════════
with tab2:
    df = st.session_state.programs
    week_ago_str = (TODAY_DT - timedelta(days=7)).strftime("%Y-%m-%d")
    new_week_df = df[df["Date Detected"] >= week_ago_str].copy()
    top5 = new_week_df.sort_values("Date Detected", ascending=False).head(5)
    risks = df[(df["Status"] == "To Verify") & (df["Priority"] == "High")].head(3)
    verified_week = new_week_df[new_week_df["Status"] == "Verified"]
    unknown_lic = len(df[df["License"] == "Unknown"])

    st.markdown(f"""
    <div class="digest-hero">
      <div class="digest-title">📋 Weekly CEO Digest</div>
      <div class="digest-sub">Week of {(TODAY_DT - timedelta(days=6)).strftime('%d %b')} — {TODAY_DT.strftime('%d %b %Y')} &nbsp;·&nbsp; Auto-generated by Affiliate Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="savings-bar">
      <div><div class="savings-item-val">~15h</div><div class="savings-item-lbl">Manual research avoided</div></div>
      <div><div class="savings-item-val">{len(df)}</div><div class="savings-item-lbl">Programs reviewed automatically</div></div>
      <div><div class="savings-item-val">{len(MONITORING_SOURCES)}</div><div class="savings-item-lbl">Sources monitored continuously</div></div>
      <div><div class="savings-item-val">{len(new_week_df)}</div><div class="savings-item-lbl">New programs detected</div></div>
    </div>
    """, unsafe_allow_html=True)

    d1,d2,d3,d4 = st.columns(4)
    d1.metric("New This Week", len(new_week_df))
    d2.metric("High Priority — To Verify", len(risks))
    d3.metric("Verified This Week", len(verified_week))
    d4.metric("Unknown License", unknown_lic)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Top Opportunities This Week</div>', unsafe_allow_html=True)
    if len(top5) == 0:
        st.info("No new programs this week. Run a scan to populate.")
    else:
        for _, row in top5.iterrows():
            st.markdown(f"""
            <div class="digest-opp-card">
              <div class="digest-opp-name">{row['Name']}</div>
              <div class="digest-opp-row"><strong>Source:</strong> {row['Source']} &nbsp;|&nbsp; <strong>GEO:</strong> {row['GEO']} &nbsp;|&nbsp; <strong>Commission:</strong> {row['Commission']}</div>
              <div class="digest-opp-row"><strong>License:</strong> {row['License']} &nbsp;|&nbsp; <strong>Status:</strong> {row['Status']} &nbsp;|&nbsp; <strong>Priority:</strong> {row['Priority']}</div>
              <div class="digest-opp-row" style="margin-top:8px;color:#52525B;">{row['Notes']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Risk Flags</div>', unsafe_allow_html=True)
    if len(risks) == 0:
        st.success("No high-priority risks this week.")
    else:
        for _, row in risks.iterrows():
            st.markdown(f'<div class="risk-flag-card">⚠️ <strong>{row["Name"]}</strong> — {row["Notes"]} | Source: {row["Source"]} | License: {row["License"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Recommended Actions</div>', unsafe_allow_html=True)
    recs = [
        f"Affiliate Manager to verify {len(risks)} high-priority programs flagged this week.",
        f"Review {unknown_lic} programs with unknown license before engagement.",
        "Update verification status in database by Friday 15:00.",
        "Monitor SpinBet Affiliates and LuckyNova — community signals mixed.",
        "Schedule weekly scan every Monday 09:00 to automate detection pipeline.",
    ]
    for rec in recs:
        st.markdown(f'<div class="rec-card">✅ {rec}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
    ex1, ex2 = st.columns(2)
    with ex1:
        buf2 = io.StringIO()
        top5.to_csv(buf2, index=False)
        st.download_button("⬇ Export Top Opportunities CSV", buf2.getvalue(), f"ceo_digest_{TODAY}.csv", "text/csv", use_container_width=True)
    with ex2:
        buf3 = io.StringIO()
        risks.to_csv(buf3, index=False)
        st.download_button("⬇ Export Risk Flags CSV", buf3.getvalue(), f"risk_flags_{TODAY}.csv", "text/csv", use_container_width=True)


# ════════════════════════ FOOTER ════════════════════════
st.markdown(f"""
<div class="app-footer">
  <div class="footer-left">© 2026 Affiliate Intelligence Platform. Internal use only.</div>
  <div class="footer-right">
    <span class="footer-badge">MVP v1.0</span>
    <span class="footer-badge">Built in 48h</span>
    <span class="footer-badge">Budget &lt;$200</span>
    <span class="footer-badge">Status: Production Prototype</span>
  </div>
</div>
""", unsafe_allow_html=True)
