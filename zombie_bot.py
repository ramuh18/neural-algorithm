# (상단 import 및 설정 부분은 이전과 동일)

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="Jxh9S9J3S5_RBIpJH4CVrDkpRiDZ_mQ99TfIm7xK7YY" />
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #050505; --text: #eeeeee; --accent: #00ff41; }}
        body {{ font-family: 'Rajdhani', sans-serif; background: var(--bg); color: var(--text); margin: 0; overflow-x: hidden; }}
        
        /* [핵심] 모바일 대응 그리드 설정 */
        .container {{ 
            max-width: 1400px; margin: 0 auto; 
            display: grid; grid-template-columns: 300px 1fr; gap: 40px; padding: 40px 20px; 
        }}
        
        /* 모바일(1000px 이하)에서는 1열로 변경하여 겹침 방지 */
        @media(max-width: 1000px) {{ 
            .container {{ grid-template-columns: 1fr; padding: 20px; }}
            .sidebar {{ border-right: none !important; border-bottom: 2px solid var(--accent); padding-bottom: 20px; margin-bottom: 20px; position: static !important; }}
            h1 {{ font-size: 2rem !important; }}
            img {{ height: 250px !important; }}
        }}

        header {{ border-bottom: 2px solid var(--accent); background: #000; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; }}
        .brand {{ font-family: 'JetBrains Mono'; font-weight: 800; color: var(--accent); text-shadow: 0 0 5px var(--accent); }}
        
        .sidebar {{ position: sticky; top: 20px; height: fit-content; border-right: 1px solid #333; padding-right: 20px; }}
        .nav-btn {{ display: block; padding: 15px; margin-bottom: 12px; background: #080808; color: #fff; text-decoration: none; border: 1px solid var(--accent); font-family: 'JetBrains Mono'; text-align: center; }}
        .nav-btn:hover {{ background: var(--accent); color: #000; box-shadow: 0 0 15px var(--accent); }}
        
        main {{ width: 100%; overflow: hidden; }}
        h1 {{ font-family: 'JetBrains Mono'; font-size: 3rem; color: #fff; line-height: 1.1; }}
        .content {{ font-size: 1.1rem; line-height: 1.7; word-break: break-word; }} /* 긴 단어 잘림 방지 */
        img {{ width: 100%; height: 450px; object-fit: cover; border: 1px solid #333; }}
        
        footer {{ border-top: 1px solid #333; padding: 40px; text-align: center; font-size: 0.8rem; color: #555; }}
    </style></head>
    <body>
    <header><div class="brand">NEURAL_NODE_v5</div><div style="color:var(--accent); font-size:0.8rem;">● ONLINE</div></header>
    <div class="container">
        <aside class="sidebar">
            <div style="color:var(--accent); font-weight:800; margin-bottom:15px;">// ACCESS_PANEL</div>
            <a href="{EMPIRE_URL}" class="nav-btn">🔓 ACCESS HQ</a>
            <a href="{AFFILIATE_LINK}" class="nav-btn">🚀 START BOT</a>
            <a href="{AMAZON_LINK}" class="nav-btn">🛡️ GET WALLET</a>
            <div style="margin-top:40px; font-size:0.8rem; color:#666;">// RECENT_LOGS</div>
            <ul style="list-style:none; padding:0; line-height:1.8;">{sidebar_html}</ul>
        </aside>
        <main>
            <div style="color:var(--accent); font-family:'JetBrains Mono'; font-size:0.8rem; margin-bottom:10px;">STATUS: DECRYPTED</div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>NODE ID: 03 | DECENTRALIZED SERVER</footer></body></html>"""

# (하단 main 로직은 이전과 동일)
