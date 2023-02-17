import tableauserverclient as TSC
import yaml

class Datasource:
    def additionalDatasourceInfo(datasourceID):

        with open('secrets.yml','r') as file:
            stuff = yaml.safe_load(file)

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