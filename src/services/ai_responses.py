import json
import os
from fastapi.logger import logger
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")
ORGANIZATION = os.environ.get("ORGANIZATION")
PROJECT_ID = os.environ.get("PROJECT_ID")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")
GOOGLE_SERVICE_ACCOUNT_URL = os.environ.get("GOOGLE_SERVICE_ACCOUNT_URL")
GOOGLE_SHEET_URL = os.environ.get("GOOGLE_SHEET_URL")

user_thread_info = {}

client = OpenAI(
  api_key=OPEN_AI_API_KEY,
  organization=ORGANIZATION,
  project=PROJECT_ID,
)


def get_ai_response(user_phone, message):
    """
    this function will generate the response for the given query
    """
    thread_id = add_message_in_thread(user_phone, message)
    text = run_thread(thread_id, user_phone)
    return text


def add_message_in_thread(user_phone, message):
    """
    this function will add the user's message in thread, if thread is not
     already created, it will create a thread and then put new message in it
    """
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


def run_thread(thread_id, user_phone):
    """
    this function will finally run the thread and return the generated response
    """
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    tool_outputs = []
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        if run.status == "completed":
            logger.info("Run completed")
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            return text

        elif run.status == 'requires_action':
            logger.info("Run required action")
            for function_call in run.required_action.submit_tool_outputs.tool_calls:
                if function_call.function.name == "handle_unanswered_question":
                    arguments = json.loads(function_call.function.arguments)
                    unanswered_question = arguments.get("question")
                    save_unanswered_questions_to_sheet(unanswered_question, user_phone)

                    tool_outputs.append({
                        "tool_call_id":
                            function_call.id,
                        "output":
                            "Unanswered question noted and saved to Google Sheets."
                    })

            if tool_outputs:
                try:
                    client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=tool_outputs)
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print("Failed to submit tool outputs:", e)

            text = "Sorry I have not been taught how to answer that question. " \
                   "We will make a note of that question and I will be able to answer it soon. " \
                   "Please try rephrasing the question and be specific so that I can understand the question better."
            return text


# Google Sheets setup and authorization
def save_unanswered_questions_to_sheet(unanswered_question, user_phone):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_SERVICE_ACCOUNT_URL, scope)
    client = gspread.authorize(creds)
    # Open the specific Google Sheet (worksheet 1 assumed for unanswered questions)
    sheet = client.open_by_url(GOOGLE_SHEET_URL)
    sheet = sheet.sheet1
    # Append each unanswered question to the sheet
    user_phone = user_phone.split(":")[-1]
    sheet.append_row([unanswered_question, user_phone])
    logger.info("Unanswered questions saved to Google Sheets.")
