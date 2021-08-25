from src.tests.base_test import BaseTestCase
from src.urls.models import Url


class TestGetBaseUrl(BaseTestCase):
    def setUp(self) -> None:
        super(TestGetBaseUrl, self).setUp()

        shorten = Url(base_address="https://google.com")
        short_url = shorten.generate_short_url()
        shorten.id = short_url

        self.db.session.add(shorten)
        self.db.session.commit()

    def test_get_valid_shorten(self):
        """Get base url and redirect status code from valid shorten"""
        shorten = Url.query.first()

        response = self.client.get("/" + shorten.id)

        self.assertEqual(response.status_code, 302)

    def test_get_invalid_shorten(self):
        """Get an error when shorten is invalid"""
        invalid_shorten = "qwerty12345"
        expected_error = "Short code was not found"

        response = self.client.get("/" + invalid_shorten)

        self.assertIn(expected_error, str(response.data))
        self.assertEqual(response.status_code, 404)
