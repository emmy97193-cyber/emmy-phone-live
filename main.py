import os, json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime, timezone
app = FastAPI()
STATUS_FILE = "/tmp/status.json"
def get_status():
    if not os.path.exists(STATUS_FILE): return {"online": False, "last_seen": "Never", "battery": 0}
    with open(STATUS_FILE) as f: return json.load(f)
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    d=get_status(); c="#00FF88" if d["online"] else "#FF4444"; t="ONLINE & ACTIVATED" if d["online"] else "OFFLINE"
    return f"<body style='background:#000;color:#fff;text-align:center;padding:50px;font-family:sans-serif'><h1>Emmy's A06</h1><div style='background:#111;border-radius:20px;padding:20px;max-width:320px;margin:auto'><div style='width:20px;height:20px;background:{c};border-radius:50%;margin:auto'></div><h2 style='color:{c}'>{t}</h2><p>Last: {d['last_seen']}</p><p>Battery: {d['battery']}%</p><p>Running on Railway</p></div></body>"
@app.post("/ping")
async def ping(r: Request):
    b=await r.json(); now=datetime.now(timezone.utc).strftime("%H:%M:%S UTC"); dat={"online":True,"last_seen":now,"battery":b.get("battery",0)}
    open(STATUS_FILE,"w").write(json.dumps(dat)); return {"ok":True}
