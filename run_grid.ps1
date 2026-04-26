# ==========================================
# Script: run_parallel_grid_fixed.ps1
# ==========================================

# 1. Define the path to your pytest inside the virtual environment
# Use absolute path to avoid issues with Start-Job
$PytestPath = Join-Path -Path $PSScriptRoot -ChildPath '.\.venv\Scripts\pytest.exe'

# Define the project root directory (where the script is located)
$ProjectRoot = $PSScriptRoot

# Check if pytest exists
if (-not (Test-Path $PytestPath)) {
    Write-Host "ERROR: Cannot find pytest at $PytestPath" -ForegroundColor Red
    Write-Host "Please check if your virtual environment folder is named '.venv'" -ForegroundColor Red
    exit
}

Write-Host "Step 1: Cleaning old data..." -ForegroundColor Cyan
Remove-Item -Recurse -Force allure-results* -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force report -ErrorAction SilentlyContinue
Write-Host "Cleaning complete." -ForegroundColor Green

Write-Host " "
Write-Host "Step 2: Starting Parallel Tests..." -ForegroundColor Cyan

# 2. Run Chrome Job
$jobChrome = Start-Job -ScriptBlock {
    param($path, $projectRoot)
    # Switch to project directory first
    Set-Location -Path $projectRoot
    # & is the 'Call Operator' used to run a command from a path variable
    & $path --executor=grid --browser=chrome --alluredir=allure-results-chrome -v
} -ArgumentList $PytestPath, $ProjectRoot

# 3. Run Firefox Job
$jobFirefox = Start-Job -ScriptBlock {
    param($path, $projectRoot)
    Set-Location -Path $projectRoot
    & $path --executor=grid --browser=firefox --alluredir=allure-results-firefox -v
} -ArgumentList $PytestPath, $ProjectRoot

# 4. Run Edge Job
$jobEdge = Start-Job -ScriptBlock {
    param($path, $projectRoot)
    Set-Location -Path $projectRoot
    & $path --executor=grid --browser=edge --alluredir=allure-results-edge -v
} -ArgumentList $PytestPath, $ProjectRoot

Write-Host "All browsers are running. Waiting..." -ForegroundColor Yellow

# Wait for all jobs to finish
Wait-Job $jobChrome, $jobFirefox, $jobEdge

Write-Host " "
Write-Host "All tests finished." -ForegroundColor Green

# Optional: Display any errors that happened inside the jobs
$jobs = $jobChrome, $jobFirefox, $jobEdge
foreach ($job in $jobs) {
    $output = Receive-Job -Job $job
    if ($output) {
        Write-Host "--- Output for $($job.Name) ---"
        $output
    }
}

# 5. Generate Report
Write-Host " "
Write-Host "Step 3: Generating Report..." -ForegroundColor Cyan

# Verify all result directories exist
$chromeExists = Test-Path allure-results-chrome
$firefoxExists = Test-Path allure-results-firefox
$edgeExists = Test-Path allure-results-edge

Write-Host "Chrome results: $(if($chromeExists){'Found'}else{'Missing'})"
Write-Host "Firefox results: $(if($firefoxExists){'Found'}else{'Missing'})"
Write-Host "Edge results: $(if($edgeExists){'Found'}else{'Missing'})"

if ($chromeExists -and $firefoxExists -and $edgeExists) {
    Write-Host "Merging results from all browsers..." -ForegroundColor Green
    # Use wildcard to include all allure-results directories
    allure generate allure-results-* -o ./report --clean
    Write-Host "Report generated successfully!" -ForegroundColor Green
} else {
    Write-Host "WARNING: Some browser results are missing!" -ForegroundColor Yellow
}

Write-Host "Step 4: Opening Report..." -ForegroundColor Cyan
allure open ./report


