pipeline {
    agent any

    environment {
        PYTHON_PATH = '.venv/Scripts/python.exe'
        PYTEST_PATH = '.venv/Scripts/pytest.exe'
        GRID_URL = 'http://localhost:4444/wd/hub'
    }

    stages {
        stage('Clean Old Data') {
            steps {
                echo 'Step 1: Cleaning old data...'
                sh '''
                    rm -rf allure-results-chrome
                    rm -rf allure-results-firefox
                    rm -rf allure-results-edge
                    rm -rf report-chrome
                    rm -rf report-firefox
                    rm -rf report-edge
                '''
                echo 'Cleaning complete.'
            }
        }

        stage('Run Parallel Grid Tests') {
            parallel {
                stage('Chrome Tests') {
                    steps {
                        echo 'Running Chrome tests...'
                        sh '${PYTEST_PATH} --executor=grid --browser=chrome --alluredir=allure-results-chrome -v'
                    }
                }

                stage('Firefox Tests') {
                    steps {
                        echo 'Running Firefox tests...'
                        sh '${PYTEST_PATH} --executor=grid --browser=firefox --alluredir=allure-results-firefox -v'
                    }
                }

                stage('Edge Tests') {
                    steps {
                        echo 'Running Edge tests...'
                        sh '${PYTEST_PATH} --executor=grid --browser=edge --alluredir=allure-results-edge -v'
                    }
                }
            }
        }

        stage('Generate Reports') {
            steps {
                echo 'Step 3: Generating Reports...'

                script {
                    // Generate Chrome report
                    sh '''
                        if [ -d "allure-results-chrome" ]; then
                            echo "Generating Chrome report..."
                            allure generate allure-results-chrome -o ./report-chrome --clean
                            echo "Chrome report generated successfully!"
                        else
                            echo "WARNING: allure-results-chrome not found!"
                        fi
                    '''

                    // Generate Firefox report
                    sh '''
                        if [ -d "allure-results-firefox" ]; then
                            echo "Generating Firefox report..."
                            allure generate allure-results-firefox -o ./report-firefox --clean
                            echo "Firefox report generated successfully!"
                        else
                            echo "WARNING: allure-results-firefox not found!"
                        fi
                    '''

                    // Generate Edge report
                    sh '''
                        if [ -d "allure-results-edge" ]; then
                            echo "Generating Edge report..."
                            allure generate allure-results-edge -o ./report-edge --clean
                            echo "Edge report generated successfully!"
                        else
                            echo "WARNING: allure-results-edge not found!"
                        fi
                    '''
                }

                echo 'Reports generated in separate directories:'
                echo '  Chrome: report-chrome'
                echo '  Firefox: report-firefox'
                echo '  Edge: report-edge'
            }
        }

        stage('Publish Allure Reports') {
            steps {
                echo 'Publishing Allure reports...'
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results-chrome'], [path: 'allure-results-firefox'], [path: 'allure-results-edge']]
                ])
            }
        }
    }

    post {
        always {
            echo 'Grid execution completed!'
            archiveArtifacts artifacts: 'report-*/**', allowEmptyArchive: true
        }

        success {
            echo 'All tests passed successfully!'
        }

        failure {
            echo 'Some tests failed. Please check the reports.'
        }
    }
}
