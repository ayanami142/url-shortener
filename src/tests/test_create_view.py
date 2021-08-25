import json

from src.tests.base_test import BaseTestCase
from src.urls.models import Url, View


class TestView(BaseTestCase):
    def setUp(self) -> None:
        super(TestView, self).setUp()

        shorten = Url(base_address="https://google.com")
        self.short_url = shorten.generate_short_url()
        shorten.id = self.short_url

        view1 = View(url_id=shorten.id, ip="127.0.0.1")
        view2 = View(url_id=shorten.id, ip="127.0.0.2")

        self.db.session.add(shorten)
        self.db.session.add(view1)
        self.db.session.add(view2)
        self.db.session.commit()

    def test_add_view_for_existing_shorten_with_existing_ip(self):
        """Assert that url view not adds to url when url has view with the same ip"""
        views_count_before = View.query.filter_by(url_id=self.short_url).count()
        shorten = Url.query.filter_by(id=self.short_url).first()
        shorten.add_view_if_not_exists(ip="127.0.0.1")
        views_count_after = View.query.filter_by(url_id=self.short_url).count()

        self.assertEqual(views_count_before, views_count_after)

    def test_add_view_for_existing_shorten_with_new_ip(self):
        """Asert that url view adds to url when url hasn't view with the same ip"""
        views_count_before = View.query.filter_by(url_id=self.short_url).count()
        shorten = Url.query.filter_by(id=self.short_url).first()
        shorten.add_view_if_not_exists(ip="127.0.0.3")
        views_count_after = View.query.filter_by(url_id=self.short_url).count()

        self.assertNotEqual(views_count_before, views_count_after)

    def test_adding_view_for_new_shorten(self):
        """Assert that view adds to url when url has been created"""
        response = self.client.post("/shorten_url", data=json.dumps({"url": "facebook.com"}), headers=self.headers)
        new_shorten = response.json.get("shortened_url").split("/")[-1]
        views_count = View.query.filter_by(url_id=new_shorten).count()

        self.assertGreater(views_count, 0)
