import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

def extract_trancript_details(link):
    try:
        video_id=link.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=''
        print(transcript_text)
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e
#extract_trancript_details("https://www.youtube.com/watch?v=Nx4bvwU0DqE")
def gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text
st.title("YT transcriptor to Note converter")
link=st.text_input("Enter youtube  video link: ")
if link:
    video_id=link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
if st.button("Get Detailed notes : "):
    transcript_text=extract_trancript_details(link)
    if transcript_text:
        summary=gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes :")
        st.write(summary)
