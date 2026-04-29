# ==========================================
# Script: run_grid.ps1
# ==========================================
# Grid Mode: Parallel execution on Chrome, Firefox, Edge
# Each browser has independent test results and report directories
# ==========================================

# 1. Define the path to your pytest inside the virtual environment
$PytestPath = Join-Path -Path $PSScriptRoot -ChildPath '.\.venv\Scripts\pytest.exe'

# Define the project root directory
$ProjectRoot = $PSScriptRoot

# Check if pytest exists
if (-not (Test-Path $PytestPath)) {
    Write-Host "ERROR: Cannot find pytest at $PytestPath" -ForegroundColor Red
    Write-Host "Please check if your virtual environment folder is named '.venv'" -ForegroundColor Red
    exit
}

# 2. Clean old data for Grid mode
Write-Host "Step 1: Cleaning old data..." -ForegroundColor Cyan
Remove-Item -Recurse -Force allure-results-chrome -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force allure-results-firefox -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force allure-results-edge -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force report-chrome -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force report-firefox -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force report-edge -ErrorAction SilentlyContinue
Write-Host "Cleaning complete." -ForegroundColor Green

# 3. Run parallel Grid tests
Write-Host " "
Write-Host "Step 2: Starting Parallel Grid Tests..." -ForegroundColor Cyan

# Chrome Job
$jobChrome = Start-Job -ScriptBlock {
    param($path, $projectRoot)
    Set-Location -Path $projectRoot
    & $path --executor=grid --browser=chrome --alluredir=allure-results-chrome -n 3 -v
} -ArgumentList $PytestPath, $ProjectRoot

# Firefox Job
$jobFirefox = Start-Job -ScriptBlock {
    param($path, $projectRoot)
    Set-Location -Path $projectRoot
    & $path --executor=grid --browser=firefox --alluredir=allure-results-firefox -n 3 -v
} -ArgumentList $PytestPath, $ProjectRoot

# Edge Job
$jobEdge = Start-Job -ScriptBlock {
    param($path, $projectRoot)
    Set-Location -Path $projectRoot
    & $path --executor=grid --browser=edge --alluredir=allure-results-edge -n 3 -v
} -ArgumentList $PytestPath, $ProjectRoot

Write-Host "All browsers are running. Waiting..." -ForegroundColor Yellow
Wait-Job $jobChrome, $jobFirefox, $jobEdge

Write-Host " "
Write-Host "All tests finished." -ForegroundColor Green

# Display job outputs for debugging
$jobs = $jobChrome, $jobFirefox, $jobEdge
foreach ($job in $jobs) {
    $output = Receive-Job -Job $job
    if ($output) {
        Write-Host "--- Output for $($job.Name) ---"
        $output
    }
}

# 4. Generate separate reports for each browser
Write-Host " "
Write-Host "Step 3: Generating Reports..." -ForegroundColor Cyan

# Generate Chrome report
if (Test-Path allure-results-chrome) {
    Write-Host "Generating Chrome report..." -ForegroundColor Green
    allure generate allure-results-chrome -o ./report-chrome --clean
    Write-Host "Chrome report generated successfully!" -ForegroundColor Green
} else {
    Write-Host "WARNING: allure-results-chrome not found!" -ForegroundColor Yellow
}

# Generate Firefox report
if (Test-Path allure-results-firefox) {
    Write-Host "Generating Firefox report..." -ForegroundColor Green
    allure generate allure-results-firefox -o ./report-firefox --clean
    Write-Host "Firefox report generated successfully!" -ForegroundColor Green
} else {
    Write-Host "WARNING: allure-results-firefox not found!" -ForegroundColor Yellow
}

# Generate Edge report
if (Test-Path allure-results-edge) {
    Write-Host "Generating Edge report..." -ForegroundColor Green
    allure generate allure-results-edge -o ./report-edge --clean
    Write-Host "Edge report generated successfully!" -ForegroundColor Green
} else {
    Write-Host "WARNING: allure-results-edge not found!" -ForegroundColor Yellow
}

Write-Host " "
Write-Host "Reports generated in separate directories:"
Write-Host "  Chrome: report-chrome"
Write-Host "  Firefox: report-firefox"
Write-Host "  Edge: report-edge"
Write-Host " "
Write-Host "To open reports, use:"
Write-Host "  allure open ./report-chrome"
Write-Host "  allure open ./report-firefox"
Write-Host "  allure open ./report-edge"

Write-Host " "
Write-Host "Grid execution completed!" -ForegroundColor Green