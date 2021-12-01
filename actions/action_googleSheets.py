import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from utils import logger

import db


def action_googleSheets(data):
    """Function for triggering action to add records to google sheets

    :param data: Object holding the relevant fields like questionId,responseId, etc.

    :return: List of anomalies

    """
    logging = logger("action google sheets")

    # Connecting to DB tables
    try:
        logging.info("[Action Google_Sheets] Connecting to the database")
        formDB = db.form_model()
        responseDB = db.response_model()
        questionDB = db.question_model()
        answerDB = db.answer_model()
        actionDB = db.action_model()
    except Exception:
        logging.exception("Connection to database failed ", exc_info=True)
        return False

    # Fetching form and action details
    try:
        logging.info(
            "[Action Google_Sheets] Fetching form & action data from respective DB"
        )
        formData = formDB.fetch_form(data["formId"])
        actionData = actionDB.fetch_action(data["actionId"])
    except Exception:
        logging.exception("Fetching form & action data failed ", exc_info=True)
        return False

    # Fetching Google sheets data
    try:
        logging.info(
            "[Action Google_Sheets] Connecting to Google Sheets with provided info"
        )
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            actionData["meta"]["json"], scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(actionData["meta"]["sheet_name"])
        sheet_instance = sheet.get_worksheet(int(actionData["meta"]["sheet_instance"]))
        num_curr_records = sheet_instance.col_count - 1
    except Exception:
        logging.exception("Connecting to Google Sheets failed ", exc_info=True)
        return False

    # Adding record into google sheet
    try:
        logging.info("[Action Google_Sheets] Adding responses to Google Sheet")

        # case where sheet is empty with 0 records
        if num_curr_records <= 0:
            logging.info(
                "[Action Google_Sheets] Adding all form responses to Google Sheet"
            )
            responses = []
            for responseID in formData[0]["responses"]:
                responseData = responseDB.fetch_response(responseID)
                response = {}
                for response in responseData["responses"]:
                    question = questionDB.fetch_question(response["questionId"])
                    answer = answerDB.fetch_answer(response["answerId"])
                    response[question] = answer
                responses.append(response)
            responses_df = pd.DataFrame(responses)
            sheet_instance.insert_rows(responses_df.values.tolist())

        # case when more than one record is required to be appended
        elif "responseId" not in data or num_curr_records < len(formData["responses"]):
            logging.info(
                "[Action Google_Sheets] Adding multiple form responses to Google Sheet"
            )
            responses = []
            for index in range(num_curr_records, len(formData[0]["responses"])):
                responseData = responseDB.fetch_response(
                    formData[0]["responses"][index]
                )
                response = {}
                for response in responseData["responses"]:
                    question = questionDB.fetch_question(response["questionId"])
                    answer = answerDB.fetch_answer(response["answerId"])
                    response[question] = answer
                responses.append(response)
            responses_df = pd.DataFrame(responses)
            sheet_instance.insert_rows(responses_df.values.tolist())

        # case when only one response is required to be appended
        else:
            logging.info("[Action Google_Sheets] Adding form response to Google Sheet")
            responseData = responseDB.fetch_response(data["responseId"])
            response = {}
            for response in responseData["responses"]:
                question = questionDB.fetch_question(response["questionId"])
                answer = answerDB.fetch_answer(response["answerId"])
                response[question] = answer
            responses_df = pd.DataFrame([response])
            sheet_instance.insert_rows(responses_df.values.tolist())
        return True
    except Exception:
        logging.exception("Adding responses to Google Sheets failed ", exc_info=True)
        return False
