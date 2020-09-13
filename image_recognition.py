from PIL import Image
import pytesseract
import cv2
import os
import config


def get_text(imagepath, preprocess):

    # Set path for Tesseract
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH

    # Load image and convert to grayscale
    image = cv2.imread(imagepath)

    image = image_resize(image, 2048, 2048)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if preprocess == "thresh":
        th, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    # Write grayscale image to disk

    filename = "{}.png".format(os.getpid())
    path = config.UPLOAD_FOLDER
    cv2.imwrite(os.path.join(path, filename), gray)
    
    # Load the image, get the text, then delete temp image
    image = Image.open(os.path.join(path, filename))

    text = pytesseract.image_to_string(image)


    # DEBUGGING #

    #cv2.imshow("Image", image)
    #cv2.imshow("Output", gray)
    cv2.waitKey(0)
    return text


def image_resize(img, max_width, max_height):
    height, width = img.shape[:2]

    # only shrink if img is bigger than required
    if max_height < height or max_width < width:
        # get scaling factor
        scaling_factor = max_height / float(height)
        if max_width / float(width) < scaling_factor:
            scaling_factor = max_width / float(width)
        # resize image
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return img
