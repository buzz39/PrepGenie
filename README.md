# PrepGenie — AI-Powered Interview Prep Coach

> A Windows desktop app that helps you **prepare for interviews** by turning practice questions into structured study material. Load a question from an image or screenshot, and let **Azure Computer Vision** + **OpenAI GPT-4** walk you through a model answer — so you can study, reflect, and build real confidence before the big day.

[![CI](https://github.com/buzz39/PrepGenie/actions/workflows/python-app.yml/badge.svg)](https://github.com/buzz39/PrepGenie/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](#requirements)

---

## 🎯 Who Is This For?

PrepGenie is built for **job seekers who want to practice smarter**:

- **Self-study sessions** — Import questions from job postings, prep books, or practice sites and study model answers at your own pace.
- **Mock-interview practice** — Run through questions solo and compare your answer against a structured AI-generated response to identify gaps.
- **Learning interview frameworks** — See how the STAR method applies to real behavioural questions, or how to structure a technical explanation clearly.
- **Career changers & new grads** — Build familiarity with unfamiliar question types before stepping into the room.

> ⚠️ **Ethical Use**: PrepGenie is designed as an **offline study and preparation aid** — not for use during live interviews. Using AI assistance in an actual interview without disclosure is deceptive and undermines your own growth. Please use this tool responsibly.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖼️ **Screenshot Capture** | Capture any practice question on screen with `Ctrl+Shift+S` for instant analysis |
| 🔍 **Azure OCR** | Extracts text from images using Azure Computer Vision |
| 🤖 **GPT-4 Coaching** | Classifies questions (technical vs. behavioural) and generates a model answer to study |
| 🗂️ **Response Modes** | Toggle between *Full Response* (structured, with examples) and *Answer Only* (concise key points) |
| 🪟 **Floating Study Panel** | Transparent, always-on-top panel lets you read the model answer while composing your own |
| 🔔 **System Tray** | Minimizes to tray; accessible at all times without cluttering the taskbar |
| 📊 **Timing Metrics** | Displays OCR and GPT-4 latency so you can benchmark your pipeline |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PrepGenie Desktop App                      │
│                                                                 │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │  Practice    │───▶│  Azure Computer  │───▶│   OpenAI     │  │
│  │  Question    │    │  Vision (OCR)    │    │   GPT-4      │  │
│  │  Image       │    │  REST API v3.2   │    │   Coach      │  │
│  └──────────────┘    └──────────────────┘    └──────┬───────┘  │
│                                                      │          │
│                                              ┌───────▼───────┐  │
│                                              │ Floating       │  │
│                                              │ Study Panel    │  │
│                                              └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Tech stack:** Python · CustomTkinter · Azure Cognitive Services · OpenAI Python SDK · PyAutoGUI · pystray

---

## 📋 Table of Contents
- [Installation](#-installation)
- [Usage](#-usage)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Requirements](#-requirements)
- [Development](#-development)
- [Contributing](#-contributing)
- [Known Limitations](#-known-limitations)
- [License](#-license)
- [Changelog](#-changelog)

---

## 🚀 Installation

### End-user (Windows executable)

1. Install the Visual C++ Redistributable:
   ```
   install_vcredist.bat
   ```

2. Create a `.env` file in the same directory as `PrepGenie.exe` (copy from [`.env.example`](.env.example)):
   ```env
   AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   AZURE_VISION_KEY=your_azure_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   > ⚠️ **Security Note**: Never commit your `.env` file or share your API keys. The `.env` file is already listed in `.gitignore`.

3. Launch `PrepGenie.exe` from the `dist` folder.

---

## 🖱️ Usage

1. **Select Image** — Click "Select Image" to load an image of a practice question.
2. **Take Screenshot** — Press `Ctrl+Shift+S` or click "Take Screenshot" to capture any question on your screen.
3. **Analyse** — Click "Analyse Question" to extract the text and generate a model answer.
4. **Study the Response** — Use the floating study panel to read the structured model answer and compare it against your own thinking.
5. **Response Format** — Use the dropdown to switch between *Full Response* (full structured breakdown) and *Answer Only* (concise key points).
6. **Close Panel** — Click "Close All Windows" or right-click the floating panel to dismiss it.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+Shift+S` | Capture a screen region |
| Right-click result window | Close the floating window |
| Click and drag result window | Reposition the overlay |

---

## 💻 Requirements

- Windows 10/11 (64-bit)
- Visual C++ Redistributable 2015–2022
- Active internet connection (for Azure + OpenAI API calls)
- Minimum 4 GB RAM
- ~100 MB free disk space

---

## 🛠️ Development

### Setting Up

```bash
git clone https://github.com/buzz39/PrepGenie.git
cd PrepGenie

python -m venv venv
.\venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your API keys (see [Installation](#-installation)).

### Building the Executable

```bash
.\build.bat
```

The executable will be created in the `dist/` folder.

### Running Tests

```bash
python -m pytest tests/ -v
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on pull requests, bug reports, and feature suggestions.

---

## ⚠️ Known Limitations

- Maximum image size: 4 MB
- Supported formats: PNG, JPG, JPEG, BMP
- Text must be clearly visible and correctly oriented
- Internet connection required for API calls
- Windows only (GUI relies on Win32 APIs via tkinter)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a full history of releases.