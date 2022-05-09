# Nutrition Facts

NutritionFacts is a website developed in Flask that is similar to other calorie-tracking websites such as MyFitnessPal.

This site allows users to upload images of the nutrition fact labels on products along with an inputted name. It utilizes Tesseract OCR to collect relevant data
from the image such as the calories, fat, carbohydrates, and protein for a serving. It then stores the data in a MySQL database.

Users can search for products that others have submitted and see the nutrition facts of that product.

## Usage

See it in action [here](https://nutri-fact.herokuapp.com/)

## Installation

* Clone the repo
* Uncomment environment variables in the Dockerfile and fill them in as appropriate
* Build and run the Docker image