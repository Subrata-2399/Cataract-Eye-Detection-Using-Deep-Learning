import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Replace with your own values
CLIENT_SECRET_FILE = 'client_secret_798812911982-9omemmvudq581ci88pomvoa0bh9c3lpu.apps.googleusercontent.com.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = '1DV_LRqCoQhPygStrQRIHPa-oxl_aeqjw'
OUTPUT_DIR = 'test'


def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def download_files(service, folder_id, output_dir):
    results = service.files().list(
        q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print('No files found.')
    else:
        for file in files:
            file_id = file['id']
            file_name = file['name']
            request = service.files().get_media(fileId=file_id)
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'wb') as f:
                downloader = request.execute()
                f.write(downloader)


def main():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    download_files(service, FOLDER_ID, OUTPUT_DIR)


if __name__ == '__main__':
    main()
