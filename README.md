# Web Automation Test Framework with Selenium

A comprehensive web automation testing framework built with Selenium WebDriver and pytest, designed for cross-browser compatibility testing and continuous integration.

## Features

- 🚀 **Cross-Browser Testing**: Support for Chrome, Firefox, and Edge browsers
- 🔄 **Local & Grid Execution**: Run tests locally or on Selenium Grid
- 📊 **Allure Reports**: Beautiful and detailed test reports with Allure
- ⚡ **Parallel Testing**: Execute tests in parallel for faster execution
- 🎯 **Page Object Model**: Clean and maintainable test architecture
- 📝 **Data-Driven Testing**: JSON-based test data management
- 🔧 **Headless Mode**: Run tests without UI for CI/CD environments
- 📱 **Responsive Design**: Test web applications across different browsers
- 🎨 **Detailed Logging**: Comprehensive logging for debugging
- 🔄 **Test Retry**: Automatic retry mechanism for flaky tests

## Project Structure

```
saucedemo/
├── base/                    # Base classes and utilities
│   └── base.py             # Base page and handle classes
├── page/                    # Page Object Model
│   ├── cart_page.py         # Cart page object
│   ├── home_page.py         # Home page object
│   ├── login_page.py        # Login page object
│   └── swag_labs.py        # Swag Labs page object
├── scripts/                 # Test scripts
│   ├── test_login.py        # Login test cases
│   └── test_shopping.py    # Shopping test cases
├── utility/                 # Utility functions
│   ├── com.py              # Common utilities
│   ├── data_reader.py      # Data reading utilities
│   └── driver_factory.py  # WebDriver factory
├── data/                    # Test data files
│   ├── test_add_to_cart.json
│   ├── test_login.json
│   └── test_login_failed.json
├── conftest.py             # Pytest configuration
├── pytest.ini              # Pytest settings
├── environment.yaml         # Environment configuration
├── run_local.ps1           # Local execution script
├── run_grid.ps1            # Grid execution script
├── Jenkinsfile             # Jenkins CI/CD pipeline
└── requirements.txt        # Python dependencies
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Allure Command Line (for test reports)
- Selenium Grid (for grid execution, optional)
- Browsers: Chrome, Firefox, Edge

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ivy345-Dong/web_auto_test_framework_selenium.git
cd web_auto_test_framework_selenium
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Allure Command Line

```bash
# On Windows (using Scoop)
scoop install allure

# On macOS (using Homebrew)
brew install allure

# On Linux
wget https://github.com/allure-framework/allure2/releases/download/2.15.3/allure-2.15.3.tgz
sudo tar -zxvf allure-2.15.3.tgz -C /opt/
sudo ln -s /opt/allure-2.15.3/bin/allure /usr/bin/allure
```

## Configuration

### Environment Configuration

Edit `environment.yaml` to configure test URL:

```yaml
web:
  url: "https://www.saucedemo.com/"
```

## Usage

### Local Execution

Run tests locally with a single browser:

```bash
# Run with default browser (Chrome)
.\run_local.ps1

# Run with specific browser
.\run_local.ps1 -Browser firefox
.\run_local.ps1 -Browser edge
```

### Grid Execution

Run tests in parallel across multiple browsers:

```bash
# Run on Selenium Grid with Chrome, Firefox, Edge
.\run_grid.ps1
```

### Manual Execution

Run specific tests manually:

```bash
# Run all tests
pytest --executor=local --browser=chrome -v

# Run specific test file
pytest scripts/test_login.py --executor=local --browser=firefox -v

# Run with headless mode
pytest --executor=local --browser=chrome --headless -v
```

## Test Reports

### Generate Allure Reports

```bash
# Generate report from test results
allure generate allure-results -o report --clean

# Open report in browser
allure open report

# Generate report for Grid execution
allure generate allure-results-chrome -o report-chrome --clean
allure generate allure-results-firefox -o report-firefox --clean
allure generate allure-results-edge -o report-edge --clean
```

### Report Features

- **Test Execution Timeline**: Visual timeline of test execution
- **Screenshots**: Automatic screenshots on test failures
- **Logs**: Detailed logs for each test step
- **Browser Information**: Browser version and capabilities
- **Test Parameters**: Parameterized test data display
- **Attachments**: Screenshots and other attachments

## Test Data Management

Test data is stored in JSON format in `data/` directory for data-driven testing. Each test case can be parameterized with multiple data sets from JSON files.

## Selenium Grid Setup

### Using Docker (Recommended)

The easiest way to set up Selenium Grid is using Docker:

```bash
# 1. Create network
docker network create my-grid

# 2. Start Selenium Grid Hub
docker run -d -p 4442-4444:4442-4444 --net my-grid --name selenium-hub selenium/hub:latest

# 3. Start Chrome Node
docker run -d --net my-grid -e SE_EVENT_BUS_HOST=selenium-hub --shm-size="2g" --name node-chrome selenium/node-chrome:latest

# 4. Start Firefox Node
docker run -d --net my-grid -e SE_EVENT_BUS_HOST=selenium-hub --shm-size="2g" --name node-firefox selenium/node-firefox:latest

# 5. Start Edge Node
docker run -d --net my-grid -e SE_EVENT_BUS_HOST=selenium-hub --shm-size="2g" --name node-edge selenium/node-edge:latest
```

### Access Grid UI

After starting the containers, access the Selenium Grid UI at:
```
http://localhost:4444/ui
```

### Using Docker (Recommended)

The easiest way to set up Selenium Grid is using Docker:

```bash
# 1. Create network
docker network create my-grid

# 2. Start Selenium Grid Hub
docker run -d -p 4442-4444:4442-4444 --net my-grid --name selenium-hub selenium/hub:latest

# 3. Start Chrome Node
docker run -d --net my-grid -e SE_EVENT_BUS_HOST=selenium-hub --shm-size="2g" --name node-chrome selenium/node-chrome:latest

# 4. Start Firefox Node
docker run -d --net my-grid -e SE_EVENT_BUS_HOST=selenium-hub --shm-size="2g" --name node-firefox selenium/node-firefox:latest

# 5. Start Edge Node
docker run -d --net my-grid -e SE_EVENT_BUS_HOST=selenium-hub --shm-size="2g" --name node-edge selenium/node-edge:latest
```

### Access Grid UI

After starting the containers, access the Selenium Grid UI at:
```
http://localhost:4444/ui
```



## CI/CD Integration

### Jenkins Pipeline

The project includes a `Jenkinsfile` for automated testing. Simply create a new Pipeline job in Jenkins and configure it to pull from your Git repository. The Jenkinsfile will automatically handle parallel test execution across Chrome, Firefox, and Edge browsers, followed by Allure report generation.

## Technology Stack

- **Language**: Python 3.8+
- **Testing Framework**: pytest
- **Web Automation**: Selenium WebDriver 4.43.0
- **Test Reporting**: Allure
- **Parallel Testing**: pytest-xdist
- **Data Management**: JSON
- **Configuration**: YAML
- **Browser Drivers**: webdriver-manager
- **CI/CD**: Jenkins

## Best Practices

1. **Page Object Model**: Maintain clean separation between test logic and page interactions
2. **Data-Driven Testing**: Use JSON files for test data management
3. **Explicit Waits**: Use WebDriverWait for stable element interaction
4. **Error Handling**: Implement proper exception handling and logging
5. **Parallel Testing**: Leverage pytest-xdist for faster execution
6. **Headless Mode**: Use headless mode for CI/CD environments
7. **Test Isolation**: Ensure tests are independent and isolated
8. **Reporting**: Generate comprehensive reports for analysis

## Troubleshooting

### Common Issues

1. **Browser Driver Not Found**
   - Solution: Use webdriver-manager for automatic driver management

2. **Connection Reset Error**
   - Solution: Reduce parallel worker count or use `--dist=loadfile`

3. **Element Not Found**
   - Solution: Increase timeout or check element locators

4. **Allure Report Not Generated**
   - Solution: Ensure test results directory exists and contains data

### Debug Mode

Run tests with verbose output:

```bash
pytest -vv --tb=long --log-cli-level=DEBUG
```

## Contact

For questions and support, please open an issue on GitHub.

## Acknowledgments

- [Selenium WebDriver](https://www.selenium.dev/)
- [pytest](https://docs.pytest.org/)
- [Allure Report](https://docs.qameta.io/allure/)
- [Swag Labs](https://www.saucedemo.com/) - Demo application for testing

---

**Happy Testing! 🚀**