from PIL import Image
import pytesseract
import cv2
import os
import config

IMAGE_SIZE = 1024
BINARY_THREHOLD = 180

def get_text(imagepath, preprocess):

    # Set path for Tesseract - Only for debugging
    # pytesseract.pytesseract.tesseract_cmd = ""


    # Load image and convert to grayscale
    image = cv2.imread(imagepath)

    # Scale by the largest factor of the image size
    if image.shape[0] > image.shape[1]:
        image = image_resize(image, height=IMAGE_SIZE)
    else:
        image = image_resize(image, width=IMAGE_SIZE)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    text = ''

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = image[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = text + '\n' + pytesseract.image_to_string(cropped)

    cv2.waitKey(0)
    return text


def image_resize(image, width = None, height = None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
