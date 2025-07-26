# Test script for Challenge 1b Multi-Collection PDF Analysis (Windows PowerShell)
# Usage: .\test_challenge_1b.ps1

Write-Host "=== Testing Challenge 1b Multi-Collection PDF Analysis ===" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "process_collections.py") -or -not (Test-Path "Dockerfile")) {
    Write-Host "Error: Please run this script from the Challenge_1b directory" -ForegroundColor Red
    exit 1
}

# Build the Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build --platform linux/amd64 -t pdf-analyzer-challenge-1b .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "Docker image built successfully!" -ForegroundColor Green

# Test the solution
Write-Host "Running Challenge 1b analysis..." -ForegroundColor Yellow
docker run --rm --network none pdf-analyzer-challenge-1b

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker run failed" -ForegroundColor Red
    exit 1
}

Write-Host "Analysis completed!" -ForegroundColor Green

# Verify output files for each collection
$collections = @("Collection 1", "Collection 2", "Collection 3")

foreach ($collection in $collections) {
    $outputFile = "$collection/challenge1b_output.json"
    
    if (Test-Path $outputFile) {
        Write-Host "✓ $collection output generated" -ForegroundColor Green
        
        # Validate JSON
        try {
            $json = Get-Content $outputFile | ConvertFrom-Json
            Write-Host "  ✓ Valid JSON structure" -ForegroundColor Green
            
            # Check required fields
            if ($json.metadata -and $json.extracted_sections -and $json.subsection_analysis) {
                Write-Host "  ✓ All required fields present" -ForegroundColor Green
                Write-Host "  - Documents processed: $($json.metadata.input_documents.Count)" -ForegroundColor Cyan
                Write-Host "  - Sections extracted: $($json.extracted_sections.Count)" -ForegroundColor Cyan
                Write-Host "  - Subsections analyzed: $($json.subsection_analysis.Count)" -ForegroundColor Cyan
            } else {
                Write-Host "  ✗ Missing required fields" -ForegroundColor Red
            }
        }
        catch {
            Write-Host "  ✗ Invalid JSON format" -ForegroundColor Red
        }
    } else {
        Write-Host "✗ $collection output not found" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host "=== Test completed successfully! ===" -ForegroundColor Green
