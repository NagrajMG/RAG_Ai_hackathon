import PyPDF2
import os
import time

def pdf_to_txt(pdf_file_path, output_txt_path):
    
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            print('Checking')
            starttime = time.time()
            reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text
            with open(output_txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(extracted_text)
        endtime = time.time()
        execution_time = endtime - starttime
        print(f"PDF to TXT conversion took {execution_time} seconds.")    
        return output_txt_path  
    
    except Exception as e:
        return f"An error occurred: {e}"

def save_uploaded_pdf(uploaded_file, save_dir):
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        pdf_save_path = os.path.join(save_dir, uploaded_file.name)
        
        with open(pdf_save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        print('PDF saved')
        return pdf_save_path
    
    except Exception as e:
        return f"An error occurred while saving the file: {e}"
