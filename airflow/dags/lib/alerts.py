import requests, json
from airflow.models import Variable

def send_teams_alert(title, summary, severity="info", link=None):
    url = Variable.get("TEAMS_WEBHOOK_URL", None)
    if not url:
        return  # silently skip in dev
    color = {"info":"#36a64f","warning":"#ffa500","error":"#d9534f"}.get(severity,"#36a64f")
    payload = {
      "@type": "MessageCard","@context": "http://schema.org/extensions",
      "themeColor": color, "summary": summary,
      "sections": [{"activityTitle": title, "text": summary + (f"\n\n[Open report]({link})" if link else "")}]
    }
    r = requests.post(url, data=json.dumps(payload))
    r.raise_for_status()
