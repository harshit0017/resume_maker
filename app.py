
import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import pdfkit
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')






val="""Key points to find from the JD:

The mission of the company (optional)"
The objective of the role: What will you be doing overall?
Competency: What kind of traits/capabilities are required of you?
Years of experience in specific space"
Strategic Bullets: Relate examples or elaborate experience that aligns with the JD



Hi {Hiring Manager}


I came across this role of engineer at company name, and seems like your team/org is expanding. That’s great.


As I was conducting my research, I found that you were likely managing this role, so I thought I’d reach out to you directly.


What especially drew me towards this role {Competency, company mission or objective of the role}; it’s something that aligns strongly with my experience and interests.


I offer X+ years of experience in {insert the relevant space}. Having done {Competency or handled similar objective/challenge before}, I believe I’ll be a solid fit for the role.


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
# def get_letter(job_desc, resume):
#     print("get letter k andr agya")
#     instructions = val

#     message = [
#         {"role": "system", "content": f"Based on the given job description {job_desc} and the user's resume {resume}, generate a cover letter"},
#         {
#             "role": "system", 
#             "content": (
#                 f'"Key rules to follow while generating a cover letter"\n'
#                 f'1. In order to write the best cover letter, you must follow {instructions}\n'
#                 f'2. Do not put the skills which are not available in the resume but are present in the job description\n'
#                 f'3. Try to find skills and talents in the resume which could be the most relevant according to the job description\n'
#                 f'4. Make a cover letter so that the hiring manager is impressed by the cover letter\n'
#                 f'5. Do not make the cover letter very long; keep it between 250 to 400 words only.'
#             )
#         }
#     ]

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-16k",
#         temperature=0.5,
#         messages=message,
#     )
#     return response['choices'][0]['message']['content']
def get_letter(job_desc, resume):
    print("get letter k andr agya")
    instructions = val

    message = [
        {"role": "system", "content": f"Based on the given job description {job_desc} and the user's resume {resume}, generate a cover letter"},
        {
            "role": "system", 
            "content": (
                f'"Key rules to follow while generating a cover letter"\n'
                f'1. The cover letter should follow this format: \n{instructions}\n'
                f'2. Only include skills and experiences that are clearly stated or implied in candidate\'s resume.\n'
                f'3. Highlight unique talents or achievements in candidate\'s resume that could set them apart from other applicants for this position.\n'
                f'4. The goal of this cover letter is to impress hiring managers by clearly showing how well-suited candidate is for this role based on their past experiences and skills as mentioned in their resume.\n'
            )
        },
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
        model="gpt-3.5-turbo",
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





def generate_resume(resume):
    # Read HTML template from file
    with open("resume_template.html", "r") as template_file:
        template_content = template_file.read()

    # Get resume content using your get_resume function
    resume_content = get_resume(template_content, resume)

    # Write the resume content to a .html file
    with open("generated_resume.html", "w") as output_file:
        output_file.write(resume_content)

    print(f"HTML content: {resume_content[:100]}...")  # Print first 100 characters

    # Convert the HTML to PDF
    input_html = 'generated_resume.html'
    output_pdf = 'output.pdf'
    
    try:
        pdfkit.from_file(input_html, output_pdf)
        print("PDF generation successful")
        
        with open(output_pdf, "rb") as f:
            pdf_data = f.read()
            
            if len(pdf_data) == 0:
                print("PDF file is empty")
            else:
                st.download_button(
                    label="Download Resume",
                    data=pdf_data,
                    file_name="output.pdf",
                    mime="application/pdf"
                )
                
                st.write("Generated Resume:")
                
    except Exception as e:
        print(f"Error during PDF generation: {e}")


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