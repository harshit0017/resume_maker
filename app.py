
import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import pdfkit
import asyncio
import streamlit as st
from pyppeteer import launch
import multiprocessing
from bs4 import BeautifulSoup
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


temp_jd= "temp_jb.txt"
temp_resume="temp_resume.txt"
temp_cover_letter="cover_letter.txt"


val="instruct.txt"

def get_letter(job_desc, resume):
    print("get letter k andr agya")
    instructions = val

    message = [
        {"role": "system", "content": f"Based on the given job description {job_desc} and the user's resume {resume}, generate a cover letter"},
        {
            "role": "system", 
            "content": (
                f'"Key rules to follow while generating a cover letter"\n'
                f'1. The cover letter should follow this format: \n{instructions}\n and write within 300 words strictly'
                f'2. Only include skills and experiences that are clearly stated or implied in candidate\'s resume.\n'
                f'3. Highlight unique talents or achievements in candidate\'s resume that could set them apart from other applicants for this position.\n'
                f'4. The goal of this cover letter is to impress hiring managers by clearly showing how well-suited candidate is for this role based on their past experiences and skills as mentioned in their resume.\n'
            )
        },
        {"role": "user", "content": f"this is resume{temp_resume} and this is job description{temp_jd}" },
        {"role": "assistant", "content": temp_cover_letter},
        {
            'role': 'user',
            'content': (
                 'Please generate a compelling cover letter that showcases my potential '
                 'and aligns my skills and experiences with what is required in '
                 'the job description.'
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
        {"role": "system", "content": f"You are an expert at composing responses following a specific template format. Given a resume and a template, your goal is to accurately and effectively transfer information from the resume to the template while adhering to the template's structure. Your responses should not introduce new sections but instead, intelligently place extracted details into the corresponding sections of the template."},
        {"role": "system", "content": f"To use resum as {resume} and template as {template}, please follow the below steps:"},
        {"role": "system", "content": "Here are the key rules to follow while generating the template:"},
        {"role": "system", "content": f"1. Maintain the original template code, only inserting relevant information from the resume."},
        {"role": "system", "content": "2. Carefully understand the content of the resume and determine the best-fitting sections in the template."},
        {"role": "system", "content": "3. Present the details using bullet points while preserving the template's indentation."},
        {"role": "system", "content": "4. Ensure the response does not exceed one page; include only necessary and impactful information."},
        {"role": "system", "content": "5. Enhance the content from the resume to make it appealing and captivating in the template."},
        {"role": "system", "content": "6. Do not keep the original content of template change it according to the content of resume."},
        {"role": "system", "content": "Provide a response following the provided template format, transferring the information from the resume as required."}
    ]
                                    
    


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.5,
        messages=message,
        
        
    )
    return response['choices'][0]['message']['content']




import subprocess
def generate_resume(resume):
    # Read HTML template from file
    with open("./index.html", "r") as template_file:
        template_content = template_file.read()

    # Get resume content using your get_resume function
    resume_content = get_resume(template_content, resume)
    print("hogyi generate")
    with open("generated_resume.html", "w") as output_file:
        output_file.write(resume_content)
    
   

    # Read the HTML file
    with open('./generated_resume.html', 'r') as f:
        html_content = f.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Read the CSS file 
    with open('./output.css', 'r') as f:
        css_content = f.read()

    # Create a new style tag with CSS content and add it into head section of HTML.
    style_tag = soup.new_tag("style")
    style_tag.string = css_content

    head_tag = soup.head
    head_tag.append(style_tag)

    # Save modified html content back to file.
    with open('./generated_resume_with_css.html', 'w') as f:
        f.write(str(soup))

    st.download_button(
        label="Download Resume",
        data=open("./generated_resume_with_css.html", "rb").read(),
        file_name="output.html",
        mime="text/html"
)
    
    st.write("Generated Resume")
    
   


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