import openai
import config
from image_response import ImageResponse
from models import Image

openai.api_key = config.OPENAI_API_KEY.replace("\r\n", "")


def get_image_response(prompt: str, session):
    """
        Sends a request to the OpenAI Chat API and returns the generated image response.
    """
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )

    # Generate image model
    image = __generate_image_model(prompt, response)

    # Save image to database
    session.add(image)
    session.commit()

    # Return image response
    return __prepare_image_response(image)


def __generate_image_model(prompt: str, response):
    image_url = response['data'][0]['url']
    return Image(prompt, image_url)


def __prepare_image_response(image: Image):
    return ImageResponse(image.prompt, image.image_url)
