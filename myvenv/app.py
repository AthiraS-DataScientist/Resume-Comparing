from flask import Flask, request, render_template
import PyPDF2
from PyPDF2 import PdfReader
import spacy
import os
import tempfile


app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')


@app.route('/')
def index():
    return render_template('index.html')


def extract_text(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def compare_resumes(uploaded_text, reference_text):
    # Perform NLP analysis on the text using spaCy or any other NLP library
    uploaded_doc = nlp(uploaded_text)
    reference_doc = nlp(reference_text)

    # Calculate similarity using spaCy's similarity method (can be customized based on your requirements)
    similarity_score = uploaded_doc.similarity(reference_doc) * 100

    return similarity_score



@app.route('/upload', methods=['POST'])
def upload():
    resume = request.files['resume']
    if resume:
        # Save the uploaded PDF to a temporary location
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, 'uploaded_resume.pdf')
        resume.save(temp_path)

        # Create a PdfReader object from the temporary file path
        text = extract_text(temp_path)

        # Compare the uploaded resume with the reference resume
        reference_text = "Nithyadas VP Junior Python Developer I seek challenging opportunities where I can fully use my skills for the success of the organization vpnithyadas@gmail.com 7594912124 Vadakkepurakkal(H),Ponmun dam(PO), Vailathur, India www.hackerrank.com/vpnithy adas linkedin.com/in/nithyadas-vp- 60a723243 github.com/NITHYADAS SKILLS HTML CSS JAVASCRIPT PYTHON MYSQL FIGMA LANGUAGES Malayalam Full Professional Proﬁciency English Full Professional Proﬁciency INTERESTS DANCING SINGING WATCHING MOVIES COOKING EDUCATION Bachelor Of Computer Science University of Calicut 2019 - 2022 , Ramapuram PLUS TWO Board of Higher Secondary Education of Kerala 2017 - 2019 , Kadungathukundu SSLC Board of Higher School Kerala 2016 , Kadungathukundu WORK EXPERIENCE Junior Python Developer Intern Softroniics Perinthalmanna INDUSTRIAL VISIT Edu Campus in Perinthalmanna (01/2022) An Exclusive Skill Hub PERSONAL PROJECTS E-quarantine (03/2022) Mobile Application for the quarantine people . This application is tracking hundreds of people in home quarantine in the district Developed using ﬂutter, python and MySQL server"
        similarity_score = compare_resumes(text, reference_text)

        # Delete the temporary file after processing
        os.remove(temp_path)
        os.rmdir(temp_dir)

        # Render the result template with the similarity score
        return render_template('result.html', similarity_score=similarity_score)

    else:
        return 'No file uploaded'

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
#python -m spacy download en_core_web_sm