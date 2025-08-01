# Local PDF to Excel Converter - Complete Setup Guide

Transform your PDFs into Excel spreadsheets using AI - completely offline and private with Ollama!

## 🎯 What You'll Get

- **Complete Privacy**: All processing happens on your local machine
- **Offline Processing**: No internet required once set up
- **AI-Powered**: Extract tables from non-searchable PDFs, scanned documents, and images
- **Batch Processing**: Convert multiple files simultaneously
- **Drag & Drop**: Reorder pages before processing

---

## 📋 Prerequisites

### 1. Install Python

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python version (3.8 or higher)
3. **Important**: Check "Add Python to PATH" during installation
4. Click "Install Now"

**Verify Installation:**
```cmd
python --version
```
You should see something like `Python 3.11.x`

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### 2. Install Ollama

**Windows:**
1. Go to [ollama.com](https://ollama.com/)
2. Download the Windows installer
3. Run the installer
4. Ollama will start automatically

**macOS:**
```bash
# Download from ollama.com or use:
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 3. Download a Vision Model

Choose one of these models (larger = more accurate but slower):

```bash
# Recommended for most users (7B parameters)
ollama pull llava

# Faster, smaller model (1.6B parameters)
ollama pull moondream

# More accurate, larger model (13B parameters)
ollama pull bakllava

# Latest Llama 3.2 vision model (11B parameters)
ollama pull llama3.2-vision
```

---

## 🚀 Quick Start

### Step 1: Download the Converter

1. Download or clone this repository
2. Navigate to the project folder:
```cmd
cd path/to/ConvertPDFNonOCRPakeAI
```

### Step 2: Start Ollama (if not running)

**Check if Ollama is running:**
```cmd
ollama list
```

**If not running, start it:**
```cmd
ollama serve
```

### Step 3: Start the Converter

**Run the proxy server:**
```cmd
python ollama-proxy-server.py
```

You should see:
```
🚀 Starting Ollama Proxy Server...
📡 Server running at: http://localhost:8080
🔗 Open: http://localhost:8080
📁 Serving files from dist-local/ directory
🔄 Proxying /api/* requests to Ollama at localhost:11434

💡 This server enables CORS for Ollama API access
⚠️  Make sure Ollama is running on localhost:11434

🛑 Press Ctrl+C to stop the server
```

### Step 4: Open in Browser

1. Open your web browser
2. Go to: **`localhost:8080`**
3. You should see the Local PDF to Excel Converter interface!

---

## 📖 How to Use

### 1. Test Connection
- Click **"Test Connection"** button
- You should see: `✓ Connected to Ollama version X.X.X`
- If successful, available models will load in the dropdown

### 2. Select Model
- Choose a vision model from the dropdown
- **Recommended**: `llava` for best balance of speed and accuracy

### 3. Upload PDFs
- **Drag & drop** PDF files onto the upload area, or
- **Click** the upload area to select files
- Supports: PDF, PNG, JPG, JPEG, WebP, BMP, TIFF, GIF

### 4. Review Pages (Optional)
- **Thumbnail preview** shows all pages
- **Delete pages** you don't want to process (click ❌)
- **Reorder pages** by dragging thumbnails

### 5. Configure Processing
- **DPI Setting**: Higher = better quality but slower
  - 150 DPI: Fast processing
  - 200 DPI: Balanced (recommended)
  - 300 DPI: High quality for detailed tables

### 6. Start Conversion
- Click **"Start PDF to Excel Conversion"**
- Watch real-time progress with:
  - Progress bar and percentage
  - Detailed processing logs
  - Time estimates

### 7. Download Results
- **Individual files**: Click "Download Excel File" for each
- **Batch download**: Click "Download All Excel Files"
- Files are saved as `filename_by_BasangData.xlsx`

---

## 🔧 Troubleshooting

### Problem: "Connection failed" Error

**Solution 1 - Restart Ollama with CORS:**
```cmd
# Stop Ollama first
taskkill /f /im ollama.exe

# Restart with CORS enabled
set OLLAMA_ORIGINS=*
ollama serve
```

**Solution 2 - Use the proxy server (current method):**
- Keep using `python ollama-proxy-server.py`
- This bypasses CORS issues automatically

### Problem: "No models found"

**Check available models:**
```cmd
ollama list
```

**Download a vision model:**
```cmd
ollama pull llava
```

### Problem: Python not found

**Windows:**
```cmd
# Try python3 instead
python3 ollama-proxy-server.py

# Or check if Python is in PATH
where python
```

**Add Python to PATH:**
1. Search "Environment Variables" in Windows
2. Edit "Path" in System Variables
3. Add Python installation directory

### Problem: Port 8080 already in use

**Find what's using the port:**
```cmd
netstat -ano | findstr :8080
```

**Kill the process:**
```cmd
taskkill /PID <process-id> /F
```

**Or use a different port:**
Edit `ollama-proxy-server.py` and change `PORT = 8080` to `PORT = 8081`

---

## 📁 File Structure

```
ConvertPDFNonOCRPakeAI/
├── dist-local/                          # Production files
│   ├── local-converter-oneliner.html    # Ultra-compressed version
│   ├── local-converter-minified.html    # Clean minified version
│   ├── local-converter-dev.html         # Development version
│   └── README.md                        # Technical documentation
├── ollama-proxy-server.py               # CORS proxy server
├── local_converter.html                 # Source file
├── build-local-converter.js             # Build script
└── SETUP-GUIDE.md                       # This guide
```

---

## 🎛️ Advanced Configuration

### Custom Ollama Settings

**Change Ollama port (if needed):**
```bash
# Set custom port
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

**Then update the proxy server:**
Edit `ollama-proxy-server.py` line ~111:
```python
ollama_url = f'http://localhost:11435{self.path}'
```

### Performance Optimization

**For better performance:**
1. **Use GPU acceleration** (if available):
   - Ollama automatically uses GPU if detected
   - Check logs for "GPU" messages

2. **Adjust model size** based on your hardware:
   - **8GB+ RAM**: llava (7B), bakllava (13B)
   - **4-8GB RAM**: moondream (1.6B)
   - **<4GB RAM**: Consider cloud processing instead

3. **Process fewer pages at once** for limited memory

---

## 🤝 Support

### Getting Help

1. **Check the logs** in the browser console (F12)
2. **Review Ollama logs** in the terminal
3. **Try different models** if accuracy is poor
4. **Restart both services** if something breaks:
   ```cmd
   # Stop proxy server (Ctrl+C)
   # Stop Ollama
   taskkill /f /im ollama.exe
   
   # Restart Ollama
   ollama serve
   
   # Restart proxy
   python ollama-proxy-server.py
   ```

### Common Model Recommendations

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| **General use** | `llava` | Best balance of speed/accuracy |
| **Fast processing** | `moondream` | Lightweight, quick results |
| **High accuracy** | `bakllava` | More parameters, better extraction |
| **Latest features** | `llama3.2-vision` | Newest model architecture |

---

## 🎉 You're Ready!

Your Local PDF to Excel Converter is now set up and ready to use! 

**Quick reminder:**
1. Run: `python ollama-proxy-server.py`
2. Open: `localhost:8080`
3. Upload PDFs and convert to Excel!

**Enjoy completely private, offline PDF to Excel conversion! 🔒✨**