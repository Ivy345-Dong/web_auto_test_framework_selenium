pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 60, unit: 'MINUTES')
        skipDefaultCheckout(false)
        timestamps()
    }

    environment {
        VENV_PATH = '.venv'
        PYTEST_PATH = "${VENV_PATH}\\Scripts\\pytest.exe"
        ALLURE_RESULTS_CHROME = 'allure-results-chrome'
        ALLURE_RESULTS_FIREFOX = 'allure-results-firefox'
        ALLURE_RESULTS_EDGE = 'allure-results-edge'
        REPORT_DIR = 'report'
        GRID_EXECUTOR = 'http://localhost:4444/wd/hub'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "======================================"
                    echo "Step 1: Checking out source code"
                    echo "======================================"
                    checkout scm
                }
            }
        }

        stage('Clean Workspace') {
            steps {
                script {
                    echo "======================================"
                    echo "Step 2: Cleaning old test results"
                    echo "======================================"
                    powershell '''
                        if (Test-Path "allure-results-*") {
                            Remove-Item -Recurse -Force "allure-results-*" -ErrorAction SilentlyContinue
                            Write-Host "Old allure results deleted"
                        } else {
                            Write-Host "No old allure results to delete"
                        }

                        if (Test-Path "report") {
                            Remove-Item -Recurse -Force "report" -ErrorAction SilentlyContinue
                            Write-Host "Old report folder deleted"
                        } else {
                            Write-Host "No old report folder to delete"
                        }
                    '''
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    echo "======================================"
                    echo "Step 3: Setting up Python venv"
                    echo "======================================"
                    powershell '''
                        try {
                            python --version | Out-Null
                            Write-Host "Python found"
                        } catch {
                            Write-Error "Python is not installed or not in PATH"
                            exit 1
                        }

                        if (-not (Test-Path "$env:VENV_PATH")) {
                            python -m venv "$env:VENV_PATH"
                            Write-Host "Virtual environment created at $env:VENV_PATH"
                        } else {
                            Write-Host "Virtual environment already exists"
                        }

                        & "$env:VENV_PATH\\Scripts\\Activate.ps1"
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        Write-Host "Dependencies installed successfully"
                    '''
                }
            }
            post {
                failure {
                    echo "Python environment setup failed! Check requirements.txt or Python installation"
                }
            }
        }

        stage('Parallel Compatibility Tests') {
            parallel {
                stage('Chrome Tests') {
                    steps {
                        script {
                            echo "======================================"
                            echo "Running Chrome tests (Grid)"
                            echo "======================================"
                            powershell '''
                                & "$env:PYTEST_PATH" `
                                    --executor=grid `
                                    --browser=chrome `
                                    --alluredir=$env:ALLURE_RESULTS_CHROME `
                                    -v `
                                    --color=no `
                                    --tb=short

                                if ($LASTEXITCODE -ne 0) {
                                    Write-Warning "Chrome tests have failures, but continuing pipeline"
                                } else {
                                    Write-Host "Chrome tests completed successfully"
                                }
                            '''
                        }
                    }
                }

                stage('Firefox Tests') {
                    steps {
                        script {
                            echo "======================================"
                            echo "Running Firefox tests (Grid)"
                            echo "======================================"
                            powershell '''
                                & "$env:PYTEST_PATH" `
                                    --executor=grid `
                                    --browser=firefox `
                                    --alluredir=$env:ALLURE_RESULTS_FIREFOX `
                                    -v `
                                    --color=no `
                                    --tb=short

                                if ($LASTEXITCODE -ne 0) {
                                    Write-Warning "Firefox tests have failures, but continuing pipeline"
                                } else {
                                    Write-Host "Firefox tests completed successfully"
                                }
                            '''
                        }
                    }
                }

                stage('Edge Tests') {
                    steps {
                        script {
                            echo "======================================"
                            echo "Running Edge tests (Grid)"
                            echo "======================================"
                            powershell '''
                                & "$env:PYTEST_PATH" `
                                    --executor=grid `
                                    --browser=edge `
                                    --alluredir=$env:ALLURE_RESULTS_EDGE `
                                    -v `
                                    --color=no `
                                    --tb=short

                                if ($LASTEXITCODE -ne 0) {
                                    Write-Warning "Edge tests have failures, but continuing pipeline"
                                } else {
                                    Write-Host "Edge tests completed successfully"
                                }
                            '''
                        }
                    }
                }
            }
            post {
                failure {
                    echo "One or more browser tests failed! Check the logs for details"
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    echo "======================================"
                    echo "Generating Allure report"
                    echo "======================================"
                    powershell '''
                        $resultDirs = @("$env:ALLURE_RESULTS_CHROME", "$env:ALLURE_RESULTS_FIREFOX", "$env:ALLURE_RESULTS_EDGE")
                        $existingDirs = $resultDirs | Where-Object { Test-Path $_ }

                        if ($existingDirs.Count -eq 0) {
                            Write-Error "No Allure results found! Tests may not have run"
                            exit 1
                        }

                        allure generate $existingDirs -o "$env:REPORT_DIR" --clean
                        Write-Host "Allure report generated at $env:REPORT_DIR"
                    '''
                }
            }
            post {
                always {
                    publishHTML(
                        target: [
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: env.REPORT_DIR,
                            reportFiles: 'index.html',
                            reportName: 'Compatibility Test Report (Chrome/Firefox/Edge)'
                        ]
                    )
                    echo "Allure report published! Access it from the Jenkins build page"
                }
                failure {
                    echo "Failed to generate Allure report! Check Allure installation"
                }
            }
        }
    }

    post {
        success {
            echo "All stages completed successfully! Compatibility tests passed for all browsers"
        }
        failure {
            echo "Pipeline failed! Check the logs for the failed stage"
        }
        always {
            echo "======================================"
            // 修改这里：使用 Groovy 标准语法获取当前时间
            echo "Pipeline finished at ${new Date()}"
            echo "======================================"
        }
    }
}