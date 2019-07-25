#!/usr/bin/env python3
# Little script to make ER diagrams of specific dbs
from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph
import argparse
import os
import sys
import tempfile
import subprocess

# Parse arguements
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--database', help="Name of db to connect to", required = True)
parser.add_argument('-i', '--host', help="Address of db server", required = True)
parser.add_argument('-p', '--port', help="Port of db server", required = True)
parser.add_argument('-u', '--user', help="Username for connection to db", required = True)
parser.add_argument('-w', '--password', help="Password for connection to db", required = True)
parser.add_argument('-s', '--schema', help="Schema within database to draw")
parser.add_argument('-o', '--file', help="Name of pdf, svg, or png file to export to")
parser.add_argument('-x', '--exclude', help="List of tables to exclude from diagram")
args = parser.parse_args()

# get connection string
db_conn_string =  'postgresql+psycopg2://%s:%s@%s:%s/%s' % (args.user, args.password, args.host, args.port, args.database)

# get connection
try:
    print('-- Connecting to %s on %s:%s' % (args.database, args.host, args.port))
    e = create_engine(db_conn_string)
    m = MetaData()
    if args.schema is not None:
        m.reflect(bind = e, schema = args.schema)
    else:
        m.reflect(bind = e)
    tables_in_db = m.tables.keys()
except Exception as e:
    print('Problems accessing database: %s' % e)
    sys.exit(1)

# remove unwanted tables
if args.exclude is not None:
    if args.exclude is list:
        for t in args.exclude:
            m.remove(m.tables[t])
    else:
        m.remove(m.tables[args.exclude])

# generate the schema graph
graph = create_schema_graph(tables = [m.tables[x] for x in list(m.tables.keys())],
                            show_datatypes=False,
                            show_indexes=False,
                            rankdir='TB',
                            concentrate=True,
                            )

# Write out graph to the corresponding file
if args.file is not None:
    # get file extension
    filename, fileext = os.path.splitext(args.file)
    fn = args.file
    print(fn)
    if fileext == '.pdf':
        graph.write_pdf(fn)
    elif fileext == '.png':
        graph.write_png(fn)
    elif fileext == '.svg':
        graph.write_svg(fn)
    else:
        graph.write_pdf(fn)
else:
    fn = tempfile.mkdtemp() + '/' + args.database + '.pdf'
    graph.write_pdf(fn)

e.dispose()

# open up the file
print('-- Opening %s' % fn)
subprocess.Popen('open %s' % fn, shell=True)
