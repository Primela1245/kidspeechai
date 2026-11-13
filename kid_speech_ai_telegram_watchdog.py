import datetime
import json
import os
import sys
import urllib.request

BOT_TOKEN = "8761566712:AAGFRszpXjWAShiXH34bhnV7DruWVKYxnjo"
CHAT_ID = "8382985037"

DEADLINES = [
    {
        "id": "nih_sbir_dec6_window_open",
        "title": "🚀 NIH SBIR $1,841,232 (6 Grants) 30-Day Submission Window",
        "date": "2026-12-06",
        "end_date": "2027-01-05",
        "action": (
            "Open Antigravity & Grants.gov (PA-27-100). The official 30-day window (Dec 6, 2026 – Jan 5, 2027) "
            "is OPEN! Attach 21_Cover_Letter.pdf and 05_Budget_Justification.pdf from "
            "C:\\Users\\prime\\Desktop\\SD Gov Documents\\3_NIH_SBIR_Federal_Grants and click Sign & Submit on all 6 grants!"
        ),
        "alert_days_before": [7, 3, 1, 0],
        "daily_during_window": True,
    },
    {
        "id": "nsf_sbir_pitch_decision_check",
        "title": "🔬 NSF SBIR Phase I ($305,000) Pitch #00132692 Status Check",
        "date": "2026-11-25",
        "end_date": "2026-12-05",
        "action": (
            "Check ceo@sdgovernmentsolutions.com and NSF Seed Fund Portal (https://nsfgov.my.site.com/mywork/s/) "
            "for Program Director invitation on Pitch #00132692 so we can submit the full $305,000 NSF Phase I proposal."
        ),
        "alert_days_before": [0, -10],
        "daily_during_window": False,
    },
    {
        "id": "tax_1099k_google_play_summary",
        "title": "🧾 Download Google Play Console & Stripe Annual Tax / 1099-K Statements",
        "date": "2027-01-31",
        "end_date": "2027-02-05",
        "action": (
            "Log into Google Play Console -> Settings -> Payments Profile and download annual 2026 payout/tax reports "
            "for SD Government Solutions LLC (FEIN 42-3932513)."
        ),
        "alert_days_before": [7, 1, 0],
        "daily_during_window": False,
    },
    {
        "id": "tax_march15_llc_return",
        "title": "🏛️ Federal/CA Partnership-LLC Tax Deadline Check (Form 1065 / CA Form 568)",
        "date": "2027-03-15",
        "end_date": "2027-03-15",
        "action": (
            "Verify whether SD Government Solutions LLC files as Partnership (due March 15) or Single-Member LLC "
            "(due April 15) and file/extend on time to avoid late penalties."
        ),
        "alert_days_before": [14, 7, 2, 0],
        "daily_during_window": False,
    },
    {
        "id": "tax_april15_ca_800_franchise_tax",
        "title": "🏛️ Federal Tax Return + CA LLC $800 Annual Franchise Tax (Form 3522 / Form 568)",
        "date": "2027-04-15",
        "end_date": "2027-04-15",
        "action": (
            "Pay California FTB $800 Annual LLC Tax (Form 3522) + file CA Form 568 & Federal Return for "
            "SD Government Solutions LLC (CA SOS #20260327479, FEIN 42-3932513) so the LLC remains in 100% Good Standing."
        ),
        "alert_days_before": [14, 7, 3, 1, 0],
        "daily_during_window": False,
    },
    {
        "id": "google_play_semi_annual_policy_check",
        "title": "📱 Google Play Console Policy, Data Safety & Families Self-Certification Audit",
        "date": "2027-05-01",
        "end_date": "2027-05-01",
        "action": (
            "Open Google Play Console -> Policy Status & App Content for Kid Speech AI (com.kidspeechai.actionnarrator) "
            "to confirm zero policy warnings and verify Families Policy / Data Safety declarations."
        ),
        "alert_days_before": [7, 0],
        "daily_during_window": False,
    },
    {
        "id": "google_play_target_sdk_annual_deadline",
        "title": "⚠️ MANDATORY Google Play Annual Target Android SDK / API Level Update Deadline!",
        "date": "2027-08-31",
        "end_date": "2027-08-31",
        "action": (
            "Google Play requires all existing apps to target the latest Android API level by August 31 each year. "
            "Ask Antigravity to bump targetSdkVersion in build.gradle, build a signed .aab, and upload to Google Play Console!"
        ),
        "alert_days_before": [60, 30, 14, 7, 3, 1, 0],
        "daily_during_window": False,
    },
    {
        "id": "sam_gov_annual_renewal",
        "title": "🏛️ URGENT: Renew SAM.gov Entity Registration (UEI: ESJKVADQZPF5 / CAGE: 255U0)",
        "date": "2027-10-04",
        "end_date": "2027-10-04",
        "action": (
            "Log into SAM.gov and renew SD Government Solutions LLC (UEI: ESJKVADQZPF5) BEFORE October 4, 2027. "
            "SAM.gov must stay continuously active to receive NIH/NSF grant funds and government contracts!"
        ),
        "alert_days_before": [60, 30, 14, 7, 3, 1, 0],
        "daily_during_window": False,
    },
]


def send_telegram(html_text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": CHAT_ID,
            "text": html_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_live_health():
    issues = []
    try:
        req = urllib.request.Request("https://kidspeechai.com", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            if r.status != 200:
                issues.append(f"kidspeechai.com returned HTTP {r.status}")
    except Exception as e:
        issues.append(f"kidspeechai.com unreachable: {e}")

    try:
        req = urllib.request.Request(
            "https://res.cloudinary.com/dppbkz59h/raw/upload/daily_manifest.json",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode("utf-8"))
            if not data.get("date"):
                issues.append("Cloudinary daily_manifest.json missing date field")
    except Exception as e:
        issues.append(f"Cloudinary daily_manifest.json check failed: {e}")

    return issues


def run_watchdog(force_summary=False):
    today = datetime.date.today()
    today_str = today.isoformat()

    health_issues = check_live_health()
    triggered_alerts = []

    for d in DEADLINES:
        target_date = datetime.date.fromisoformat(d["date"])
        end_date = datetime.date.fromisoformat(d["end_date"])
        days_until = (target_date - today).days
        days_until_end = (end_date - today).days

        should_alert = False
        if days_until in d["alert_days_before"]:
            should_alert = True
        elif d.get("daily_during_window") and target_date <= today <= end_date:
            should_alert = True

        if should_alert:
            triggered_alerts.append((d, days_until, days_until_end))

    if health_issues:
        msg = (
            "🚨 <b>KID SPEECH AI CRITICAL OUTAGE ALERT (@AiKidBlogBot)</b>\n\n"
            + "\n".join(f"❌ {i}" for i in health_issues)
        )
        send_telegram(msg)

    if triggered_alerts or force_summary:
        lines = [
            f"🔔 <b>KID SPEECH AI — IMPORTANT DEADLINE REMINDER ({today_str})</b>"
        ]
        for d, days_until, days_until_end in triggered_alerts:
            when_str = (
                f"Starts in {days_until} days ({d['date']})"
                if days_until > 0
                else f"OPEN NOW — Closes {d['end_date']} ({days_until_end} days left)"
            )
            lines.append(
                f"\n<b>{d['title']}</b>\n"
                f"📅 <b>Window:</b> {when_str}\n"
                f"👉 <b>Action:</b> {d['action']}"
            )
        send_telegram("\n".join(lines))
        print(f"Sent {len(triggered_alerts)} important reminder(s) to @AiKidBlogBot.")
    else:
        print(f"No important deadline reminders due today ({today_str}) — staying 100% silent.")


if __name__ == "__main__":
    force = "--force" in sys.argv
    run_watchdog(force_summary=force)
