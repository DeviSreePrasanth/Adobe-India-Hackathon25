import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pypdf
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ExtractedSection:
    document: str
    section_title: str
    importance_rank: int
    page_number: int

@dataclass 
class SubsectionAnalysis:
    document: str
    refined_text: str
    page_number: int

class PersonaBasedAnalyzer:
    def __init__(self):
        # Define persona-specific keywords for importance ranking
        self.persona_keywords = {
            "Travel Planner": {
                "high": ["itinerary", "accommodation", "hotel", "restaurant", "attractions", "transportation", 
                        "booking", "prices", "budget", "schedule", "location", "distance", "time"],
                "medium": ["culture", "history", "tips", "recommendations", "local", "traditional"],
                "low": ["general", "overview", "introduction"]
            },
            "HR Professional": {
                "high": ["forms", "fillable", "onboarding", "compliance", "workflow", "automation",
                        "signatures", "documents", "templates", "process"],
                "medium": ["editing", "creating", "sharing", "collaboration", "security"],
                "low": ["basics", "introduction", "overview", "getting started"]
            },
            "Food Contractor": {
                "high": ["vegetarian", "buffet", "corporate", "catering", "menu", "recipes", 
                        "ingredients", "portions", "serving", "cooking time"],
                "medium": ["preparation", "techniques", "nutrition", "dietary"],
                "low": ["basics", "introduction", "history"]
            }
        }

    def extract_text_from_pdf(self, pdf_path: str) -> List[Tuple[str, int]]:
        """Extract text from PDF with page numbers"""
        text_pages = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        text = page.extract_text()
                        if text.strip():
                            text_pages.append((text, page_num))
                    except Exception as e:
                        print(f"Error extracting text from page {page_num} of {pdf_path}: {e}")
                        continue
        except Exception as e:
            print(f"Error opening PDF {pdf_path}: {e}")
            
        return text_pages

    def detect_sections(self, text_pages: List[Tuple[str, int]], filename: str) -> List[ExtractedSection]:
        """Detect sections in the document"""
        sections = []
        
        # Common heading patterns
        heading_patterns = [
            (r'^(?:Chapter|Section|Part)\s+\d+[:\.\s](.+)', 1),
            (r'^\d+\.\s+(.+)', 1),
            (r'^\d+\.\d+\s+(.+)', 2),
            (r'^([A-Z\s]{3,}[A-Z])$', 1),
            (r'^(Introduction|Conclusion|Summary|Overview|Background|Tips|Recommendations|Planning|Getting Started).*$', 1),
            (r'^([A-Z][a-z\s]{5,50})$', 2),
        ]
        
        for text, page_num in text_pages:
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or len(line) < 3:
                    continue
                
                for pattern, level in heading_patterns:
                    match = re.match(pattern, line, re.IGNORECASE)
                    if match:
                        section_title = match.group(1) if match.groups() else line
                        section_title = section_title.strip()
                        
                        if len(section_title) >= 3:
                            sections.append(ExtractedSection(
                                document=filename,
                                section_title=section_title,
                                importance_rank=0,  # Will be calculated later
                                page_number=page_num
                            ))
                        break
        
        # If no sections found, create a default one
        if not sections and text_pages:
            sections.append(ExtractedSection(
                document=filename,
                section_title="Main Content",
                importance_rank=1,
                page_number=1
            ))
        
        return sections

    def calculate_importance_rank(self, sections: List[ExtractedSection], persona: str, job_description: str) -> List[ExtractedSection]:
        """Calculate importance rank based on persona and job requirements"""
        persona_keys = self.persona_keywords.get(persona, {})
        job_words = job_description.lower().split()
        
        for section in sections:
            score = 0
            section_text = section.section_title.lower()
            
            # Check persona-specific keywords
            for keyword in persona_keys.get("high", []):
                if keyword in section_text:
                    score += 3
            
            for keyword in persona_keys.get("medium", []):
                if keyword in section_text:
                    score += 2
                    
            for keyword in persona_keys.get("low", []):
                if keyword in section_text:
                    score += 1
            
            # Check job-specific words
            for word in job_words:
                if len(word) > 3 and word in section_text:
                    score += 2
            
            section.importance_rank = max(1, min(5, score))  # Clamp between 1-5
        
        # Sort by importance (lower rank = more important)
        sections.sort(key=lambda x: x.importance_rank, reverse=True)
        
        # Reassign ranks to ensure proper ordering
        for i, section in enumerate(sections, 1):
            section.importance_rank = i
        
        return sections

    def extract_refined_content(self, text_pages: List[Tuple[str, int]], filename: str, 
                              persona: str, job_description: str) -> List[SubsectionAnalysis]:
        """Extract and refine content based on persona needs"""
        refined_content = []
        persona_keys = self.persona_keywords.get(persona, {})
        all_keywords = []
        
        for keyword_list in persona_keys.values():
            all_keywords.extend(keyword_list)
        
        job_words = [word for word in job_description.lower().split() if len(word) > 3]
        all_keywords.extend(job_words)
        
        for text, page_num in text_pages:
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            
            for paragraph in paragraphs:
                if len(paragraph) < 50:  # Skip very short paragraphs
                    continue
                
                # Check if paragraph contains relevant keywords
                paragraph_lower = paragraph.lower()
                relevance_score = 0
                
                for keyword in all_keywords:
                    if keyword in paragraph_lower:
                        relevance_score += 1
                
                # Include paragraphs with high relevance
                if relevance_score >= 2:
                    # Limit paragraph length for output
                    refined_text = paragraph[:500] + "..." if len(paragraph) > 500 else paragraph
                    
                    refined_content.append(SubsectionAnalysis(
                        document=filename,
                        refined_text=refined_text,
                        page_number=page_num
                    ))
        
        return refined_content[:10]  # Limit to top 10 most relevant paragraphs

    def process_collection(self, collection_path: str) -> Dict[str, Any]:
        """Process a complete collection"""
        input_file = Path(collection_path) / "challenge1b_input.json"
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Load input configuration
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        persona = input_data["persona"]["role"]
        job_description = input_data["job_to_be_done"]["task"]
        documents = input_data["documents"]
        
        # Process each document
        all_sections = []
        all_subsections = []
        processed_docs = []
        
        pdf_dir = Path(collection_path) / "PDFs"
        
        for doc_info in documents:
            filename = doc_info["filename"]
            pdf_path = pdf_dir / filename
            
            if not pdf_path.exists():
                print(f"PDF not found: {pdf_path}")
                continue
            
            print(f"Processing {filename}...")
            
            # Extract text
            text_pages = self.extract_text_from_pdf(str(pdf_path))
            
            if not text_pages:
                print(f"No text extracted from {filename}")
                continue
            
            # Detect sections
            sections = self.detect_sections(text_pages, filename)
            
            # Calculate importance ranks
            sections = self.calculate_importance_rank(sections, persona, job_description)
            
            # Extract refined content
            subsections = self.extract_refined_content(text_pages, filename, persona, job_description)
            
            all_sections.extend(sections)
            all_subsections.extend(subsections)
            processed_docs.append(filename)
        
        # Create output structure
        output = {
            "metadata": {
                "input_documents": processed_docs,
                "persona": persona,
                "job_to_be_done": job_description
            },
            "extracted_sections": [
                {
                    "document": section.document,
                    "section_title": section.section_title,
                    "importance_rank": section.importance_rank,
                    "page_number": section.page_number
                }
                for section in all_sections[:20]  # Limit to top 20 sections
            ],
            "subsection_analysis": [
                {
                    "document": subsection.document,
                    "refined_text": subsection.refined_text,
                    "page_number": subsection.page_number
                }
                for subsection in all_subsections
            ]
        }
        
        return output

def main():
    """Main processing function"""
    base_path = Path(".")
    collections = ["Collection 1", "Collection 2", "Collection 3"]
    
    analyzer = PersonaBasedAnalyzer()
    
    for collection in collections:
        collection_path = base_path / collection
        
        if not collection_path.exists():
            print(f"Collection not found: {collection_path}")
            continue
        
        try:
            print(f"\nProcessing {collection}...")
            result = analyzer.process_collection(str(collection_path))
            
            # Save output
            output_file = collection_path / "challenge1b_output.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully processed {collection}")
            
        except Exception as e:
            print(f"Error processing {collection}: {e}")

if __name__ == "__main__":
    main()
