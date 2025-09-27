import cv2
import pytesseract
from pytesseract import Output
import numpy as np
from PIL import Image

# If needed on Windows, uncomment and set the tesseract path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def compare_with_ocr(img1: Image.Image, img2: Image.Image) -> np.ndarray:
    """
    Compare two screenshots using OCR and highlight changes in the second image.
    
    Args:
        img1: PIL.Image (before screenshot)
        img2: PIL.Image (after screenshot)

    Returns:
        np.ndarray (RGB image with differences highlighted)
    """
    # Convert PIL to OpenCV format
    img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)

    # Extract text + bounding boxes
    data1 = pytesseract.image_to_data(img1, output_type=Output.DICT)
    data2 = pytesseract.image_to_data(img2, output_type=Output.DICT)

    text_boxes1 = {
        data1['text'][i]: (data1['left'][i], data1['top'][i], data1['width'][i], data1['height'][i])
        for i in range(len(data1['text'])) if data1['text'][i].strip()
    }

    text_boxes2 = {
        data2['text'][i]: (data2['left'][i], data2['top'][i], data2['width'][i], data2['height'][i])
        for i in range(len(data2['text'])) if data2['text'][i].strip()
    }

    # Compare texts – highlight only differences
    for text, box2 in text_boxes2.items():
        if text not in text_boxes1:  # new or changed text
            x, y, w, h = box2
            cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Convert back to RGB for Streamlit display
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    return img2_rgb
