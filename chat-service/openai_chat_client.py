import os
import uuid
from datetime import datetime
import openai
from response import ChatResponse
from models import Chat
from app import db

openai.api_key = os.environ['OPENAI_API_KEY']
model_engine = "gpt-3.5-turbo"


def get_chat_response(role: str, prompt: str):
    """
        Sends a request to the OpenAI Chat API and returns the chat response.
    """
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": role, "content": prompt},
        ]
    )

    # Save chat to database
    chat = __generate_chat_model(role, prompt, response)
    db.session.add(chat)
    db.session.commit()

    # Return chat response
    return __prepare_chat_response(chat)


def __generate_chat_model(role: str, prompt: str, response):
    openai_message = response.choices[0].message
    return Chat(id=f"id_{uuid.uuid4()}", request_role=role, prompt=prompt, response_role=openai_message.get("role"),
                response=openai_message.get("content").strip(),
                created_at=datetime.utcnow())


def __prepare_chat_response(chat: Chat):
    return ChatResponse(role=chat.response_role, response=chat.response)
