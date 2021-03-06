import sqlite3
from datetime import date

import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from flaskr.sql_helper import count_users, user_set


def get_db() -> sqlite3.Connection:
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

        # add a custom function to the database
        g.db.create_function("count_users", 1, count_users)

    return g.db


def close_db(e=None) -> None:
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db() -> None:
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def populate_db() -> None:
    """Push fake data to the database."""
    from faker import Faker

    db = get_db()
    db.execute("INSERT INTO user (username, password, dateOfBirth, admin) VALUES (?, ?, ?, ?)",
               ("admin", generate_password_hash("admin"), date(2000, 1, 1), 1))

    db.execute("INSERT INTO user (username, password, dateOfBirth) VALUES (?, ?, ?)",
               ("user", generate_password_hash("user"), date(2000, 1, 1)))

    faker = Faker('fr_FR')

    for user_id in range(2, 13):
        profile = faker.simple_profile()

        db.execute("INSERT INTO user (username, password, dateOfBirth, email) VALUES (?, ?, ?, ?)",
                   (profile["username"], generate_password_hash(faker.password()),
                    profile["birthdate"], profile["mail"]))

        db.execute("INSERT INTO post (body, author_id) VALUES (?, ?)", (faker.sentence(), user_id))

    db.commit()


@click.command("populate-db")
@with_appcontext
def populate_db_command() -> None:
    """Push fake data to the database."""
    populate_db()
    click.echo("populated the database.")


def init_app(app: Flask) -> None:
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
