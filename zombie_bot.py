import os, json, random, requests, markdown, urllib.parse, time, re, sys, io, textwrap
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration] 3호기 설정 (배당/복리)
BLOG_TITLE = "Dividend Compounding" 
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
# 아마존 링크는 스마트 매칭으로 자동 생성

# [주제 리스트 50개: 배당/복리/은퇴설계]
BACKUP_TOPICS = [
    "The Power of Compound Interest", "Dividend Aristocrats Strategy", "High Yield Savings Risks",
    "Real Estate Investment Trusts (REITs)", "FIRE Movement Guide", "Passive Income Streams 2026",
    "Early Retirement Planning", "Dividend Tax Implications", "DRIP Investing Explained",
    "Blue Chip Stocks Analysis", "Inflation-Proof Portfolio", "The 4% Withdrawal Rule",
    "Growth vs Dividend Investing", "Monthly Dividend Stocks", "ETF Investing for Beginners",
    "Index Fund Long-Term Strategy", "Crypto Staking Rewards", "Stablecoin Yield Farming",
    "Peer-to-Peer Lending Returns", "Rental Property Cash Flow", "Corporate Bond Yields",
    "Treasury Bills vs CDs", "Wealth Preservation Tactics", "Asset Allocation for Seniors",
    "The Snowball Effect in Finance", "Covered Call Strategies", "Preferred Stock Analysis",
    "Energy Sector Dividends", "Utility Stocks for Safety", "Healthcare REITs Outlook",
    "Consumer Staples Stability", "Dividend Payout Ratios", "Free Cash Flow Analysis",
    "Share Buybacks vs Dividends", "Special Dividends Explained", "Dividend Cuts Warning Signs",
    "International Dividend Stocks", "Withholding Tax on Dividends", "Roth IRA Compounding",
    "401k Maximization Secrets", "Hedge Fund Dividend Picks", "Warren Buffett's Strategy",
    "Economic Moat Importance", "Value Investing Principles", "Margin of Safety Concept",
    "Avoiding Value Traps", "High Yield Debt Risks", "Municipal Bonds Tax Free",
    "Generational Wealth Building", "Automated Wealth Management"
]

# [문단 블록 15개: 장기투자/안정성 강조]
CONTENT_BLOCKS = [
    """
    ## The Miracle of Compounding
    Albert Einstein reportedly called compound interest the "eighth wonder of the world." In the context of **{topic}**, this principle is the engine of wealth creation. Unlike speculative trading, focusing on {topic} allows time to do the heavy lifting. The longer your capital remains deployed in {topic}, the steeper your wealth trajectory becomes.
    """,
    """
    ## Building Passive Cash Flow
    The ultimate goal of financial independence is to decouple time from money. **{topic}** serves as a foundational pillar for this objective. By strategically allocating capital into assets related to {topic}, investors can generate a recurring income stream that persists regardless of market volatility. Cash flow is king.
    """,
    """
    ## Stability in Volatile Markets
    When the market corrects, speculative assets crash, but high-quality assets tied to **{topic}** often hold their value or continue to pay investors. History shows that during bear markets, the reinvestment of dividends from {topic} accelerates recovery times. {topic} is your defensive shield against economic downturns.
    """,
    """
    ## Analyzing the Payout Ratio
    A critical metric when evaluating **{topic}** is the sustainability of the payout. Investors must scrutinize the cash flow backing {topic}. If the yield looks too good to be true, it is often a yield trap. Sustainable growth in {topic} comes from robust underlying business fundamentals, not financial engineering.
    """,
    """
    ## The Inflation Hedge
    Cash in the bank is a losing position due to inflation. **{topic}** offers a mechanism to preserve purchasing power. Companies that can raise prices and pass those profits to shareholders via {topic} are the best hedge against currency debasement.
    """,
    """
    ## Tax Efficiency Matters
    Understanding the tax implications of **{topic}** can significantly boost your net returns. Whether it's qualified dividends or tax-advantaged accounts, optimizing how you hold assets related to {topic} is as important as the asset selection itself. Don't let taxes erode the benefits of {topic}.
    """,
    """
    ## The Psychological Edge
    Investing in **{topic}** provides a psychological advantage. While day traders panic over daily price swings, dividend investors view price drops as an opportunity to buy more income-producing assets regarding {topic} at a discount. This mindset shift is essential for long-term success.
    """,
    """
    ## REITs and Real Assets
    Integrating real assets into your portfolio via **{topic}** provides diversification. Real Estate Investment Trusts (REITs) related to {topic} allow retail investors to own institutional-grade properties without the headaches of being a landlord. This is liquid real estate exposure at its finest.
    """,
    """
    ## The Role of ETFs
    For those seeking instant diversification, ETFs focused on **{topic}** are a powerful tool. They eliminate single-stock risk while providing exposure to the broad theme of {topic}. Automated monthly contributions to these funds create a dollar-cost averaging effect that smooths out entry prices.
    """,
    """
    ## Dividend Aristocrats
    Companies with a multi-decade history of raising payments are often central to the **{topic}** strategy. These "Aristocrats" have proven their ability to navigate recessions while prioritizing shareholder returns. Betting on {topic} through these stalwarts is a bet on corporate resilience.
    """,
    """
    ## Crypto Yields vs Traditional
    The emergence of DeFi has introduced a new dimension to **{topic}**. While traditional yields are lower, crypto staking offers higher potential returns regarding {topic}, albeit with higher risk. A balanced portfolio might blend the stability of traditional {topic} with the aggressive growth of digital yields.
    """,
    """
    ## The 4% Rule and {topic}
    Retirement planning often cites the 4% rule. However, a robust portfolio built around **{topic}** might allow for a higher withdrawal rate or, better yet, living solely off the yield without touching the principal. This is the ultimate "sleep well at night" strategy.
    """,
    """
    ## Reinvestment Protocols
    The secret sauce of **{topic}** is the Automatic Dividend Reinvestment Plan (DRIP). By automatically funneling payouts back into {topic}, you purchase more shares, which generate more income, creating a virtuous cycle. Over 20 years, the majority of total returns come from this reinvestment.
    """,
    """
    ## Sector Allocation
    Not all sectors are created equal regarding **{topic}**. Utilities and consumer staples are traditional defensives, while tech is becoming a new source of dividend growth. Balancing your exposure to {topic} across different sectors prevents concentration risk.
    """,
    """
    ## Exit Strategy vs Forever Hold
    With **{topic}**, the best holding period is often "forever." Unlike growth stocks that require timing the exit, the goal with {topic} is to accumulate an income stream that outlives you. This generational thinking shifts the focus from price appreciation to income reliability.
    """
]

# [3호기 스마트 매칭: 은퇴/배당/절세]
def get_smart_amazon_link(topic):
    topic_lower = topic.lower()
    search_keyword = "dividend+investing+books" # 기본값
    button_text = "📚 WEALTH BOOKS"

    if any(x in topic_lower for x in ["real", "estate", "reit", "property", "rental"]):
        search_keyword = "real+estate+investing+books"
        button_text = "🏠 REAL ESTATE GUIDE"
    elif any(x in topic_lower for x in ["tax", "ira", "401k", "retirement", "fire"]):
        search_keyword = "tax+free+wealth+book"
        button_text = "📉 TAX STRATEGIES"
    elif any(x in topic_lower for x in ["crypto", "staking", "yield", "defi"]):
        search_keyword = "ledger+nano+x"
        button_text = "🔐 SECURE YIELD"
    elif any(x in topic_lower for x in ["gold", "bond", "treasury", "safe"]):
        search_keyword = "gold+coins+investment"
        button_text = "💰 BUY GOLD ASSETS"
    
    return f"https://www.amazon.com/s?k={search_keyword}&tag=empireanalyst-20", button_text

def get_live_trends():
    selected_topic = random.choice(BACKUP_TOPICS)
    return [selected_topic]

def generate_deep_report(topic):
    intro = f"""
# Wealth Report: {topic}

## Investment Thesis
Building long-term wealth requires a strategy that works while you sleep. **{topic}** represents a cornerstone of this philosophy. By prioritizing cash flow and compound growth, investors can navigate market volatility with confidence. This report explores the mechanics of {topic} for the intelligent investor.
"""
    
    amazon_url, btn_text = get_smart_amazon_link(topic)
    selected_blocks = random.sample(CONTENT_BLOCKS, 4)
    body_content = ""
    
    for block in selected_blocks[:2]:
        body_content += textwrap.dedent(block).format(topic=topic) + "\n"

    # [중간 광고] 3호기 테마: 초록색(성장/수익)
    body_content += f"""
<div style="margin: 30px 0; padding: 20px; background: #f0fdf4; border-left: 5px solid #15803d; border-radius: 4px;">
    <h3 style="margin-top:0; color:#14532d;">🌱 Grow Your Passive Income</h3>
    <p>Maximize your returns on <strong>{topic}</strong> with the right tools and strategies.</p>
    <a href="{amazon_url}" style="display:inline-block; background:#15803d; color:#fff; padding:10px 20px; text-decoration:none; font-weight:bold; border-radius:4px;">{btn_text}</a>
    <a href="{AFFILIATE_LINK}" style="display:inline-block; background:#d97706; color:#fff; padding:10px 20px; text-decoration:none; font-weight:bold; border-radius:4px; margin-left:10px;">📈 START COMPOUNDING</a>
</div>
"""
    for block in selected_blocks[2:]:
        body_content += textwrap.dedent(block).format(topic=topic) + "\n"

    conclusion = f"""
## Final Verdict
Consistency is the key to success with **{topic}**. Time in the market beats timing the market.
<br><br>
**Start your compounding journey today.**
<div style="background: #fff; padding: 20px; border: 1px solid #ddd; margin-top: 20px; border-radius: 4px; border-top: 4px solid #15803d;">
    <h3>💰 Wealth Recommendations</h3>
    <ul style="margin-bottom: 20px;">
        <li>Reinvest all dividends automatically.</li>
        <li>Focus on companies with wide economic moats.</li>
    </ul>
    <a href="{EMPIRE_URL}" style="background: #14532d; color: white; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 4px; font-size: 0.9rem;">ACCESS WEALTH PORTFOLIO</a>
</div>
"""
    return intro + body_content + conclusion

def generate_seo_files(history):
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{BLOG_BASE_URL}</loc><priority>1.0</priority></url>\n'
    for h in history[:50]:
        sitemap += f'  <url><loc>{BLOG_BASE_URL}{h["file"]}</loc><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write(sitemap)
    robots = f"User-agent: *\nAllow: /\nSitemap: {BLOG_BASE_URL}sitemap.xml"
    with open("robots.txt", "w", encoding="utf-8") as f: f.write(robots)

def create_final_html(topic, img_url, body_html, sidebar_html, amazon_url, btn_text):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="여기에_인증태그_입력" />
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        /* 3호기 테마: 딥그린 & 골드 (돈, 성장, 안정) */
        :root {{ --main-green: #15803d; --accent-gold: #d97706; --soft-bg: #f0fdf4; }}
        body {{ font-family: 'Lato', sans-serif; background: #fafaf9; color: #1c1917; line-height: 1.8; margin: 0; }}
        header {{ background: #fff; color: var(--main-green); padding: 30px; text-align: center; border-bottom: 5px solid var(--main-green); }}
        .brand {{ font-family: 'Playfair Display', serif; font-size: 2.2rem; letter-spacing: 1px; color: var(--main-green); }}
        .container {{ max-width: 1100px; margin: 40px auto; display: grid; grid-template-columns: 1fr 320px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 900px) {{ .container {{ grid-template-columns: 1fr; }} }}
        main {{ background: #fff; padding: 50px; border: 1px solid #e7e5e4; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-radius: 8px; }}
        h1 {{ color: var(--main-green); font-family: 'Playfair Display', serif; font-size: 2.4rem; margin-top:0; }}
        .content h2 {{ color: #064e3b; margin-top: 40px; border-bottom: 2px solid var(--accent-gold); padding-bottom: 10px; font-size: 1.6rem; }}
        img {{ width: 100%; height: auto; margin-bottom: 30px; border-radius: 8px; }}
        .side-card {{ background: #fff; padding: 25px; border: 1px solid #e7e5e4; margin-bottom: 20px; border-top: 4px solid var(--main-green); border-radius: 8px; }}
        .btn {{ display: block; padding: 12px; background: var(--main-green); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 10px; border-radius: 4px; font-size: 0.9rem; transition: 0.3s; }}
        .btn:hover {{ background: var(--accent-gold); }}
        footer {{ text-align: center; padding: 50px; color: #78716c; background: #fff; border-top: 1px solid #e7e5e4; margin-top: 50px; }}
        .footer-links a {{ color: #57534e; margin: 0 10px; cursor: pointer; text-decoration: none; font-weight: bold; }}
        .amazon-disclaimer {{ font-size: 0.8rem; color: #a8a29e; margin-top: 20px; font-style: italic; }}
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); }}
        .modal-content {{ background: #fff; margin: 15% auto; padding: 30px; width: 80%; max-width: 600px; border-radius: 8px; font-family: sans-serif; }}
        .close {{ float: right; font-size: 28px; cursor: pointer; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div><div style="font-size:0.9rem; color:#78716c;">BUILDING GENERATIONAL WEALTH</div></header>
    <div class="container">
        <main>
            <div style="color:var(--accent-gold); font-size:0.8rem; margin-bottom:10px; font-weight:bold; text-transform:uppercase;">Long-Term Strategy</div>
            <h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <h3 style="margin-top:0; color:var(--main-green); font-family:'Playfair Display';">Wealth Tools</h3>
                <a href="{EMPIRE_URL}" class="btn">🌳 GROW PORTFOLIO</a>
                <a href="{AFFILIATE_LINK}" class="btn" style="background:#064e3b;">📊 HIGH YIELD</a>
                <a href="{amazon_url}" class="btn" style="background:#d97706;">{btn_text}</a>
            </div>
            <div class="side-card">
                <h3>Recent Insights</h3>
                <ul style="padding-left:20px; list-style-type: circle;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>
        <div class="footer-links">
            <a onclick="openModal('about')">About Us</a>
            <a onclick="openModal('privacy')">Privacy Policy</a>
            <a onclick="openModal('contact')">Contact</a>
        </div>
        &copy; 2026 {BLOG_TITLE}. Compounding Since Day 1.
        <div class="amazon-disclaimer">* As an Amazon Associate, we earn from qualifying purchases.</div>
    </footer>
    <div id="infoModal" class="modal"><div class="modal-content"><span class="close" onclick="closeModal()">&times;</span><div id="modalBody"></div></div></div>
    <script>
        const info = {{
            about: "<h2>About Dividend Compounding</h2><p>We focus on building passive income streams through dividend stocks, REITs, and smart asset allocation.</p>",
            privacy: "<h2>Privacy Policy</h2><p>We do not collect personal data. Cookies are used for analytics only.</p>",
            contact: "<h2>Contact</h2><p>Admin: admin@empire-analyst.digital</p>"
        }};
        function openModal(id) {{ document.getElementById('modalBody').innerHTML = info[id]; document.getElementById('infoModal').style.display = "block"; }}
        function closeModal() {{ document.getElementById('infoModal').style.display = "none"; }}
    </script>
    </body></html>"""

def main():
    topic = get_live_trends()[0] 
    amazon_url, btn_text = get_smart_amazon_link(topic)
    body_text = generate_deep_report(topic) 
    html_body = markdown.markdown(body_text)
    
    # [3호기 이미지] 'Growing Money', 'Gold', 'Graph' 느낌
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('growing money tree gold coins financial graph green nature 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#1c1917; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    generate_seo_files(history)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html, amazon_url, btn_text)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
