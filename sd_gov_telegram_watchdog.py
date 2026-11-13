import datetime
import json
import os
import sys
import urllib.request

BOT_TOKEN = "9214612989:AAEUB-vkH3X5XmNx53hm6-Zjh2uDM109CY0"
CHAT_ID = "8382985037"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sd_gov_watchdog_state.json")


def get_deadlines(today: datetime.date):
    yr = today.year
    def annual_date(month: int, day: int) -> str:
        d = datetime.date(yr, month, day)
        if (d - today).days < -5:
            d = datetime.date(yr + 1, month, day)
        return d.isoformat()

    return [
        {
            "id": "md_emma_nov16_upload_check",
            "title": "🛡️ Maryland eMMA #BPM059527 ($2.40M) Upload Check — Chief Albert Lemon",
            "date": "2026-11-16",
            "end_date": "2026-11-16",
            "category": "SECURITY BID DEADLINE",
            "action": (
                "Confirm with Chief Albert Lemon (United Security Agency, LLC — chieflemon@unitedsecurityagencyllc.com) "
                "that he uploaded 4_UPDATED_MASTER_eMMA_SUBMITTAL_BINDER_United_Security_Agency_BPM059527.pdf on Maryland eMMA!"
            ),
            "alert_days_before": [3, 2, 1, 0],
            "daily_during_window": True,
        },
        {
            "id": "orange_county_nov20_bid_opening",
            "title": "🏆 County of Orange RFP #017-3034501-JC ($7.76M) Bid Opening Check!",
            "date": "2026-11-20",
            "end_date": "2026-11-20",
            "category": "SEALED BID OPENING",
            "action": (
                "Check OpenGov Project #249227 (https://procurement.opengov.com/portal/ocgov/projects/249227) after 4:00 PM PT "
                "for bid opening results on All Out Security Guard, Inc.'s sealed Proposal #616680 ($4,656,960 3-Yr / $7,761,600 5-Yr)!"
            ),
            "alert_days_before": [3, 1, 0],
            "daily_during_window": False,
        },
        {
            "id": "nsf_sbir_pitch_decision_check",
            "title": "🔬 NSF SBIR Phase I ($305,000) Pitch #00131710 / #00132692 Status Check",
            "date": "2026-11-25",
            "end_date": "2026-12-05",
            "category": "FEDERAL GRANTS ($305K)",
            "action": (
                "Check ceo@sdgovernmentsolutions.com and NSF Seed Fund Portal (https://nsfgov.my.site.com/mywork/s/) "
                "for Program Director invitation to submit full $305,000 NSF Phase I proposal."
            ),
            "alert_days_before": [7, 3, 1, 0, -5],
            "daily_during_window": False,
        },
        {
            "id": "nih_sbir_dec6_window_open",
            "title": "🚀 NIH SBIR $1,841,232 (6 Grants) 30-Day Submission Window (PA-27-100)",
            "date": "2026-12-06",
            "end_date": "2027-01-05",
            "category": "FEDERAL GRANTS ($1.84M)",
            "action": (
                "Open Grants.gov (PA-27-100). The 30-day window (Dec 6, 2026 – Jan 5, 2027) is OPEN! "
                "Submit all 6 upgraded NIH SBIR Phase I grants from 3_NIH_SBIR_Federal_Grants."
            ),
            "alert_days_before": [14, 7, 3, 2, 1, 0],
            "daily_during_window": True,
        },
        {
            "id": "ca_sellers_permit_cdtfa_annual_return",
            "title": "🛒 CA Seller's Permit / CDTFA Annual Return (Account #: 245-279968)",
            "date": annual_date(1, 31),
            "end_date": annual_date(1, 31),
            "category": "CA SELLER'S PERMIT (CDTFA)",
            "action": (
                "Log into https://onlineservices.cdtfa.ca.gov under CDTFA Account #245-279968 (SD Government Solutions LLC) "
                "and file your annual Sales and Use Tax return (even if $0 taxable goods sold) so your California Seller's Permit "
                "to sell goods is NEVER closed or revoked!"
            ),
            "alert_days_before": [30, 14, 7, 3, 2, 1, 0],
            "daily_during_window": False,
        },
        {
            "id": "irs_1099_annual_tax_statements",
            "title": "🧾 IRS 1099-NEC / 1099-K and Annual Tax Statements (FEIN: 42-3932513)",
            "date": annual_date(1, 31),
            "end_date": annual_date(1, 31),
            "category": "TAXES AND 1099 COMPLIANCE",
            "action": (
                "Download annual bank, Stripe, and Google Play tax statements for SD Government Solutions LLC (FEIN: 42-3932513) "
                "and verify any 1099-NEC / 1099-K forms before January 31."
            ),
            "alert_days_before": [21, 14, 7, 3, 1, 0],
            "daily_during_window": False,
        },
        {
            "id": "tax_march15_llc_partnership_check",
            "title": "🏛️ March 15 LLC / Partnership Tax Return Check (Form 1065 / CA Form 568)",
            "date": annual_date(3, 15),
            "end_date": annual_date(3, 15),
            "category": "FEDERAL AND CA TAXES",
            "action": (
                "Verify whether SD Government Solutions LLC (FEIN: 42-3932513 | CA SOS: #20260327479) files on March 15 "
                "(Partnership) or April 15 (Single-Member LLC) and file/extend on time to avoid any FTB penalty."
            ),
            "alert_days_before": [30, 14, 7, 3, 1, 0],
            "daily_during_window": False,
        },
        {
            "id": "tax_april15_ca_800_franchise_tax",
            "title": "💰 MANDATORY: CA LLC $800 Annual Franchise Tax (Form 3522) + Tax Return",
            "date": annual_date(4, 15),
            "end_date": annual_date(4, 15),
            "category": "CA LLC $800 TAX AND IRS RETURN",
            "action": (
                "Pay California FTB $800 Annual LLC Tax (Form 3522 at https://www.ftb.ca.gov/pay/) + file CA Form 568 "
                "and Federal Tax Return for SD Government Solutions LLC (CA SOS #20260327479, FEIN 42-3932513) by April 15!"
            ),
            "alert_days_before": [45, 30, 21, 14, 7, 5, 3, 2, 1, 0],
            "daily_during_window": False,
        },
        {
            "id": "ca_sos_llc_statement_of_info_july16",
            "title": "🏛️ CA Secretary of State LLC Renewal / Statement of Info (SOS #: 20260327479)",
            "date": annual_date(7, 16),
            "end_date": annual_date(7, 31),
            "category": "CA LLC GOOD STANDING",
            "action": (
                "Log into https://bizfileonline.sos.ca.gov for SD Government Solutions LLC (Entity #20260327479, formed 07/16/2026) "
                "to verify Active Good Standing and file Statement of Information (Form LLC-12, $20 fee) if due!"
            ),
            "alert_days_before": [45, 30, 14, 7, 3, 1, 0],
            "daily_during_window": False,
        },
        {
            "id": "el_cajon_business_license_check",
            "title": "🏢 City of El Cajon Business License and CDTFA Mid-Year Check",
            "date": annual_date(7, 31),
            "end_date": annual_date(7, 31),
            "category": "LOCAL PERMIT AND CDTFA",
            "action": (
                "Check City of El Cajon Business License renewal (1229 Linalda Dr, El Cajon, CA 92021) and verify "
                "CDTFA Seller's Permit #245-279968 status at https://onlineservices.cdtfa.ca.gov."
            ),
            "alert_days_before": [30, 14, 7, 1, 0],
            "daily_during_window": False,
        },
        {
            "id": "sam_gov_annual_renewal_oct4",
            "title": "🚨 CRITICAL: Renew SAM.gov Entity Registration (UEI: ESJKVADQZPF5 / CAGE: 255U0)",
            "date": annual_date(10, 4),
            "end_date": annual_date(10, 4),
            "category": "SAM.GOV FEDERAL REGISTRATION",
            "action": (
                "Log into https://sam.gov and renew SD Government Solutions LLC (UEI: ESJKVADQZPF5 | CAGE: 255U0 | DUNS: 148031019) "
                "BEFORE October 4! Never let SAM.gov expire so all federal contracts and NIH/NSF grants remain 100% active!"
            ),
            "alert_days_before": [60, 45, 30, 21, 14, 7, 5, 3, 2, 1, 0],
            "daily_during_window": False,
        },
    ]


def send_telegram(html_text: str):
    safe_html = html_text.replace(" & ", " &amp; ")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": CHAT_ID,
            "text": safe_html[:4050],
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_watchdog(force_summary: bool = False):
    today = datetime.date.today()
    today_str = today.isoformat()
    deadlines = get_deadlines(today)

    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    urgent_alerts = []
    upcoming_lines = []

    for d in deadlines:
        start_dt = datetime.date.fromisoformat(d["date"])
        end_dt = datetime.date.fromisoformat(d["end_date"])
        days_until = (start_dt - today).days
        days_until_end = (end_dt - today).days

        if days_until_end < -10:
            continue

        if days_until > 0:
            status_badge = f"⏳ <b>{days_until} days left</b> ({d['date']})"
        elif days_until_end >= 0:
            status_badge = f"🚨 <b>ACTIVE NOW!</b> ({days_until_end} days left until {d['end_date']})"
        else:
            status_badge = f"⚠️ <b>Follow-up Window</b> ({d['date']})"

        upcoming_lines.append(
            f"• <b>{d['title']}</b>\n"
            f"  └ {status_badge}\n"
            f"  └ <i>Action:</i> {d['action']}"
        )

        should_trigger = False
        if days_until in d["alert_days_before"]:
            should_trigger = True
        if d.get("daily_during_window") and start_dt <= today <= end_dt:
            should_trigger = True

        alert_key = f"{d['id']}_{today_str}"
        if should_trigger and not state.get(alert_key):
            urgent_alerts.append(
                f"🚨 <b>{d['category']} ALERT:</b>\n"
                f"<b>{d['title']}</b>\n"
                f"📅 <b>Deadline:</b> {d['date']} (<b>{max(days_until, 0)} days</b>)\n"
                f"✅ <b>What To Do:</b> {d['action']}"
            )
            state[alert_key] = True

    is_monday_heartbeat = (today.weekday() == 0 and not state.get(f"monday_{today_str}"))
    is_monthly_briefing = (today.day == 1 and not state.get(f"monthly_{today_str}"))

    if force_summary or urgent_alerts or is_monday_heartbeat or is_monthly_briefing:
        msg_parts = [
            f"🏛️ <b>SD GOVERNMENT SOLUTIONS LLC — 24/7 CLOUD COMPLIANCE &amp; TAX WATCHDOG (@SDGOV_bot)</b>",
            f"📅 <b>Date:</b> {today.strftime('%A, %B %d, %Y')}",
            f"🏢 <b>Entity:</b> SD Government Solutions LLC",
            f"• <b>CA SOS Entity #:</b> <code>20260327479</code> (Formed <code>07/16/2026</code>)",
            f"• <b>Federal EIN:</b> <code>42-3932513</code> | <b>CDTFA Seller's Permit #:</b> <code>245-279968</code>",
            f"• <b>SAM.gov UEI:</b> <code>ESJKVADQZPF5</code> | <b>CAGE:</b> <code>255U0</code> | <b>DUNS:</b> <code>148031019</code>",
        ]

        if urgent_alerts:
            msg_parts.append("\n🔥 <b>URGENT ACTION ALERTS TODAY:</b>\n" + "\n\n".join(urgent_alerts))

        msg_parts.append(
            "\n📋 <b>MASTER COMPLIANCE, PERMIT, TAX &amp; GRANT CALENDAR:</b>\n" + "\n\n".join(upcoming_lines)
        )
        msg_parts.append(
            "\n☁️ <i>24/7 Cloud Backup Active: This bot runs automatically on GitHub Cloud Servers every day at 8:30 AM PT even when your laptop is turned off!</i>"
        )

        send_telegram("\n".join(msg_parts))
        if is_monday_heartbeat:
            state[f"monday_{today_str}"] = True
        if is_monthly_briefing:
            state[f"monthly_{today_str}"] = True
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass
        print("Sent @SDGOV_bot Telegram compliance summary successfully!")
    else:
        print("No urgent alerts due today (quiet check passed).")


if __name__ == "__main__":
    force = "--summary" in sys.argv or "--force" in sys.argv
    run_watchdog(force_summary=force)
