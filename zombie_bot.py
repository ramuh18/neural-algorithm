import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] ★3호기 전용 설정★
BLOG_TITLE = "Neural Algorithm" 
BLOG_BASE_URL = "https://ramuh18.github.io/neural-algorithm/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [📊 구글 트렌드 실시간 수집]
def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Cipher Breach", "Node Overload"]
    except:
        return ["Data Intercept", "Neural Protocol"]

# [🖋️ 3호기 전용 1,500자급 '데이터 유출' 엔진]
def generate_hacker_report(topic):
    return f"""
# [SIGNAL DECRYPTED] INTERNAL LEAK: {topic} Manipulation Detected

## // DATA NODE INTERCEPTION: PHASE 1
The signal regarding **{topic}** was intercepted from an encrypted node within the shadow liquidity pools. Our neural-processing units have identified a massive correlation between {topic} and high-frequency institutional front-running protocols. The financial elite are utilizing sub-millisecond AI execution to front-run retail liquidity, and {topic} is the primary smokescreen currently being deployed.

## // ALGORITHMIC BREACH: PHASE 2
Our deep-dive analysis of the {topic} data stream reveals a systematic attempt to trigger retail stop-losses. We have identified 'Spoofing' and 'Layering' patterns that suggest an imminent liquidity flush. The legacy institutions are no longer hiding their intentions; they are stress-testing the public's tolerance for capital erasure through the strategic manipulation of {topic}.

The nodes associated with {topic} show a 180% increase in dark-pool activity, confirming that a major structural realignment is being executed outside the view of public exchanges. If you are holding your assets on centralized custodial platforms, you are effectively providing the very liquidity they need to execute this breach.

## // SOVEREIGNTY PROTOCOL: PHASE 3
To survive the **{topic}** signal, you must disconnect from the centralized grid. The only defense against algorithmic capital erasure is absolute self-custody. Move your assets to cold storage immediately. The convenience of the 'Exchange App' is the trap that binds your capital to their failing architecture.

The migration to hardware-secured vaults is the ultimate act of financial resistance. By securing your own private keys, you effectively opt-out of the manipulative algorithms currently surrounding {topic}. The systemic reset is accelerating, and only those who maintain control of their digital nodes will survive the final decryption cycle.

## // TERMINAL CONCLUSION
The supercycle of 2026 is reaching its terminal phase. The signal from **{topic}** is a direct warning to the sovereign participant. Disconnect from the legacy system. Secure your assets in physical vaults. Do not wait for the official broadcast; the broadcast itself is the deception. Sovereignty is the only asset that survives the reset.
"""

def create_final_html(topic, img_url, body_html, sidebar_html):
    # [3호기 테마] 다크 모드, 네온 그린 (해커 느낌)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Rajdhani:wght@600&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon-green: #00ff41; --dark-bg: #050505; --alert-red: #ff003c; }}
        body {{ font-family: 'Rajdhani', sans-serif; background: var(--dark-bg); color: #eeeeee; line-height: 1.7; margin: 0; }}
        
        header {{ background: #000; color: var(--neon-green); padding: 30px; text-align: center; border-bottom: 2px solid var(--neon-green); box-shadow: 0 0 15px var(--neon-green); }}
        .brand {{ font-family: 'JetBrains Mono', monospace; font-size: 1.8rem; font-weight: 800; letter-spacing: -1px; }}
        
        .container {{ max-width: 1300px; margin: 30px auto; display: grid; grid-template-columns: 300px 1fr; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} .sidebar {{ order: 2; }} }}
        
        main {{ background: #0a0a0a; padding: 40px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,0,0,0.5); }}
        h1 {{ font-family: 'JetBrains Mono'; color: var(--neon-green); font-size: 2.5rem; line-height: 1.1; margin-top: 0; text-transform: uppercase; }}
        .content h2 {{ color: var(--neon-green); border-left: 4px solid var(--neon-green); padding-left: 15px; margin-top: 50px; font-family: 'JetBrains Mono'; font-size: 1.3rem; }}
        img {{ width: 100%; height: auto; border: 1px solid var(--neon-green); margin-bottom: 30px; filter: grayscale(1) contrast(1.2) brightness(0.8); }}
        
        .side-card {{ background: #000; padding: 25px; border: 1px solid var(--neon-green); margin-bottom: 25px; box-shadow: 0 0 10px rgba(0, 255, 65, 0.1); }}
        .btn {{ display: block; padding: 15px; background: #000; color: var(--neon-green); text-decoration: none; font-weight: 800; text-align: center; margin-bottom: 12px; border: 1px solid var(--neon-green); font-family: 'JetBrains Mono'; transition: 0.3s; font-size: 0.9rem; }}
        .btn-red {{ color: var(--alert-red); border-color: var(--alert-red); }}
        .btn:hover {{ background: var(--neon-green); color: #000; box-shadow: 0 0 20px var(--neon-green); }}
        
        footer {{ text-align: center; padding: 60px 20px; color: #444; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; border-top: 1px solid #222; }}
        .amazon-disclaimer {{ margin-top: 10px; color: #333; font-style: italic; }}
    </style></head>
    <body>
    <header><div class="brand">NEURAL_ALGORITHM_NODE_03</div></header>
    <div class="container">
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn btn-red">🔓 UNLOCK_EXIT_PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn">🚀 START_SIGNAL_BOT</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ GET_HARDWARE_KEY</a>
            </div>
            <div class="side-card">
                <h3 style="margin-top:0; color:var(--neon-green); font-family:'JetBrains Mono'; font-size:0.85rem;">// ARCHIVE_NODES</h3>
                <ul style="list-style:none; padding:0; line-height:2.2; font-size:0.8rem;">{sidebar_html}</ul>
            </div>
        </aside>
        <main>
            <div style="color:var(--neon-green); font-family:'JetBrains Mono'; margin-bottom:10px; font-size:0.8rem;">[ SIGNAL_RECEIVED: SUCCESS ]</div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>
        SERVER_ID: 03-NA | ENCRYPTION_STRENGTH: 2048-BIT<br>
        &copy; 2026 {BLOG_TITLE}. ALL DATA DECENTRALIZED.
        <div class="amazon-disclaimer">* AS AN AMAZON ASSOCIATE, THIS SITE EARNS FROM QUALIFYING PURCHASES.</div>
    </footer></body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_hacker_report(topic) 
    html_body = markdown.markdown(body_text)
    # 이미지 스타일: 매트릭스, 사이버펑크, 코드 비주얼
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk matrix code hacking green neon data 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><b style='color:var(--neon-green);'>_</b> <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#777; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ 3호기 Neural Signal Update Complete: {topic}")

if __name__ == "__main__": main()
