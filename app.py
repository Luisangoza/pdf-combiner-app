
import streamlit as st
import fitz  # PyMuPDF

def create_cover_page(title):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), title, fontsize=24)
    return doc

def create_index_page(index_text):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), index_text, fontsize=12)
    return doc

st.title("Unir PDFs con Índice y Portada")

uploaded_files = st.file_uploader("Sube tus archivos PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    index_text = "Índice de Documentos PDF\n\n"
    merged_pdf = fitz.open()
    
    # Crear portada
    cover_page = create_cover_page("Documento Combinado")
    merged_pdf.insert_pdf(cover_page)
    
    # Crear índice
    for i, file in enumerate(uploaded_files):
        index_text += f"{i+1}. {file.name}\n"
    index_page = create_index_page(index_text)
    merged_pdf.insert_pdf(index_page)
    
    # Unir PDFs
    for file in uploaded_files:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        merged_pdf.insert_pdf(pdf)
    
    # Guardar PDF combinado
    merged_pdf.save("output.pdf")
    
    # Botón para descargar
    with open("output.pdf", "rb") as f:
        st.download_button("Descargar PDF combinado", f, file_name="documento_completo.pdf")
