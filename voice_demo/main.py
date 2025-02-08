import os
from groq import Groq

# Initialize the Groq client
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Specify the path to the audio file
filename = "sample_audio.mp3"

# Open the audio file
with open(filename, "rb") as file:
    # Create a translation of the audio file
    translation = client.audio.translations.create(
      file=(filename, file.read()), # Required audio file
      model="voice_demo-large-v3", # Required model to use for translation
      prompt="Specify context or spelling",  # Optional
      response_format="json",  # Optional
      temperature=0.0  # Optional
    )
    # Print the translation text
    print(translation.text)