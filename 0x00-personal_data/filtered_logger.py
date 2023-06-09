#!/usr/bin/env python3
"""
Filtered Logger module
"""
import re
import mysql.connector
import os
import logging
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    for f in fields:
        message = re.sub(fr'{f}=.+?{separator}', f'{f}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filters incoming records using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database
    """
    return mysql.connector.connect(
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'root'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'),
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'localhost'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''))


def main():
    """takes no arguments and returns nothing.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={}; \
            ip={}; last_login={}; user_agent={}; ".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
