import pytest
from app import create_app, db
from app.models import Task
from config import Config


@pytest.fixture(scope='session')
def testapp():         # создание приложения и БД
    _app = create_app()
    _app.config.from_object(Config)
    _app.config.update({'SQLALCHEMY_DATABASE_URI': "postgresql+psycopg2://postgres:12345@localhost:5432/test_db_api"})
    _app.config.update({"SECRET_KEY": "4598ujrjwoiip[]dmk//?kojkdiou732940imkf;d"})
    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def task(testapp):
    task = Task(title='Task # 1', body='Body of task # 1', date_to_do='2022-05-30')
    db.session.add(task)
    db.session.commit()

    return task
