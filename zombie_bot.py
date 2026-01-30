import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM]
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 3호기: NEURAL ALGORITHM (다크/왼쪽사이드바)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "NEURAL ALGORITHM"
BLOG_BASE_URL = "https://ramuh18.github.io/neural-algorithm/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# [Monetization] 후킹용 링크
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

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

# [FALLBACK] 비상용 1,500자 리포트 (AI 실패시 작동)
FALLBACK_REPORT = """
## SYSTEM ALERT: The 2026 Algorithmic Decoupling Event

The global financial architecture is undergoing a forced reset. As we enter the second quarter of 2026, the divergence between legacy equity markets and decentralized automated liquidity pools has reached a critical breaking point. We are witnessing the death of manual trading and the rise of the autonomous economy.

### 1. The Death of Human Latency
Institutional capital is now completely dominated by high-frequency execution bots. In this environment, human reaction time is a liability. The 'Alpha' is no longer found in traditional analysis but in execution speed and algorithmic precision. Retail traders attempting to navigate this volatility without automated assistance are mathematically guaranteed to lose capital against sub-millisecond execution systems. The only survival strategy is to align with algorithmic systems that operate on institutional logic, leveraging AI to predict market movements before they appear on the retail charts.

### 2. Digital Sovereignty and Cold Storage Protocol
With central bank digital currencies (CBDCs) encroaching on financial privacy, the migration of smart money to hardware-secured sovereignty is accelerating. The Ledger ecosystem and non-custodial wallets are becoming the only true safe havens. Our on-chain analysis reveals a massive outflow of Bitcoin and high-cap alts from centralized exchanges into private cold storage. This supply shock will inevitably drive price discovery to unprecedented levels, leaving those without sovereign custody at the mercy of frozen exchanges and regulatory overreach.

### 3. The AI-DeFi Singularity: Future Protocol
We are witnessing the merger of Artificial Intelligence and Decentralized Finance. Smart contracts are evolving into autonomous agents capable of managing complex portfolios with zero human oversight. This shift necessitates a complete re-evaluation of asset allocation. Investors must now prioritize protocols that offer programmable liquidity and AI-driven yield optimization. The static portfolio is dead; the dynamic, AI-managed portfolio is the only vehicle capable of outpacing the coming inflationary wave.

### 4. Strategic Execution: The Path Forward
To maintain purchasing power in this new era, one must adopt a dual strategy: aggressive automated accumulation via algorithmic bots for income generation, and defensive fortification via cold storage for wealth preservation. This is not merely an investment suggestion; it is a survival protocol for the digital age.
"""

def generate_part(topic, focus):
    prompt = f"Write a deep, technical 600-word analysis on '{topic}'. Focus: {focus}. Tone: Cyberpunk, Institutional, Urgent. Use detailed data points. Markdown. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}, timeout=30)
        res = resp.json()['candidates'][0]['content']['parts'][0]['text']
        return re.sub(r'\{"role":.*?"content":', '', res, flags=re.DOTALL).replace('"}', '').strip()
    except: return ""

def create_final_html(topic, img_url, body_html, sidebar_html):
    # [핵심] 서치콘솔 태그가 삽입된 HTML 헤더
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
        .nav-btn {{ display: block; padding: 15px; margin-bottom: 12px; background: #080808; color: #fff; text-decoration: none; font-weight: 800; border: 1px solid var(--accent); transition: 0.3s; font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; text-align: left; }}
        .nav-btn:hover {{ background: var(--accent); color: #000; box-shadow: 0 0 15px var(--accent); transform: translateX(5px); }}
        .btn-icon {{ float: right; }}
        
        /* 본문 */
        h1 {{ font-family: 'JetBrains Mono', monospace; font-size: 3rem; color: #fff; margin-bottom: 10px; text-transform: uppercase; letter-spacing: -2px; line-height: 1.1; }}
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
            <div class="meta-line">STATUS: DECRYPTED | SOURCE: NEURAL-NET</div>
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
    log("⚡ Unit 3 (Neural) Finalizing...")
    topic = "The Convergence of AI Algorithmic Trading and Crypto Assets"
    
    # [핵심] 3개 파트로 1,500자 확보
    p1 = generate_part(topic, "Algorithmic Efficiency")
    p2 = generate_part(topic, "Decentralized Sovereignty")
    p3 = generate_part(topic, "Future Protocol")
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    
    if len(full_content) < 1000: 
        log("⚠️ AI content short. Engaging Fallback.")
        full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk matrix code rain neon green data center 8k wallpaper')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    # 사이드바 로그 링크 스타일
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
