from .shared import db

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(50))
    openness = db.Column(db.Integer)
    conscientiousness = db.Column(db.Integer)
    extrovertedness = db.Column(db.Integer)
    agreeableness = db.Column(db.Integer)
    empathy = db.Column(db.Integer)
    playlist = db.Column(db.String(255))

    def __repr__(self):
        return '<Recommendation %s>' % self.handle
