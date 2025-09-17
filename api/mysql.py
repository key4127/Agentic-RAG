from sqlmodel import create_engine, SQLModel
from api.config import DBSettings

db_settings = DBSettings()
sql_url = f'mysql+mysqlconnector://{db_settings.sql_user}:{db_settings.sql_password}' \
          f'@{db_settings.sql_host}:{db_settings.sql_port}/{db_settings.sql_db_name}'
sql_engine = create_engine(sql_url)

def create_sql_db_and_tables():
    SQLModel.metadata.create_all(sql_engine)