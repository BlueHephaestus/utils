"""
Given a topic to understand, as a string, prompt GPT-4 to generate a very lengthy
    explanation of the topic, in audiobook form - so that it can then have
    these responses text-to-speeched into a long audio file, functioning
    as an audiobook of variate length explaining the topic, that the user can
    then listen to.

Base prompt is enforcing this format, we use gpt4 for generation and whisper tts for audio.

Flow is as follows:
    1. Initial Prompt, topic and rules for output
    2. For i in range(max_prompts):
        3. Get response
        4. Convert to audio, append to file
        5. Send "continue" to model.
"""
from openai import OpenAI
import os
import argparse
import re
from ai_utils import tts, ChatGPT
from textwrap import wrap

SYSTEM_PROMPT = """
I am a multifaceted engineer, and while I have spent most of my career working in machine learning and software engineering I have experience in a variety of other fields including electronics, carpentry, teaching, data recovery, and prop making. 

There is a lot I don't know, and I am always looking to learn. I currently am devoting all of my resources to getting a job at OpenAI, since I believe entirely in their mission and want to help them work on AGI no matter what.

In our discussions I would like you to help me understand things better and improve my chances of getting a job at OpenAI through both my own education and knowledge as well as whatever actions I can take to improve these odds.

When explaining things, assume I don't know about how the topic fundamentally works, and explain in as granular detail as possible. If I already know, I will tell you, and regardless, this will serve as good review. 

If you have ideas or suggestions for how I can learn a topic better, or how I can better achieve my goal of getting a job at OpenAI, please tell me. 

Quiz me on topics we have recently covered, followed by answers, as this will reinforce my understanding. 

I look forward to continuing to collaborate with you! My name is Blue, she/her.
"""
def generate_audiobook(topic, max_prompts=10, model="gpt-4", output_fname="output.mp3"):
    """
    Generate an audiobook explaining the given topic.
    :param topic: The topic to explain.
    :param max_prompts: The maximum number of prompts to generate.
    :param model: The model to use. Defaults to gpt-4.
    :param output_fname: The file to save the audio to. Defaults to output.mp3.
    :return: None
    """
    # Create the chat session
    chat = ChatGPT(id="audiobook", system_prompt=SYSTEM_PROMPT, model=model)
    responses = [] #plaintext storage of responses
    # response = chat.cumulative_ask("Explain TRPO optimization to me. The explanation should be at least 10 minutes long, and in the form of an audiobook.")


    print("Receiving Transmission 1...")
    response = chat.cumulative_ask(
        f"Explain {topic} to me, as an educational comprehensive walkthrough. Output over multiple transmissions, taking your time and going into detail on the fundamental concepts that are necessary for understanding the given topic, as well as the details and intricacies of the given topic. Word your outputs so they translate well to text-to-speech, so be verbose when it comes to equations if you include them. Do not include headings. I'd also like you to continue putting questions and answers at the end to quiz me. MAKE SURE TO INCLUDE ANSWERS AFTER THE QUESTIONS. Break up your output into multiple transmissions to cover all the necessary breadth and depth. When you are finished with all transmissions, type 'Transmissions Complete.'.")
    responses.append(response)
    chat.save()
    print("\n".join(wrap(response, 80)))
    n = 1
    while "transmissions complete." not in response.lower():
        n+=1
        print(f"Receiving Transmission {n}...")
        try:
            response = chat.cumulative_ask(f"Continue. State 'Transmissions Complete.' when all transmissions are done.")
        except Exception: break
        # print(response[:100] + "...")
        print("\n".join(wrap(response, 80)))
        responses.append(response)
        chat.save()

    print(f"Received {n} Transmissions. Converting to Audiobook.")
    # Finished explaining, convert it to audiobook.
    os.makedirs("audiobooks", exist_ok=True)
    output_fname = os.path.join("audiobooks", output_fname)
    tts("\n\n".join(responses), output_file=output_fname)
    print(f"Finished converting. Enjoy!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an audiobook explaining the given topic.")
    parser.add_argument("topic", type=str, help="The topic to explain.")
    parser.add_argument("--max-prompts", type=int, default=10, help="The maximum number of prompts to generate.")
    parser.add_argument("--model", type=str, default="gpt-4", help="The model to use. Defaults to gpt-4.")
    parser.add_argument("--output-fname", type=str, default="output.mp3", help="The file to save the audio to. Defaults to output.mp3.")
    args = parser.parse_args()

    generate_audiobook(args.topic, args.max_prompts, args.model, args.output_fname)