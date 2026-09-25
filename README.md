# 💀 Future Dev Roast

<div align="center">

[![Live Demo](https://img.shields.io/badge/🚀_Live_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://future-developer-roast-pyzkegee6mj5pycl95xvsd.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini AI](https://img.shields.io/badge/Powered_by-Gemini_AI-8E44AD?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

### **“Paste your code. See your future. Get roasted.”**

A viral, savage, and surprisingly accurate AI code reviewer built to analyze developer code, predict career futures, and give zero-mercy feedback.

[👉 **TRY THE LIVE APP HERE** 👈](https://future-developer-roast-pyzkegee6mj5pycl95xvsd.streamlit.app/)

</div>

---

## 🚀 Project Overview

**Future Dev Roast** is an interactive AI application that acts like a senior tech lead having a bad day. 

Paste a GitHub repository link, a code snippet, or a project description—the app evaluates your developer energy, assigns a **1–10 Skill Score**, forecasts where your career will be in 3–6 months, and hits you with a hilarious roast paired with a real improvement roadmap.

> *"It’s part code review, part fortune-teller, and 100% savage."*

---

## 🔥 Live Demo

Click the badge below or link to test your code right now:

👉 **[Launch Future Dev Roast App](https://future-developer-roast-pyzkegee6mj5pycl95xvsd.streamlit.app/)** 👈

---

## 💡 Features

- 💻 **Flexible Inputs**: Roast via GitHub Repo URL, raw code snippets, or project descriptions.
- 💀 **Dynamic Verdicts**: Get categorized into verdicts like *Future FAANG Dev 🔥*, *Stuck in Tutorial Hell 💀*, or *AI Prompt Engineer in Denial 🤖*.
- 📊 **Skill Score & Progress Bar**: Visual 1–10 developer skill rating.
- 🚀 **Future Career Prediction**: Realistic + dramatic 3–6 month forecasts.
- 🧠 **Strengths & ⚠️ Weaknesses**: Sharp 2–3 bullet points pinpointing clean code vs bad habits.
- 😈 **Dual Roast Modes**:
  - 😇 **Normal Mode**: Lighthearted, constructive feedback with a gentle roast.
  - 😈 **Savage Mode**: Brutal, unfiltered, hilarious roast with zero filter.
- 💡 **Improvement Roadmap**: Clear, actionable next steps to level up your career.
- 🔥 **“You vs Top 1% Dev” Gap**: Side-by-side metric comparison (Code Quality, Commit Consistency, Console.log Dependency).
- 🐦 **1-Click Viral Sharing**: Tweet your roast result directly to X/Twitter or copy formatted summary text for Discord, LinkedIn, or WhatsApp.

---

## 🧠 How It Works

1. **LLM Powered Analysis**: Connects to **Google Gemini AI** (or OpenAI compatible endpoints) to evaluate code patterns, error handling, modularity, and framework choices.
2. **Zero-Downtime Fallback Engine**: If no API key is provided or API limits are reached, a custom **Smart Heuristic Engine** takes over seamlessly, analyzing code smells and keyword density so the app **NEVER crashes**.
3. **Structured JSON Output**: All outputs are parsed into clean structured cards for optimal rendering and high visual aesthetic.
4. **Viral Product Focus**: Designed with modern dark glassmorphism UI tokens, micro-animations, and instant share buttons.

---

## ⚙️ Tech Stack

- **Frontend & Framework**: [Streamlit](https://streamlit.io/)
- **Programming Language**: Python 3.13+
- **AI Model**: Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`)
- **API Integrations**: GitHub REST API (Public repository metadata fetching)
- **UI & Aesthetics**: Custom CSS3 (Glassmorphism Dark Vibe)

---

## 🖥️ Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Dhanya562004/future-developer-roast.git
cd future-developer-roast
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit application
```bash
streamlit run app.py
```

---

## 🔐 API Key (Optional)

The app works **100% out of the box** using the built-in smart fallback engine!

If you want live Gemini AI capabilities, simply create a file at `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

*(You can also paste your API key directly in the app's sidebar UI!)*

---

## 🎯 Why This Project?

Most developer tools are dry and academic. **Future Dev Roast** was created to bring internet culture, humor, and engagement into code reviews. It transforms code evaluation into something fun that developers actively share with friends, teammates, and recruiters.

---

## 📸 Screenshots

### 🏠 Home Screen
*(Placeholder: Upload screenshot of input section & mode toggles)*
`![Home Screen Placeholder](https://raw.githubusercontent.com/Dhanya562004/future-developer-roast/main/docs/home_preview.png)`

### 📊 Output & Roast Experience
*(Placeholder: Upload screenshot of verdict, skill bar, savage roast & top 1% comparison)*
`![Output Preview Placeholder](https://raw.githubusercontent.com/Dhanya562004/future-developer-roast/main/docs/output_preview.png)`

---

## ⭐ Support & Star

If this tool made you laugh (or hurt your feelings slightly), drop a **Star ⭐** on the repo!

> **“Built for developers who want brutal honesty 💀”**

[👉 **Try Future Dev Roast Live**](https://future-developer-roast-pyzkegee6mj5pycl95xvsd.streamlit.app/)
