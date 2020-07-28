import psycopg2

CONECTIONPG = psycopg2.connect(dbname='postgres', user='postgres',
                            password='postgres', host='localhost', port='5433')
