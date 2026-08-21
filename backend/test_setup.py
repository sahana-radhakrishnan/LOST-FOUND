from app.database.config import settings
from app.database.session import engine
from app.models import Alert, Detection, LostItem, Match


print("Database:", settings.MYSQL_DATABASE)
print("Host:", settings.MYSQL_HOST)
print("Models loaded:")
print("-", LostItem.__tablename__)
print("-", Detection.__tablename__)
print("-", Match.__tablename__)
print("-", Alert.__tablename__)

try:
    with engine.connect() as connection:
        print("MySQL connection: SUCCESS")
except Exception as error:
    print("MySQL connection: FAILED")
    print(error)