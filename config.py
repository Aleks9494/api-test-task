import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    #SECRET_KEY = "4598ujrjwoiip[]dmk//?kojkdiou732940imkf;d"
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:12345@localhost:5432/test_db_api"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

