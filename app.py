# FLASK APP - Run the app using flask --app app.py run
import os, sys
from flask import Flask, request, render_template
from pypdf import PdfReader 
import json
from resumeparser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
@app.route("/process", methods=["POST"])
def ats():
    doc = request.files['pdf_doc']
    file_path = os.path.join(UPLOAD_PATH, "file.pdf")
    doc.save(file_path)

    resume_text = _read_file_from_path(file_path)
    print(f"[DEBUG] Resume Text (First 300 chars): {resume_text[:300]}")

    parsed_data = ats_extractor(resume_text)
    print(f"[DEBUG] Parsed Data: {parsed_data}")

    return render_template('index.html', data=json.loads(parsed_data))

def _read_file_from_path(path):
    reader = PdfReader(path) 
    data = ""

    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no] 
        data += page.extract_text()

    return data 


if __name__ == "__main__":
    app.run(port=8000, debug=True)

