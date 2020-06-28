# Nutrition Facts

NutritionFacts is a website developed in Flask that is similar to other calorie-tracking websites such as MyFitnessPal.

This site allows users to upload images of the nutrition fact labels on products along with an inputted name. It utilizes Tesseract OCR to collect relevant data
from the image such as the calories, fat, carbohydrates, and protein for a serving. It then stores the data in a MySQL database.

Users can search for products that others have submitted and see the nutrition facts of that product.

## Usage

I currently do not have a public server for this project as it is a work-in-progress. You can see usage examples on my [website](https://herariom.github.io)

## Installation

Note: these instructions are a work in progress. I am currently making it more portable and easier to install

* Clone the project to your PC

* Install the required packages with the command `$ pip install -r requirements.txt`

* Create a database and table using the `database.sql` file in the configuration folder

* Configure the `config.py` file to your environment

* Run `main.py`!
