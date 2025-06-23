# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types

INPUT_FILE = "file_input.md"
OUTPUT_FILE = "file_output.html"


def parse_input_file(path):
    """
    Reads the input file and returns (system_prompt, user_input).
    If the file contains:
    ---
    SYSTEM PROMPT
    ---
    USER INPUT
    ---
    It will split accordingly. Otherwise, the whole file is user input.
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.strip() == "":
        return ("", "")
    if content.count("---") >= 2:
        parts = content.split("---")
        system_prompt = parts[1].strip()
        user_input = parts[2].strip() if len(parts) > 2 else ""
        return (system_prompt, user_input)
    else:
        return ("", content.strip())


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    system_prompt, user_input = parse_input_file(INPUT_FILE)

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[types.Part.from_text(text=system_prompt)],
    )

    output = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-pro-preview-05-06",
        contents=contents,
        config=generate_content_config,
    ):
        output += chunk.text

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)


if __name__ == "__main__":
    generate()
