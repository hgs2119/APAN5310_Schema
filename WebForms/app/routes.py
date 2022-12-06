from flask import render_template

from app import app, db
from app.forms import NewCaseForm
from app.forms import UpdateCaseForm
from app.models import LawFirms


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/newcase', methods=['GET', 'POST'])
def newcase():
    form = NewCaseForm()
    if form.validate_on_submit():
        investigation_product = form.investigation_product.data
        ad_investigation_number = form.ad_investigation_number.data
        ad_country = form.ad_country.data
        cvd_investigation_number = form.cvd_investigation_number.data
        cvd_country = form.cvd_country.data
        commodity_code = form.commodity_code.data
        petitioner_firm_name = form.petitioner_firm_name.data
        law_firm_name = form.law_firm_name.data
        law_firm_lead = form.law_firm_lead.data
        new_law_firm = LawFirms(firm_name=law_firm_name, lead=law_firm_lead)
        new_petitioner = Petitioners(firm_name=petitioner_firm_name)
        db.session.add(new_law_firm)
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
        itc_sup_investigator_name = form.itc_sup.investigator_name.data
        itc_staff_name = form.itc_staff_name.data
        itc_staff_role = form.itc_staff_role.data
        hearing_date = form.hearing_date.data
        db.session.commit()
    return render_template("updatecase.html", form=form)

@app.route('/lawfirms', methods=['GET', 'POST'])
def lawfirms():
    law_firms = LawFirms.query.all()
    return render_template("lawfirms.html", law_firms=law_firms)
