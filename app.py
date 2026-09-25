import os
import re
import json
import random
import urllib.parse
import requests
import streamlit as st

# Setup page configuration
st.set_page_config(
    page_title="Future Dev Roast 🔥",
    page_icon="💀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Modern / Cyber Aesthetics
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Fira+Code:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    /* Header styling */
    .hero-container {
        text-align: center;
        padding: 2rem 1rem 1.5rem 1.5rem;
        background: linear-gradient(135deg, rgba(255,75,75,0.1) 0%, rgba(138,43,226,0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #FF4B4B, #FF8E53, #8A2BE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -1px;
    }

    .hero-tagline {
        font-size: 1.25rem;
        color: #E0E0E0;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .hero-sub {
        font-size: 0.95rem;
        color: #8B949E;
    }

    /* Custom Card Styling */
    .roast-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .roast-card:hover {
        border-color: #FF4B4B;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Verdict Badge */
    .verdict-badge {
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        padding: 1rem;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.2) 0%, rgba(255, 142, 83, 0.15) 100%);
        border: 2px solid #FF4B4B;
        color: #FFFFFF;
        letter-spacing: 0.5px;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.2);
    }

    /* Score Bar styling */
    .score-container {
        margin: 1rem 0;
    }
    .score-header {
        display: flex;
        justify-content: space-between;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
    }
    .score-bar-bg {
        width: 100%;
        height: 16px;
        background-color: #21262D;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #30363D;
    }
    .score-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8E53 50%, #00F5FF 100%);
        border-radius: 8px;
        transition: width 1s ease-in-out;
    }

    /* Compare Section */
    .compare-box {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1rem;
    }
    .compare-card {
        background: #0D1117;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #30363D;
        text-align: center;
    }
    .compare-score {
        font-size: 2rem;
        font-weight: 900;
        margin-top: 0.2rem;
    }
    .you-score { color: #FF4B4B; }
    .top-score { color: #00F5FF; }

    /* Reality Check Quote Box */
    .quote-box {
        border-left: 4px solid #8A2BE2;
        background: rgba(138, 43, 226, 0.08);
        padding: 1rem 1.2rem;
        border-radius: 0 12px 12px 0;
        font-style: italic;
        font-size: 1.1rem;
        color: #D2A8FF;
        margin: 1rem 0;
    }

    /* Buttons & Tweaks */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4) !important;
    }

    /* Hide default Streamlit footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Function to get Gemini API Key from Secrets, Env, or User Input
def get_api_key(user_key_input=""):
    if user_key_input and user_key_input.strip():
        return user_key_input.strip()
    
    # Try streamlit secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
        if "GOOGLE_API_KEY" in st.secrets:
            return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass
        
    # Try environment variables
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if env_key:
        return env_key
        
    return None

# Function to fetch GitHub Repo Metadata
def fetch_github_repo_info(url):
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, url)
    if not match:
        return None
    owner, repo = match.group(1), match.group(2).replace(".git", "")
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        res = requests.get(api_url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "name": data.get("full_name"),
                "description": data.get("description") or "No description provided",
                "language": data.get("language") or "Unknown",
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "topics": data.get("topics", [])
            }
    except Exception:
        pass
    return None

# Smart Heuristic Generator (Fallback when API key is not present or API fails)
def generate_heuristic_roast(input_type, content, repo_info, savage_mode):
    content_lower = content.lower()
    
    # Analyze keywords
    has_react = "react" in content_lower or "jsx" in content_lower or "tsx" in content_lower
    has_python = "python" in content_lower or "def " in content_lower or "print(" in content_lower or "import " in content_lower
    has_js = "javascript" in content_lower or "const " in content_lower or "let " in content_lower or "function" in content_lower
    has_crud = "crud" in content_lower or "create" in content_lower or "database" in content_lower or "sql" in content_lower
    has_ai = "ai" in content_lower or "openai" in content_lower or "prompt" in content_lower or "llm" in content_lower
    has_todo = "todo" in content_lower or "fixme" in content_lower
    has_eval = "eval(" in content_lower or "exec(" in content_lower
    has_any = "any" in content_lower
    
    # Assign Verdict
    if has_ai:
        verdict = "AI Prompt Engineer in Denial 🤖"
        score = random.randint(3, 5)
    elif has_crud and has_react:
        verdict = "Stuck in Tutorial Hell 💀"
        score = random.randint(3, 6)
    elif "linux" in content_lower or "kernel" in content_lower or "c++" in content_lower or "rust" in content_lower:
        verdict = "Future FAANG Dev 🔥"
        score = random.randint(7, 9)
    elif len(content.strip()) < 40:
        verdict = "Lazy Code Writer 💤"
        score = random.randint(2, 4)
    else:
        verdict = "Average Dev Energy 😐"
        score = random.randint(4, 6)
        
    top_dev_score = round(min(score + random.uniform(3.2, 4.8), 9.9), 1)

    # Future predictions
    predictions_savage = [
        "In 6 months you will likely have 19 half-finished React side projects on GitHub and still fail to explain async/await in an interview.",
        "In 6 months you will spend 3 weeks debating Tailwind vs CSS Modules before abandoning the app entirely.",
        "In 6 months you will re-write your entire codebase in Rust because Twitter told you JS is slow, only to get stuck on the borrow checker.",
        "In 6 months you will add 5 new AI wrappers to your resume and still search StackOverflow for 'how to center a div'.",
        "In 6 months you will apply for 200 Senior Engineer jobs while your local dev environment refuses to compile."
    ]
    predictions_normal = [
        "In 6 months you will master state management and build a production-ready application if you stick to finishing one project!",
        "In 6 months you will overcome tutorial hell and land your first solid freelance or junior developer role.",
        "In 6 months you willRefactor this code into modular components and write your first suite of unit tests.",
        "In 6 months you will move from basic app building into full-stack cloud deployment."
    ]
    
    future_prediction = random.choice(predictions_savage if savage_mode else predictions_normal)

    # Strengths
    strengths_pool = [
        "Has the courage to put code out into the world without dying of shame.",
        "Uses clean variable names instead of single-letter variables like `x` and `temp`.",
        "Shows clear enthusiasm for modern stack tools and framework ecosystems.",
        "Understands basic structure and problem-solving flow."
    ]
    strengths = random.sample(strengths_pool, 2)

    # Weaknesses
    weaknesses_pool = []
    if savage_mode:
        weaknesses_pool = [
            "Zero error handling in sight—one null value and your server goes straight to the shadow realm.",
            "You rely on `console.log` / `print` statements more than a toddler relies on nightlights.",
            "Architectural modularity is non-existent; it's a monolithic tower of spaghetti code.",
            "Looks like 80% of this was copy-pasted directly from ChatGPT without reading line 2."
        ]
    else:
        weaknesses_pool = [
            "Needs stronger error checking and input validation.",
            "Code modularity could be improved by splitting logic into separate utility functions.",
            "Missing automated tests or boundary condition validation.",
            "Inline documentation or docstrings could make this much easier to maintain."
        ]
    weaknesses = random.sample(weaknesses_pool, 2 if len(weaknesses_pool)>=2 else 1)

    # Savage vs Normal Roasts
    if savage_mode:
        roasts = [
            "You start projects like a high-budget Netflix series... but cancel them after Episode 1 💀",
            "This code runs on hope, caffeine, and 14 unclosed StackOverflow tabs. One API update and it crumbles 💀",
            "Your commit history looks like a Morse code signal for help: 'fix bug', 'fix again', 'asdfghjkl' 💀",
            "If code quality was a currency, your repo would be in severe hyperinflation right now 💀"
        ]
    else:
        roasts = [
            "Your code gets the job done, but it definitely looks like it survived a high-speed collision with deadlines 😅",
            "You have great momentum, though your folder structure is currently giving chaotic energy!",
            "It works! But future you will look back at this code in 3 months and wonder what past you was thinking."
        ]
    roast = random.choice(roasts)

    # Roadmaps
    roadmaps = [
        "1. Stop buying domain names for apps you haven't even initialized with `npm init`.",
        "2. Add try-catch blocks and actual logging before production crashes your career.",
        "3. Pick ONE project and push it to production on Vercel or Render before starting a new repo.",
        "4. Learn Git rebase so your commit log doesn't look like 'test 1', 'test 2', 'final final v2'."
    ]

    # Reality checks
    reality_checks = [
        "LeetCode is waiting for you bro 💀",
        "This won't survive a real senior code review, but it's a start!",
        "CSS center alignment is your true final boss.",
        "Your console.log count is currently higher than your unit test coverage.",
        "Remember: It's not a bug, it's an undocumented feature."
    ]
    reality_check = random.choice(reality_checks)

    return {
        "verdict": verdict,
        "score": score,
        "top_dev_score": top_dev_score,
        "future_prediction": future_prediction,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "roast": roast,
        "roadmap": roadmaps,
        "reality_check": reality_check,
        "comparison_details": {
            "code_quality": f"{score}/10 vs 9.8/10",
            "commit_consistency": f"{random.randint(2, 5)}/10 vs 9.5/10",
            "console_log_dependency": "10/10 vs 1/10 💀"
        }
    }

# Gemini API Generator Call
def generate_gemini_roast(api_key, input_type, content, repo_info, savage_mode):
    mode_str = "SAVAGE MODE (Brutally funny, witty, sarcastic, savage developer roast, zero filter)" if savage_mode else "NORMAL MODE (Fun, witty, constructive developer roast)"
    
    repo_context = ""
    if repo_info:
        repo_context = f"\nGitHub Repo Context:\nName: {repo_info['name']}\nLanguage: {repo_info['language']}\nStars: {repo_info['stars']}\nDescription: {repo_info['description']}\n"
    
    prompt = f"""
You are "Future Dev Roast", an expert, hilarious AI Tech Lead and Code Reviewer.
Analyze the following developer input and generate a viral, fun assessment in valid JSON format ONLY.

INPUT TYPE: {input_type}
MODE: {mode_str}
{repo_context}
INPUT CONTENT:
{content}

Respond ONLY with a valid JSON object matching this exact schema:
{{
  "verdict": "Verdict Title with single Emoji (e.g., 'Stuck in Tutorial Hell 💀' or 'Future FAANG Dev 🔥' or 'Average Dev Energy 😐')",
  "score": 4 (Integer between 1 and 10),
  "top_dev_score": 9.5 (Float between 9.0 and 9.9),
  "future_prediction": "Dramatic, realistic prediction starting with 'In 6 months you will likely...'",
  "strengths": ["Short strength bullet 1", "Short strength bullet 2"],
  "weaknesses": ["Sharp weakness bullet 1", "Sharp weakness bullet 2"],
  "roast": "Funny, savage, punchy roast paragraph tailored specifically to their input",
  "roadmap": ["Actionable step 1", "Actionable step 2", "Actionable step 3"],
  "reality_check": "Short witty quote line (e.g. 'LeetCode is waiting for you bro')",
  "comparison_details": {{
    "code_quality": "4/10 vs 9.8/10",
    "commit_consistency": "3/10 vs 9.5/10",
    "console_log_dependency": "9/10 vs 1/10"
  }}
}}

Make sure the JSON is 100% valid and free of markdown formatting outside of the json block.
"""

    # Strategy 1: Try official google-genai SDK
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        for model_name in ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if response and response.text:
                    text_cleaned = re.sub(r'```json\s*', '', response.text)
                    text_cleaned = re.sub(r'```\s*$', '', text_cleaned).strip()
                    return json.loads(text_cleaned)
            except Exception:
                continue
    except Exception:
        pass

    # Strategy 2: Try google-generativeai SDK
    try:
        import google.generativeai as genai_old
        genai_old.configure(api_key=api_key)
        for m in ['gemini-1.5-flash', 'gemini-2.0-flash']:
            try:
                model = genai_old.GenerativeModel(m)
                response = model.generate_content(prompt)
                if response and response.text:
                    text_cleaned = re.sub(r'```json\s*', '', response.text)
                    text_cleaned = re.sub(r'```\s*$', '', text_cleaned).strip()
                    return json.loads(text_cleaned)
            except Exception:
                continue
    except Exception:
        pass

    # Strategy 3: Direct REST endpoint calls
    try:
        for model_endpoint in ['gemini-1.5-flash', 'gemini-2.0-flash']:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_endpoint}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.8, "responseMimeType": "application/json"}
            }
            res = requests.post(url, headers=headers, json=payload, timeout=10)
            if res.status_code == 200:
                res_data = res.json()
                text_response = res_data['candidates'][0]['content']['parts'][0]['text']
                text_cleaned = re.sub(r'```json\s*', '', text_response)
                text_cleaned = re.sub(r'```\s*$', '', text_cleaned).strip()
                return json.loads(text_cleaned)
    except Exception:
        pass
        
    # If API calls fail or time out, fallback seamlessly to heuristic engine
    return generate_heuristic_roast(input_type, content, repo_info, savage_mode)

# --- SIDEBAR & OPTIONS ---
with st.sidebar:
    st.markdown("### ⚙️ Settings & Options")
    
    # Mode Switcher
    st.markdown("#### 🎭 Roast Intensity")
    savage_mode = st.toggle("😈 Savage Mode", value=True, help="Toggle between Normal mode and Savage mode for extra brutal roasts!")
    
    if savage_mode:
        st.error("🔥 **SAVAGE MODE ACTIVE**: Prepare for zero mercy!")
    else:
        st.info("😇 **NORMAL MODE ACTIVE**: Constructive feedback with a light roast.")
        
    st.markdown("---")
    st.markdown("#### 🔑 Gemini API Key (Optional)")
    user_api_key = st.text_input("Paste API Key", type="password", placeholder="AQ.Ab... or AIZA...", help="Supports all Gemini / Google AI key formats. If left blank, smart fallback engine is used.")
    
    final_api_key = get_api_key(user_api_key)
    if final_api_key:
        st.success("⚡ Live Gemini AI Connected!")
    else:
        st.warning("💡 Smart Fallback Engine Ready (Works 100% without API key). Add key in `.streamlit/secrets.toml` for live Gemini API.")

    st.markdown("---")
    st.markdown("#### 💡 Quick Examples")
    if st.button("Example 1: React CRUD App"):
        st.session_state["preset_input"] = "Built a basic CRUD app in React with Express backend and MongoDB. Uses console.log for debugging everywhere and has 15 TODO comments."
        st.session_state["preset_type"] = "📝 Project Description"
    if st.button("Example 2: Python Script"):
        st.session_state["preset_input"] = "def process_data(data):\n    # TODO: fix this later\n    for i in range(len(data)):\n        for j in range(len(data)):\n            if data[i] == data[j]:\n                print('Found match:', data[i])\n    return True"
        st.session_state["preset_type"] = "💻 Code Snippet"
    if st.button("Example 3: GitHub Repo"):
        st.session_state["preset_input"] = "https://github.com/facebook/react"
        st.session_state["preset_type"] = "🔗 GitHub Repo URL"


# --- MAIN HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🔥 Future Dev Roast</div>
    <div class="hero-tagline">“Paste your code. See your future. Get roasted.”</div>
    <div class="hero-sub">The viral AI code reviewer that tells you what your future in tech actually looks like. 💀</div>
</div>
""", unsafe_allow_html=True)

# Preset Sync
input_type_default = st.session_state.get("preset_type", "💻 Code Snippet")
preset_content = st.session_state.get("preset_input", "")

# Input Navigation Tabs
input_tab = st.radio(
    "Select Input Method:",
    ["💻 Code Snippet", "🔗 GitHub Repo URL", "📝 Project Description"],
    index=["💻 Code Snippet", "🔗 GitHub Repo URL", "📝 Project Description"].index(input_type_default) if input_type_default in ["💻 Code Snippet", "🔗 GitHub Repo URL", "📝 Project Description"] else 0,
    horizontal=True
)

user_content = ""
repo_info = None

if input_tab == "💻 Code Snippet":
    user_content = st.text_area(
        "Paste your code snippet here:",
        value=preset_content if input_type_default == "💻 Code Snippet" else "",
        height=180,
        placeholder="// Paste your React, Python, C++, or JS code here...\nfunction calculateTotal(items) {\n  return items.reduce((a, b) => a + b, 0);\n}"
    )
elif input_tab == "🔗 GitHub Repo URL":
    user_content = st.text_input(
        "Paste public GitHub Repository URL:",
        value=preset_content if input_type_default == "🔗 GitHub Repo URL" else "",
        placeholder="https://github.com/username/repository-name"
    )
    if user_content and "github.com" in user_content:
        with st.spinner("Fetching repository info from GitHub..."):
            repo_info = fetch_github_repo_info(user_content)
            if repo_info:
                st.success(f"📦 Found Repo: **{repo_info['name']}** ({repo_info['language']}) | ⭐ {repo_info['stars']} Stars")
            else:
                st.info("ℹ️ Repo URL noted. We'll roast the URL pattern!")
else:
    user_content = st.text_area(
        "Describe your project or tech stack:",
        value=preset_content if input_type_default == "📝 Project Description" else "",
        height=150,
        placeholder="e.g. Built a basic CRUD app in React with Firebase auth and TailwindCSS..."
    )

# Analyze Button
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_clicked = st.button("🚀 Analyze My Future", use_container_width=True, type="primary")

if analyze_clicked:
    if not user_content.strip():
        st.error("⚠️ Please paste some code, a repo URL, or project description first!")
    else:
        with st.spinner("🔥 Analyzing code metrics, calculating developer fate, compiling roast..."):
            if final_api_key:
                result = generate_gemini_roast(final_api_key, input_tab, user_content, repo_info, savage_mode)
            else:
                result = generate_heuristic_roast(input_tab, user_content, repo_info, savage_mode)
            
            st.session_state["last_result"] = result

# --- DISPLAY RESULTS EXPERIENCE ---
if "last_result" in st.session_state:
    res = st.session_state["last_result"]
    
    st.markdown("---")
    
    # 💀 VERDICT
    st.markdown(f"""
    <div class="verdict-badge">
        💀 VERDICT: {res.get('verdict', 'Developer in Progress 😐')}
    </div>
    """, unsafe_allow_html=True)
    
    # 📊 SKILL SCORE
    score = int(res.get('score', 5))
    fill_pct = score * 10
    
    st.markdown(f"""
    <div class="roast-card">
        <div class="card-title">📊 Skill Score: {score}/10</div>
        <div class="score-container">
            <div class="score-bar-bg">
                <div class="score-bar-fill" style="width: {fill_pct}%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🚀 FUTURE PREDICTION
    st.markdown(f"""
    <div class="roast-card">
        <div class="card-title">🚀 Future Prediction</div>
        <p style="font-size: 1.15rem; color: #E0E0E0; margin-bottom: 0;">
            “{res.get('future_prediction', 'In 6 months you will be deploying code to production!')}”
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 😈 THE ROAST & REALITY CHECK
    st.markdown(f"""
    <div class="roast-card" style="border-left: 4px solid #FF4B4B;">
        <div class="card-title" style="color: #FF4B4B;">😈 The Savage Roast</div>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #FAFAFA;">
            {res.get('roast', 'You start projects with immense hype... but abandon them when the first error appears.')}
        </p>
        <div class="quote-box">
            💬 Dev Reality Check: “{res.get('reality_check', 'LeetCode is waiting for you bro')}'”
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🧠 STRENGTHS & ⚠️ WEAKNESSES
    col_str, col_weak = st.columns(2)
    with col_str:
        strengths_list = "".join([f"<li>{s}</li>" for s in res.get('strengths', ['Clean syntax'])])
        st.markdown(f"""
        <div class="roast-card">
            <div class="card-title" style="color: #3FB950;">🧠 Strengths</div>
            <ul style="padding-left: 1.2rem; color: #C9D1D9;">
                {strengths_list}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_weak:
        weaknesses_list = "".join([f"<li>{w}</li>" for w in res.get('weaknesses', ['Needs error handling'])])
        st.markdown(f"""
        <div class="roast-card">
            <div class="card-title" style="color: #F85149;">⚠️ Weaknesses</div>
            <ul style="padding-left: 1.2rem; color: #C9D1D9;">
                {weaknesses_list}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 🔥 COMPARE WITH TOP 1% DEV
    top_score = res.get('top_dev_score', 9.5)
    comp = res.get('comparison_details', {})
    
    st.markdown(f"""
    <div class="roast-card">
        <div class="card-title">🔥 You vs Top 1% Dev Gap</div>
        <div class="compare-box">
            <div class="compare-card">
                <div style="color: #8B949E; font-size: 0.9rem;">YOUR SKILL SCORE</div>
                <div class="compare-score you-score">{score}/10</div>
            </div>
            <div class="compare-card">
                <div style="color: #8B949E; font-size: 0.9rem;">TOP 1% DEV SCORE</div>
                <div class="compare-score top-score">{top_score}/10</div>
            </div>
        </div>
        <div style="margin-top: 1rem; background: #0D1117; padding: 0.8rem; border-radius: 10px; font-size: 0.95rem;">
            ⚡ <b>Code Quality Gap:</b> {comp.get('code_quality', f'{score}/10 vs 9.8/10')}<br>
            📅 <b>Commit Consistency:</b> {comp.get('commit_consistency', '4/10 vs 9.5/10')}<br>
            🚨 <b>Console.log Dependency:</b> {comp.get('console_log_dependency', '10/10 vs 1/10')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 💡 IMPROVEMENT ROADMAP
    roadmap_items = res.get('roadmap', ['Write clean code', 'Deploy to production'])
    roadmap_html = "".join([f"<p style='margin-bottom: 0.5rem;'><b>Step {i+1}:</b> {item}</p>" for i, item in enumerate(roadmap_items)])
    
    st.markdown(f"""
    <div class="roast-card">
        <div class="card-title" style="color: #00F5FF;">💡 Improvement Roadmap</div>
        <div style="color: #E0E0E0; font-size: 1rem;">
            {roadmap_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- VIRAL SHARE & COPY FEATURES ---
    st.markdown("### 🚀 Share & Flex")
    
    tweet_text = f"I just got roasted by Future Dev Roast 💀\n\nVerdict: {res.get('verdict')}\nSkill Score: {score}/10\nPrediction: {res.get('future_prediction')}\n\nTry it here:"
    encoded_tweet = urllib.parse.quote(tweet_text)
    twitter_url = f"https://twitter.com/intent/tweet?text={encoded_tweet}"
    
    copy_text_summary = f"""🔥 FUTURE DEV ROAST RESULT 🔥
💀 VERDICT: {res.get('verdict')}
📊 Skill Score: {score}/10 (vs Top 1% Dev: {top_score}/10)
🚀 Future Prediction: {res.get('future_prediction')}
😈 Roast: {res.get('roast')}
💬 Dev Reality Check: {res.get('reality_check')}
"""

    col_share1, col_share2 = st.columns(2)
    with col_share1:
        st.markdown(f"""
        <a href="{twitter_url}" target="_blank" style="text-decoration: none;">
            <button style="
                width: 100%;
                background-color: #1DA1F2;
                color: white;
                border: none;
                padding: 0.7rem;
                border-radius: 12px;
                font-weight: 700;
                font-size: 1rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
            ">
                🐦 Share on Twitter / X
            </button>
        </a>
        """, unsafe_allow_html=True)
        
    with col_share2:
        if st.button("📋 Copy Full Result Summary", use_container_width=True):
            st.code(copy_text_summary, language="text")
            st.success("✅ Summary formatted above! Copy to clipboard for WhatsApp/LinkedIn!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8B949E; font-size: 0.85rem; margin-top: 1rem;">
    Future Dev Roast • Built for developers with ❤️ & 💀 • Powered by Streamlit & Gemini AI
</div>
""", unsafe_allow_html=True)
