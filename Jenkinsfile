pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 60, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Clean Workspace') {
            steps {
                echo 'Cleaning old results...'
                // Windows command to delete folders
                bat 'if exist allure-results-* rd /s /q allure-results-*'
                bat 'if exist report rd /s /q report'
            }
        }

        stage('Setup Python') {
            steps {
                echo 'Installing dependencies...'
                // Create venv and install requirements
                bat '''
                    python -m venv .venv
                    call .venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Parallel Tests') {
            parallel {
                stage('Chrome') {
                    steps {
                        echo 'Running Chrome tests...'
                        // Run pytest directly using the venv path
                        bat '.venv\\Scripts\\pytest.exe --executor=grid --browser=chrome --alluredir=allure-results-chrome -v --color=no'
                    }
                }
                stage('Firefox') {
                    steps {
                        echo 'Running Firefox tests...'
                        bat '.venv\\Scripts\\pytest.exe --executor=grid --browser=firefox --alluredir=allure-results-firefox -v --color=no'
                    }
                }
                stage('Edge') {
                    steps {
                        echo 'Running Edge tests...'
                        bat '.venv\\Scripts\\pytest.exe --executor=grid --browser=edge --alluredir=allure-results-edge -v --color=no'
                    }
                }
            }
        }

        stage('Generate Report') {
            steps {
                echo 'Generating Allure report...'
                // Ensure Allure is installed on your Windows machine
                bat 'allure generate allure-results-chrome allure-results-firefox allure-results-edge -o report --clean'
            }
            post {
                always {
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'report',
                        reportFiles: 'index.html',
                        reportName: 'Allure Report'
                    ])
                }
            }
        }
    }
}
