# Test script for Challenge 1a PDF Processing Solution (Windows PowerShell)
# Usage: .\test_challenge_1a.ps1

Write-Host "=== Testing Challenge 1a PDF Processing Solution ===" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "process_pdfs.py") -or -not (Test-Path "Dockerfile")) {
    Write-Host "Error: Please run this script from the Challenge_1a directory" -ForegroundColor Red
    exit 1
}

# Build the Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build --platform linux/amd64 -t pdf-processor-challenge-1a .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "Docker image built successfully!" -ForegroundColor Green

# Create test output directory
if (-not (Test-Path "test_output")) {
    New-Item -ItemType Directory -Path "test_output" | Out-Null
}

# Test with sample dataset
Write-Host "Testing with sample dataset..." -ForegroundColor Yellow
docker run --rm `
    -v "${PWD}/sample_dataset/pdfs:/app/input:ro" `
    -v "${PWD}/test_output:/app/output" `
    --network none `
    pdf-processor-challenge-1a

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker run failed" -ForegroundColor Red
    exit 1
}

Write-Host "Testing completed!" -ForegroundColor Green

# Verify output files
Write-Host "Verifying output files..." -ForegroundColor Yellow
if (Test-Path "test_output") {
    Write-Host "Output files generated:"
    Get-ChildItem "test_output" | Format-Table Name, Length, LastWriteTime
    
    # Check if JSON files are valid
    Get-ChildItem "test_output/*.json" | ForEach-Object {
        Write-Host "Validating $($_.Name)..." -ForegroundColor Cyan
        try {
            Get-Content $_.FullName | ConvertFrom-Json | Out-Null
            Write-Host "✓ $($_.Name) is valid JSON" -ForegroundColor Green
        }
        catch {
            Write-Host "✗ $($_.Name) is invalid JSON" -ForegroundColor Red
        }
    }
}
else {
    Write-Host "Error: No output directory found" -ForegroundColor Red
    exit 1
}

Write-Host "=== Test completed successfully! ===" -ForegroundColor Green
