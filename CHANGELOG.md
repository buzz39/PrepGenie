# Changelog

All notable changes to PrepGenie will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed
- Rebranded application positioning: PrepGenie is now framed as an **interview preparation and practice coach** rather than a live interview assistant, with clear ethical-use guidance
- Updated README: new tagline, added "Who Is This For?" section with positive use cases, added Ethical Use notice, refreshed feature descriptions and usage guide
- Updated UI title from "AI Interview Assistant" to "Interview Prep Coach" with a new subtitle clarifying the study-first purpose
- Renamed "Process Image" button to "Analyse Question" and updated placeholder text to reflect a preparation context
- Updated GPT-4 system prompts to position responses as model answers for study and learning rather than real-time answer generation
- Rebranded application from "OCR Assistant" to **PrepGenie** across the UI, system tray, and build spec (previous release)
- Replaced hardcoded developer path in `ocr_app.spec` with a dynamic `importlib.util.find_spec` lookup
- Upgraded GitHub Actions to `actions/checkout@v4` and `actions/setup-python@v5`
- CI now runs the full test suite (`pytest tests/`) instead of only `tests/test_basic.py`
- Improved `README.md`: architecture diagram, feature table, tech-stack overview, and fixed placeholder clone URL
- Improved `.env.example` with resource creation links and clearer comments

---

## [1.0.0] — 2024-03-08

### Added
- Initial public release
- Image OCR using Azure Computer Vision REST API v3.2
- GPT-4 integration with automatic question classification (technical vs. behavioural)
- *Full Response* and *Answer Only* response modes
- Screenshot capture with interactive region-selection overlay (`Ctrl+Shift+S`)
- Floating transparent result window (always-on-top, draggable, right-click to close)
- System tray support (minimise to tray, show/hide/exit)
- Timing metrics for OCR and GPT-4 latency
- Support for PNG, JPG, JPEG, and BMP input formats
- Structured logging to both console and `ocr_app.log`
- Unit tests for `AzureOCRService` and `OpenAIService`
- GitHub Actions CI pipeline
