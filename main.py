from website.initdb import initialize 
from website import app
import os

DB_host = "localhost"
DB_name = "auction"
DB_user = "postgres"
DB_password = "asd"

HEROKU = False
if __name__ == '__main__':

    if not HEROKU:
        os.environ['DATABASE_URL'] = "dbname='{}' user='{}' \
        host='{}' password={}".format(DB_name, DB_user, DB_host, DB_password)
        initialize(os.environ.get('DATABASE_URL'))

        app.run(debug=True)
    else:
        app.run()    

    
