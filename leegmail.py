from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    #Mostrar labels de gmail

    creds= None
    #token.pickle guardara y actualizara tokens, se crea automaticamente
    # cuando se completa la autorizacion la primera vez
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as token:
            creds=pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds = flow.run_local_server(port=0)

        #Guardar credenciales para la proxima vez
        with open('token.pickle','wb') as token:
            pickle.dump(creds,token)

    service = build('gmail','v1', credentials=creds)

    #llamar Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels',[])

    # if not labels:
    #     print('No se encontraron labels')
    # else:
    #     print('Labels')
    #     for label in labels:
    #         print(label['name'])


    results = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()
    messages = results.get('messages',[])

    message_count = int(input('Cuantos mensajes quiere mostrar?'))
    if not messages:
        print('No hay mensajes en INBOX')
    else:
        print('Mensajes:')
        #retornar los mensajes
        for message in messages[:message_count]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(msg['snippet'])
            print('\n')
            time.sleep(2)

if __name__=='__main__':
    main()
