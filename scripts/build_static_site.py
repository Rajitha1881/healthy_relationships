#!/usr/bin/env bash
import os
import sys
import json
import shutil

# Ensure the repository root is in Python's module search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relationship_messages import MESSAGES

def build():
    output_dir = "public"
    os.makedirs(output_dir, exist_ok=True)

    messages_json = json.dumps(MESSAGES, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Healthy Relationships App</title>
  <meta name="description" content="Daily advice, healthy communication tips, and relationship affirmations.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>❤️</text></svg>">
  <style>
    :root {{
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --muted: #94a3b8;
      --accent: #ec4899;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    body {{ background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; }}
    .card {{ background: var(--card-bg); max-width: 680px; width: 100%; border-radius: 20px; box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5); padding: 40px; text-align: center; border: 1px solid #334155; position: relative; overflow: hidden; }}
    .card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #6366f1, #ec4899, #8b5cf6); }}
    h1 {{ font-size: 2rem; font-weight: 800; color: #ffffff; margin-bottom: 8px; letter-spacing: -0.025em; }}
    p.subtitle {{ color: var(--muted); font-size: 1rem; margin-bottom: 30px; line-height: 1.5; }}
    .message-box {{ background: #0f172a; border-radius: 16px; padding: 32px 24px; margin-bottom: 28px; min-height: 140px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 1px solid #334155; transition: all 0.25s ease; }}
    .category-badge {{ display: inline-block; background: var(--primary); color: white; padding: 6px 16px; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); }}
    .message-text {{ font-size: 1.25rem; font-weight: 500; line-height: 1.6; color: #f1f5f9; }}
    .btn-group {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 24px; }}
    button {{ background: #334155; color: #f1f5f9; border: 1px solid #475569; padding: 10px 18px; border-radius: 10px; font-size: 0.92rem; font-weight: 600; cursor: pointer; transition: all 0.2s ease; }}
    button:hover {{ background: #475569; border-color: var(--primary); transform: translateY(-2px); }}
    button.btn-primary {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; color: white; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4); }}
    button.btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6); }}
    .actions-bar {{ display: flex; gap: 12px; justify-content: center; margin-top: 10px; }}
    .copy-btn {{ background: transparent; border: 1px solid #475569; color: var(--muted); font-size: 0.85rem; padding: 6px 14px; border-radius: 8px; }}
    .copy-btn:hover {{ color: white; border-color: var(--muted); }}
    .footer-links {{ margin-top: 28px; font-size: 0.85rem; color: var(--muted); border-top: 1px solid #334155; padding-top: 20px; }}
    .footer-links a {{ color: var(--primary); text-decoration: none; font-weight: 500; margin: 0 8px; transition: color 0.15s ease; }}
    .footer-links a:hover {{ color: #a5b4fc; text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Healthy Relationships</h1>
    <p class="subtitle">Daily guidance, healthy communication tips, and relationship affirmations</p>

    <div class="message-box" id="box">
      <span class="category-badge" id="categoryBadge">Growth</span>
      <p class="message-text" id="messageText">Celebrate each other's personal growth, even when it brings new changes.</p>
    </div>

    <div class="btn-group">
      <button class="btn-primary" onclick="getRandomMessage()">🎲 Random Message</button>
      <button onclick="getMessageByCategory('growth')">🌱 Growth</button>
      <button onclick="getMessageByCategory('communication')">💬 Communication</button>
      <button onclick="getMessageByCategory('appreciation')">❤️ Appreciation</button>
      <button onclick="getMessageByCategory('boundaries')">🛡️ Boundaries</button>
      <button onclick="getMessageByCategory('conflict_resolution')">🤝 Conflict Resolution</button>
    </div>

    <div class="actions-bar">
      <button class="copy-btn" onclick="copyMessage()" id="copyBtn">📋 Copy Message</button>
    </div>

    <div class="footer-links">
      <span>Docker Container: <code>docker pull ghcr.io/rajitha1881/healthy_relationships:latest</code></span>
      <br><br>
      <a href="https://github.com/Rajitha1881/healthy_relationships" target="_blank">View on GitHub</a> •
      <a href="https://github.com/Rajitha1881/healthy_relationships/pkgs/container/healthy_relationships" target="_blank">GitHub Packages</a>
    </div>
  </div>

  <script>
    const MESSAGES = {messages_json};

    function getRandomMessage() {{
      const allCategories = Object.keys(MESSAGES);
      const randomCat = allCategories[Math.floor(Math.random() * allCategories.length)];
      getMessageByCategory(randomCat);
    }}

    function getMessageByCategory(category) {{
      const list = MESSAGES[category];
      if (!list || list.length === 0) return;
      const message = list[Math.floor(Math.random() * list.length)];
      
      const badge = document.getElementById('categoryBadge');
      const text = document.getElementById('messageText');
      
      badge.innerText = category.replace('_', ' ');
      text.innerText = message;
      
      const copyBtn = document.getElementById('copyBtn');
      copyBtn.innerText = "📋 Copy Message";
    }}

    function copyMessage() {{
      const text = document.getElementById('messageText').innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const copyBtn = document.getElementById('copyBtn');
        copyBtn.innerText = "✓ Copied to Clipboard!";
        setTimeout(() => {{
          copyBtn.innerText = "📋 Copy Message";
        }}, 2000);
      }});
    }}
  </script>
</body>
</html>
"""

    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✓ Static site built successfully in public/index.html")

if __name__ == "__main__":
    build()
