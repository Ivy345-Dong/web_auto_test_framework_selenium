pipeline {
    agent any

    environment {
        // Python 虚拟环境路径
        VENV_PATH = '.venv'

        // Selenium Grid 地址
        SELENIUM_GRID_URL = 'http://localhost:4444/wd/hub'
    }

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

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    # 检查 Python 版本
                    python3 --version

                    # 创建虚拟环境（如果不存在）
                    if [ ! -d "$VENV_PATH" ]; then
                        echo "Creating virtual environment..."
                        python3 -m venv $VENV_PATH
                    fi

                    # 激活虚拟环境并升级 pip
                    echo "Activating virtual environment..."
                    source $VENV_PATH/bin/activate
                    pip install --upgrade pip

                    # 安装项目依赖（关键步骤！）
                    echo "Installing dependencies from requirements.txt..."
                    pip install -r requirements.txt

                    # 验证安装
                    echo "Verifying installations..."
                    pytest --version
                    allure --version
                '''
            }
        }

        stage('Verify Selenium Grid') {
            steps {
                echo 'Checking Selenium Grid availability...'
                sh '''
                    curl -f $SELENIUM_GRID_URL/status || {
                        echo "ERROR: Selenium Grid is not accessible"
                        exit 1
                    }
                    echo "Selenium Grid is ready!"
                '''
            }
        }

        stage('Clean Previous Results') {
            steps {
                echo 'Cleaning previous test results...'
                sh '''
                    rm -rf allure-results-*
                    rm -rf report
                '''
            }
        }

        stage('Parallel Tests') {
            parallel {
                stage('Chrome') {
                    steps {
                        echo 'Running Chrome tests...'
                        sh '''
                            source $VENV_PATH/bin/activate
                            pytest --executor=grid --browser=chrome \
                                --alluredir=allure-results-chrome \
                                --color=no -v scripts/
                        '''
                    }
                }

                stage('Firefox') {
                    steps {
                        echo 'Running Firefox tests...'
                        sh '''
                            source $VENV_PATH/bin/activate
                            pytest --executor=grid --browser=firefox \
                                --alluredir=allure-results-firefox \
                                --color=no -v scripts/
                        '''
                    }
                }

                stage('Edge') {
                    steps {
                        echo 'Running Edge tests...'
                        sh '''
                            source $VENV_PATH/bin/activate
                            pytest --executor=grid --browser=edge \
                                --alluredir=allure-results-edge \
                                --color=no -v scripts/
                        '''
                    }
                }
            }
        }

        stage('Generate Report') {
            steps {
                echo 'Generating Allure report...'
                sh '''
                    allure generate \
                        allure-results-chrome \
                        allure-results-firefox \
                        allure-results-edge \
                        -o ./report --clean
                '''
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
                    archiveArtifacts artifacts: 'report/**/*', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Tests failed! Check Allure report.'
        }
        always {
            echo 'Pipeline completed.'
        }
    }
}
