from datetime import datetime
from flask import Flask, render_template_string
import pandas as pd
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

DATA = {
    "Source_IP": [
        "192.168.1.10", "192.168.1.11", "192.168.1.12",
        "192.168.1.20", "192.168.1.20", "192.168.1.20",
        "192.168.1.30", "192.168.1.31", "192.168.1.32",
        "192.168.1.40"
    ],
    "Packets": [20, 25, 30, 1500, 1700, 1600, 28, 35, 22, 30],
    "Bytes": [1200, 1500, 1800, 90000, 95000, 92000, 1400, 1600, 1300, 1500],
    "Connections": [5, 6, 7, 200, 250, 220, 6, 8, 5, 7]
}

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#101827">
<title>NIDS Security Dashboard</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#edf2f7;font:16px system-ui,Arial}
main{max-width:850px;margin:auto;padding:18px}.hero{padding:22px;border-radius:18px;background:#17243a}
h1{font-size:24px;margin:0 0 8px}.muted{color:#a9b8cc}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0}
.card{background:#17243a;border:1px solid #293b55;border-radius:14px;padding:14px;overflow-wrap:anywhere}
.num{font-size:26px;font-weight:700;margin-top:4px}.btn{display:block;text-align:center;background:#18a56b;color:white;padding:14px;border-radius:12px;text-decoration:none;font-weight:700;margin-top:15px}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:10px 7px;border-bottom:1px solid #293b55}th{color:#a9b8cc}
.ok{color:#61e6a3;font-weight:700}.bad{color:#ff8585;font-weight:700}.tablewrap{overflow-x:auto}
@media(max-width:480px){main{padding:12px}.stats{gap:6px}.card{padding:10px}.num{font-size:22px}table{font-size:12px}th,td{padding:8px 4px}}
</style></head><body><main>
<section class="hero"><h1>🛡️ NIDS Security Dashboard</h1>
<div class="muted">Machine-learning traffic anomaly demo</div>
<div class="muted">Last analysis: {{ timestamp }}</div>
<a class="btn" href="/">ANALYZE TRAFFIC AGAIN</a></section>
<section class="stats">
<div class="card"><div class="muted">Total records</div><div class="num">{{ total }}</div></div>
<div class="card"><div class="muted">Normal</div><div class="num ok">{{ normal }}</div></div>
<div class="card"><div class="muted">Intrusions</div><div class="num bad">{{ alerts|length }}</div></div>
</section>
<section class="card"><h2>Traffic analysis</h2><div class="tablewrap"><table>
<thead><tr><th>Source IP</th><th>Packets</th><th>Bytes</th><th>Connections</th><th>Status</th></tr></thead>
<tbody>{% for r in rows %}<tr><td>{{r.ip}}</td><td>{{r.packets}}</td><td>{{r.bytes}}</td><td>{{r.connections}}</td>
<td class="{{'bad' if r.suspicious else 'ok'}}">{{'INTRUSION DETECTED' if r.suspicious else 'NORMAL'}}</td></tr>{% endfor %}</tbody>
</table></div></section>
<section class="card" style="margin-top:14px"><h2>Security alerts</h2>
{% if alerts %}{% for a in alerts %}<p class="bad">⚠ {{a.ip}} — {{a.packets}} packets, {{a.bytes}} bytes, {{a.connections}} connections</p>{% endfor %}
{% else %}<p class="ok">No suspicious sample records detected.</p>{% endif %}
</section>
<p class="muted">Demo only: analyzes 10 fixed sample records. It does not monitor live phone network traffic. IsolationForest is refitted on each analysis; anomaly flags are not proof of an attack.</p>
</main></body></html>"""

@app.route("/")
def home():
    df = pd.DataFrame(DATA)
    features = df[["Packets", "Bytes", "Connections"]]
    model = IsolationForest(contamination=0.3, random_state=42)
    df["Prediction"] = model.fit_predict(features)
    rows = []
    alerts = []
    for _, r in df.iterrows():
        item = {
            "ip": str(r["Source_IP"]),
            "packets": int(r["Packets"]),
            "bytes": int(r["Bytes"]),
            "connections": int(r["Connections"]),
            "suspicious": int(r["Prediction"]) == -1,
        }
        rows.append(item)
        if item["suspicious"]:
            alerts.append(item)
    return render_template_string(
        PAGE, rows=rows, alerts=alerts, total=len(rows),
        normal=len(rows)-len(alerts),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
