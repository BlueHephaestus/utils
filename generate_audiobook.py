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
from ai_utils import tts
