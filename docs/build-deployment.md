# Build & Deployment Guide

## Development Build

### Backend Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_SECRET_KEY="dev-secret-key"

# Run development server
python backend/app.py
```

### Frontend Development Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# In separate terminal, build for testing
npm run build
```

## Production Build

### Backend Production Build

#### Using PyInstaller
```bash
# Install PyInstaller
pip install pyinstaller

# Create spec file
pyi-makespec --onedir --name="AI-Video-Editor-Backend" backend/app.py

# Edit AI-Video-Editor-Backend.spec:
```

```python
# AI-Video-Editor-Backend.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['backend/app.py'],
    pathex=[],
    binaries=[
        ('venv/Lib/site-packages/cv2/opencv_videoio_ffmpeg*.dll', 'cv2'),  # Windows
    ],
    datas=[
        ('backend/templates', 'templates'),
        ('backend/static', 'static'),
        ('wan2gp', 'wan2gp'),
    ],
    hiddenimports=[
        'flask',
        'cv2',
        'torch',
        'ffmpeg',
        'PIL',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI-Video-Editor-Backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI-Video-Editor-Backend'
)
```

```bash
# Build backend
pyinstaller AI-Video-Editor-Backend.spec

# Test build
cd dist/AI-Video-Editor-Backend
./AI-Video-Editor-Backend  # Linux/Mac
AI-Video-Editor-Backend.exe  # Windows
```

#### Using Docker (Alternative)
```dockerfile
# Dockerfile.backend
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements và install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY wan2gp/ ./wan2gp/

# Create necessary directories
RUN mkdir -p uploads temp output logs

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app/backend

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "backend/app.py"]
```

### Frontend Production Build

#### Using Electron Builder
```json
// package.json - add to frontend/package.json
{
  "main": "electron.js",
  "scripts": {
    "build": "react-scripts build",
    "electron": "electron .",
    "electron-dev": "concurrently \"npm start\" \"wait-on http://localhost:3000 && electron .\"",
    "dist": "npm run build && electron-builder",
    "pack": "electron-builder --dir"
  },
  "build": {
    "appId": "com.aivideo.editor",
    "productName": "AI Video Editor",
    "directories": {
      "output": "dist"
    },
    "files": [
      "build/**/*",
      "electron.js"
    ],
    "mac": {
      "category": "public.app-category.video",
      "target": "dmg"
    },
    "win": {
      "target": "nsis",
      "icon": "assets/icon.ico"
    },
    "linux": {
      "target": "AppImage",
      "category": "AudioVideo"
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true
    }
  }
}
```

```javascript
// frontend/electron.js
const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'assets/icon.png')
  });

  const startUrl = isDev 
    ? 'http://localhost:3000' 
    : `file://${path.join(__dirname, '../build/index.html')}`;
    
  mainWindow.loadURL(startUrl);
  
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
```

```bash
# Build frontend
cd frontend
npm run build
npm run dist
```

## Cross-Platform Build

### Build Scripts

#### build.sh (Linux/Mac)
```bash
#!/bin/bash
set -e

echo "Building AI Video Editor..."

# Build backend
echo "Building backend..."
cd backend
python -m venv build_env
source build_env/bin/activate
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --onedir --name="ai-video-backend" app.py
deactivate
cd ..

# Build frontend
echo "Building frontend..."
cd frontend
npm ci
npm run build
npm run dist
cd ..

# Create final package
echo "Creating package..."
mkdir -p dist/AI-Video-Editor
cp -r backend/dist/ai-video-backend/* dist/AI-Video-Editor/backend/
cp -r frontend/dist/* dist/AI-Video-Editor/frontend/

# Create launcher script
cat > dist/AI-Video-Editor/start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./backend/ai-video-backend &
BACKEND_PID=$!
sleep 3
./frontend/AI\ Video\ Editor
kill $BACKEND_PID
EOF

chmod +x dist/AI-Video-Editor/start.sh

echo "Build complete! Package location: dist/AI-Video-Editor"
```

#### build.bat (Windows)
```batch
@echo off
echo Building AI Video Editor...

REM Build backend
echo Building backend...
cd backend
python -m venv build_env
call build_env\Scripts\activate.bat
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --onedir --name="ai-video-backend" app.py
call build_env\Scripts\deactivate.bat
cd ..

REM Build frontend
echo Building frontend...
cd frontend
call npm ci
call npm run build
call npm run dist
cd ..

REM Create final package
echo Creating package...
mkdir dist\AI-Video-Editor
xcopy /E /I backend\dist\ai-video-backend\* dist\AI-Video-Editor\backend\
xcopy /E /I frontend\dist\* dist\AI-Video-Editor\frontend\

REM Create launcher script
echo @echo off > dist\AI-Video-Editor\start.bat
echo cd /d "%%~dp0" >> dist\AI-Video-Editor\start.bat
echo start /min backend\ai-video-backend.exe >> dist\AI-Video-Editor\start.bat
echo timeout /t 3 /nobreak ^> nul >> dist\AI-Video-Editor\start.bat
echo start frontend\"AI Video Editor.exe" >> dist\AI-Video-Editor\start.bat

echo Build complete! Package location: dist\AI-Video-Editor
pause
```

## Testing Builds

### Automated Testing Script
```python
# test_build.py
import subprocess
import time
import requests
import os
import sys

def test_backend():
    """Test backend executable"""
    print("Testing backend...")
    
    # Start backend
    if sys.platform == "win32":
        proc = subprocess.Popen(['dist/AI-Video-Editor/backend/ai-video-backend.exe'])
    else:
        proc = subprocess.Popen(['dist/AI-Video-Editor/backend/ai-video-backend'])
    
    # Wait for startup
    time.sleep(5)
    
    try:
        # Test API endpoints
        response = requests.get('http://localhost:5000/api/status', timeout=10)
        if response.status_code == 200:
            print("✓ Backend API working")
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False
    finally:
        proc.terminate()
        proc.wait()
    
    return True

def test_frontend():
    """Test frontend executable"""
    print("Testing frontend...")
    
    frontend_paths = [
        'dist/AI-Video-Editor/frontend/AI Video Editor.exe',  # Windows
        'dist/AI-Video-Editor/frontend/AI Video Editor.app',  # Mac
        'dist/AI-Video-Editor/frontend/AI Video Editor.AppImage'  # Linux
    ]
    
    frontend_exe = None
    for path in frontend_paths:
        if os.path.exists(path):
            frontend_exe = path
            break
    
    if not frontend_exe:
        print("❌ Frontend executable not found")
        return False
    
    # Basic file check
    if os.path.getsize(frontend_exe) > 100 * 1024 * 1024:  # > 100MB
        print("✓ Frontend executable size OK")
        return True
    else:
        print("❌ Frontend executable too small")
        return False

def main():
    print("=== Build Testing ===")
    
    success = True
    
    if not test_backend():
        success = False
    
    if not test_frontend():
        success = False
    
    if success:
        print("\n✓ All tests passed! Build is ready for distribution.")
    else:
        print("\n❌ Some tests failed. Check build configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Distribution

### Creating Installer

#### Windows NSIS Installer
```nsis
; installer.nsi
!define APPNAME "AI Video Editor"
!define COMPANYNAME "AI Video Solutions"
!define DESCRIPTION "AI-powered video editing tool"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0

Name "${APPNAME}"
OutFile "AI-Video-Editor-Setup.exe"
InstallDir "$PROGRAMFILES\${APPNAME}"

Section "install"
    SetOutPath $INSTDIR
    File /r "dist\AI-Video-Editor\*"
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\start.bat"
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\start.bat"
SectionEnd

Section "uninstall"
    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete "$DESKTOP\${APPNAME}.lnk"
    RMDir /r "$SMPROGRAMS\${APPNAME}"
    RMDir /r $INSTDIR
SectionEnd
```

#### macOS DMG Creation
```bash
# create_dmg.sh
#!/bin/bash

APP_NAME="AI Video Editor"
DMG_NAME="AI-Video-Editor-v1.0.0"
SOURCE_DIR="dist/AI-Video-Editor"

# Create temporary DMG
hdiutil create -volname "${APP_NAME}" -srcfolder "${SOURCE_DIR}" -ov -format UDZO "${DMG_NAME}.dmg"

echo "DMG created: ${DMG_NAME}.dmg"
```

#### Linux AppImage
```bash
# create_appimage.sh
#!/bin/bash

# Download AppImage tools
wget -c https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p AI-Video-Editor.AppDir/usr/bin
mkdir -p AI-Video-Editor.AppDir/usr/share/applications
mkdir -p AI-Video-Editor.AppDir/usr/share/icons/hicolor/256x256/apps

# Copy application files
cp -r dist/AI-Video-Editor/* AI-Video-Editor.AppDir/usr/bin/

# Create desktop file
cat > AI-Video-Editor.AppDir/AI-Video-Editor.desktop << EOF
[Desktop Entry]
Type=Application
Name=AI Video Editor
Exec=start.sh
Icon=ai-video-editor
Categories=AudioVideo;Video;
EOF

# Copy icon
cp assets/icon.png AI-Video-Editor.AppDir/usr/share/icons/hicolor/256x256/apps/ai-video-editor.png
cp assets/icon.png AI-Video-Editor.AppDir/ai-video-editor.png

# Create AppRun
cat > AI-Video-Editor.AppDir/AppRun << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/usr/bin"
./start.sh
EOF
chmod +x AI-Video-Editor.AppDir/AppRun

# Build AppImage
./appimagetool-x86_64.AppImage AI-Video-Editor.AppDir AI-Video-Editor.AppImage

echo "AppImage created: AI-Video-Editor.AppImage"
```

## Deployment Checklist

### Pre-deployment Verification
- [ ] All dependencies included
- [ ] Environment variables set correctly
- [ ] File permissions configured
- [ ] Security settings applied
- [ ] Performance testing completed
- [ ] Cross-platform compatibility verified
- [ ] Installation/uninstallation tested
- [ ] User documentation included

### Release Process
1. Tag version trong Git: `git tag v1.0.0`
2. Build all platforms
3. Run automated tests
4. Create installers
5. Upload to distribution platform
6. Update documentation
7. Announce release 