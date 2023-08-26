
import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
import langchain
langchain.verbose = False
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import subprocess
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
val="""Key points to find from the JD:

The mission of the company (optional)"
The objective of the role: What will you be doing overall?
Competency: What kind of traits/capabilities are required of you?
Years of experience in specific space"
Strategic Bullets: Relate examples or elaborate experience that aligns with the JD



Hi {Hiring Manager}


I came across this role of {insert role} at {Insert team/company}, and seems like your team/org is expanding. That’s great.


As I was conducting my research, I found that you were likely managing this role, so I thought I’d reach out to you directly.


What especially drew me towards this role {Competency, company mission or objective of the role}; it’s something that aligns strongly with my experience and interests.


I offer {X+ years of experience} in {insert the relevant space}. Having done {Competency or handled similar objective/challenge before}, I believe I’ll be a solid fit for the role.


A few highlights of my career include:

Key Highlight Header: {Example or elaboration from the resume} 
Key Highlight Header: {Example or elaboration from the resume}
Key Highlight Header: {Example or elaboration from the resume}
Technology Stack(optional)

I’ve included my resume in the email, highlighting my career profile and significant accomplishments that align with your position.

I’d welcome the opportunity to speak with you if you feel I’d be a strong candidate for this or other positions within your organization. Thank you so much for considering me.


Best,
Your Name


"""
def get_letter(job_desc, resume):
    print("get letter k andr agya")
    instructions = val

    message = [
        {"role": "system", "content": f"Based on the given job description {job_desc} and the user's resume {resume}, generate a cover letter"},
        {
            "role": "system", 
            "content": (
                f'"Key rules to follow while generating a cover letter"\n'
                f'1. In order to write the best cover letter, you must follow {instructions}\n'
                f'2. Do not put the skills which are not available in the resume but are present in the job description\n'
                f'3. Try to find skills and talents in the resume which could be the most relevant according to the job description\n'
                f'4. Make a cover letter so that the hiring manager is impressed by the cover letter\n'
                f'5. Do not make the cover letter very long; keep it between 250 to 400 words only.'
            )
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.5,
        messages=message,
    )
    return response['choices'][0]['message']['content']

def get_resume(template,resume):
    print("resume k liye gpt ke pass")
    message = [
   
    {"role": "system", "content": f"you are expert to write the informations from {resume} to {template} with maximum accuracy and experince which helps people create awesoem resume to get their dream job "},
    {"role": "system", "content":  " key rules to follow while writing the template"
                                   "1.Do not change the code only insert the relevant information from result to {template} "
                                   "2. Understant the text from resume and then choose the best section where you can put the detail in template"
                                   "3. write details in points Do not distort the indentation of template "
                                   "4. make sure it do not exceed one page ,only put the necessary information and useful in template"
                                   "5. Try to enhance the content from resume to make it more attractive and be eye catching in the template "
    },  
                                    
    
]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.5,
        messages=message,
        
        
    )
    return response['choices'][0]['message']['content']




def generate_resume(resume):
    # Read LaTeX template from file
    print("resume k fn ke andr")
    with open("resume_template.tex", "r") as template_file:
        template_content = template_file.read()

    resume_content= get_resume(template_content,resume)

    # Write the resume content to a .tex file
    with open("generated_resume.txt", "w") as output_file:
        output_file.write(resume_content)
    
    # Display and provide a download link for the generated PDF
    st.write("Generated Resume:")
    print("resume bn chuka")
    st.download_button(
        label="Download Resume",
        data=resume_content,
        file_name="generated_resume.txt",
        mime="text/plain"
     )
    

def main():
    st.set_page_config(page_title="Resume helper")
    st.header("Cover Letter generator")

    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if pdf is not None:
        pdf_reader =  PdfReader(pdf)
        resume = ""
        for page in pdf_reader.pages:
            resume += page.extract_text()

        
        
        #if st.button("Generate Cover Letter"):
        job_description = st.text_area("Enter the job description")
        if st.button("Generate Cover letter"):
            print("enter to hogya h")
            
            print("job description k andr") 
            
            letter = get_letter(job_description, resume)
            print("yha agya hoon")
            print(letter)
            if letter:
                st.write("Generated Letter:")
                st.write(letter)
                
                download_button = st.download_button(
                    "Download Letter",
                    data=letter,
                    file_name="generated_letter.txt",
                    key="download_btn"
                )
        
                
        if st.button("Generate new resume"):
            print("resume ke andr")
            generate_resume(resume)
if __name__ == '__main__':
    main()