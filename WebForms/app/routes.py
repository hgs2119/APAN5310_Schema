from flask import render_template

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


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/newcase', methods=['GET', 'POST'])
def newcase():
    form = NewCaseForm()
    if form.validate_on_submit():
# define variables
        investigation_product = form.investigation_product.data
        ad_investigation_number = form.ad_investigation_number.data
        ad_country = form.ad_country.data
        cvd_investigation_number = form.cvd_investigation_number.data
        cvd_country = form.cvd_country.data
        commodity_code = form.commodity_code.data
        petitioner_firm_name = form.petitioner_firm_name.data
        law_firm_name = form.law_firm_name.data
        law_firm_lead = form.law_firm_lead.data
# assign values to load
        # create lists for countries,  investigation numbers, scope codes
        ad_no_list = ad_investigation_number.split(",")
        ad_cty_list = ad_country.split(",")
        cvd_no_list = cvd_investigation_number.split(",")
        cvd_cty_list = cvd_country.split(",")
        scope_list = commodity_code.split(",")
        # assign investigation title
        investigation_countries = ", ".join(set(ad_country.split(", ")+cvd_country.split(", ")))
        investigation_title = str(investigation_product+" "+investigation_countries)
        # get or write product code, product_id
        new_product = Products(product_name=investigation_product)
        db.session.add(new_product)
        db.session.flush()
        product_id = new_product.product_id
        # assign group and get id
        new_group = Case_Groups(product_from_countries=investigation_title, product_id=product_id)
        db.session.add(new_group)
        db.session.flush()
        group_id=new_group.group_id
        # write investigations
        # AD investigations
        for i in range (0, len(ad_no_list)):
            investigation_number = "731-TA-"+ad_no_list[i].strip()
            country_name = ad_cty_list[i].strip()
            country_code = db.session.query(Country.country_code).filter_by(country_name = country_name).first()
            new_investigation = Investigations(investigation_number=investigation_number, country_code=country_code['country_code'], product_id=product_id, group_id=group_id, investigation_title=investigation_title)
            db.session.add(new_investigation)
        # CVD investigations
        for i in range (0, len(cvd_no_list)):
            investigation_number = "701-TA-"+cvd_no_list[i].strip()
            country_name = cvd_cty_list[i].strip()
            country_code = db.session.query(Country.country_code).filter_by(country_name = country_name).first()
            new_investigation = Investigations(investigation_number=investigation_number, country_code=country_code['country_code'], product_id=product_id, group_id=group_id, investigation_title=investigation_title)
            db.session.add(new_investigation)
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
        ad_investigation_number = form.ad_investigation_number.data
        ad_determination = form.ad_determination.data
        cvd_investigation_number = form.cvd_investigation_number.data
        cvd_determination = form.cvd_determination.data
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
        db.session.commit()
    return render_template("updatecase.html", form=form)

@app.route('/investigations', methods=['GET', 'POST'])
def investigations():
    investigations = Investigations.query.all()
    return render_template("investigations.html", investigations=investigations)
