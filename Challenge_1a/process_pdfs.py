import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any
import pypdf
from dataclasses import dataclass

@dataclass 
class OutlineItem:
    level: str
    text: str
    page: int

class PDFProcessor:
    def __init__(self):
        # Patterns for detecting headings based on common formatting
        self.heading_patterns = [
            # Chapter/Section numbers
            (r'^(?:Chapter|Section|Part)\s+\d+[:\.\s](.+)', 'H1'),
            (r'^\d+\.\s+(.+)', 'H1'),
            (r'^\d+\.\d+\s+(.+)', 'H2'),
            (r'^\d+\.\d+\.\d+\s+(.+)', 'H3'),
            
            # All caps headings (likely major sections)
            (r'^([A-Z\s]{3,}[A-Z])$', 'H1'),
            
            # Title case with certain keywords
            (r'^(Introduction|Conclusion|Summary|Overview|Background|Methodology|Results|Discussion|References)$', 'H1'),
            (r'^(Abstract|Acknowledgments|Appendix)$', 'H1'),
            
            # Lines that are significantly shorter and capitalized
            (r'^([A-Z][a-z\s]{5,40})$', 'H2'),
        ]

    def extract_text_with_page_info(self, pdf_path: str) -> List[tuple]:
        """Extract text from PDF with page numbers"""
        text_pages = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_pages.append((text, page_num))
                except Exception as e:
                    print(f"Error extracting text from page {page_num}: {e}")
                    continue
        
        return text_pages

    def detect_title(self, first_page_text: str) -> str:
        """Extract title from first page"""
        lines = [line.strip() for line in first_page_text.split('\n') if line.strip()]
        
        if not lines:
            return "Untitled Document"
        
        # Look for the first substantial line that could be a title
        for line in lines[:10]:  # Check first 10 lines
            if len(line) > 10 and len(line) < 200:
                # Skip lines that look like headers/footers
                if not re.match(r'^\d+$|^page\s+\d+|^chapter\s+\d+', line.lower()):
                    return line
        
        return lines[0] if lines else "Untitled Document"

    def extract_outline(self, text_pages: List[tuple]) -> List[OutlineItem]:
        """Extract document outline based on text patterns"""
        outline_items = []
        
        for text, page_num in text_pages:
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or len(line) < 3:
                    continue
                
                # Check each heading pattern
                for pattern, level in self.heading_patterns:
                    match = re.match(pattern, line, re.MULTILINE)
                    if match:
                        heading_text = match.group(1) if match.groups() else line
                        heading_text = heading_text.strip()
                        
                        # Avoid duplicates and very short headings
                        if (len(heading_text) >= 3 and 
                            not any(item.text.lower() == heading_text.lower() 
                                   for item in outline_items)):
                            outline_items.append(OutlineItem(level, heading_text, page_num))
                        break
        
        # If no headings found, create basic structure
        if not outline_items and text_pages:
            outline_items.append(OutlineItem('H1', 'Document Content', 1))
        
        return outline_items

    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process a single PDF file"""
        print(f"Processing {pdf_path}...")
        
        try:
            # Extract text with page information
            text_pages = self.extract_text_with_page_info(pdf_path)
            
            if not text_pages:
                return {
                    "title": "Empty Document",
                    "outline": []
                }
            
            # Extract title from first page
            title = self.detect_title(text_pages[0][0])
            
            # Extract outline
            outline_items = self.extract_outline(text_pages)
            
            # Convert to required format
            outline = [
                {
                    "level": item.level,
                    "text": item.text,
                    "page": item.page
                }
                for item in outline_items
            ]
            
            return {
                "title": title,
                "outline": outline
            }
            
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return {
                "title": f"Error Processing: {Path(pdf_path).stem}",
                "outline": [
                    {
                        "level": "H1",
                        "text": "Processing Error",
                        "page": 1
                    }
                ]
            }

def process_pdfs():
    """Main processing function"""
    # Get input and output directories
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize processor
    processor = PDFProcessor()
    
    # Get all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    for pdf_file in pdf_files:
        try:
            # Process the PDF
            result = processor.process_pdf(str(pdf_file))
            
            # Create output JSON file
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully processed {pdf_file.name} -> {output_file.name}")
            
        except Exception as e:
            print(f"Failed to process {pdf_file.name}: {e}")

if __name__ == "__main__":
    print("Starting PDF processing...")
    process_pdfs() 
    print("PDF processing completed!")