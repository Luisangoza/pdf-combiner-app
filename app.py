
import streamlit as st
import fitz  # PyMuPDF

st.title("Unir PDFs con Índice")

uploaded_files = st.file_uploader("Sube tus archivos PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    index_text = "Índice de Documentos PDF\n\n"
    merged_pdf = fitz.open()
    for i, file in enumerate(uploaded_files):
        index_text += f"{i+1}. {file.name}\n"
    index_page = fitz.open()
    index_page.insert_page(0, text=index_text)
    merged_pdf.insert_pdf(index_page)
    for file in uploaded_files:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        merged_pdf.insert_pdf(pdf)
    merged_pdf.save("output.pdf")
    with open("output.pdf", "rb") as f:
        st.download_button("Descargar PDF combinado", f, file_name="documento_completo.pdf")
