# Cross-Platform Build Guide for DownFileOrg

This guide explains how to build DownFileOrg executables for Windows, Linux, and macOS.

## 🔧 Prerequisites

### All Platforms
1. **Python 3.8+** installed
2. **Required Python packages** (install via `pip install -r requirements.txt`):
   - pyinstaller
   - tkinter (usually included with Python)
   - watchdog
   - scikit-learn
   - pandas
   - numpy
   - joblib

### Platform-Specific Requirements

#### Windows
- No additional requirements
- Works on Windows 10/11

#### Linux
- **tkinter**: `sudo apt-get install python3-tk` (Ubuntu/Debian)
- **X11 development libraries**: `sudo apt-get install libx11-dev`
- For other distributions, install equivalent packages

#### macOS
- **Xcode Command Line Tools**: `xcode-select --install`
- **Homebrew** (recommended): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

## 🚀 Building

### Method 1: Automatic Cross-Platform Builder (Recommended)

```bash
# Build for current platform
python build_cross_platform.py
```

This script automatically detects your platform and uses the appropriate configuration.

### Method 2: Manual Build with PyInstaller

#### Windows
```bash
pyinstaller file_organizer_watchdog.spec --clean
```

#### Linux
```bash
pyinstaller file_organizer_linux.spec --clean
```

#### macOS
```bash
pyinstaller file_organizer_macos.spec --clean
```

## 📦 Output Files

### Windows
- **Output**: `dist/DownFileOrg.exe`
- **Type**: Single executable file
- **Size**: ~50-80 MB
- **Distribution**: Copy the .exe file

### Linux
- **Output**: `dist/DownFileOrg`
- **Type**: Single executable file
- **Size**: ~50-80 MB
- **Distribution**: Copy the executable file
- **Usage**: `chmod +x DownFileOrg && ./DownFileOrg`

### macOS
- **Output**: `dist/DownFileOrg.app`
- **Type**: macOS app bundle
- **Size**: ~50-80 MB
- **Distribution**: Copy the .app bundle
- **Usage**: Double-click or drag to Applications

## 🔍 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Install missing packages
pip install -r requirements.txt

# For tkinter on Linux
sudo apt-get install python3-tk
```

#### "Permission denied" on Linux/macOS
```bash
chmod +x dist/DownFileOrg
```

#### macOS "Unidentified Developer" warning
1. Right-click the app → Open
2. Or go to System Preferences → Security & Privacy → Allow

#### Large executable size
- This is normal for PyInstaller builds
- Includes Python interpreter and all dependencies
- For smaller size, consider using `--exclude-module` for unused packages

### Platform-Specific Issues

#### Linux
- **Missing libraries**: Install development packages
  ```bash
  sudo apt-get install python3-dev python3-tk libx11-dev
  ```
- **Different distributions**: May need different package names

#### macOS
- **Code signing**: For distribution, consider signing the app
- **Notarization**: Required for macOS Catalina+ distribution
- **Architecture**: Build on same architecture as target (Intel vs Apple Silicon)

## 🎯 Distribution Tips

### Windows
- Single .exe file is completely portable
- No Python installation required on target machines
- Works on Windows 10/11

### Linux
- Test on different distributions (Ubuntu, CentOS, etc.)
- Consider creating .deb or .rpm packages
- AppImage format for universal Linux distribution

### macOS
- For public distribution, code signing is recommended
- Test on different macOS versions
- Consider creating .dmg installer

## 🔄 Building for Multiple Platforms

### Virtual Machines
Use VMs to build for different platforms:
- **Windows**: VMware/VirtualBox with Windows 10/11
- **Linux**: Docker or VM with Ubuntu/CentOS
- **macOS**: Use macOS machine or VM (license restrictions apply)

### Cloud Build Services
- **GitHub Actions**: Can build for all platforms
- **Travis CI**: Multi-platform builds
- **Azure DevOps**: Windows, Linux, macOS builds

### Docker (Linux builds)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python build_cross_platform.py
```

## 📋 Build Verification

After building, test the executable:

1. **Functionality**: Test file organization features
2. **Dependencies**: Ensure all libraries are bundled
3. **Performance**: Check startup time and memory usage
4. **GUI**: Verify interface renders correctly
5. **File permissions**: Test read/write access

## 🚀 Automation

### Automated Builds with GitHub Actions

Create `.github/workflows/build.yml`:

```yaml
name: Build DownFileOrg

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Build executable
      run: |
        python build_cross_platform.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: DownFileOrg-${{ matrix.os }}
        path: dist/
```

This will automatically build for all platforms on every commit!
