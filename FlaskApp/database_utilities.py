from sqlalchemy import create_engine
from flask import Flask
app = Flask(__name__)


def generate_query_from_column_list(table, column_list):
    return "select {} from {}".format(",".join(column_list),table )


def query_database(query):
    """
    query example - "select * from user_details"
    """
    try:
        engine = create_engine("mysql://root@localhost/lba")
        conn = engine.connect()
        results_of_query =  conn.execute(query)
        results = [row for row in results_of_query]
        app.logger.info("{} --- query returned results----- {}".format(query, results))
        conn.close()
        return results
    except Exception as e:
        app.logger.error("Couldn't return results for the query {}. Returning []. Error {}".format(query,e))
        return []



def insert_database(query):
    """
    query example - 'select * from user_details'
    """
    try:
        engine = create_engine("mysql://root@localhost/lba")
        conn = engine.connect()
        conn.execute(query)
        app.logger.info(" ---Insert successful----- {}".format(query))
        conn.close()
    except Exception as e:
        app.logger.error("Couldn't insert results for the query {}. Error {}".format(query,e))
