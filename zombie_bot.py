import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM]
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration] 3호기: 다크 네온 & 왼쪽 사이드바
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "NEURAL ALGORITHM"
BLOG_BASE_URL = "https://ramuh18.github.io/neural-algorithm/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# [Monetization] 수익화 링크 (트레이딩 봇 & 하드웨어 월렛)
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [Sitemap] 2호기의 강력한 자동 생성 기능 탑재
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
    print("📡 System Log: Sitemap updated.")

# [FALLBACK] 3호기 전용: 미래지향적/분석적 톤의 리포트
FALLBACK_REPORT = """
## SYSTEM ALERT: Algorithmic Market Divergence Detected

The neural networks have identified a significant divergence in global asset classes. As 2026 progresses, the correlation between traditional equity markets and decentralized liquidity pools is breaking down.

### 1. The Rise of Algo-Driven Capital
Institutional capital is now primarily managed by high-frequency execution bots. This shift means that human reaction times are no longer competitive. The 'Alpha' is generated in microseconds. To survive, investors must leverage automated signals and secure their assets in cold storage environments.

### 2. Digital Sovereignty Protocol
Our analysis indicates a mass migration of smart money towards hardware-secured sovereignty. The Ledger ecosystem and decentralized exchanges are becoming the new Swiss Bank accounts. Ignoring this trend is a critical risk factor for any portfolio targeting growth in the AI era.
"""

def generate_part(topic, focus):
    # 프롬프트: 사이버펑크, 데이터 중심 톤
    prompt = f"Write a futuristic 600-word tech analysis on '{topic}'. Focus: {focus}. Tone: Cyberpunk, Data-driven, Institutional. Markdown. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}, timeout=30)
        res = resp.json()['candidates'][0]['content']['parts'][0]['text']
        return re.sub(r'\{"role":.*?"content":', '', res, flags=re.DOTALL).replace('"}', '').strip()
    except: return ""

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        /* [THEME] 다크 모드 & 네온 그린 */
        :root {{ --bg: #050505; --text: #e0e0e0; --accent: #00ff41; --panel: #111; --border: #333; }}
        body {{ font-family: 'Rajdhani', sans-serif; line-height: 1.6; color: var(--text); background: var(--bg); margin: 0; }}
        
        /* [LAYOUT] 사이드바 왼쪽 배치 (Grid: 320px | 1fr) */
        .container {{ max-width: 1600px; margin: 0 auto; display: grid; grid-template-columns: 320px 1fr; gap: 60px; padding: 40px 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        
        /* 헤더: 터미널 스타일 */
        header {{ border-bottom: 1px solid var(--accent); background: #000; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); }}
        .brand {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 1.4rem; color: var(--accent); letter-spacing: -1px; }}
        .status {{ font-size: 0.8rem; color: #888; font-family: 'JetBrains Mono', monospace; }}
        
        /* 사이드바 (왼쪽) */
        .sidebar {{ position: sticky; top: 100px; height: fit-content; border-right: 1px solid var(--border); padding-right: 40px; text-align: right; }}
        .nav-header {{ color: #666; font-size: 0.7rem; letter-spacing: 2px; margin-bottom: 15px; display: block; }}
        .nav-btn {{ display: block; padding: 15px; margin-bottom: 10px; background: #0f0f0f; color: #aaa; text-decoration: none; font-weight: 700; border-right: 2px solid #333; transition: 0.3s; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }}
        .nav-btn:hover {{ background: #1a1a1a; color: var(--accent); border-right: 2px solid var(--accent); }}
        
        /* 본문 영역 */
        h1 {{ font-family: 'JetBrains Mono', monospace; font-size: 3.2rem; color: #fff; margin-bottom: 20px; text-transform: uppercase; letter-spacing: -2px; line-height: 1.1; }}
        .meta-line {{ border-top: 1px dashed #333; border-bottom: 1px dashed #333; padding: 10px 0; color: var(--accent); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-bottom: 30px; }}
        
        .content {{ font-size: 1.2rem; text-align: justify; color: #ccc; }}
        .content h2 {{ color: #fff; border-left: 3px solid var(--accent); padding-left: 15px; margin-top: 50px; font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; }}
        .content p {{ margin-bottom: 25px; }}
        
        /* 이미지: 매트릭스 느낌 */
        .img-wrapper {{ margin-bottom: 40px; border: 1px solid #333; padding: 5px; background: #000; }}
        .featured-img {{ width: 100%; height: 500px; object-fit: cover; filter: contrast(1.2) saturate(1.2); opacity: 0.9; }}
        .img-caption {{ background: #0a0a0a; color: var(--accent); padding: 15px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; border-top: 1px solid #333; }}
        
        footer {{ border-top: 1px solid #333; padding: 60px; text-align: center; font-size: 0.8rem; color: #444; margin-top: 100px; font-family: 'JetBrains Mono', monospace; }}
    </style></head>
    <body>
    <header>
        <div class="brand">>_ NEURAL_ALGORITHM</div>
        <div class="status">● SYSTEM ONLINE</div>
    </header>
    <div class="container">
        <aside class="sidebar">
            <span class="nav-header">// TERMINAL ACCESS</span>
            <a href="{EMPIRE_URL}" class="nav-btn">ACCESS MAIN NODE</a>
            <a href="{AFFILIATE_LINK}" class="nav-btn">INITIATE TRADING BOT</a>
            <a href="{AMAZON_LINK}" class="nav-btn">SECURE HARDWARE</a>
            
            <span class="nav-header" style="margin-top:50px;">// SYSTEM LOGS</span>
            <ul style="list-style:none; padding:0; line-height:2;">{sidebar_html}</ul>
        </aside>
        
        <main>
            <h1>{topic}</h1>
            <div class="meta-line">Encryption: AES-256 | Source: Neural Network | Status: Decrypted</div>
            
            <div class="img-wrapper">
                <img src="{img_url}" class="featured-img">
                <div class="img-caption">
                    [SYSTEM DETECTED HIGH VALUE SIGNAL]<br>
                    <a href="{EMPIRE_URL}" style="color:#fff; text-decoration:underline;">Download Full Strategy File at Main Node >></a>
                </div>
            </div>
            
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>
        <div>NODE ID: 03 | LOCATION: DECENTRALIZED</div>
        <div>Amazon Disclaimer: As an Amazon Associate, I earn from qualifying purchases.</div>
    </footer></body></html>"""

def main():
    print("⚡ Unit 3 (Neural) Initializing...")
    topic = "The Convergence of AI Algorithmic Trading and Crypto Assets"
    
    # 3단계 생성으로 1,500자 확보
    p1 = generate_part(topic, "Algorithmic Efficiency")
    p2 = generate_part(topic, "Market Decentralization")
    p3 = generate_part(topic, "Future Protocol")
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    if len(full_content) < 1000: full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    # 이미지: 사이버펑크, 네온, 매트릭스 스타일
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk matrix code rain neon green data center 8k wallpaper')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    # 사이드바 링크 생성 (네온 그린 컬러)
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#00ff41; text-decoration:none; font-family:JetBrains Mono; font-size:0.8rem;'>{h.get('title','Log Data')}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(full_html)
    with open(os.path.join(BASE_DIR, archive_name), "w", encoding="utf-8") as f: f.write(full_html)
    
    generate_sitemap(history)
    print("✅ System Update Complete.")

if __name__ == "__main__": main()
