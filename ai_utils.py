"""
Utils to use AI in some way shape or form.
    It's very generic for now.

All of these will assume an API key in the environment variable OPENAI_API_KEY
"""
import nltk # didn't see this functionality for sentence splitting in the openai api
nltk.download("punkt")
import os
from tqdm import tqdm
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def tts(text, output_file="output.mp3", model="tts-1-hd", voice="fable", chunk_size=4096):
    """
    Convert text to speech using the OpenAI API, and save it to a file.

    Since OpenAI has a limit on the character limit that can be sent to the API,
    this function will split the text into chunks of full length 4096 and send them individually.

    It splits on sentence boundaries, so that the audio doesn't cut off mid-sentence.

    :param text: The text to convert to speech. Should only be a string.
    :param output_file: The file to save the audio to. Defaults to output.mp3.
    :param model: The model to use. Defaults to tts-1.
    :param voice: The voice to use. Defaults to fable.
    :return: The audio data.
    """

    open(output_file, "w").close()  # clear the file

    # Iterate in chunk_size sentence-delimited chunks until all text processed
    chunk = ""
    for sent in tqdm(nltk.sent_tokenize(text), desc="TTS: "):
        if len(chunk+sent)+1 < chunk_size:
            chunk += sent + " "
        else:
            #Process the chunk and reset it
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=chunk
            )
            # add this chunk to the file
            with open(output_file, "ab") as f:
                for filechunk in response.iter_bytes(chunk_size=1024): # arbitrary chunk size
                    f.write(filechunk)
