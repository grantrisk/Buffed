# Buffed - Meal Planning App
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<div align="center">
</div>

## About Buffed
[![Buffed Screen Shot][buffed-product-screenshot]](https://buffed.herokuapp.com/)
<br>
Our application __**BUFFED**__ will use web technologies to allow the average person to be able to look up recommended meals throughout the day.  This will be based on the calorie limit as well as macronutrient proportions they wish to achieve. This application will be targeting individuals looking to improve their health through nutrition and dieting.  It will provide a user-friendly interface for those looking to improve their health and physique, whether they are at home or on the run.

## Getting Started

1. Install Pycharm
2. Clone the repo onto your machine
   ```sh
   git clone https://github.com/UNCW-CSC-450/team-project-team-1
   ```
3. Open "team-project-team-1" folder, which was cloned from repo, in Pycharm
4. Create or add Virtual Environment into your project folder inside IDE (Make sure python version 3.9 or less is being used for venv)
5. [Install all dependencies](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html) from requirements.txt into your virtual environment 
6. Open Run Configurations and add the required environment variables
7. If you need the API key from firebase, go to the databse project in Firebase, click "Project setting", and copy the key next to "Web API Key"
8. Run app.py through IDE
9. Open website on http://127.0.0.1:5000 (local host) in chrome browser

## Buffed Environment Variables

| Environment                      | Default                | Description                             |
| -------------------------------- | ---------------------- | --------------------------------------- |
| FIREBASE_WEB_API_KEY=<key_id>    | None                   | The Web API Key From Firebase           |

## Required Technology Downloads

* Python 3.9 - [Python Download Page](https://www.python.org/downloads/) | [Python Installation Instructions](https://phoenixnap.com/kb/how-to-install-python-3-windows)
* Pycharm - [Pycharm Download Page](https://www.jetbrains.com/pycharm/download/#section=mac) | [Pycharm Installation Instructions](https://www.jetbrains.com/help/pycharm/installation-guide.html)

## Running System Tests

1. Open Buffed project and run app.py 
2. Open Google Chrome and install Selenium IDE into chrome extensions
3. Open Selenium IDE
4. Click "Open an existing project"
5. Go into the Buffed directory and find the file named "Buffed.side" inside "test_selenium" directory
6. Click on one of the tests and clikc "Run current test" or click "Run all tests" to run the test suite 


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/grantrisk/Buffed.svg?style=for-the-badge
[contributors-url]: https://github.com/grantrisk/Buffed/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/grantrisk/Buffed.svg?style=for-the-badge
[forks-url]: https://github.com/grantrisk/Buffed/network/members
[stars-shield]: https://img.shields.io/github/stars/grantrisk/Buffed.svg?style=for-the-badge
[stars-url]: https://github.com/grantrisk/Buffed/stargazers
[issues-shield]: https://img.shields.io/github/issues/grantrisk/Buffed.svg?style=for-the-badge
[issues-url]: https://github.com/grantrisk/Buffed/issues
[buffed-product-screenshot]: img/buffed-dashboard-screenshot.png
