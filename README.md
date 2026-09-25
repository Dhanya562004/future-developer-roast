# 🔥 Future Dev Roast

> **“Paste your code. See your future. Get roasted.”**

Future Dev Roast is a viral, fun, slightly savage AI web app designed to evaluate developers' code snippets, GitHub repositories, or project descriptions. It predicts their career future with a mix of realistic tech insights, savage humor, skill scores, improvement roadmaps, and instant viral share links for Twitter/X and LinkedIn!

---

## ✨ Features

- **💀 Verdict & Skill Meter**: Instant classification (e.g. *Future FAANG Dev 🔥*, *Stuck in Tutorial Hell 💀*, *AI Prompt Engineer in Denial 🤖*) with visual 1–10 skill bar.
- **🚀 Future Prediction**: Realistic, dramatic 6-month developer career forecasts.
- **😈 Dual Modes**: 
  - 😇 **Normal Mode**: Lighthearted roast with constructive feedback.
  - 😈 **Savage Mode**: Brutally honest, hilarious code review without mercy.
- **🧠 Strengths & ⚠️ Weaknesses**: 2–3 sharp bullet points analyzing your code quality.
- **🔥 You vs Top 1% Dev Gap**: Side-by-side metric comparison (Code quality, commit consistency, console.log dependency).
- **💡 Improvement Roadmap**: Step-by-step actionable advice to elevate your code skills.
- **🐦 Viral Social Features**: 1-click **Share on Twitter / X** button and **Copy Summary** for instant sharing on Discord, LinkedIn, or WhatsApp.
- **⚡ Built-in Smart Fallback**: Works 100% reliably out of the box even without an API key using the built-in heuristic analysis engine, or powers up with live Gemini AI when an API key is provided!

---

## 🛠️ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Dhanya562004/future-developer-roast.git
cd future-developer-roast
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Gemini API Key (Optional)
You can provide your Google Gemini API Key in `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

*Note: If no API key is set, the app seamlessly runs on its smart fallback heuristic engine so it never crashes!*

### 4. Run the Streamlit app
```bash
streamlit run app.py
```

---

## 🎨 Tech Stack

- **Frontend / Framework**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Google Gemini API](https://ai.google.dev/) (with Smart Heuristic Engine fallback)
- **Styling**: Custom CSS (Glassmorphism Dark Cyber Theme)
- **API Integration**: GitHub REST API for public repository fetching

---

## 📄 License

MIT License © 2026 Future Dev Roast
