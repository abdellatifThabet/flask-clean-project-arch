import os

from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def load_fixture_from_file(db_session: Session, file_name: str):
    # Get the current working directory
    cwd = os.getcwd()

    sql_file = open(os.path.join(cwd, 'tests/fixtures', file_name), 'r')

    query = text(sql_file.read())

    sql_file.close()

    db_session.execute(query)