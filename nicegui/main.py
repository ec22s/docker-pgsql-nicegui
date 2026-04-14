import psycopg2
import random
import string
from nicegui import app, ui
from tortoise.contrib.fastapi import register_tortoise

def main():
  rows = [ { 'id': r[0], 'data': r[1] } for r in fetch_items_data()]
  columns = [
    { 'col_name': 'col_id', 'label':'Id', 'field': 'id' },
    { 'col_name': 'col_data', 'label': 'Data', 'field': 'data' },
  ]
  ui.table(
    columns=columns,
    rows=rows
  ).classes("mx-auto my-auto mt-4")
  ui.run()

def fetch_items_data():
  example_data = [
    ''.join(random.choice(string.ascii_uppercase + string.digits)
    for _ in range(20)) for _ in range(20)
  ]

  cnx = psycopg2.connect("host=db dbname=postgres user=user password=postgres")
  cur = cnx.cursor()
  cur.execute('drop table if exists test')
  cur.execute('''
    create table if not exists test (
      id serial PRIMARY KEY,
      data varchar(20)
    )
  ''')
  for data in example_data:
    cur.execute(f"insert into test (data) values('{data}')")
  cur.execute('select * from test')
  rows = cur.fetchall()
  cur.close()
  cnx.close()
  return rows

main()
