import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")


def generate(prompt: str, num: int = 1) -> tuple[list[str], str] | None:
    try:
        response = openai.Image.create(prompt=prompt, n=num)
    except openai.error.AuthenticationError:
        return

    return [i["url"] for i in response["data"]], str(response["created"])
