import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Affiliate Programs Monitor",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Base */
  [data-testid="stAppViewContainer"] { background: #0f0f13; }
  [data-testid="stHeader"] { background: transparent; }
  section[data-testid="stSidebar"] { background: #17171e; }

  /* Typography */
  html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: #e8e8f0;
  }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: #17171e;
    border: 1px solid #2a2a36;
    border-radius: 10px;
    padding: 16px 20px;
  }
  [data-testid="stMetricLabel"] { color: #6b6b80 !important; font-size: 12px !important; }
  [data-testid="stMetricValue"] { color: #e8e8f0 !important; font-size: 28px !important; font-weight: 600 !important; }

  /* Dataframe */
  [data-testid="stDataFrame"] { border: 1px solid #2a2a36; border-radius: 10px; overflow: hidden; }
  .dvn-scroller { background: #17171e !important; }

  /* Buttons */
  .stButton > button {
    background: #7c6bff;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 500;
    font-size: 14px;
    transition: opacity 0.15s;
  }
  .stButton > button:hover { opacity: 0.85; background: #7c6bff; color: #fff; border: none; }

  /* Selectbox */
  [data-testid="stSelectbox"] > div > div {
    background: #17171e;
    border: 1px solid #2a2a36;
    border-radius: 8px;
    color: #e8e8f0;
  }

  /* Section headers */
  .section-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b6b80;
    margin: 32px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #2a2a36;
  }

  /* Alert cards */
  .alert-card {
    background: #17171e;
    border: 1px solid #2a2a36;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
  }
  .alert-card.new { border-left: 3px solid #7c6bff; }
  .alert-card.verify { border-left: 3px solid #fbbf24; }
  .alert-card.risk { border-left: 3px solid #f87171; }

  .alert-title { font-weight: 600; font-size: 14px; margin-bottom: 8px; }
  .alert-row { font-size: 13px; color: #9999b0; margin-bottom: 4px; }
  .alert-row strong { color: #e8e8f0; }

  /* Next steps */
  .step-item {
    background: #17171e;
    border: 1px solid #2a2a36;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 14px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
  }
  .step-num {
    color: #7c6bff;
    font-weight: 700;
    font-size: 13px;
    min-width: 22px;
  }

  /* Scan log */
  .log-box {
    background: #0d0d11;
    border: 1px solid #2a2a36;
    border-radius: 8px;
    padding: 14px 16px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #34d399;
    line-height: 1.8;
  }

  /* Footer */
  .footer {
    margin-top: 48px;
    padding-top: 16px;
    border-top: 1px solid #2a2a36;
    text-align: center;
    font-size: 12px;
    color: #6b6b80;
  }

  /* Status badges */
  .badge-new { color: #7c6bff; font-weight: 600; }
  .badge-verify { color: #fbbf24; font-weight: 600; }
  .badge-verified { color: #34d399; font-weight: 600; }

  /* Live dot */
  .live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #34d399;
  }
  .live-dot {
    width: 7px;
    height: 7px;
    background: #34d399;
    border-radius: 50%;
    display: inline-block;
  }

  /* Divider */
  hr { border-color: #2a2a36 !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "programs" not in st.session_state:
    st.session_state.programs = pd.DataFrame([
        {
            "Name": "Bet365 Partners",
            "Date Detected": "2026-05-10",
            "Source": "AffPapa",
            "GEO": "EU, UK, AU",
            "License": "UKGC",
            "Affiliate URL": "partners.bet365.com",
            "Status": "Verified",
            "Priority": "High",
            "Notes": "One of the largest programs globally. Stable payouts."
        },
        {
            "Name": "888 Affiliates",
            "Date Detected": "2026-05-12",
            "Source": "AffPapa",
            "GEO": "EU, UK, CA",
            "License": "UKGC, Gibraltar",
            "Affiliate URL": "888affiliates.com",
            "Status": "Verified",
            "Priority": "High",
            "Notes": "Long-established program. Lower rev share vs newer players."
        },
        {
            "Name": "LeoVegas Affiliates",
            "Date Detected": "2026-05-15",
            "Source": "GPWA",
            "GEO": "EU, UK, SE",
            "License": "MGA, UKGC",
            "Affiliate URL": "leovegas.com/affiliates",
            "Status": "Verified",
            "Priority": "High",
            "Notes": "Strong in Nordics. Well-reviewed affiliate community."
        },
        {
            "Name": "Income Access Network",
            "Date Detected": "2026-05-18",
            "Source": "Affiliate Guard Dog",
            "GEO": "Tier 1, CA, AU",
            "License": "MGA",
            "Affiliate URL": "incomeaccess.com",
            "Status": "Verified",
            "Priority": "High",
            "Notes": "Large network. Verified reputation. Strong for Tier 1."
        },
        {
            "Name": "Rizk Partners",
            "Date Detected": "2026-05-20",
            "Source": "GPWA",
            "GEO": "EU, UK",
            "License": "MGA",
            "Affiliate URL": "rizk.com/affiliates",
            "Status": "Verified",
            "Priority": "Medium",
            "Notes": "Solid program. Well-reviewed by affiliates."
        },
        {
            "Name": "Stake Affiliates",
            "Date Detected": "2026-05-22",
            "Source": "AskGamblers",
            "GEO": "Worldwide",
            "License": "Curaçao",
            "Affiliate URL": "stake.com/affiliates",
            "Status": "Verified",
            "Priority": "High",
            "Notes": "Crypto casino. Large traffic volume. Complex partner verification."
        },
        {
            "Name": "PlayAmo Partners",
            "Date Detected": "2026-05-25",
            "Source": "AskGamblers",
            "GEO": "AU, EU, CA",
            "License": "Curaçao",
            "Affiliate URL": "playamo.com/affiliates",
            "Status": "To Verify",
            "Priority": "Medium",
            "Notes": "Growing in AU market. Mixed Trustpilot reviews - monitor."
        },
        {
            "Name": "Fortune Affiliates",
            "Date Detected": "2026-05-27",
            "Source": "Affiliate Guard Dog",
            "GEO": "Worldwide",
            "License": "MGA",
            "Affiliate URL": "fortuneaffiliates.com",
            "Status": "To Verify",
            "Priority": "Medium",
            "Notes": "Mid-size network. Slow payment reports on forums."
        },
        {
            "Name": "Coldbet Partners",
            "Date Detected": "2026-06-01",
            "Source": "AffPapa",
            "GEO": "EU, UK, CA",
            "License": "MGA",
            "Affiliate URL": "coldbet.com/partners",
            "Status": "New",
            "Priority": "High",
            "Notes": "New launch. Casino + sportsbook. Transparent analytics."
        },
        {
            "Name": "Betwinner Affiliates",
            "Date Detected": "2026-06-03",
            "Source": "AffPapa",
            "GEO": "Worldwide",
            "License": "Curaçao",
            "Affiliate URL": "betwinner-partners.com",
            "Status": "To Verify",
            "Priority": "Medium",
            "Notes": "International audience. Reputation concerns in forums."
        },
        {
            "Name": "22Bet Partners",
            "Date Detected": "2026-06-05",
            "Source": "SBC News",
            "GEO": "150+ markets",
            "License": "Curaçao",
            "Affiliate URL": "22bet-partners.com",
            "Status": "New",
            "Priority": "High",
            "Notes": "CPA/RS/Hybrid. Crypto + fiat. Fast onboarding (24h)."
        },
        {
            "Name": "FoxSlots Partners",
            "Date Detected": "2026-06-08",
            "Source": "GPWA",
            "GEO": "EU, AU, CA",
            "License": "Curaçao",
            "Affiliate URL": "foxslots.com/partners",
            "Status": "New",
            "Priority": "Medium",
            "Notes": "Launched Jan 2026. Crypto casino. CPA/RevShare/Hybrid."
        },
    ])

if "scan_log" not in st.session_state:
    st.session_state.scan_log = []

if "last_scan" not in st.session_state:
    st.session_state.last_scan = None


# ── New programs pool for scan simulation ─────────────────────────────────────
NEW_PROGRAMS_POOL = [
    {
        "Name": "SpinBet Affiliates",
        "Date Detected": datetime.now().strftime("%Y-%m-%d"),
        "Source": "SBC News",
        "GEO": "EU, UA",
        "License": "Curaçao",
        "Affiliate URL": "spinbet-affiliates.com",
        "Status": "New",
        "Priority": "High",
        "Notes": "High RevShare 45%. Brand has no track record yet.",
    },
    {
        "Name": "LuckyNova Partners",
        "Date Detected": datetime.now().strftime("%Y-%m-%d"),
        "Source": "Reddit",
        "GEO": "UA, EU",
        "License": "Unknown",
        "Affiliate URL": "luckynova.io/partners",
        "Status": "To Verify",
        "Priority": "High",
        "Notes": "Found via r/gambling. License unconfirmed - verify before engagement.",
    },
    {
        "Name": "MegaSlot Affiliates",
        "Date Detected": datetime.now().strftime("%Y-%m-%d"),
        "Source": "AffPapa",
        "GEO": "EU, UA",
        "License": "Curaçao",
        "Affiliate URL": "megaslot.io/affiliates",
        "Status": "New",
        "Priority": "Medium",
        "Notes": "New launch announced today. High bonus offers.",
    },
    {
        "Name": "CryptoLuck Partners",
        "Date Detected": datetime.now().strftime("%Y-%m-%d"),
        "Source": "GPWA",
        "GEO": "Worldwide",
        "License": "Unknown",
        "Affiliate URL": "cryptoluck.gg/partners",
        "Status": "To Verify",
        "Priority": "Medium",
        "Notes": "Crypto-native brand. Community buzz on Reddit. License unclear.",
    },
    {
        "Name": "Rocketpot Affiliates",
        "Date Detected": datetime.now().strftime("%Y-%m-%d"),
        "Source": "Affiliate Guard Dog",
        "GEO": "Worldwide",
        "License": "Curaçao",
        "Affiliate URL": "rocketpot.io/affiliates",
        "Status": "New",
        "Priority": "Medium",
        "Notes": "RevShare 25-45%. Competitive structure for crypto traffic.",
    },
]

SOURCES = [
    {"Source": "AffPapa", "Type": "Affiliate Directory", "Monitors": "New program listings, terms changes", "Frequency": "Daily", "Priority": "High"},
    {"Source": "GPWA", "Type": "Affiliate Forum", "Monitors": "New program announcements, affiliate feedback", "Frequency": "Daily", "Priority": "High"},
    {"Source": "Affiliate Guard Dog", "Type": "Watchdog Forum", "Monitors": "Rogue programs, payment issues, new listings", "Frequency": "3x/week", "Priority": "High"},
    {"Source": "AskGamblers", "Type": "Review Platform", "Monitors": "New affiliate programs, complaint trends", "Frequency": "Daily", "Priority": "High"},
    {"Source": "SBC News", "Type": "Industry News", "Monitors": "New program launches, partnership announcements", "Frequency": "Daily", "Priority": "High"},
    {"Source": "Gambling Insider", "Type": "Industry News", "Monitors": "Market launches, M&A activity", "Frequency": "Daily", "Priority": "Medium"},
    {"Source": "Reddit", "Type": "Community Forum", "Monitors": "New programs, community buzz, warnings", "Frequency": "Daily", "Priority": "Medium"},
    {"Source": "Trustpilot", "Type": "Review Platform", "Monitors": "Reputation signals, complaint trends", "Frequency": "Weekly", "Priority": "Medium"},
]


# ── Header ────────────────────────────────────────────────────────────────────
col_logo, col_live = st.columns([3, 1])
with col_logo:
    st.markdown("## 📡 Affiliate Programs Monitor")
    st.markdown("<div style='color:#6b6b80; font-size:13px; margin-top:-8px;'>iGaming affiliate program tracking — MVP prototype</div>", unsafe_allow_html=True)
with col_live:
    st.markdown("<br>", unsafe_allow_html=True)
    last_scan_text = st.session_state.last_scan.strftime("%d %b %Y, %H:%M") if st.session_state.last_scan else "Not yet run"
    st.markdown(f"""
    <div style='text-align:right;'>
      <div class='live-indicator'><span class='live-dot'></span> Live</div>
      <div style='font-size:11px; color:#6b6b80; margin-top:4px;'>Last scan: {last_scan_text}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")


# ── Dashboard metrics ─────────────────────────────────────────────────────────
df = st.session_state.programs
now = datetime.now()
week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")

total = len(df)
new_this_week = len(df[df["Date Detected"] >= week_ago])
to_verify = len(df[df["Status"] == "To Verify"])
verified = len(df[df["Status"] == "Verified"])

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Programs", total)
m2.metric("New This Week", new_this_week, delta=f"+{new_this_week}")
m3.metric("To Verify", to_verify)
m4.metric("Verified", verified)
m5.metric("Sources Monitored", len(SOURCES))

st.markdown("<br>", unsafe_allow_html=True)


# ── Scan button ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Scan Controls</div>', unsafe_allow_html=True)

scan_col, _ = st.columns([2, 4])
with scan_col:
    if st.button("🔍 Run Scan Now", use_container_width=True):
        with st.spinner("Scanning sources..."):
            time.sleep(1.5)

        existing_names = st.session_state.programs["Name"].tolist()
        available = [p for p in NEW_PROGRAMS_POOL if p["Name"] not in existing_names]

        if len(available) < 3:
            available = NEW_PROGRAMS_POOL[:3]
            for p in available:
                p["Date Detected"] = datetime.now().strftime("%Y-%m-%d")

        new_batch = random.sample(available, min(3, len(available)))

        new_df = pd.DataFrame(new_batch)
        st.session_state.programs = pd.concat(
            [st.session_state.programs, new_df], ignore_index=True
        )

        scan_time = datetime.now()
        st.session_state.last_scan = scan_time

        log_entries = [f"[{scan_time.strftime('%H:%M:%S')}] Scan started across {len(SOURCES)} sources"]
        for src in ["AffPapa", "GPWA", "SBC News", "Reddit", "Affiliate Guard Dog"]:
            log_entries.append(f"[{scan_time.strftime('%H:%M:%S')}] Scanning {src}...")
        for p in new_batch:
            log_entries.append(f"[{scan_time.strftime('%H:%M:%S')}] ✓ NEW: {p['Name']} detected via {p['Source']}")
        log_entries.append(f"[{scan_time.strftime('%H:%M:%S')}] Scan complete. {len(new_batch)} new programs added.")

        st.session_state.scan_log = log_entries

        st.success(f"✅ Scan completed. {len(new_batch)} new affiliate programs detected.")

if st.session_state.scan_log:
    st.markdown('<div class="section-title">Scan Log</div>', unsafe_allow_html=True)
    log_html = "<br>".join(st.session_state.scan_log)
    st.markdown(f'<div class="log-box">{log_html}</div>', unsafe_allow_html=True)


# ── Database + Filters ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Affiliate Programs Database</div>', unsafe_allow_html=True)

df = st.session_state.programs

f1, f2, f3 = st.columns(3)
with f1:
    status_filter = st.selectbox("Status", ["All", "New", "To Verify", "Verified"])
with f2:
    priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
with f3:
    source_filter = st.selectbox("Source", ["All"] + sorted(df["Source"].unique().tolist()))

filtered = df.copy()
if status_filter != "All":
    filtered = filtered[filtered["Status"] == status_filter]
if priority_filter != "All":
    filtered = filtered[filtered["Priority"] == priority_filter]
if source_filter != "All":
    filtered = filtered[filtered["Source"] == source_filter]

st.markdown(f"<div style='font-size:12px; color:#6b6b80; margin-bottom:8px;'>Showing {len(filtered)} of {len(df)} programs</div>", unsafe_allow_html=True)

st.table(filtered.reset_index(drop=True))

# ── Monitoring Sources ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Monitoring Sources</div>', unsafe_allow_html=True)
sources_df = pd.DataFrame(SOURCES)
st.table(sources_df)


# ── Alert Examples ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Alert Examples</div>', unsafe_allow_html=True)

st.markdown("""
<div class="alert-card new">
  <div class="alert-title">🟣 New Affiliate Program Detected</div>
  <div class="alert-row"><strong>Program:</strong> SpinBet Affiliates</div>
  <div class="alert-row"><strong>Source:</strong> SBC News</div>
  <div class="alert-row"><strong>GEO:</strong> EU, UA &nbsp;|&nbsp; <strong>Rev Share:</strong> 45%</div>
  <div class="alert-row"><strong>Reason:</strong> New program announced with unusually high revenue share. No track record.</div>
  <div class="alert-row" style="margin-top:8px; color:#7c6bff;"><strong>Next action:</strong> Affiliate Manager to verify terms and license within 24h.</div>
</div>

<div class="alert-card verify">
  <div class="alert-title">🟡 License Verification Required</div>
  <div class="alert-row"><strong>Program:</strong> LuckyNova Partners</div>
  <div class="alert-row"><strong>Source:</strong> Reddit (r/gambling)</div>
  <div class="alert-row"><strong>GEO:</strong> UA, EU &nbsp;|&nbsp; <strong>License:</strong> Unknown</div>
  <div class="alert-row"><strong>Reason:</strong> Community reporting delayed payments. License cannot be confirmed from public sources.</div>
  <div class="alert-row" style="margin-top:8px; color:#fbbf24;"><strong>Next action:</strong> Affiliate Manager to verify licensing information and reputation signals.</div>
</div>

<div class="alert-card risk">
  <div class="alert-title">🔴 Reputation Risk Flagged</div>
  <div class="alert-row"><strong>Program:</strong> Fortune Affiliates</div>
  <div class="alert-row"><strong>Source:</strong> Affiliate Guard Dog</div>
  <div class="alert-row"><strong>GEO:</strong> Worldwide &nbsp;|&nbsp; <strong>License:</strong> MGA</div>
  <div class="alert-row"><strong>Reason:</strong> Multiple reports of slow payments on Affiliate Guard Dog forum. Pattern consistent over 3 months.</div>
  <div class="alert-row" style="margin-top:8px; color:#f87171;"><strong>Next action:</strong> Flag for review. Do not onboard until reputation confirmed.</div>
</div>
""", unsafe_allow_html=True)


# ── Next Steps ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Next Steps — Scaling the MVP</div>', unsafe_allow_html=True)

steps = [
    ("01", "Connect real scrapers / APIs", "Apify or ParseHub for AffPapa, GPWA, SBC News. WhoisXML API for domain monitoring."),
    ("02", "Add deduplication logic", "Prevent same program from appearing multiple times from different sources."),
    ("03", "Set up scheduled scan", "Automate daily scan via cron job or Make.com workflow. Run at 09:00 daily."),
    ("04", "Assign business owner", "Affiliate Manager or SEO Head owns the weekly verification process."),
    ("05", "Add Slack / email notifications", "Trigger alert to #affiliate-monitoring channel on every new detection."),
    ("06", "Build weekly digest for CEO", "Auto-generate Monday morning summary: new programs, risks, recommended actions."),
]

for num, title, desc in steps:
    st.markdown(f"""
    <div class="step-item">
      <div class="step-num">{num}</div>
      <div>
        <div style="font-weight:600; margin-bottom:3px;">{title}</div>
        <div style="color:#6b6b80; font-size:13px;">{desc}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Prototype MVP. Built to validate monitoring logic before connecting live sources.<br>
  Sources: AffPapa · GPWA · Affiliate Guard Dog · AskGamblers · SBC News · Gambling Insider · Reddit · Trustpilot
</div>
""", unsafe_allow_html=True)
