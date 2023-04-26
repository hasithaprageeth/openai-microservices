import os

MYSQL_HOST = os.getenv('MYSQL_HOST', 'database-1.c1hflofbzezz.eu-west-2.rds.amazonaws.com')
MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
MYSQL_USER = os.getenv('MYSQL_USER', 'admin')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'NH8jdEG6mEWtfJJZK9wL')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'completion_service_db_dev')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')
SECRET_KEY = os.getenv('API_KEY', "a&9X5R4^wsyjKf28GhPxz#N#v6C$L@!")
MODEL_ENGINE = "gpt-3.5-turbo"


class SQLConfig:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
