import pytesseract
import cv2
import easyocr
import os

reader = easyocr.Reader(['en'])  # Initialize once globally

from PIL import Image, UnidentifiedImageError

def extract_text_from_image(file_path: str) -> str:
    try:
        with Image.open(file_path) as img:
            return pytesseract.image_to_string(img)
    except UnidentifiedImageError:
        raise ValueError(f"File at {file_path} is not a valid image.")
