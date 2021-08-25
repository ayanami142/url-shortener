import base64
from datetime import datetime

from src.db import db


class Url(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.String(31), primary_key=True)
    base_address = db.Column(db.String(127), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.relationship("View", backref="url", lazy="dynamic")

    def __repr__(self):
        return self.base_address

    def generate_short_url(self, length: int = 10) -> str:
        """
        Generate random string from ascii letters and digits
        :param int length: length of random string, 10 by default
        :return str: generated string
        """
        byte_url = self.base_address.encode("UTF-8")
        return base64.b64encode(byte_url).decode("UTF-8")[len(byte_url) - length :]

    @staticmethod
    def generate_short_url_from_link(url: str = "", length: int = 10) -> str:
        """
        Generate random string from ascii letters and digits
        The same logic like in generate_short_url but as helper static method
        :param url: base url
        :param int length: length of random string, 10 by default
        :return str: generated string
        """
        byte_url = url.encode("UTF-8")
        return base64.b64encode(byte_url).decode("UTF-8")[len(byte_url) - length :]

    def add_view_if_not_exists(self, ip: str) -> None:
        """
        Find existing view with the same url and ip or create new instance
        :param str ip: user ip
        :return: None
        """
        view: View = View.query.filter_by(url_id=self.id, ip=ip).first()
        if not view:
            view = View(url_id=self.id, ip=ip)
            db.session.add(view)
            db.session.commit()


class View(db.Model):
    __tablename__ = "views"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(31), nullable=True)
    url_id = db.Column(db.String(31), db.ForeignKey("urls.id"))

    def __repr__(self):
        return f"{self.url.name} view"
