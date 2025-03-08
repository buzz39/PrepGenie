# OCR Assistant

A desktop application for Optical Character Recognition (OCR) with GPT-4 integration for analyzing interview questions.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- Image OCR using Azure Computer Vision
- GPT-4 integration for analyzing interview questions
- Screenshot capture with selection overlay
- Floating transparent results window
- Modern and clean user interface
- Support for multiple image formats
- Progress tracking and timing information

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Requirements](#requirements)
- [Development](#development)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)
- [Changelog](#changelog)

## Installation

1. First, install the Visual C++ Redistributable by running:
   ```
   install_vcredist.bat
   ```

2. Create a `.env` file in the same directory as the application with your API keys (copy from `.env.example`):
   ```
   AZURE_VISION_ENDPOINT=your_vision_endpoint_here
   AZURE_VISION_KEY=your_vision_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   ⚠️ **Security Note**: Never commit your `.env` file or share your API keys. The `.env` file is already in `.gitignore` to prevent accidental commits.

3. Run the application by double-clicking `OCR Assistant.exe` in the `dist` folder.

## Usage

1. **Select Image**: Click "Select Image" to choose an image file containing text to analyze.

2. **Take Screenshot**: Press `Ctrl+Shift+S` or click "Take Screenshot" to capture a portion of your screen.

3. **Process Image**: Click "Process Image" to perform OCR and get GPT-4 analysis.

4. **Response Format**: Choose between "Full Response" or "Answer Only" from the dropdown menu.

5. **Close Windows**: Click "Close All Windows" to close any floating result windows.

## Keyboard Shortcuts

- `Ctrl+Shift+S`: Take a screenshot
- Right-click on result window: Close the window
- Click and drag result window: Move the window

## Requirements

- Windows 10/11 64-bit
- Visual C++ Redistributable 2015-2022
- Internet connection for API access
- Minimum 4GB RAM recommended
- 100MB free disk space

## Development

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PrepGenie.git
   cd PrepGenie
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables (see Installation section)

### Building from Source

1. Run the build script:
   ```bash
   .\build.bat
   ```
   This will create an executable in the `dist` folder.

### Running Tests

```bash
python -m pytest tests/
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Support

If you encounter any issues:
1. Make sure you have installed the Visual C++ Redistributable
2. Verify your API keys in the `.env` file
3. Check your internet connection
4. Ensure you have sufficient permissions to run the application

For additional support:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the FAQ in our wiki

## Known Limitations

- Maximum image size: 4MB
- Supported image formats: PNG, JPG, JPEG, BMP
- Text must be clearly visible and properly oriented
- Internet connection required for API calls

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0 (2024-03-08)
- Initial public release
- Basic OCR functionality
- GPT-4 integration
- Screenshot capability
- Floating window interface 