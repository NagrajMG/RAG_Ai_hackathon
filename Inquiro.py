import streamlit as st
import pathlib
from RAG_and_LLM import  MCQSolver, Brief_Description
from PDF2TXT import save_uploaded_pdf, pdf_to_txt
import os
# Title of the app
st.title("Inquiro")

# Instructions on how to use the tool
st.markdown("""
### How to Use This MCQ Solver Tool:

1. **Enter the Question**: Start by entering the multiple-choice question you want to solve in the input box provided.

2. **Enter the Options**: Fill in all four answer options (A, B, C, D) in their respective input fields.

3. **Submit**: Once the question and all options are filled, click on the **Submit** button to get the results.

   - If all options are filled, the tool will display the correct answer along with a brief explanation.
   
   - If some options are missing, the tool will provide only a brief explanation.

4. **Results**: After submitting, the results section will show:
   - **Correct Answer**: The correct option (if all options are provided).
   - **Brief Explanation**: A brief description related to the question or the correct answer.
""")
root_dir = pathlib.Path(__file__).parent
folder_path=str(root_dir /'textbooks'/'en' / 'extras.txt')
New_pdfs= str(root_dir / 'Additional_pdfs'/'extra_pdfs.pdf')

st.subheader("Upload PDF for providing additional information:")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.write(f"PDF '{uploaded_file.name}' uploaded successfully!")
    New_pdfs = save_uploaded_pdf(uploaded_file, New_pdfs )
    
    print(New_pdfs)
    New_txts = pdf_to_txt(New_pdfs, folder_path)
    st.write(f"Saving text file to: {New_txts}")

    


question = st.text_area("Enter the question:")
option_a = st.text_input("Option A:")
option_b = st.text_input("Option B:")
option_c = st.text_input("Option C:")
option_d = st.text_input("Option D:")

options = {
    "A": option_a,
    "B": option_b,
    "C": option_c,
    "D": option_d,
}


if st.button("Submit"):
    
    if all([option_a, option_b, option_c, option_d]):
        correct_answer = MCQSolver(question, options)  
        brief_info = Brief_Description(question)
        
        st.subheader("Results:")
        st.write(f"**Correct Answer:** Option {correct_answer}")
        st.write(f"**The Option is based on the following Information:** {brief_info}")
    else:
        brief_info = Brief_Description(question)
        st.subheader("Results:")
        st.write("Some options are missing, only showing the brief information.")
        st.write(f"**Brief Information:** {brief_info}")





