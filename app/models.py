from app import db


class URL(db.Model):
    __tablename__ = "urls"

    slug = db.Column(db.String(6), primary_key=True)
    forward_url = db.Column(db.String(2048))

    def __init__(self, slug, forward_url):
        self.slug = slug
        self.forward_url = forward_url

    def __repr__(self):
        return f"<URL {self.slug}>"
