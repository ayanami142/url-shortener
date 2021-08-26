from unittest import TestCase

from src.app import create_app
from src.db import db


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.app = create_app(test=True)
        self.db = db
        self.db.create_all()
        self.client = self.app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
