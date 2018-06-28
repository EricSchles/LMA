from app import models, db

data = models.FAATwitter.query.all()

[db.session.delete(datum) for datum in data]
db.session.commit()
