import tableauserverclient as TSC
import yaml

class Workbook:
    def additionalWorkbookInfo(workbookID):

        with open('secrets.yml','r') as file:
            stuff = yaml.safe_load(file)

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