
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
                f'1. The cover letter should strictly follow this format: \n{instructions}\n and write within 300 words strictly'
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


def get_resume(template,resume, job_desc):
    print("resume k liye gpt ke pass")
    if job_desc is None:
        job_desc= "software engineer"
    message = [
        {"role": "system", "content": f"You are an expert AI in transforming information in form to another you understand the given information and carefully fill it into the another provided format following all the guidelines"},
        {"role": "system", "content": f"To transfer data from {resume} to template {template}, please follow the below steps:"},
        {"role": "system", "content":  "1. Create  content from the resume with availble information do not self assume any information and insert it into the template code."},
        {"role": "system", "content": f"2. Maintain the original template code, only inserting relevant information from the resume.Do not add information which is not asked or mentioned in template "},
        {"role": "system", "content":  "3. Do not keep duplicate sections in the template, remove unnecessary sections and keep only the sections which are required in the template"},
        {"role": "system", "content":  "4. Carefully understand the content of the resume and determine the best-fitting sections in the template."},
        {"role": "system", "content":  "5. The template is just a format do not keep it's content  replace that content with content from the resume"},
        {"role": "system", "content": f"6. Do not add information which is not available in resume but try to make the most out of the information to favour the job description{job_desc}"}, 
        {"role": "system", "content":  "7. Provide a response following the provided template format, transferring the information from the resume as required."},
        {"role": "system", "content":  "8. Make it informative."},
    ]
                                    
    


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.5,
        messages=message,
        
        
    )
    return response['choices'][0]['message']['content']




import subprocess
def generate_resume(resume,job_desc):
    # Read HTML template from file
    with open("./index.html", "r") as template_file:
        template_content = template_file.read()

    # Get resume content using your get_resume function
    resume_content = get_resume(template_content, resume, job_desc)
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
            generate_resume(resume, job_description)
if __name__ == '__main__':
    main()
