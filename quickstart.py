from __future__ import print_function
from io import BytesIO
import io

import os.path
import re
import requests
import PyPDF2

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def getFileContent(file_link):
    file_id = re.search('/file/d/([^/]+)', file_link).group(1)
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('Config/token.json'):
        creds = Credentials.from_authorized_user_file('Config/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
         # Call the Drive v3 API to get the file content
        file_content = service.files().get_media(fileId=file_id).execute()

        # read the PDF file using PyPDF2 library
        with io.BytesIO(file_content) as pdf_buffer:
            pdf_reader = PyPDF2.PdfReader(pdf_buffer)
            num_pages = len(pdf_reader.pages)
            pdf_content = ''
            for i in range(num_pages):
                page = pdf_reader.pages[i]
                pdf_content += page.extract_text()
        return pdf_content
    except HttpError as error:
        return "An Error Occured, Please try again"
