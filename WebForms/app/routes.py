from flask import render_template
from sqlalchemy import func

from app import app, db
from app.forms import NewCaseForm
from app.forms import UpdateCaseForm
from app.models import LawFirms
from app.models import Products
from app.models import Country
from app.models import Case_Groups
from app.models import Investigations
from app.models import Petitioners
from app.models import Representations
from app.models import Date_Dim
from app.models import Determinations
from app.models import Scopes
from app.models import Publications
from app.models import ITC_Staff
from app.models import Staff_assigned


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/newcase', methods=['GET', 'POST'])
def newcase():
    form = NewCaseForm()
    if form.validate_on_submit():
# define variables
        investigation_product = form.investigation_product.data
        # handle nones in investigation number lists
        if  form.ad_investigation_number.data is not None and form.ad_country.data is not None :
            ad_investigation_number = form.ad_investigation_number.data
            ad_country = form.ad_country.data
            ad_no_list = ad_investigation_number.split(",")
            ad_cty_list = ad_country.split(",")
        else :
            ad_investigation_number = None
            ad_country = None
        if  form.cvd_investigation_number.data is not None and form.cvd_country.data is not None :
            cvd_investigation_number = form.cvd_investigation_number.data
            cvd_country = form.cvd_country.data
            cvd_no_list = cvd_investigation_number.split(",")
            cvd_cty_list = cvd_country.split(",")
        else :
            cvd_investigation_number = None
            cvd_country = None
        commodity_code = form.commodity_code.data
        petitioner_firm_name = form.petitioner_firm_name.data
        law_firm_name = form.law_firm_name.data
        law_firm_lead = form.law_firm_lead.data
        scope_codes = commodity_code.replace('.','')
        scope_list = scope_codes.split(",")
        # assign investigation title
        investigation_countries = ", ".join(set(ad_cty_list+cvd_cty_list))
        investigation_title = str(investigation_product+" "+investigation_countries)
        # get or write product code, product_id
        product_id_query = db.session.query(Products.product_id).filter_by(product_name = investigation_product).first()
        if product_id_query is None:
            new_product = Products(product_name=investigation_product)
            db.session.add(new_product)
            db.session.flush()
            product_id = new_product.product_id
        else:
            product_id = product_id_query['product_id']
        # assign group and get id
        new_group = Case_Groups(product_from_countries=investigation_title, product_id=product_id)
        db.session.add(new_group)
        db.session.flush()
        group_id=new_group.group_id
        # write investigations
        # AD investigations
        if ad_investigation_number is not None:
            for i in range (0, len(ad_no_list)):
                investigation_number = "731-TA-"+ad_no_list[i].strip()
                country_name = ad_cty_list[i].strip()
                country_code = db.session.query(Country.country_code).filter_by(country_name = country_name).first()
                new_investigation = Investigations(investigation_number=investigation_number, country_code=country_code['country_code'], product_id=product_id, group_id=group_id, investigation_title=investigation_title)
                db.session.add(new_investigation)
        # CVD investigations
        if cvd_investigation_number is not None:
            for i in range (0, len(cvd_no_list)):
                investigation_number = "701-TA-"+cvd_no_list[i].strip()
                country_name = cvd_cty_list[i].strip()
                country_code = db.session.query(Country.country_code).filter_by(country_name = country_name).first()
                new_investigation = Investigations(investigation_number=investigation_number, country_code=country_code['country_code'], product_id=product_id, group_id=group_id, investigation_title=investigation_title)
                db.session.add(new_investigation)
        # write scope
        for j in range (0,len(scope_list)):
            hs_code = scope_list[j].strip()
            new_scope_code = Scopes(group_id=group_id, hs_code = hs_code)
            db.session.add(new_scope_code)
        # write petitioners
        new_petitioner = Petitioners(firm_name=petitioner_firm_name, group_id=group_id)
        db.session.add(new_petitioner)
        # write law firm
        new_law_firm = LawFirms(firm_name=law_firm_name, lead=law_firm_lead)
        db.session.add(new_law_firm)
        # write representations
        new_representation = Representations(petitioner_name=petitioner_firm_name, group_id=group_id, law_firm_name=law_firm_name, law_lead=law_firm_lead)
        db.session.add(new_representation)
        # commit changes
        db.session.commit()
    return render_template("newcase.html", form=form)

@app.route('/updatecase', methods=['GET', 'POST'])
def updatecase():
    form = UpdateCaseForm()
    if form.validate_on_submit():
        pub_no = form.pub_no.data
        phase = form.phase.data
        investigation_number = form.investigation_number.data
        determination = form.determination.data
        itc_investigator_name = form.itc_investigator_name.data
        itc_analyst_name = form.itc_analyst_name.data
        itc_economist_name = form.itc_economist_name.data
        itc_accountant_name = form.itc_accountant_name.data
        itc_statistician_name = form.itc_statistician_name.data
        itc_attorney_name = form.itc_attorney_name.data
        itc_sup_investigator_name = form.itc_sup_investigator_name.data
        itc_staff_name = form.itc_staff_name.data
        itc_staff_role = form.itc_staff_role.data
        hearing_date = form.hearing_date.data
        # find group from investigation number
        group_id = db.session.query(Investigations.group_id).filter_by(investigation_number = investigation_number).first()
        # generate list of all associated investigations
        investigation_list = db.session.query(Investigations.investigation_number).filter_by(group_id = group_id).all()
        # iterate over investigation list
        for i in range(0,len(investigation_list)):
            investigation_number_write = investigation_list[i]
        # write publication
            new_publication = Publications(pub_no=pub_no, investigation_number=investigation_number_write, phase=phase)
            db.session.add(new_publication)
        # write determination
            new_determination = Determinations(investigation_number=investigation_number_write, phase=phase, hearing_date=hearing_date, determination=determination)
            db.session.add(new_determination)
        # write ITC Staff and assignments
        itc_name_list = [itc_investigator_name, itc_analyst_name, itc_economist_name, itc_accountant_name, itc_statistician_name, itc_attorney_name, itc_sup_investigator_name]
        itc_role_list = ['investigator', 'analyst', 'economist', 'accountant', 'statistician', 'attorney', 'supervisory investigator']
        if itc_staff_name is not None:
            itc_name_list.append(itc_staff_name)
            itc_role_list.append(itc_staff_role)
        for j in range(0,len(itc_name_list)):
            query = db.session.query(ITC_Staff.id).filter_by(name=itc_name_list[i]).first()
            if query is None:
                new_staff = ITC_Staff(name=itc_name_list[i], title=itc_role_list[i])
                db.session.add(new_staff)
                db.session.flush()
                staff_id = new_staff.id
                new_assignment = Staff_assigned(group_id=group_id, staff_id = staff_id)
                db.session.add(new_assignment)
            else :
                staff_id = query['id']
                new_assignment = Staff_assigned(group_id=group_id, staff_id = staff_id)
                db.session.add(new_assignment)
        # commit new adds
        db.session.commit()
    return render_template("updatecase.html", form=form)

@app.route('/investigations', methods=['GET', 'POST'])
def investigations():
    investigations = Investigations.query.all()
    return render_template("investigations.html", investigations=investigations)
