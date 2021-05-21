import os

class Settings:
    secret="sajdjsah#@!$#cxbcxbn(*12ssap[s"
    
    #Heroku database settings
    host=os.environ['dbhost']
    database=os.environ['dbname']
    user=os.environ['dbusername']
    password=os.environ['dbpassword']

    #local dev database settings
    # host='localhost'
    # database='furniture'
    # user='root'
    # password='rootpass'