import csv
from .website.models import City
import click
from flask.cli import with_appcontext
from . import db

#make each row a JSON object
def read_csv_file(filename):
    # sourcery skip: for-append-to-extend, simplify-generator
    rows = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

def populate_database(rows):
    for row in rows:
        city = City(name=row['name'], state=row['state'])
        db.session.add(city)
    db.session.commit()

@click.command('populate-db')
@click.argument('filename')

@with_appcontext
def populate_db_command(filename):
    rows = read_csv_file(filename)
    populate_database(rows)
    click.echo('Database populated successfully!')