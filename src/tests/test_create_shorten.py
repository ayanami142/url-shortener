import json

from src.tests.base_test import BaseTestCase
from src.urls.models import Url

TEST_URL = "https://google.com"


class TestCreateShorten(BaseTestCase):
    def test_create_shorten(self):
        """Test generated response and status code with valid input"""
        response = self.client.post(
            "/shorten_url",
            headers=self.headers,
            data=json.dumps({"url": TEST_URL}),
        )

        excepted = Url.generate_short_url_from_link(TEST_URL)

        self.assertIn(excepted, str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_empty_shorten(self):
        """Test generated response and status code with empty input"""
        response = self.client.post(
            "/shorten_url",
            headers=self.headers,
            data=json.dumps({"url": ""}),
        )

        expected_error = "Url can not be empty"

        self.assertIn(expected_error, str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_invalid_shorten(self):
        """Test generated response and status code with invalid input"""
        """Test generated response and status code with empty input"""
        response = self.client.post(
            "/shorten_url",
            headers=self.headers,
            data=json.dumps({"url": "not valid url"}),
        )

        expected_error = "Url should be valid"

        self.assertIn(expected_error, str(response.data))
        self.assertEqual(response.status_code, 400)
