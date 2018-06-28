from app import models

q = models.FAATwitter.query.yield_per(1).enable_eagerlaods(False)
