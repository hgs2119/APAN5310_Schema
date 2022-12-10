from app import db


class Country(db.Model):
    __tablename__ = 'country'

    country_code = db.Column(db.String(4), primary_key=True)
    country_name = db.Column(db.String(100))
    region = db.Column(db.String(100))
    trade_relationship = db.Column(db.String(50))
    country_rel = db.relationship('Investigations', backref='country', lazy=True)

    def __repr__(self):
        return '<Country {}>'.format(self.country_code)


class Products(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), unique=True)
    product_type = db.Column(db.String(100))
    prod_group_rel = db.relationship('Case_Groups', backref='products', lazy=True, cascade="all, delete")
    prod_investigation_rel = db.relationship('Investigations', backref='products', lazy=True, cascade="all, delete")

    def __repr__(self):
        return '<Product {}>'.format(self.product_id)


class Date_Dim(db.Model):
    __tablename__ = 'date_dim'

    date = db.Column(db.Date, primary_key=True)
    day = db.Column(db.SmallInteger, nullable=False)
    daySuffix = db.Column(db.String(2), nullable=False)
    weekdayname = db.Column(db.String(10), nullable=False)
    weekdayname_short = db.Column(db.String(3), nullable=False)
    month = db.Column(db.SmallInteger, nullable=False)
    monthname = db.Column(db.String(10), nullable=False)
    monthname_short = db.Column(db.String(3), nullable=False)
    quarter = db.Column(db.SmallInteger, nullable=False)
    quartername = db.Column(db.String(6), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mmyyyy = db.Column(db.String(6), nullable=False)
    monthyear = db.Column(db.String(7), nullable=False)

    dets_rel = db.relationship('Determinations', backref='date_dim', lazy=True)

    def __repr__(self):
        return '<Date_Dim {}>'.format(self.date)

class Commodities(db.Model):
    __tablename__ = 'commodities'

    hs_code = db.Column(db.String(10), primary_key=True)
    hs_description = db.Column(db.String(500), nullable=False)
    scope_rel = db.relationship('Scopes', backref='commodities', lazy=True)

    def __repr__(self):
        return '<Commodities {}>'.format(self.hs_code)

class Case_Groups(db.Model):
    __tablename__ = 'case_groups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_from_countries = db.Column(db.String(150), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    inv_group_rel = db.relationship('Investigations', backref='case_groups', lazy=True, cascade="all, delete")
    pet_group_rel = db.relationship('Petitioners', backref='case_groups', lazy=True, cascade="all, delete")
    staff_group_rel = db.relationship('Staff_assigned', backref='case_groups', lazy=True, cascade="all, delete")
 
    def __repr__(self):
        return '<Case_Groups {}>'.format(self.group_id)

class Commissioners(db.Model):
    __tablename__ = 'commissioners'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commissioner_name = db.Column(db.String(150), nullable=False)
    term_begin_date = db.Column(db.Date, db.ForeignKey('date_dim.date'), nullable=False)
    term_end_date = db.Column(db.Date, db.ForeignKey('date_dim.date'))

    term_begin_rel = db.relationship('Date_Dim', foreign_keys=[term_begin_date])
    term_end_rel = db.relationship('Date_Dim', foreign_keys=[term_end_date])

    def __repr__(self):
        return '<Commissioners {}>'.format(self.commissioner_name)

class ITC_Staff(db.Model):
    __tablename__ = 'itc_staff'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    title = db.Column(db.String(150))
    staff_assigned_rel = db.relationship('Staff_assigned', backref='itc_staff', lazy=True)

    def __repr__(self):
        return '<ITC_Staff {}>'.format(self.name)

class LawFirms(db.Model):
    __tablename__ = 'law_firms'

    firm_name = db.Column(db.String(150), primary_key=True)
    lead = db.Column(db.String(150), primary_key=True)
    reps_law_rel = db.relationship('Representations', backref='law_firms', lazy=True)

    def __repr__(self):
        return '<LawFirms {}>'.format(self.firm_name)

class Investigations(db.Model):
    __tablename__ = 'investigations'

    investigation_number = db.Column(db.String(11), primary_key=True)
    country_code = db.Column(db.String(5), db.ForeignKey('country.country_code'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('case_groups.group_id'), nullable=False)
    investigation_title = db.Column(db.String(150))
    inv_pub_rel = db.relationship('Publications', backref='investigations', lazy=True, cascade="all, delete")

    def __repr__(self):
        return '<Investigations {}>'.format(self.investigation_number)


class Petitioners(db.Model):
    __tablename__ = 'petitioners'

    firm_name = db.Column(db.String(150), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('case_groups.group_id'), primary_key=True)
    reps_pet_rel = db.relationship('Representations', backref='petitioners', lazy=True, cascade="all, delete")

    def __repr__(self):
        return '<Petitioners {}>'.format(self.firm_name)

class Determinations(db.Model):
    __tablename__ = 'determinations'

    investigation_number = db.Column(db.String(10), primary_key=True)
    phase = db.Column(db.String(100), db.CheckConstraint("phase IN ('prelim', 'final', 'review')"), primary_key=True)
    hearing_date = db.Column(db.Date, db.ForeignKey('date_dim.date'))
    determination = db.Column(db.String(15), db.CheckConstraint("determination IN ('affirmative', 'negative', 'terminated')"), nullable=False)

    def __repr__(self):
        return '<Determinations {}>'.format(self.investigation_number)

class Publications(db.Model):
    __tablename__ = 'publications'

    pub_no = db.Column(db.String(4), primary_key=True)
    investigation_number = db.Column(db.String(11), db.ForeignKey('investigations.investigation_number'), nullable=False)
    phase = db.Column(db.String(50), db.CheckConstraint("phase IN ('prelim', 'final', 'review')"), nullable = False)
    
    def __repr__(self):
        return '<Publications {}>'.format(self.pub_no)

class Staff_assigned(db.Model):
    __tablename__ = 'staff_assigned'

    group_id = db.Column(db.Integer, db.ForeignKey('case_groups.group_id'), primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('itc_staff.id'), primary_key=True)

    def __repr__(self):
        return '<Staff_assigned {}>'.format(self.group_id)

class Representations(db.Model):
    __tablename__ = 'representations'

    group_id = db.Column(db.Integer, primary_key=True)
    petitioner_name = db.Column(db.String(150), primary_key=True)
    law_firm_name = db.Column(db.String(150), primary_key=True)
    law_lead = db.Column(db.String(150), primary_key=True)
    
    __table_args__ = (db.ForeignKeyConstraint(['group_id', 'petitioner_name'], ['petitioners.group_id', 'petitioners.firm_name']),db.ForeignKeyConstraint(['law_firm_name', 'law_lead'], ['law_firms.firm_name', 'law_firms.lead']),{})

    def __repr__(self):
        return '<Representations {}>'.format(self.group_id)

class Scopes(db.Model):
    __tablename__ = 'scopes'

    group_id = db.Column(db.Integer, db.ForeignKey('case_groups.group_id'), primary_key=True)
    hs_code = db.Column(db.String(10), db.ForeignKey('commodities.hs_code'), primary_key=True)

    def __repr__(self):
        return '<Scopes {}>'.format(self.group_id)