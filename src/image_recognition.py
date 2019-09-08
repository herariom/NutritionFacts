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

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    # Write grayscale image to disk

    filename = "{}.png".format(os.getpid())
    path = "C:\\Users\\Logan\\PycharmProjects\\PySelenium\\src\\static"
    cv2.imwrite(os.path.join(path, filename), gray)

    # Load the image, get the text, then delete temp image

    text = pytesseract.image_to_string(Image.open(os.path.join(path, filename)))

    os.remove(os.path.join(path, filename))


    # DEBUGGING #

    #cv2.imshow("Image", image)
    #cv2.imshow("Output", gray)
    cv2.waitKey(0)
    return text


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
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