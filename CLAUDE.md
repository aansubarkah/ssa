# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains educational materials and code examples for "Sekolah Sabtu Auditor" (SSA) - a Saturday school focused on data analysis, automation, and auditing techniques using Python. The project is organized into multiple directories covering different topics and skills.

## Repository Structure

### Core Learning Modules
- **BasicPython/** - Fundamental Python programming concepts and exercises
- **WebScraping/** - Web scraping techniques using Requests, Selenium, and other tools
- **DataViz/** & **InteractiveDashboard/** - Data visualization using Python libraries and Streamlit
- **MembukaDatabase/** - Database connections and data extraction techniques
- **MembukaPDF/** - PDF processing and data extraction from PDF documents

### Specialized Automation Projects
- **AutomateKlikBCA/** - Internet banking automation for BCA (Bank Central Asia)
- **InputOtomatisKeWeb/** - Automated web form filling
- **ScrapeIG/** & **ScrapeTwitter/** - Social media scraping tools
- **WebScrapeECom/** & **WebScrapeGovts/** - E-commerce and government website scraping

### Document Processing
- **FakturPajakPDFExcel/** - Tax invoice PDF to Excel conversion
- **RCPDFExcel/** - Bank statement PDF to Excel conversion
- **ConvertPDFNonOCRPakeAI/** - AI-powered PDF to Excel conversion for non-OCR documents with secure API key storage
- **ConvertGambarNotaJadiExcel/** - Receipt image to Excel conversion

### Specialized Tools
- **TrimVideo/** - Video editing and trimming utilities
- **DownloadSirup/** - Government procurement data downloading from SIRUP system
- **DataDikti/** - Higher education data processing and similarity analysis

## Common Development Environment

### Python Environment
- Primary development uses **Jupyter Notebooks** (.ipynb files)
- Virtual environment setup available in `BasicPython/env/`
- Common libraries used:
  - `pandas` - Data manipulation and analysis
  - `selenium` & `undetected-chromedriver` - Web automation
  - `requests` - HTTP requests for API calls and web scraping
  - `streamlit` - Interactive dashboard creation
  - `matplotlib`, `plotly` - Data visualization
  - `PyPDF2`, `pdfplumber` - PDF processing

### File Patterns
- **Jupyter Notebooks**: Main development format, extensive use of `.ipynb` files
- **Data Files**: Excel (`.xlsx`), CSV (`.csv`), PDF (`.pdf`), JSON (`.json`)
- **Presentation Materials**: PowerPoint files (`.pptx`) for educational content
- **Configuration**: Credentials stored in `credentials.py` files (typically excluded from version control)

## Development Workflow

### Running Jupyter Notebooks
```bash
# Navigate to the specific project directory
cd [ProjectDirectory]

# Start Jupyter Notebook
jupyter notebook

# Or use Jupyter Lab
jupyter lab
```

### Installing Dependencies
Most projects use standard Python libraries. Install common dependencies:
```bash
pip install pandas selenium undetected-chromedriver requests streamlit matplotlib plotly PyPDF2 pdfplumber openpyxl
```

### Web Automation Setup
For projects involving web scraping or automation:
1. Install Chrome browser and appropriate ChromeDriver
2. Use `undetected-chromedriver` for sites with anti-bot detection
3. Selenium WebDriver setup is standardized across projects

## Project-Specific Notes

### Banking Automation (AutomateKlikBCA)
- Uses `undetected-chromedriver` to avoid detection
- Handles iFrames and complex authentication flows
- Demo site available at: https://bca.tanpa.download/login.htm

### Data Visualization Projects
- Streamlit applications for interactive dashboards
- Standard pattern: data loading → processing → visualization
- Examples available in `InteractiveDashboard/` with numbered progression files

### PDF Processing
- Multiple approaches: PyPDF2 for text extraction, AI-powered for complex layouts
- Batch processing capabilities for multiple files
- Output typically to Excel format for further analysis
- **ConvertPDFNonOCRPakeAI** features:
  - Single-file HTML application with embedded Tailwind CSS
  - Secure API key storage using XOR encryption in localStorage
  - Real-time thumbnail generation and processing status
  - Google Gemini AI integration for table extraction
  - Optimized for non-OCR PDF documents
  - **PRODUCTION READY**: Complete SEO optimization, build system, and deployment automation
  - **Latest Achievement**: Full production deployment with automated scripts for pdf-to-excel.basangdata.com

### Web Scraping Projects
- Combination of Requests (for APIs) and Selenium (for dynamic content)
- Rate limiting and respectful scraping practices
- Data storage in multiple formats (JSON, Excel, CSV)

## Educational Context

This repository serves as course material for data analysis and automation training. Each directory typically contains:
- Jupyter notebooks with step-by-step tutorials
- Sample data files for practice
- PowerPoint presentations for instruction
- Copywriting text files with course descriptions

When working with this codebase, consider the educational nature and ensure examples remain clear and well-documented for learning purposes.

## Recent Major Achievement: ConvertPDFNonOCRPakeAI Production Deployment

**Status**: ✅ COMPLETED (January 2025)  
**Domain**: pdf-to-excel.basangdata.com  
**Project Summary**: Complete transformation from single HTML file to production-ready web application

### Key Accomplishments:
1. **Enhanced User Experience**: Implemented API key validation, modal warnings, and smart button states
2. **SEO Optimization**: Full optimization for "pdf to excel" keywords with meta tags, structured data, and content strategy
3. **Build System**: Automated Tailwind CSS compilation and HTML minification with 10.3% file size reduction
4. **Production Deployment**: Apache configuration, CORS setup, and automated deployment scripts for both Windows and Linux
5. **Cross-Platform Support**: Both Bash (.sh) and PowerShell (.ps1) deployment scripts
6. **Documentation**: Comprehensive guides including PLANNING.md, TASKS.md, build-guide.md, and QUICK-START.md

### Technical Stack:
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **AI Integration**: Google Gemini API for table extraction
- **Build Tools**: Node.js, npm, custom minification scripts
- **Deployment**: Apache2, Linux VPS (VULTR), automated SSH deployment
- **Security**: XOR encryption for API keys, proper file permissions

### Files Created (15 total):
- Production-ready minified HTML (dist/index-oneliner.html)
- Enhanced Tailwind CSS components (src/input.css)
- Automated deployment scripts (deploy.sh, deploy.ps1)
- Comprehensive documentation and build guides
- Apache virtual host configuration

This project demonstrates the complete journey from prototype to production-ready web application with professional deployment automation.