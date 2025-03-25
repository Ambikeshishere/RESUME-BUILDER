import ollama
import docx
from docx import Document
from docx.shared import Pt
import fitz
import os

OUTPUT_FOLDER = "output"

# ----------------------------
# 📚 Read and Extract Text
# ----------------------------
def read_resume(file_path):
    if file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
    else:
        return None


# ----------------------------
# 📖 Read PDF Files
# ----------------------------
def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text


# ----------------------------
# 🤖 Generate Refined Resume with LLaMA
# ----------------------------
def generate_prompt(resume_text):
    prompt = f"""
    Refine the following resume and generate an ATS-optimized, professional version in Markdown format:
    
    Resume Text:
    ```
    {resume_text}
    ```
    """

    response = ollama.chat(model="llama3.2:1b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


# ----------------------------
# 🎨 Convert Markdown to DOCX
# ----------------------------
def convert_markdown_to_docx(markdown_text, output_filename):
    doc = Document()
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            doc.add_heading(line.replace("# ", ""), level=1)
        elif line.startswith("## "):
            doc.add_heading(line.replace("## ", ""), level=2)
        elif line.startswith("- "):
            doc.add_paragraph(line.replace("- ", ""), style="ListBullet")
        elif line.strip():
            doc.add_paragraph(line)

    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    doc.save(output_path)
    return output_filename


# ----------------------------
# 🚀 Main: Create Refined Resume
# ----------------------------
def create_refined_resume(file_path):
    resume_text = read_resume(file_path)
    if not resume_text:
        return None

    refined_markdown = generate_prompt(resume_text)
    docx_filename = file_path.split("/")[-1].replace(".pdf", ".docx").replace(".txt", ".docx")
    return convert_markdown_to_docx(refined_markdown, docx_filename)
