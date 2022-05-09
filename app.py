import image_recognition
from nutrition_facts import process_text
import os
import database
import config
from flask import render_template, url_for
from flask import flash, request, redirect
from flask import Flask
from werkzeug.utils import secure_filename
from product import Product
from image import s3_upload_file
import boto3
from botocore.client import Config
from werkzeug.exceptions import RequestEntityTooLarge

import uuid

app = Flask(__name__)

app.debug = False

app.config['MAX_CONTENT_LENGTH'] = int(config.MAX_CONTENT_LENGTH)

BUCKET = os.environ['S3_BUCKET']

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__) + "/" + config.UPLOAD_FOLDER)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

app.config['SQLALCHEMY_POOL_RECYCLE'] = 90

db_handler = database.DatabaseHandler(app)


@app.route('/favicon.ico')
def icon():
    return redirect(url_for('static', filename='favicon.ico'), code=302)


# Determines if a file's extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route("/")
def start():
    return render_template('index.html')


@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/facts', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        print("Test")
        product = request.args.get('product_name')
        responses = db_handler.get_nutrition_db(str(product))
        products = []
        for response in responses:
            temp_prod = Product(response.product_name, response.file_name)
            temp_prod.facts['Calories'] = response.calories
            temp_prod.facts['Fat'] = response.fat
            temp_prod.facts['Carbohydrates'] = response.carbohydrates
            temp_prod.facts['Protein'] = response.protein

            products.append(temp_prod)

        result = ""
        for prod in products:
            result = result + str(prod) + "\n"

        print("BEFORE S3")

        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                          aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                          config=Config(signature_version='s3v4'),
                          region_name='us-east-2')

        print("FILENAME: " + response.file_name)

        url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': response.file_name},
                                        ExpiresIn=100)

        print("URL: " + url)

        return render_template('searchlist.html', data=products, resource=url)
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
                s3_upload_file(os.path.join(app.config['UPLOAD_FOLDER'], new_name), BUCKET, new_name)

                product = Product(new_name, os.path.join(app.config['UPLOAD_FOLDER'], new_name))

                text = image_recognition.get_text(product.img_path, config.PREPROCESSOR)

                if text is None or text == '':
                    os.remove(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], new_name)))
                    return render_template('error.html', error="Unable to process the nutrition facts!")

                product.facts = process_text(text)

                facts = product.facts

                # Add new image to database

                n_facts = database.product_data(file_name=product.name, product_name=request.form['product_name'],
                                                calories=int(facts['Calories']), fat=int(facts['Fat']),
                                                carbohydrates=int(facts['Carbohydrates']), protein=int(facts['Protein']))

                db_handler.add_model(n_facts)

                s3 = boto3.client('s3',
                                  aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                                  aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                                  config=Config(signature_version='s3v4'),
                                  region_name='us-east-2')

                url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': new_name},
                                                ExpiresIn=100)

                return render_template('results.html', message=facts, resource=url,
                                       productName=request.form['product_name'])
            else:
                return render_template('error.html', error="File already exists")


@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    return 'File Too Large', 413


@app.route('/download/<resource>')
def download_image(resource):
    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                      aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                      config=Config(signature_version='s3v4'),
                      region_name='us-east-2')

    url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': resource}, ExpiresIn=100)
    return redirect(url, code=302)


if __name__ == "__main__":
    # Generate session key
    app.secret_key = os.urandom(24)

    app.run()
