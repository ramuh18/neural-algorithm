import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM]
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 3호기: NEURAL ALGORITHM
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "NEURAL ALGORITHM"
BLOG_BASE_URL = "https://ramuh18.github.io/neural-algorithm/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# [Monetization]
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [🔥 ENGLISH HOOKING TITLES] 8단어 미만, 유튜브 썸네일 스타일
HOOKING_TITLES = [
    "AI Predicts 2026 Market Crash: Warning",
    "Leaked: Wall Street's Secret AI Algorithm",
    "Move Your Crypto to Cold Storage NOW",
    "Exposed: The Banking Collapse Hidden Signs",
    "1000x Signal: AI Detects Massive Accumulation",
    "Do Not Ignore This AI Wealth Warning",
    "Revealed: Central Bank's Digital Kill Switch",
    "The Great AI Wealth Shift Is Here",
    "Whistleblower: How Bots Manipulate Bitcoin Price",
    "Urgent: The End of Manual Trading"
]

# [Sitemap]
def generate_sitemap(history):
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    today = datetime.now().strftime('%Y-%m-%d')
    urls = [f"<url><loc>{BLOG_BASE_URL}</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>"]
    for item in history[:50]:
        file_name = item.get('file', '')
        file_date = item.get('date', today)
        if file_name:
            urls.append(f"<url><loc>{BLOG_BASE_URL}{file_name}</loc><lastmod>{file_date}</lastmod><priority>0.8</priority></url>")
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(urls)}</urlset>'
    with open(sitemap_path, "w", encoding="utf-8") as f: f.write(xml_content)
    log("📡 Sitemap.xml updated.")

# [FALLBACK] 비상용 원고 (영어, 긴급 톤)
FALLBACK_REPORT = """
## URGENT: The 2026 Algorithmic Shift

**This is not a drill.** The divergence between legacy markets and automated liquidity pools has reached a breaking point. We are witnessing the death of manual trading.

### 1. Humans Can't Compete
Institutional capital is now dominated by high-frequency bots. Human reaction time is a liability. The 'Alpha' is in microseconds. Retail traders without automation are guaranteed to lose.

### 2. The Run to Cold Storage
With CBDCs threatening privacy, smart money is fleeing to hardware wallets. The Ledger ecosystem is the new Swiss Bank. Our data shows massive Bitcoin outflows from exchanges to private vaults.

### 3. Action Required
To survive, adopt a dual strategy: aggressive AI accumulation and defensive cold storage. **Ignore this at your own risk.**
"""

def generate_part(topic, focus):
    # 프롬프트: 영어 작성 강제 (English Only)
    prompt = f"Write a shocking, controversial 600-word whistleblower report on '{topic}'. Focus: {focus}. Tone: Urgent, Secretive, 'Don't let them know', Cyberpunk. Reveal hidden truths. Use short, punchy sentences. Markdown. **English Only.**"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.6}}, timeout=30)
        res = resp.json()['candidates'][0]['content']['parts'][0]['text']
        return re.sub(r'\{"role":.*?"content":', '', res, flags=re.DOTALL).replace('"}', '').strip()
    except: return ""

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="Jxh9S9J3S5_RBIpJH4CVrDkpRiDZ_mQ99TfIm7xK7YY" />
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        /* [THEME] 매트릭스 다크 & 네온 그린 */
        :root {{ --bg: #050505; --text: #eeeeee; --accent: #00ff41; --border: #333; }}
        body {{ font-family: 'Rajdhani', sans-serif; line-height: 1.6; color: var(--text); background: var(--bg); margin: 0; }}
        
        /* [LAYOUT] 사이드바 왼쪽 (300px) */
        .container {{ max-width: 1600px; margin: 0 auto; display: grid; grid-template-columns: 300px 1fr; gap: 50px; padding: 40px 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        
        /* 헤더 */
        header {{ border-bottom: 2px solid var(--accent); background: #000; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .brand {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 1.5rem; color: var(--accent); text-shadow: 0 0 5px var(--accent); }}
        
        /* 사이드바 */
        .sidebar {{ position: sticky; top: 120px; height: fit-content; border-right: 1px solid #333; padding-right: 30px; }}
        .nav-header {{ color: #fff; font-size: 0.8rem; font-weight:800; letter-spacing: 2px; margin-bottom: 15px; display: block; border-bottom: 1px solid #444; padding-bottom:5px; }}
        
        /* 후킹 버튼 스타일 */
        .nav-btn {{ display: block; padding: 15px; margin-bottom: 12px; background: #080808; color: #fff; text-decoration: none; font-weight: 800; border: 1px solid var(--accent); transition: 0.3s; font-family: 'JetBrains Mono', sans-serif; font-size: 0.95rem; text-align: left; }}
        .nav-btn:hover {{ background: var(--accent); color: #000; box-shadow: 0 0 15px var(--accent); transform: translateX(5px); }}
        .btn-icon {{ float: right; }}
        
        /* 본문 */
        h1 {{ font-family: 'JetBrains Mono', monospace; font-size: 3rem; color: #fff; margin-bottom: 10px; font-weight: 800; line-height: 1.1; letter-spacing: -2px; text-transform: uppercase; }}
        .meta-line {{ color: var(--accent); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-bottom: 40px; border: 1px dashed var(--accent); display: inline-block; padding: 5px 10px; }}
        
        .content {{ font-size: 1.15rem; text-align: justify; color: #ddd; }}
        .content h2 {{ color: #fff; border-left: 4px solid var(--accent); padding-left: 15px; margin-top: 50px; font-family: 'JetBrains Mono', monospace; font-size: 1.6rem; }}
        
        /* 이미지 */
        .featured-img {{ width: 100%; height: 450px; object-fit: cover; border: 1px solid #333; filter: brightness(0.9) contrast(1.1); }}
        .img-caption {{ background: #111; color: #aaa; padding: 15px; text-align: center; font-family: 'JetBrains Mono', monospace; border: 1px solid #333; font-size: 0.8rem; }}
        .img-caption a {{ color: var(--accent); font-weight: bold; text-decoration: none; border-bottom: 1px solid var(--accent); }}
        
        footer {{ border-top: 1px solid #333; padding: 60px; text-align: center; font-size: 0.8rem; color: #555; margin-top: 100px; }}
    </style></head>
    <body>
    <header>
        <div class="brand">NEURAL_NODE_v5</div>
        <div style="color:#fff; font-family:'JetBrains Mono'; font-size:0.8rem;">● ONLINE</div>
    </header>
    <div class="container">
        <aside class="sidebar">
            <span class="nav-header">// SECRET TOOLS</span>
            <a href="{EMPIRE_URL}" class="nav-btn">🔓 ACCESS HQ INTEL <span class="btn-icon">>></span></a>
            <a href="{AFFILIATE_LINK}" class="nav-btn">🚀 START AI TRADING <span class="btn-icon">>></span></a>
            <a href="{AMAZON_LINK}" class="nav-btn">🛡️ GET COLD WALLET <span class="btn-icon">>></span></a>
            
            <span class="nav-header" style="margin-top:50px;">// SYSTEM LOGS</span>
            <ul style="list-style:none; padding:0; line-height:1.8;">{sidebar_html}</ul>
        </aside>
        
        <main>
            <h1>{topic}</h1>
            <div class="meta-line">STATUS: LEAKED | SOURCE: CLASSIFIED</div>
            <div style="margin-bottom:40px;">
                <img src="{img_url}" class="featured-img">
                <div class="img-caption">
                    [SYSTEM DETECTED HIGH VALUE SIGNAL]<br>
                    <a href="{EMPIRE_URL}">Download the 2026 Strategy File at Empire Analyst HQ</a>
                </div>
            </div>
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>
        <div>NODE ID: 03 | DECENTRALIZED SERVER</div>
        <div>Amazon Disclaimer: As an Amazon Associate, I earn from qualifying purchases.</div>
    </footer></body></html>"""

def main():
    log("⚡ Unit 3 (Neural) English Hook Ver. Started")
    
    # [핵심] 8단어 미만 영어 후킹 제목 랜덤 선택
    topic = random.choice(HOOKING_TITLES)
    log(f"Selected Title: {topic}")
    
    # 3개 파트로 1,500자 확보
    p1 = generate_part(topic, "The Hidden Danger")
    p2 = generate_part(topic, "The Secret Mechanism")
    p3 = generate_part(topic, "The Escape Plan")
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    
    if len(full_content) < 1000: 
        log("⚠️ AI content short. Engaging Fallback.")
        full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk matrix code rain neon green data center 8k wallpaper')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    # 사이드바 로그 링크
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#00ff41; font-weight:bold; text-decoration:none; font-family:JetBrains Mono; font-size:0.85rem;'>[{h.get('date','LOG')}] {h.get('title','Log Data')}</a></li>" for h in history[:8]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(full_html)
    with open(os.path.join(BASE_DIR, archive_name), "w", encoding="utf-8") as f: f.write(full_html)
    
    generate_sitemap(history)
    log("✅ System Update Complete.")

if __name__ == "__main__": main()
