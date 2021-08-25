from src.tests.base_test import BaseTestCase
from src.urls.models import Url, View
from random import randint


class TestGetTop10Urls(BaseTestCase):
    def setUp(self) -> None:
        super(TestGetTop10Urls, self).setUp()

        self.urls_list = [
            "https://google.com",
            "https://facebook.com",
            "https://amazon.com",
            "https://twitch.tv",
            "https://github.com",
            "https://python.com",
            "https://flask.com",
            "https://django.com",
            "https://shorten.com",
            "https://yahoo.com",
            "https://microsoft.com",
            "https://twitter.com",
        ]

        # generate shortens list objects from urls list
        shortens_list = [Url(base_address=url) for url in self.urls_list]

        view_counter = 15  # generate 15 view for first shorten
        # create Url instances for tests
        for shorten in shortens_list:
            shorten_url = shorten.generate_short_url()
            shorten.id = shorten_url
            self.db.session.add(shorten)
            self.db.session.commit()

            # generate {counter}" number of views for each shorten with random ip
            for _ in range(1, view_counter):
                shorten.add_view_if_not_exists(ip=f"127.0.{randint(0, 100)}.{randint(0, 100)}")
            view_counter -= 1

    def test_get_ten_urls_from_top(self):
        """Get top 10 urls by views and compare with initial list"""
        response = self.client.get("/top10", headers=self.headers)

        response_list = response.json.get("Most popular urls")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_list, ", ".join(self.urls_list[:10]))
