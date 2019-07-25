# Make ERD

This is a little python script to generate an ER diagram by connecting to the database and reading the metadata. It makes use of `sqlalchemy_schemadisplay`. It can output in PNG, PDF or SVG format.

## Arguments

* **`-d/--database`** - The name of the database to connect to [Required].
* **`-i/--host`** - The IP address of the server hosting the database [Required].
* **`-p/--port`** - The port for the database connection [Required].
* **`-u/--user`** - The username for the database connection [Required].
* **`-w/--password`** - The password for the database connection [Required].
* **`-s/--schema`** - The schema containing the tables to be drawn. If none is given then sqlalchemy seems to default to `public`.
* **`-o/--file`** - The filename to save the diagram to. If none is given then a pdf file is created in a temporary folder.
* **`-x/--exclude`** - A space separated list of table names to be excluded from the diagram.

## Requirements

This works nicely on Python 3.7, and requires:

```
psycopg2==2.8.3
pydot==1.4.1
pyparsing==2.4.1.1
SQLAlchemy==1.3.6
sqlalchemy-schemadisplay==1.3
```

## Example

![Example ERD]()
