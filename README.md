# scraping-tutorial
# Project Setup Instructions

This document outlines the steps to set up the environment for the web scraping project.

## Setting Up the Project

### 1. Clone the Project Repository
Clone the project repository to your local machine 
```bash
git clone https://github.com/Ellie-Brakoniecki/scraping-tutorial.git
cd scraping-tutorial
```
### 2. Create a Virtual Environment
Create a Python virtual environment in your project directory:
```bash
python -m venv env
```

Activate the virtual environment:
```bash
.\env\Scripts\activate
```

### 3. Install python packages
Install the required Python packages using the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 4. Setting up Chromedriver
1. Download win32 chromedriver here https://googlechromelabs.github.io/chrome-for-testing/. (Same number as your version of chrome in the DAP)
2. Place the downloaded chromedriver.exe file inside the chromedriver folder.


### 5. Running the scraping script
```bash
python scraper.py
```
