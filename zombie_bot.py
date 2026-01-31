import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM]
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BLOG_TITLE = "NEURAL ALGORITHM"
BLOG_BASE_URL = "https://ramuh18.github.io/neural-algorithm/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [🔥 English Hooking Titles]
HOOKING_TITLES = [
    "AI Predicts 2026 Market Crash: Warning",
    "Leaked: Wall Street's Secret AI Algorithm",
    "Move Your Crypto to Cold Storage NOW",
    "Exposed: The Banking Collapse Hidden Signs",
    "Whistleblower: How Bots Manipulate Bitcoin Price"
]

def generate_hacker_leak(topic):
    # [분량 확보 로직] 해커가 데이터를 단계별로 유출하는 컨셉으로 3개 파트 생성
    leak_parts = [
        "Phase 1: Deep Web Signal Interception",
        "Phase 2: Explaining the Manipulative Algorithm",
        "Phase 3: The Final Exit Strategy for Retailers"
    ]
    full_leak = f"# [DECRYPTED] INTERNAL LEAK: {topic}\n\n"
    
    for part in leak_parts:
        prompt = f"""
        You are a dark-web whistleblower leaking classified information.
        Topic: '{topic}'
        Focus Area: '{part}'
        Style: Paranoid, aggressive, revealing hidden truths. Use tech slang (Algorithm, Node, Cipher).
        Length: 600 words for this section. English Only. Markdown.
        """
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.8}}, timeout=40)
            res = resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            full_leak += f"## {part}\n\n" + res + "\n\n---\n\n"
            time.sleep(2) # RPM 제한 방지
        except:
            continue
            
    return full_leak if len(full_leak) > 500 else "## DECRYPTION FAILED. ACCESS DENIED."

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="Jxh9S9J3S5_RBIpJH4CVrDkpRiDZ_mQ99TfIm7xK7YY" />
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #050505; --text: #eeeeee; --accent: #00ff41; }}
        body {{ font-family: 'Rajdhani', sans-serif; background: var(--bg); color: var(--text); margin: 0; overflow-x: hidden; }}
        
        /* [반응형 디자인] 모바일 가림 방지 */
        .container {{ 
            max-width: 1400px; margin: 0 auto; 
            display: grid; grid-template-columns: 300px 1fr; gap: 40px; padding: 40px 20px; 
        }}
        
        @media(max-width: 1000px) {{ 
            .container {{ grid-template-columns: 1fr; padding: 20px; }}
            .sidebar {{ position: static !important; border-right: none !important; border-bottom: 2px solid var(--accent); padding-bottom: 30px; margin-bottom: 30px; }}
            h1 {{ font-size: 2.2rem !important; }}
            img {{ height: 280px !important; }}
        }}

        header {{ border-bottom: 2px solid var(--accent); background: #000; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; }}
        .brand {{ font-family: 'JetBrains Mono'; font-weight: 800; color: var(--accent); text-shadow: 0 0 5px var(--accent); }}
        
        .sidebar {{ position: sticky; top: 20px; height: fit-content; border-right: 1px solid #333; padding-right: 20px; }}
        .nav-btn {{ display: block; padding: 15px; margin-bottom: 12px; background: #080808; color: #fff; text-decoration: none; border: 1px solid var(--accent); font-family: 'JetBrains Mono'; text-align: center; font-weight: 800; transition: 0.3s; }}
        .nav-btn:hover {{ background: var(--accent); color: #000; box-shadow: 0 0 15px var(--accent); }}
        
        main {{ width: 100%; overflow: hidden; }}
        h1 {{ font-family: 'JetBrains Mono'; font-size: 3.5rem; color: #fff; line-height: 1.1; margin-bottom: 20px; }}
        .content {{ font-size: 1.15rem; line-height: 1.8; color: #ddd; }}
        .content h2 {{ color: var(--accent); border-left: 4px solid var(--accent); padding-left: 15px; margin-top: 50px; font-family: 'JetBrains Mono'; }}
        
        img {{ width: 100%; height: 450px; object-fit: cover; border: 1px solid #333; margin-bottom: 30px; filter: brightness(0.8); }}
        
        footer {{ border-top: 1px solid #333; padding: 60px; text-align: center; font-size: 0.8rem; color: #555; background: #000; }}
    </style></head>
    <body>
    <header><div class="brand">NEURAL_NODE_v5</div><div style="color:var(--accent); font-size:0.8rem;">● STATUS: ONLINE</div></header>
    <div class="container">
        <aside class="sidebar">
            <div style="color:var(--accent); font-weight:800; margin-bottom:20px;">// SYSTEM_TOOLS</div>
            <a href="{EMPIRE_URL}" class="nav-btn">🔓 ACCESS HQ</a>
            <a href="{AFFILIATE_LINK}" class="nav-btn">🚀 START BOT</a>
            <a href="{AMAZON_LINK}" class="nav-btn">🛡️ GET WALLET</a>
            <div style="margin-top:40px; font-size:0.85rem; color:var(--accent); font-weight:800; border-bottom:1px solid #333; padding-bottom:5px;">// LOG_ARCHIVE</div>
            <ul style="list-style:none; padding:0; line-height:2;">{sidebar_html}</ul>
        </aside>
        <main>
            <div style="color:var(--accent); font-family:'JetBrains Mono'; font-size:0.8rem; margin-bottom:10px;">[ENCRYPTED_SIGNAL_RECEIVED]</div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>NODE ID: 03 | DECENTRALIZED ENCRYPTION SERVER</footer></body></html>"""

def main():
    log("⚡ Unit 3 (Neural) Executing High-Volume Protocol...")
    topic = random.choice(HOOKING_TITLES)
    full_text = generate_hacker_leak(topic)
    html_body = markdown.markdown(full_text)
    
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk matrix code rain neon green data center 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:var(--accent); text-decoration:none; font-size:0.85rem;'>[{h.get('date')}] {h.get('title')[:20]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Neural Protocol Complete.")

if __name__ == "__main__": main()
