import fitz  # PyMuPDF
import json
from pathlib import Path
import os
import re
from collections import Counter

# --- Smart Path Configuration ---
# This block automatically detects if we are in Docker and sets paths accordingly.
IS_DOCKER = Path("/app/input").exists()

if IS_DOCKER:
    INPUT_DIR, OUTPUT_DIR = Path("/app/input"), Path("/app/output")
else:
    BASE_DIR = Path(__file__).parent
    INPUT_DIR = BASE_DIR / "sample_dataset/pdfs"
    OUTPUT_DIR = BASE_DIR / "sample_dataset/outputs"

def get_pdf_title(doc, pdf_path):
    """
    Intelligently extracts the title from the PDF.
    1. Checks metadata.
    2. Looks for the largest font text on the first page.
    3. Falls back to a cleaned-up filename.
    """
    # 1. Try metadata
    if doc.metadata and doc.metadata.get('title'):
        title = doc.metadata['title'].strip()
        if title and len(title) > 5 and title.lower() != 'untitled':
            return title

    # 2. Try largest font on first page
    try:
        page = doc[0]
        blocks = page.get_text("dict", sort=True)["blocks"]
        if blocks:
            max_font_size = 0
            potential_title = ""
            for b in blocks:
                if "lines" in b:
                    for l in b["lines"]:
                        if "spans" in l:
                            for s in l["spans"]:
                                if s["size"] > max_font_size:
                                    max_font_size = s["size"]
                                    potential_title = s["text"]
            # Clean up potential title and check if it's meaningful
            potential_title = potential_title.strip()
            if len(potential_title) > 4 and not potential_title.isnumeric():
                 return potential_title
    except Exception:
        pass # Ignore errors in title finding

    # 3. Fallback to filename
    return pdf_path.stem.replace('_', ' ').replace('-', ' ').title()

def generate_heuristic_outline(doc):
    """
    Generates a 'best-effort' outline if no official one exists.
    It identifies headings based on font size.
    """
    print("No official outline found. Generating a heuristic-based outline...")
    outline = []
    font_counts = Counter()
    
    # First pass: Determine the most common font size (body text)
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    if "spans" in l and l["spans"]:
                        font_counts[round(l["spans"][0]["size"])] += 1

    if not font_counts:
        return []

    # The most common font size is likely the body text
    body_font_size = font_counts.most_common(1)[0][0]
    
    # Identify heading sizes (e.g., anything > 20% larger than body text)
    heading_sizes = sorted([size for size in font_counts if size > body_font_size * 1.2], reverse=True)
    
    # Create a mapping from font size to heading level (e.g., largest is level 1)
    size_to_level = {size: level + 1 for level, size in enumerate(heading_sizes)}

    # Second pass: Extract text that matches heading sizes
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    if "spans" in l and l["spans"]:
                        span = l["spans"][0]
                        font_size = round(span["size"])
                        if font_size in size_to_level:
                            text = l["spans"][0]["text"].strip()
                            # Filter out short or irrelevant text
                            if len(text) > 2 and not text.isnumeric():
                                # *** CHANGE 1: FORMAT HEADING LEVEL ***
                                heading_level = f"H{size_to_level[font_size]}"
                                outline.append({
                                    "level": heading_level,
                                    "text": text,
                                    "page": page_num + 1
                                })
    return outline


def process_pdf_file(pdf_path):
    """
    Extracts title and outline, with a fallback to generate the outline if needed.
    """
    print(f"Processing {pdf_path.name}...")
    try:
        doc = fitz.open(pdf_path)
        
        # 1. Get the document title
        title = get_pdf_title(doc, pdf_path)

        # 2. Try to get the official outline (Table of Contents)
        toc = doc.get_toc()
        
        if toc:
            print("Found official outline (TOC).")
            # *** CHANGE 2: FORMAT HEADING LEVEL ***
            # Format the official outline to match the schema
            outline = [
                {"level": f"H{item[0]}", "text": str(item[1]), "page": int(item[2])}
                for item in toc
            ]
        else:
            # If no official TOC, generate one heuristically
            outline = generate_heuristic_outline(doc)

        # Construct the final JSON
        output_data = {"title": title, "outline": outline}
        
        doc.close()

        # Save the output JSON file
        output_filename = OUTPUT_DIR / f"{pdf_path.stem}.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"Successfully generated {output_filename.name}")

    except Exception as e:
        print(f"FATAL ERROR processing {pdf_path.name}: {e}")

def main():
    """Main function to find and process all PDF files."""
    print(f"Starting PDF processing... (Running {'in Docker' if IS_DOCKER else 'Locally'})")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {INPUT_DIR}.")
        return

    for pdf_file in pdf_files:
        process_pdf_file(pdf_file)

    print("All PDF files processed.")

if __name__ == "__main__":
    main()