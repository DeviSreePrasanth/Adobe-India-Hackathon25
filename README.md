# Adobe India Hackathon 2025

## Welcome to the "Connecting the Dots" Challenge

### Rethink Reading. Rediscover Knowledge

What if every time you opened a PDF, it didn't just sit there—it spoke to you, connected ideas, and narrated meaning across your entire library?

That's the future we're building — and we want you to help shape it.

In the Connecting the Dots Challenge, your mission is to reimagine the humble PDF as an intelligent, interactive experience—one that understands structure, surfaces insights, and responds to you like a trusted research companion.

### The Journey Ahead

**Round 1:**
Kick things off by building the brains — extract structured outlines from raw PDFs with blazing speed and pinpoint accuracy. Then, power it up with on-device intelligence that understands sections and links related ideas together.

**Round 2:**
It's showtime! Build a beautiful, intuitive reading webapp using Adobe's PDF Embed API. You will be using your Round 1 work to design a futuristic webapp.

### Why This Matters

In a world flooded with documents, what wins is not more content — it's context. You're not just building tools — you're building the future of how we read, learn, and connect. No matter your background — ML hacker, UI builder, or insight whisperer — this is your stage.

Are you in?

It's time to read between the lines. Connect the dots. And build a PDF experience that feels like magic. Let's go.

---

## Project Structure

```
Adobe-India-Hackathon25/
├── README.md                           # This file - project overview
├── DEVELOPMENT.md                      # Comprehensive development guide
├── Challenge_1a/                       # Basic PDF processing solution
│   ├── process_pdfs.py                # Enhanced PDF processor with real extraction
│   ├── Dockerfile                     # Optimized container configuration
│   ├── requirements.txt               # Python dependencies
│   ├── test_challenge_1a.ps1         # Automated test script
│   ├── sample_dataset/               # Test data and output schema
│   └── README.md                     # Challenge 1a detailed documentation
└── Challenge_1b/                      # Advanced multi-collection analysis
    ├── process_collections.py        # Persona-based intelligent analyzer
    ├── Dockerfile                    # Container for multi-collection processing
    ├── requirements.txt              # Python dependencies
    ├── test_challenge_1b.ps1        # Automated test script
    ├── Collection 1/                 # Travel planning documents
    ├── Collection 2/                 # Adobe Acrobat learning materials
    ├── Collection 3/                 # Recipe and cooking guides
    └── README.md                     # Challenge 1b detailed documentation
```

## Quick Start

### Prerequisites

- Docker Desktop (with AMD64/Linux container support)
- PowerShell (Windows) or Bash (Linux/Mac)
- Git

### Setup and Testing

```powershell
# Clone and navigate to project
git clone <repository-url>
cd Adobe-India-Hackathon25

# Challenge 1a - PDF Processing
cd Challenge_1a
docker build --platform linux/amd64 -t pdf-processor-challenge-1a .
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/test_output:/app/output --network none pdf-processor-challenge-1a

# Test the solution
.\test_challenge_1a.ps1

# Challenge 1b - Multi-Collection Analysis
cd ../Challenge_1b
docker build --platform linux/amd64 -t pdf-analyzer-challenge-1b .
docker run --rm --network none pdf-analyzer-challenge-1b

# Test the solution
.\test_challenge_1b.ps1
```

## Challenge Solutions

### [Challenge 1a: Enhanced PDF Processing Solution](./Challenge_1a/README.md)

**Advanced PDF processing with intelligent structure detection**

**Key Features:**

- ✅ **Real PDF Text Extraction**: Using pypdf library for accurate text extraction
- ✅ **Intelligent Heading Detection**: Pattern-based section identification
- ✅ **Document Structure Analysis**: Automatic outline generation
- ✅ **Performance Optimized**: Sub-10-second processing for 50-page PDFs
- ✅ **Docker Containerized**: Fully containerized with AMD64 compatibility
- ✅ **Schema Compliant**: Outputs conform to provided JSON schema
- ✅ **Automated Testing**: Complete test suite with validation

**Technical Highlights:**

- Multi-level heading detection (H1, H2, H3)
- Title extraction from document content
- Memory-efficient streaming processing
- Error handling for corrupted PDFs
- Cross-platform compatibility

### [Challenge 1b: Persona-Based Multi-Collection PDF Analysis](./Challenge_1b/README.md)

**Intelligent document analysis tailored to specific user personas and tasks**

**Key Features:**

- 🎯 **Persona-Driven Analysis**: Content ranking based on user roles
- 📚 **Multi-Collection Processing**: Simultaneous analysis of document sets
- 🔍 **Intelligent Section Extraction**: Context-aware content identification
- 📊 **Importance Ranking**: AI-powered relevance scoring
- 🎨 **Refined Content Analysis**: Paragraph-level content extraction
- 🏗️ **Scalable Architecture**: Modular design for easy persona addition

**Supported Personas:**

- **Travel Planner**: Optimized for itinerary and travel content
- **HR Professional**: Focused on forms, compliance, and processes
- **Food Contractor**: Specialized in recipes and catering needs

**Collection Analysis:**

- **Collection 1**: South of France travel guides (7 documents)
- **Collection 2**: Adobe Acrobat tutorials (15 documents)
- **Collection 3**: Recipe and cooking guides (9 documents)

## Key Enhancements Made

### 🚀 Performance Improvements

- **Optimized PDF Processing**: Real text extraction vs. dummy data
- **Memory Management**: Efficient handling of large documents
- **Parallel Processing**: Multi-document processing capabilities
- **Docker Optimization**: Slim base images and efficient builds

### 🧠 Intelligence Features

- **Pattern Recognition**: Advanced heading detection algorithms
- **Context Awareness**: Persona-based content understanding
- **Importance Scoring**: Relevance ranking based on user needs
- **Content Refinement**: Intelligent paragraph extraction

### 🛠️ Developer Experience

- **Automated Testing**: Complete test suites for both challenges
- **Development Documentation**: Comprehensive guides and best practices
- **Setup Automation**: One-command project initialization
- **Cross-Platform Support**: Works on Windows, Linux, and macOS

### 📊 Production Ready

- **Error Handling**: Graceful handling of edge cases
- **Logging**: Comprehensive logging for debugging
- **Validation**: JSON schema compliance verification
- **Monitoring**: Performance and memory usage tracking

## Testing and Validation

### Automated Test Coverage

- **Docker Build Tests**: Verify container functionality
- **JSON Schema Validation**: Ensure output compliance
- **Performance Tests**: Validate speed requirements
- **Error Handling Tests**: Verify graceful failure modes

### Performance Benchmarks

- **Challenge 1a**: Processes 50-page PDFs in under 10 seconds
- **Challenge 1b**: Analyzes multiple collections efficiently
- **Memory Usage**: Stays within 16GB RAM constraint
- **CPU Utilization**: Optimized for 8-core systems

## Documentation

- **[DEVELOPMENT.md](./DEVELOPMENT.md)**: Complete development guide
- **[Challenge_1a/README.md](./Challenge_1a/README.md)**: Challenge 1a implementation details
- **[Challenge_1b/README.md](./Challenge_1b/README.md)**: Challenge 1b architecture and features

## Contributing

We welcome contributions! Please see our development guide for:

- Code style guidelines
- Testing procedures
- Performance optimization tips
- Feature enhancement suggestions

---

**Note**: This is a complete, production-ready implementation that goes beyond the basic sample requirements. Each challenge includes real PDF processing capabilities, intelligent analysis features, comprehensive testing, and detailed documentation.
