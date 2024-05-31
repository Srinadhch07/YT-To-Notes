from reportlab.pdfgen import canvas
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
global_summary=''
genai.configure(api_key=GOOGLE_API_KEY)
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
] 
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
model = genai.GenerativeModel(
model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
convo = model.start_chat(history=[])  
prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

def extract_trancript_details(link):
    try:
        video_id=link.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=''
        #print(transcript_text)
        for i in transcript_text:
            transcript += " " + i["text"]
            return transcript
    except Exception as e:
        raise e
def prepare_notes(prompt,text):
    #genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    convo.send_message(prompt+text)
    response=str(convo.last.text)
    return response
def pdf(response):
    prompt="Give me one single  Tittle for this text."+response
    convo.send_message(prompt)
    title=str(convo.last.text)
    filename = "{title}.pdf"

    pdf = canvas.Canvas("Hello.pdf")

    # Set font and title
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(300, 750, title)

    # Add your text conten
    pdf.drawString(50, 700, response)

    # Save the PDF
    pdf.save()
    
st.title("Youtube to Notes")
link=st.text_input("Enter youtube video link: ")
if link:
    video_id=link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
if st.button("Prepare Notes"):
    transcript_text=extract_trancript_details(link)
    if transcript_text:
        summary=prepare_notes(prompt,transcript_text)
        global_summary=summary
        st.markdown("## Detailed Notes :")
        st.write(summary)
# Future : Make pdf for notes
#if st.button("Donwload PDF"):
#   pdf(global_summary) '''
