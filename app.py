
import streamlit as st
import fitz  # PyMuPDF

def create_cover_page(title, subtitle, logo_path):
    cover_page = fitz.open()
    page = cover_page.new_page()
    page.insert_text((72, 72), title, fontsize=24, fontname="helv")
    page.insert_text((72, 100), subtitle, fontsize=18, fontname="helv")
    if logo_path:
        page.insert_image((72, 150), logo_path, keep_proportion=True, width=100)
    return cover_page

def create_index_page(file_names):
    index_text = "Índice de Documentos PDF

"
    for i, name in enumerate(file_names):
        index_text += f"{i+1}. {name}
"
    index_page = fitz.open()
    page = index_page.new_page()
    page.insert_text((72, 72), index_text, fontsize=12, fontname="helv")
    return index_page

def create_separator_page(file_name):
    separator_page = fitz.open()
    page = separator_page.new_page()
    page.insert_text((72, 72), file_name, fontsize=18, fontname="helv")
    return separator_page

st.title("Unir PDFs con Portada e Índice")

logo = st.file_uploader("Sube tu logo", type=["png", "jpg", "jpeg"])
title = st.text_input("Título de la portada", "Documento Combinado")
subtitle = st.text_input("Subtítulo de la portada", "Generado por Streamlit")

uploaded_files = st.file_uploader("Sube tus archivos PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    file_names = [file.name for file in uploaded_files]
    cover_page = create_cover_page(title, subtitle, logo)
    index_page = create_index_page(file_names)
    merged_pdf = fitz.open()
    merged_pdf.insert_pdf(cover_page)
    merged_pdf.insert_pdf(index_page)
    for file in uploaded_files:
        separator_page = create_separator_page(file.name)
        merged_pdf.insert_pdf(separator_page)
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        merged_pdf.insert_pdf(pdf)
    merged_pdf.save("output.pdf")
    with open("output.pdf", "rb") as f:
        st.download_button("Descargar PDF combinado", f, file_name="documento_completo.pdf")
