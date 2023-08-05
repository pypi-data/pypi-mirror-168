import os
import logging
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtGui import QIcon
from jal.constants import Setup
from decimal import Decimal


# FIXME all database calls should be via JalDB (or mate) class. Get rid of SQL calls from other code

# -------------------------------------------------------------------------------------------------------------------
# Return "canonical" string for decimal number
def format_decimal(d) -> str:
    return str(d.normalize())

# Removes exponent and trailing zeros from Decimal number
def remove_exponent(d) -> str:
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


# -------------------------------------------------------------------------------------------------------------------
# Returns absolute path to a folder from where application was started
def get_app_path() -> str:
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep


# -------------------------------------------------------------------------------------------------------------------
def get_dbfilename(app_path):
    return app_path + Setup.DB_PATH


# -------------------------------------------------------------------------------------------------------------------
# returns QIcon loaded from the file with icon_name located in folder Setup.ICONS_PATH
def load_icon(icon_name) -> QIcon:
    return QIcon(get_app_path() + Setup.ICONS_PATH + os.sep + icon_name)


# -------------------------------------------------------------------------------------------------------------------
# This function returns SQLite connection used by JAL or fails with RuntimeError exception
def db_connection():
    db = QSqlDatabase.database(Setup.DB_CONNECTION)
    if not db.isValid():
        raise RuntimeError(f"DB connection '{Setup.DB_CONNECTION}' is invalid")
    if not db.isOpen():
        logging.fatal(f"DB connection '{Setup.DB_CONNECTION}' is not open")
    return db

# -------------------------------------------------------------------------------------------------------------------
# prepares SQL query from given sql_text
# params_list is a list of tuples (":param", value) which are used to prepare SQL query
# Current transactin will be commited if 'commit' set to true
# Parameter 'forward_only' may be used for optimization
# return value - QSqlQuery object (to allow iteration through result)
def executeSQL(sql_text, params=[], forward_only=True, commit=False):
    db = db_connection()
    query = QSqlQuery(db)
    query.setForwardOnly(forward_only)
    if not query.prepare(sql_text):
        logging.error(f"SQL prep: '{query.lastError().text()}' for query '{sql_text}' with params '{params}'")
        return None
    for param in params:
        query.bindValue(param[0], param[1])
    if not query.exec():
        logging.error(f"SQL exec: '{query.lastError().text()}' for query '{sql_text}' with params '{params}'")
        return None
    if commit:
        db.commit()
    return query


# -------------------------------------------------------------------------------------------------------------------
# the same as executeSQL() but after query execution it takes first line of query result and:
# - returns None if no records were fetched by query
# - otherwise returns first row of the query result:
# named = False: result is packed into a list of field values
# named = True: result is packet into a dictionary with field names as keys
# - check_unique = True: checks that only 1 record was returned by query, otherwise returns None
def readSQL(sql_text, params=None, named=False, check_unique=False):
    if params is None:
        params = []
    query = QSqlQuery(db_connection())   # TODO reimplement via ExecuteSQL() call in order to get rid of duplicated code
    query.setForwardOnly(True)
    if not query.prepare(sql_text):
        logging.error(f"SQL prep: '{query.lastError().text()}' for query '{sql_text}' | '{params}'")
        return None
    for param in params:
        query.bindValue(param[0], param[1])
    if not query.exec():
        logging.error(f"SQL exec: '{query.lastError().text()}' for query '{sql_text}' | '{params}'")
        return None
    if query.next():
        res = readSQLrecord(query, named=named)
        if check_unique and query.next():
            return None  # More than one record in result when only one expected
        return res
    else:
        return None


def readSQLrecord(query, named=False):
    if named:
        values = {}
    else:
        values = []
    for i in range(query.record().count()):
        if named:
            values[query.record().fieldName(i)] = query.value(i)
        else:
            values.append(query.value(i))
    if values:
        if len(values) == 1 and not named:
            return values[0]
        else:
            return values
    else:
        return None
