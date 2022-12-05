from app import db


class LawFirms(db.Model):
    __tablename__ = 'law_firms'

    firm_name = db.Column(db.String(255), primary_key=True)
    lead = db.Column(db.String(255), primary_key=True)

    def __repr__(self):
        return '<LawFirms {}>'.format(self.firm_name)
