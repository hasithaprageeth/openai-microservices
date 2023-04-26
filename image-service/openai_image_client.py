import os
import openai
from image_models.image_response import ImageResponse

openai.api_key = os.environ['OPENAI_API_KEY']


def get_image_response(prompt: str):
    """
        Sends a request to the OpenAI Chat API and returns the generated image response.
    """
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']
    return __prepare_image_response(prompt, image_url)


def __prepare_image_response(prompt: str, image_url: str):
    response = ImageResponse(prompt, image_url)
    return response.__dict__
