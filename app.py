import streamlit as st
from PIL import Image
import pdfplumber
import pytesseract
from io import BytesIO
import docx
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text2text-generation", model="Rishi-Bethi/LegalSummerizer")

# Set the path to the tesseract executable if it's not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Rishi-Bethi/LegalSummerizer")
model = AutoModelForSeq2SeqLM.from_pretrained("Rishi-Bethi/LegalSummerizer")

def summarize_text(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=4096, truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=256, min_length=30, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_word(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

st.title("Legal Document Summarization")

option = st.selectbox("Choose an input method", ["Enter text directly", "Upload a PDF", "Upload an image", "Upload a Word document (.docx)"])

if option == "Enter text directly":
    text_input = st.text_area("Enter the text for summarization", height=300)
    if st.button("Summarize Text"):
        if text_input:
            st.write("Summarizing the text...")
            summary = summarize_text(text_input)
            st.write("Summary:")
            st.write(summary)
        else:
            st.error("Please enter some text.")

elif option == "Upload a PDF":
    uploaded_pdf = st.file_uploader("Upload a PDF file", type='pdf')
    if uploaded_pdf is not None:
        st.write("Extracting text from PDF...")
        text = extract_text_from_pdf(uploaded_pdf)
        if text:
            st.write("Summarizing the text...")
            summary = summarize_text(text)
            st.write("Summary:")
            st.write(summary)
        else:
            st.error("Failed to extract text from the PDF.")

elif option == "Upload an image":
    uploaded_image = st.file_uploader("Upload an image file", type=['png', 'jpg', 'jpeg'])
    if uploaded_image is not None:
        st.write("Extracting text from image...")
        text = extract_text_from_image(uploaded_image)
        if text:
            st.write("Summarizing the text...")
            summary = summarize_text(text)
            st.write("Summary:")
            st.write(summary)
        else:
            st.error("Failed to extract text from the image.")

elif option == "Upload a Word document (.docx)":
    uploaded_doc = st.file_uploader("Upload a Word document", type=['docx'])
    if uploaded_doc is not None:
        st.write("Extracting text from Word document...")
        text = extract_text_from_word(uploaded_doc)
        if text:
            st.write("Summarizing the text...")
            summary = summarize_text(text)
            st.write("Summary:")
            st.write(summary)
        else:
            st.error("Failed to extract text from the Word document.")