from app import db


class Country(db.Model):
    __tablename__ = 'country'

    country_code = db.Column(db.String(4), primary_key=True)
    country_name = db.Column(db.String(100))
    region = db.Column(db.String(100))
    trade_relationship = db.Column(db.String(50))
    country_rel = db.relationship('Investigations', backref='country', lazy=True)

    def __init__(self, country_code, country_name, region, trade_relationship):
        self.country_code = country_code
        self.country_name = country_name
        self.region = region
        self.trade_relationship = trade_relationship

class Products(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.String(3), primary_key=True)
    product_name = db.Column(db.String(100), unique=True)
    product_type = db.Column(db.String(100))
    prod_group_rel = db.relationship('Case_Groups', backref='products', lazy=True)
    prod_investigation_rel = db.relationship('Investigations', backref='products', lazy=True)

    def __init__(self, product_id, product_name, product_type):
        self.product_id = product_id
        self.product_name = product_name
        self.product_type = product_type

class Date_Dim(db.Model):
    __tablename__ = 'date_dim'

    date = db.Column(db.Date, primary_key=True, nullable=False)
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
    terms_rel = db.relationship('Commissioners', backref='date_dim', lazy=True)
    hearings_rel = db.relationship('Publications', backref='date_dim', lazy=True)

    def __init__(self, date, day, daySuffix, weekdayname, weekdayname_short, month, monthname, monthname_short, quarter, quartername, year, mmyyyy, monthyear):
        self.date = date
        self.day = day
        self.daySuffix = daySuffix
        self.weekdayname = weekdayname
        self.weekdayname_short = weekdayname_short
        self.month = month
        self.monthname = monthname
        self.monthname_short = monthname_short
        self.quarter = quarter
        self.quartername = quartername
        self.year = year
        self.mmyyyy = mmyyyy
        self.monthyear = monthyear

class Commodities(db.Model):
    __tablename__ = 'commodities'

    hs_code = db.Column(db.String(10), primary_key=True)
    hs_description = db.Column(db.String(500), nullable=False)
    scope_rel = db.relationship('Scopes', backref='commodities', lazy=True)

    def __init__(self, hs_code, hs_description):
        self.hs_code = hs_code
        self.hs_description = hs_description 

class Case_Groups(db.Model):
    __tablename__ = 'case_groups'
    group_id = db.Column(db.String(5), primary_key=True)
    product_from_countries = db.Column(db.String(150), nullable=False)
    product_id = db.Column(db.String(3), db.ForeignKey('products.product_id'), nullable=False)
    inv_group_rel = db.relationship('Investigations', backref='case_groups', lazy=True)
    pet_group_rel = db.relationship('Petitioners', backref='case_groups', lazy=True)
    staff_group_rel = db.relationship('Staff_assigned', backref='case_groups', lazy=True)
    reps_group_rel = db.relationship('Representations', backref='case_groups', lazy=True)
 
    def __init__(self, group_id, product_from_countries, product_id):
        self.group_id = group_id
        self.product_from_countries = product_from_countries
        self.product_id = product_id 

class Commissioners(db.Model):
    __tablename__ = 'commissioners'

    id = db.Column(db.String(10), primary_key=True)
    commissioner_name = db.Column(db.String(150), nullable=False)
    term_begin_date = db.Column(db.Date, db.ForeignKey('date_dim.date'), nullable=False)
    term_end_date = db.Column(db.Date, db.ForeignKey('date_dim.date'))

    def __init__(self, id, commissioner_name, term_begin_date, term_end_date):
        self.id = id
        self.commissioner_name = commissioner_name
        self.term_begin_date = term_begin_date
        self.term_end_date = term_end_date

class ITC_Staff(db.Model):
    __tablename__ = 'itc_staff'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(150))
    title = db.Column(db.String(150))
    staff_assigned_rel = db.relationship('Staff_assigned', backref='itc_staff', lazy=True)

    def __init__(self, id, name, title):
        self.id = id
        self.name = name
        self.title = title

class LawFirms(db.Model):
    __tablename__ = 'law_firms'

    firm_name = db.Column(db.String(150), primary_key=True)
    lead = db.Column(db.String(150), primary_key=True)
    reps_law_rel = db.relationship('Representations', backref='law_firms', lazy=True)

    def __init__(self, firm_name, lead):
        self.firm_name = firm_name
        self.lead = lead

    def __repr__(self):
        return '<LawFirms {}>'.format(self.firm_name)

class Investigations(db.Model):
    __tablename__ = 'investigations'

    investigation_number = db.Column(db.String(11), primary_key=True)
    country_code = db.Column(db.String(5), db.ForeignKey('country.country_code'), nullable=False)
    product_id = db.Column(db.String(3), db.ForeignKey('products.product_id'), nullable=False)
    group_id = db.Column(db.String(5), db.ForeignKey('case_groups.group_id'), nullable=False)
    investigation_title = db.Column(db.String(150))
    inv_pub_rel = db.relationship('Publications', backref='investigations', lazy=True)

    def __init__(self, investigation_number, country_code, product_id, group_id, investigation_title):
        self.investigation_number = investigation_number
        self.country_code = country_code
        self.product_id = product_id
        self.group_id = group_id
        self.investigation_title = investigation_title

class Petitioners(db.Model):
    __tablename__ = 'petitioners'

    firm_name = db.Column(db.String(150), primary_key=True)
    group_id = db.Column(db.String(5), db.ForeignKey('case_groups.group_id'), primary_key=True)
    reps_pet_rel = db.relationship('Representations', backref='petitioners', lazy=True)

    def __init__(self, firm_name, group_id):
        self.firm_name = firm_name
        self.group_id = group_id

class Determinations(db.Model):
    __tablename__ = 'determinations'

    investigation_number = db.Column(db.String(10), primary_key=True)
    phase = db.Column(db.String(100), db.CheckConstraint("phase IN ('prelim', 'final', 'review')"), primary_key=True)
    hearing_date = db.Column(db.Date), db.ForeignKey('date_dim.date')
    determination = db.Column(db.String(15), db.CheckConstraint("determination IN ('affirmative', 'negative', 'terminated')", nullable=False))

    def __init__(self, investigation_number, phase, hearing_date, determination):
        self.investigation_number = investigation_number
        self.phase = phase
        self.hearing_date = hearing_date
        self.determination = determination

class Publications(db.Model):
    __tablename__ = 'publications'

    pub_no = db.Column(db.String(4), primary_key=True)
    investigation_number = db.Column(db.String(11), db.ForeignKey('investigations.investigation_number'), nullable=False)
    phase = db.Column(db.String(50), db.CheckConstraint("phase IN ('prelim', 'final', 'review')"), nullable = False)
    
    def __init__(self, pub_no, investigation_number, phase):
        self.pub_no = pub_no
        self.investigation_number = investigation_number
        self.phase = phase

class Staff_assigned(db.Model):
    __tablename__ = 'staff_assigned'
    group_id = db.Column(db.String(5), db.ForeignKey('case_groups.group_id'), primary_key=True)
    staff_id = db.Column(db.String(10), db.ForeignKey('itc_staff.id'), primary_key=True)

    def __init__(self, group_id, staff_id):
        self.group_id = group_id
        self.staff_id = staff_id

class Representations(db.Model):
    __tablename__ = 'representations'
    group_id = db.Column(db.String(5), db.ForeignKey('case_groups.group_id'), primary_key=True)
    petitioner_name = db.Column(db.String(150), db.ForeignKey('petitioners.firm_name'), primary_key=True)
    law_firm_name = db.Column(db.String(150), db.ForeignKey('law_firms.firm_name'), primary_key=True)
    law_lead = db.Column(db.String(150), db.ForeignKey('law_firms.lead', nullable=False))

    def __init__(self, group_id, petitioner_name, law_firm_name, law_lead):
        self.group_id = group_id
        self.petitioner_name = petitioner_name
        self.law_firm_name = law_firm_name
        self.law_lead = law_lead

class Scopes(db.Model):
    __tablename__ = 'scopes'

    group_id = db.Column(db.String(5), db.ForeignKey('case_groups.group_id'), primary_key=True, nullable=False)
    hs_code = db.column(db.String(10), db.ForeignKey('commodities.commodity_code'), primary_key=True, nullable=False)

    def __init__(self, group_id, hs_code):
        self.group_id = group_id
        self.hs_code = hs_code