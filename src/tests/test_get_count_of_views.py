from src.tests.base_test import BaseTestCase
from src.urls.models import Url


class TestGetCountOfViews(BaseTestCase):
    def setUp(self) -> None:
        super(TestGetCountOfViews, self).setUp()

        shorten_list = [Url(base_address="https://google.com"), Url(base_address="https://facebook.com"),
                        Url(base_address="https://github.com")]

        views_counter = 10
        for shorten in shorten_list:
            shorten_url = shorten.generate_short_url()
            shorten.id = shorten_url
            self.db.session.add(shorten)
            self.db.session.commit()

            # generate views for each shorten (total 36)
            for i in range(0, views_counter):
                shorten.add_view_if_not_exists(ip=f"127.0.0.{i + views_counter}")
            views_counter += 2

    def test_most_popular_url_by_views(self):
        """Send request and get shortened urls count"""
        response = self.client.get("/shortened_urls_count")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("Number of shortened urls"), 36)
