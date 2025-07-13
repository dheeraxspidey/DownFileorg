
<p align="center">
  <img width="400"  src="https://github.com/user-attachments/assets/fe41a50a-5853-43d5-ab9e-3693d2ef9a36" alt="Remove background project (2)" />
</p>


# ⚡ DownFileOrg Pro - AI File Organizer -

## 🛠️ Installation & Setup

### Option 1: Pre-built Executable (Recommended)

#### 📥 Download Links
- **Windows**: [Download DownFileOrg.exe](https://github.com/dheeraxspidey/DownFileorg/raw/main/dist/DownFileOrg.exe)
- **Linux**: `Coming Soon...` 🚧
- **macOS**: `Coming Soon...` 🚧

*No Python installation required! Just download and run.*

### Option 2: Run from Source

A modern, AI-powered file organization tool with real-time monitoring and automatic file classification using Random Forest machine learning. Features a premium dark theme GUI and cross-platform executable support.

## 🚀 Features

- **🤖 AI-Powered Classification**: Random Forest ML model with intelligent file categorization
- **👁️ Real-Time Monitoring**: Automatically organizes new files as they appear
- **🎨 Modern UI**: Premium dark theme with large, readable fonts
- **⚡ Cross-Platform**: Build executables for Windows, Linux, and macOS
- **📁 Smart Categories**: Education, Movies, Games, Apps, Entertainment, Career, Finance, Others
- **🔄 Watchdog Integration**: Monitor folders for instant file organization
- **💾 Self-Contained**: Embedded ML model and resources in executable

## 📊 Model Performance

- **Accuracy**: High precision Random Forest classification  
- **Speed**: <100ms per file prediction
- **Categories**: 8 smart categories for comprehensive organization
- **Features**: 25 engineered features for accurate classification

## � Screenshots

### Main Application Interface
![DownFileOrg Main Interface](screenshots/Screenshot%202025-07-13%20204718.png)


### File Organization in Action
![File Organization Process](screenshots/Screenshot%202025-07-13%20204600.png)


*Experience the modern dark theme interface with intuitive controls for file organization and real-time monitoring.*

## �🛠️ Installation & Setup

### Option 1: Pre-built Executable (Recommended)
Download the latest release for your platform:
- **Windows**: `DownFileOrg.exe`
- **Linux**: `DownFileOrg` 
- **macOS**: `DownFileOrg.app`

### Option 2: Run from Source
1. **Clone the repository**:
   ```bash
   git clone https://github.com/dheeraxspidey/DownFileorg.git
   cd DownFileorg
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python file_classifier_gui_watchdog.py
   ```

## 📁 Project Structure

```
DownFileorg/
├── file_classifier_gui_watchdog.py    # Main application with modern UI
├── random_forest_classifier.py        # Core ML classifier  
├── rf_file_classifier.joblib          # Pre-trained model
├── logo.ico                           # Application icon
├── requirements.txt                   # Python dependencies
├── file_organizer_watchdog.spec      # Windows build config
├── file_organizer_linux.spec         # Linux build config  
├── file_organizer_macos.spec         # macOS build config
├── build_cross_platform.py           # Cross-platform build script
├── BUILD_GUIDE.md                    # Detailed build instructions
├── CROSS_PLATFORM_GUIDE.md          # Platform-specific guidance
└── README.md                         # This file
```

## 🎯 Quick Start

### GUI Application
```bash
python file_classifier_gui_watchdog.py
```

**Main Features:**
- **📂 Folder Selection**: Browse and select any folder to organize
- **🚀 Instant Organization**: Click "Organize Now" to sort all existing files
- **👁️ Real-Time Monitoring**: Enable "Start Watching" for automatic organization of new files
- **🎨 Premium Interface**: Modern dark theme with large, readable fonts
- **📊 Live Statistics**: See file counts and AI status in real-time

### Building Executables

**For Current Platform:**
```bash
python build_cross_platform.py
```

**Platform-Specific Builds:**
```bash
# Windows
pyinstaller file_organizer_watchdog.spec --clean

# Linux (run on Linux machine)
pyinstaller file_organizer_linux.spec --clean

# macOS (run on macOS machine)  
pyinstaller file_organizer_macos.spec --clean
```

See `BUILD_GUIDE.md` and `CROSS_PLATFORM_GUIDE.md` for detailed instructions.

## 🤖 Python API Usage

```python
from random_forest_classifier import RandomForestFileClassifier

# Initialize classifier
classifier = RandomForestFileClassifier()
classifier.load_model('rf_file_classifier.joblib')

# Classify a file
result = classifier.predict("/path/to/document.pdf")
print(f"Category: {result['folder_name']}")
print(f"Confidence: {result['confidence']:.2f}")
```

## 📋 Core Components

1. **`file_classifier_gui_watchdog.py`**
   - Modern GUI with premium dark theme and real-time monitoring
   - Real-time file system watching with automatic organization
   - Professional interface with large, readable fonts
   - Embedded icon and resource handling for executables

2. **`random_forest_classifier.py`**
   - Random Forest ML classifier with feature extraction
   - Pre-trained model with 8 smart categories  
   - Fast prediction (<100ms per file)

3. **`rf_file_classifier.joblib`**
   - Pre-trained Random Forest model
   - Embedded in executables for self-contained distribution
   - Compact size (~10MB)

4. **Cross-Platform Build System**
   - Windows: Creates `DownFileOrg.exe`
   - Linux: Creates `DownFileOrg` binary
   - macOS: Creates `DownFileOrg.app` bundle
   - Automated build scripts and CI/CD support

## 🎯 Categories & Examples

| Category | Extensions | Keywords | Size |
|----------|------------|----------|------|
| **Education** | `.pdf`, `.docx`, `.pptx`, `.txt` | assignment, notes, class, syllabus, exam | Small-Medium |
| **Movies** | `.mp4`, `.mkv`, `.avi`, `.mov` | movie, film, trailer, hd, bluray | Large-Huge |
| **Games** | `.zip`, `.exe`, `.iso`, `.apk` | game, gta, nfs, setup, steam | Large-Huge |
| **Apps** | `.exe`, `.apk`, `.dmg` | setup, installer, app, software | Medium-Large |
| **Entertainment** | `.mp3`, `.wav`, `.mp4`, `.webm` | music, song, comedy, dance, funny | Medium-Large |
| **Career** | `.pdf`, `.docx` | resume, cv, job, interview, offer | Small |
| **Finance** | `.pdf`, `.xlsx` | invoice, bank, bill, salary, tax | Small-Medium |
| **Others** | Various system files | temp, cache, config, system, log | Tiny-Medium |

## � Technical Details

- **Language**: Python 3.8+
- **GUI Framework**: tkinter with modern styling
- **ML Library**: scikit-learn Random Forest
- **Dependencies**: watchdog, pandas, numpy, joblib
- **Build Tool**: PyInstaller for cross-platform executables
- **Architecture**: Self-contained executables with embedded resources

## 🚀 Distribution

- **Windows**: Single `.exe` file (no Python required)
- **Linux**: Native binary with GUI support
- **macOS**: `.app` bundle for easy installation
- **Self-contained**: All dependencies and models embedded

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Open source - feel free to use and modify for your needs!

---

**⚡ Made with AI for smarter file organization**
