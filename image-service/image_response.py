import uuid


class ImageResponse:
    def __init__(self, prompt, image_url):
        self.id = f"id_{uuid.uuid4()}"
        self.prompt = prompt
        self.image_url = image_url
