# PrepGenie — AI-Powered Interview Assistant

> A Windows desktop app that captures interview questions via screenshot or image upload, uses **Azure Computer Vision** for OCR, and leverages **OpenAI GPT-4** to generate structured, context-aware answers in real time.

[![CI](https://github.com/buzz39/PrepGenie/actions/workflows/python-app.yml/badge.svg)](https://github.com/buzz39/PrepGenie/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](#requirements)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖼️ **Screenshot Capture** | Select any region of your screen with `Ctrl+Shift+S` |
| 🔍 **Azure OCR** | Extracts text from images using Azure Computer Vision |
| 🤖 **GPT-4 Analysis** | Classifies questions (technical vs. behavioural) and generates tailored answers |
| 🗂️ **Response Modes** | Toggle between *Full Response* (structured, with examples) and *Answer Only* (concise) |
| 🪟 **Floating Result Window** | Transparent, always-on-top answer overlay — no need to switch windows |
| 🔔 **System Tray** | Minimizes to tray; accessible at all times without cluttering the taskbar |
| 📊 **Timing Metrics** | Displays OCR and GPT-4 latency so you can benchmark your pipeline |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PrepGenie Desktop App                    │
│                                                                 │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │  Screenshot  │───▶│  Azure Computer  │───▶│   OpenAI     │  │
│  │  / Image     │    │  Vision (OCR)    │    │   GPT-4      │  │
│  │  Capture     │    │  REST API v3.2   │    │   API        │  │
│  └──────────────┘    └──────────────────┘    └──────┬───────┘  │
│                                                      │          │
│                                              ┌───────▼───────┐  │
│                                              │ Floating       │  │
│                                              │ Result Window  │  │
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

1. **Select Image** — Click "Select Image" to load an image file containing text.
2. **Take Screenshot** — Press `Ctrl+Shift+S` or click "Take Screenshot" to capture a screen region.
3. **Process Image** — Click "Process Image" to run OCR and generate a GPT-4 answer.
4. **Response Format** — Use the dropdown to switch between *Full Response* and *Answer Only*.
5. **Close Overlay** — Click "Close All Windows" or right-click the floating result window to dismiss it.

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