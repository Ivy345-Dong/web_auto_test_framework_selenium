# run_local.ps1 - 本地运行脚本（单浏览器）

$PytestPath = Join-Path -Path $PSScriptRoot -ChildPath '.\.venv\Scripts\pytest.exe'
$ProjectRoot = $PSScriptRoot

if (-not (Test-Path $PytestPath)) {
    Write-Host "ERROR: Cannot find pytest at $PytestPath" -ForegroundColor Red
    exit
}

Write-Host "Running local tests..." -ForegroundColor Cyan

# Clean old data
Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force report -ErrorAction SilentlyContinue

# Run tests with default allure-results directory
& $PytestPath --executor=local --browser=chrome --alluredir=allure-results -v

# Generate report
Write-Host "Generating report..." -ForegroundColor Cyan
allure generate allure-results -o ./report --clean
allure open ./report
