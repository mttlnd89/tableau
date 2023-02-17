from flask import Flask, request
import smtplib
from smtplib import SMTPException
from email.message import EmailMessage
import tableauserverclient as TSC
import yaml
from emailAlerts import Email
from workbook import Workbook
from datasource import Datasource

app = Flask(__name__)

@app.route('/failedworkbookrefresh', methods = ['Post'])
def workbookrefreshfail():
    payload = request.get_json()
    print(payload)

    workbookObj = Workbook()
    lastRefresh, url, userName, userEmail = workbookObj.additionalWorkbookInfo(payload['resource_luid'])
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
    
    '''.format(payload['resource'],payload['event_type'],payload['resource_name'],payload['created_at'],lastRefresh,url,userName,userEmail)

    print('Email message created')
    print(_message)

    email = Email()
    email.emailMessage(_message, _subject)

    return 'Success!'


@app.route('/failedDatasourceRefresh', methods = ['Post'])
def failedDatasourceRefresh():
    payload = request.get_json()
    print(payload)


    datasourceObj = Datasource()
    lastRefresh, url, userName, userEmail = datasourceObj.additionalDatasourceInfo(payload['resource_luid'])
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
    
    '''.format(payload['resource'],payload['event_type'],payload['resource_name'],payload['created_at'],lastRefresh,url,userName,userEmail)

    print('Email message created')
    print(_message)
    
    email = Email()
    email.emailMessage(_message, _subject)

    return 'Success!'


@app.route('/publishWorkbook', methods = ['Post'])
def publishWorkbook():
    payload = request.get_json()
    print(payload)

    workbookObj = Workbook()
    project, workbookURL, userName, userEmail  = workbookObj.additionalWorkbookInfo(payload['resource_luid'])
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
    
    '''.format(payload['resource'],payload['event_type'],payload['resource_name'],project,payload['created_at'],workbookURL,userName,userEmail)

    print('Email message created')
    print(_message)

    if project == 'UAT':
        email = Email()
        email.emailMessage(_message, _subject)
        print('Project is UAT and email will be sent')

    return 'Success!'


#if __name__ == '__main__':
#    app.run(host=stuff['host'], port=stuff['port'], debug=True)


