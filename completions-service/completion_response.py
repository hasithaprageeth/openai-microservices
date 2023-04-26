import uuid


class CompletionResponse:
    def __init__(self, prompt, completed_text):
        self.id = f"id_{uuid.uuid4()}"
        self.prompt = prompt
        self.completed_text = completed_text
