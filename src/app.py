from flask import Flask, request
import smtplib
from smtplib import SMTPException
from email.message import EmailMessage
import tableauserverclient as TSC
import yaml

app = Flask(__name__)

with open('secrets.yaml','r') as file:
    stuff = yaml.safe_load(file)

def email(_message, _subject):
    try:
        msg = EmailMessage()
        msg['Subject'] = _subject
        msg['From'] = stuff['gmailuser']
        msg['To'] = stuff['gmailuser']
        msg.set_content(_message)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(stuff['gmailuser'],stuff['gmailapppassword'])
        s.send_message(msg)
        print('Email sent')
        s.quit()
    except SMTPException:
        print('Error: unable to send email')

def additionalWorkbookInfo(workbookID):
    tableau_auth = TSC.TableauAuth(stuff[user], stuff['password'], stuff['mland'])
    server = TSC.Server(stuff[server], use_server_version = True)

    with server.auth.sign_in(tableau_auth):
        workbook = server.workbooks.get_by_id(workbookID)
        print('workbook project is', workbook.project_name)
        workbookURL = workbook.webpage_url
        ownerID = workbook.owner_id
        user = server.users.get_by_id(ownerID)
        userName = user.name
        userEmail = user.email
    
    return workbook.project_name, workbookURL, userName, userEmail 

def additionalDatasourceInfo(datasourceID):
    tableau_auth = TSC.TableauAuth(stuff[user], stuff['password'], stuff['mland'])
    server = TSC.Server(stuff[server], use_server_version = True)

    with server.auth.sign_in(tableau_auth):
        datasource = server.datasources.get_by_id(datasourceID)
        print('Datasource last refresh was:', datasource.updated_at)
        lastRefresh = datasource.updated_at
        url = datasource.webpage_url
        ownerID = datasource.owner_id
        user = server.users.get_by_id(ownerID)
        userName = user.name
        userEmail = user.email

    return lastRefresh, url, userName, userEmail
        
@app.route('/failedworkbookrefresh', methods = ['Post'])
def workbookrefreshfail():
    payload = request.get_json()
    print('JSON Payload received')
    print(payload)
    resource = payload['resource']
    event_type = payload['event_type']
    resource_name = payload['resource_name']
    site_luid = payload['site_luid']
    resource_luid = payload['resource_luid']
    created_at = payload['created_at']

    lastRefresh, url, userName, userEmail = additionalWorkbookInfo(resource_luid)
    print('running additional workbook Info method')

    _subject = '!Workbook Refresh Failure!'

    _message = '''
    
    A workbook refresh has failed. Please see below for more details.

    Resource: {}
    Event Type: {}
    Resource Name: {}
    Project: {}
    Created AT: {}
    LastRefresh: {}
    URL: {}
    Owner's Name: {}
    Owner's Email: {}
    
    Thank you
    
    '''.format(resource,event_type,resource_name,created_at,lastRefresh,url,userName,userEmail)

    print('Email message created')
    print(_message)

    email(_message, _subject)

    return 'Success!'


@app.route('/failedDatasourceRefresh', methods = ['Post'])
def failedDatasourceRefresh():
    payload = request.get_json()
    print('JSON Payload received')
    print(payload)
    resource = payload['resource']
    event_type = payload['event_type']
    resource_name = payload['resource_name']
    site_luid = payload['site_luid']
    resource_luid = payload['resource_luid']
    created_at = payload['created_at']

    lastRefresh, url, userName, userEmail = additionalDatasourceInfo(resource_luid)
    print('running additional datasource Info method')

    _subject = '!Datasource Refresh Failure!'

    _message = '''
    
    A datasource refresh has failed. Please see below for more details.

    Resource: {}
    Event Type: {}
    Resource Name: {}
    Project: {}
    Created AT: {}
    LastRefresh: {}
    URL: {}
    Owner's Name: {}
    Owner's Email: {}
    
    Thank you
    
    '''.format(resource,event_type,resource_name,created_at,lastRefresh,url,userName,userEmail)

    print('Email message created')
    print(_message)

    email(_message,_subject)

    return 'Success!'



@app.route('/publishWorkbook', methods = ['Post'])
def publishWorkbook():
    payload = request.get_json()
    print('JSON Payload received')
    print(payload)
    resource = payload['resource']
    event_type = payload['event_type']
    resource_name = payload['resource_name']
    site_luid = payload['site_luid']
    resource_luid = payload['resource_luid']
    created_at = payload['created_at']

    project, workbookURL, userName, userEmail  = additionalWorkbookInfo(resource_luid)
    print('running additionalInfo method')

    _subject = '!Workbook Published in UAT!'

    _message = '''
    
    A workbook has just been published. Please see below for more details.

    Resource: {}
    Event Type: {}
    Resource Name: {}
    Project: {}
    Created AT: {}
    URL: {}
    Owner's Name: {}
    Owner's Email: {}
    
    Please promote or deny with workbook and inform the owner
    
    Thank you
    
    '''.format(resource,event_type,resource_name,project,created_at,workbookURL,userName,userEmail)

    print('Email message created')
    print(_message)

    if project == 'UAT':
        email(_message,_subject)
        print('Project is UAT and email will be sent')

    return 'Success!'


if __name__ == '__main__':
    app.run(host=stuff['host'], port=stuff['port'], debug=True)


