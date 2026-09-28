from dotenv import load_dotenv
from openai import OpenAI 

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

def transcribe(audio_file,raw_file):
    audio_file_data = open(audio_file,"rb")
    transcription = client.audio.transcriptions.create(
        model="gpt-transcribe",
        file=audio_file_data
    )
    with open(raw_file,"w") as raw_file_path:
        raw_file_path.write(transcription.text)
    print("Transcription completed.")

transcribe("audio_chunk_0.wav","raw_meeting.txt")