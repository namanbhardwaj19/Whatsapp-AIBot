import os

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ORGANIZATION = os.environ.get("ORGANIZATION")
PROJECT_ID = os.environ.get("PROJECT_ID")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

user_thread_info = {}

client = OpenAI(
  api_key=OPENAI_API_KEY,
  organization=ORGANIZATION,
  project=PROJECT_ID,
)


def get_ai_response(user_phone, message):
    thread_id = add_message_in_thread(user_phone, message)
    text = run_thread(thread_id)
    return text


def add_message_in_thread(user_phone, message):
    thread_id = user_thread_info.get(user_phone)
    if not thread_id:
        new_thread = client.beta.threads.create()
        thread_id = new_thread.id
        user_thread_info[user_phone] = thread_id
    client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_id


def run_thread(thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            return text
