import image_recognition
from nutrition_facts import NutritionFacts
import os
import database
import config
from flask import render_template
from flask import flash, request, redirect
from flask import Flask
from werkzeug.utils import secure_filename
from product import Product
from s3_file import s3_upload_file
import boto3

import uuid

app = Flask(__name__)

app.debug = False

BUCKET = os.environ['S3_BUCKET']

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__) + "/" + config.UPLOAD_FOLDER)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

app.config['SQLALCHEMY_POOL_RECYCLE'] = 90

db_handler = database.DatabaseHandler(app)

# Determines if a file's extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route("/")
def start():
    return render_template('index.html')


@app.route('/facts', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        product = request.args.get('product_name')
        responses = db_handler.get_nutrition_db(str(product))
        products = []
        for response in responses:
            temp_prod = Product(response.product_name, response.file_name)
            temp_prod.facts['Calories'] = response.calories
            temp_prod.facts['fat'] = response.fat
            temp_prod.facts['carbohydrates'] = response.carbohydrates
            temp_prod.facts['protein'] = response.protein

            products.append(temp_prod)

        result = ""
        for prod in products:
            result = result + str(prod) + "\n"
        return render_template('searchlist.html', data=products, resource=request.args.get('product_name'))
    return render_template('error.html', error="Problem finding product")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.referrer)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.referrer)
        if file and allowed_file(secure_filename(file.filename)):
            filename = secure_filename(file.filename)

            if not os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                new_name = str(uuid.uuid4()) + filename[(filename.index('.')):]  # Appends file extension to UUID

                # Check for name collisions to ensure unique filename
                while os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], new_name)):
                    new_name = str(uuid.uuid4()) + filename[(filename.index('.')):]

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_name))

                # Upload file to S3 bucket
                s3_upload_file(os.path.join(app.config['UPLOAD_FOLDER'], new_name), BUCKET)

                product = Product(new_name, os.path.join(app.config['UPLOAD_FOLDER'], new_name))

                text = image_recognition.get_text(product.img_path, config.PREPROCESSOR)

                if text is None or text == '':
                    os.remove(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], new_name)))
                    return render_template('error.html', error="Unable to process the nutrition facts!")

                n = NutritionFacts()

                product.facts = n.process_text(text)

                facts = product.facts

                if facts['Calories'] < 0 or facts['Carbohydrates'] < 0 or facts['Protein'] < 0:
                    os.remove(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], new_name)))
                    return render_template('error.html', error="Unable to correctly parse image data,"
                                                               " please upload a higher quality image")

                # Add new image to database

                n_facts = database.product_data(file_name=product.name, product_name=request.form['product_name'],
                                                calories=int(facts['Calories']), fat=int(facts['Fat']),
                                                carbohydrates=int(facts['Carbohydrates']), protein=int(facts['Protein']))

                db_handler.add_model(n_facts)

                return render_template('results.html', message=facts, imgDirectory=new_name,
                                       productName=request.form['product_name'])
            else:
                return render_template('error.html', error="File already exists")


@app.route('/download/<resource>')
def download_image(resource):
    """ resource: name of the file to download"""
    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                      aws_secret_access_key=os.environ['S3_SECRET_KEY'])

    url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': resource}, ExpiresIn=100)
    return redirect(url, code=302)

if __name__ == "__main__":
    # Generate session key
    app.secret_key = os.urandom(24)

    app.run()




