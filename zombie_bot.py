import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM]
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BLOG_TITLE = "NEURAL ALGORITHM"
BLOG_BASE_URL = "https://ramuh18.github.io/neural-algorithm/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

HOOKING_TITLES = [
    "AI Predicts 2026 Market Crash: Warning",
    "Leaked: Wall Street's Secret AI Algorithm",
    "Move Your Crypto to Cold Storage NOW",
    "Exposed: The Banking Collapse Hidden Signs",
    "Whistleblower: How Bots Manipulate Bitcoin Price"
]

# [🛡️ 3호기 전용 비상 원고]
HACKER_FALLBACK = """
## [URGENT] SYSTEM BREACH: The Algorithmic Manipulation Detected

**The following data was intercepted from a high-frequency trading node.** The financial elite are utilizing sub-millisecond AI execution to front-run retail liquidity. This isn't a theory; it's the operational reality of the 2026 markets.

### 1. The Shadow Liquidity Pools
Institutional whales are no longer buying on public exchanges. They use dark pools to accumulate Bitcoin and Ethereum while retail is distracted by volatility. 

### 2. The Kill Switch
Our analysis shows a 'Kill Switch' protocol embedded in CBDC architectures. Your financial freedom is at risk. Move assets to cold storage immediately to maintain sovereignty.

### 3. Conclusion
Adopt automated accumulation. Secure your keys. The reset is imminent.
"""

def generate_hacker_leak(topic):
    leak_parts = ["Phase 1: Signal Interception", "Phase 2: Algorithm Reveal", "Phase 3: Survival Guide"]
    full_leak = f"# [DECRYPTED] INTERNAL LEAK: {topic}\n\n"
    
    success_count = 0
    for part in leak_parts:
        prompt = f"Whistleblower leak about '{topic}'. Focus: '{part}'. 600 words. Hacker style. English Only. Markdown."
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.8}}, timeout=45)
            res = resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            full_leak += f"## {part}\n\n" + res + "\n\n---\n\n"
            success_count += 1
            time.sleep(5) # 간격 5초로 확대하여 안정성 강화
        except:
            continue
            
    # 하나라도 성공했으면 결과를 반환하고, 전부 실패하면 비상 원고 반환
    return full_leak if success_count > 0 else HACKER_FALLBACK

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #050505; --text: #eeeeee; --accent: #00ff41; }}
        body {{ font-family: 'Rajdhani', sans-serif; background: var(--bg); color: var(--text); margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 300px 1fr; gap: 40px; padding: 40px 20px; }}
        @media(max-width: 1000px) {{ 
            .container {{ grid-template-columns: 1fr; padding: 20px; }}
            .sidebar {{ position: static !important; border-right: none !important; border-bottom: 2px solid var(--accent); padding-bottom: 30px; margin-bottom: 30px; }}
        }}
        header {{ border-bottom: 2px solid var(--accent); background: #000; padding: 15px 40px; }}
        .brand {{ font-family: 'JetBrains Mono'; font-weight: 800; color: var(--accent); }}
        .sidebar {{ position: sticky; top: 20px; height: fit-content; border-right: 1px solid #333; padding-right: 20px; }}
        .nav-btn {{ display: block; padding: 15px; margin-bottom: 12px; background: #080808; color: #fff; text-decoration: none; border: 1px solid var(--accent); text-align: center; }}
        h1 {{ font-family: 'JetBrains Mono'; font-size: 3rem; color: #fff; }}
        .content {{ font-size: 1.15rem; line-height: 1.8; color: #ddd; }}
        img {{ width: 100%; height: 450px; object-fit: cover; border: 1px solid #333; margin-bottom: 30px; }}
        footer {{ border-top: 1px solid #333; padding: 40px; text-align: center; font-size: 0.8rem; color: #555; }}
    </style></head>
    <body>
    <header><div class="brand">NEURAL_NODE_v5</div></header>
    <div class="container">
        <aside class="sidebar">
            <a href="{EMPIRE_URL}" class="nav-btn">🔓 ACCESS HQ</a>
            <a href="{AFFILIATE_LINK}" class="nav-btn">🚀 START BOT</a>
            <ul style="list-style:none; padding:0; line-height:2;">{sidebar_html}</ul>
        </aside>
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>NODE ID: 03 | DECENTRALIZED SERVER</footer></body></html>"""

def main():
    log("⚡ Unit 3 Stability Version Executing...")
    topic = random.choice(HOOKING_TITLES)
    full_text = generate_hacker_leak(topic)
    html_body = markdown.markdown(full_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk hacker neon green 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:var(--accent);'>[{h.get('date')}] {h.get('title')[:20]}...</a></li>" for h in history[:8]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Neural Stability Update Complete.")

if __name__ == "__main__": main()
