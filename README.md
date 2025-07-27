# Adobe India Hackathon 2025 - PDF Analyzer

## 🎯 Connecting the Dots Challenge Submission

**Rethink Reading. Rediscover Knowledge.**

This project reimagines PDFs as intelligent, interactive experiences that understand structure, surface insights, and respond like trusted research companions.

---

## 🚀 Project Overview

### Challenge Solutions

**✅ Challenge 1a: Enhanced PDF Processing**
- Real PDF text extraction using pypdf library
- Intelligent heading detection and document structure analysis
- JSON schema-compliant output
- Sub-10-second processing for large PDFs

**✅ Challenge 1b: Persona-Based Analysis**
- Multi-collection PDF analysis
- Persona-driven content ranking
- Context-aware section extraction
- Intelligent importance scoring

**✅ Bonus: Interactive Web Application**
- Professional single-file HTML/CSS/JS webapp
- Drag-and-drop PDF upload
- Custom persona input
- JSON output with syntax highlighting
- Professional UI with Font Awesome icons

---

## 📁 Project Structure

```
Adobe-India-Hackathon25/
├── README.md                           # Project overview and instructions
├── pdf_analyzer_webapp.html            # Complete web application
├── Challenge_1a/                       # PDF structure extraction
│   ├── process_pdfs.py                # Main processing script
│   ├── Dockerfile                     # Container configuration
│   ├── requirements.txt               # Python dependencies
│   ├── test_challenge_1a.ps1         # Test script
│   └── sample_dataset/               # Test data and schema
└── Challenge_1b/                      # Persona-based analysis
    ├── process_collections.py        # Main analysis script
    ├── Dockerfile                    # Container configuration
    ├── requirements.txt              # Python dependencies
    ├── test_challenge_1b.ps1        # Test script
    ├── Collection 1/                 # Travel planning documents
    ├── Collection 2/                 # Adobe Acrobat tutorials
    └── Collection 3/                 # Recipe and cooking guides
```

---

## 🔧 Quick Start

### Prerequisites
- Docker Desktop
- PowerShell (Windows)
- Modern web browser

### Running Challenge 1a
```powershell
cd Challenge_1a
docker build --platform linux/amd64 -t pdf-processor-challenge-1a .
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/test_output:/app/output --network none pdf-processor-challenge-1a
.\test_challenge_1a.ps1
```

### Running Challenge 1b
```powershell
cd Challenge_1b
docker build --platform linux/amd64 -t pdf-analyzer-challenge-1b .
docker run --rm --network none pdf-analyzer-challenge-1b
.\test_challenge_1b.ps1
```

### Running Web Application
Simply open `pdf_analyzer_webapp.html` in any modern web browser.

---

## ✨ Key Features

### 🎨 Professional Web Interface
- **Modern Design**: Clean, professional UI with classic color scheme
- **Drag & Drop**: Intuitive file upload experience
- **Custom Personas**: Support for any professional role
- **JSON Output**: Formatted results with syntax highlighting
- **Responsive**: Works on desktop, tablet, and mobile

### 🧠 Intelligent Processing
- **Real Text Extraction**: Accurate content parsing from PDFs
- **Structure Recognition**: Automatic heading and section detection
- **Persona Awareness**: Content analysis tailored to user roles
- **Performance Optimized**: Fast processing with memory efficiency

### 🏗️ Production Ready
- **Docker Containerized**: Consistent deployment across platforms
- **Schema Compliant**: Outputs conform to provided specifications
- **Error Handling**: Graceful handling of edge cases
- **Comprehensive Testing**: Automated test suites included

---

## 🎯 Supported Personas

- **Travel Planner**: Optimized for itineraries and travel content
- **HR Professional**: Focused on forms and compliance
- **Food Contractor**: Specialized in recipes and catering
- **Custom Personas**: Any professional role via text input

---

## � Technical Highlights

- **Processing Speed**: Sub-10-second analysis for 50-page PDFs
- **Memory Efficient**: Optimized for large document collections
- **Cross-Platform**: Windows, Linux, and macOS compatibility
- **Modern Web Standards**: HTML5, CSS3, ES6+ JavaScript
- **Professional Icons**: Font Awesome integration
- **Accessibility**: WCAG compliant interface design

---

## 🏆 Submission Details

**Team**: Individual Submission  
**Technologies**: Python, Docker, HTML/CSS/JavaScript, Font Awesome  
**Testing**: Comprehensive test suites with automated validation  
**Documentation**: Complete setup and usage instructions  

This submission represents a complete, production-ready solution that goes beyond the basic requirements to deliver an exceptional user experience.

---

**Ready to connect the dots and revolutionize PDF reading!** 🚀
