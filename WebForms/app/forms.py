from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired


class NewCaseForm(FlaskForm):
    investigation_product = StringField('Product', validators=[DataRequired()])
    ad_investigation_number = StringField('AD Investigation Numbers: integer values beginning 731-TA-, separate with commas')
    ad_country = StringField('AD Investigation Countries, separate with commas')
    cvd_investigation_number = StringField('CVD Investigation Numbers: integer values beginning 701-TA-, separate with commas')
    cvd_country = StringField('CVD Investigation Countries, separate with commas')
    commodity_code = StringField('Scope HTS (0000.00.00.00)')
    petitioner_firm_name = StringField('Petitioner Companies or Coalition Name')
    law_firm_name = StringField('Petitioner Law Firm')
    law_firm_lead = StringField('Petitioner Lead Counsel')
    submit = SubmitField('Submit')

class UpdateCaseForm(FlaskForm):
    pub_no = IntegerField('Publication Number', validators=[DataRequired()])
    phase = SelectField('Investigation Phase', choices=[('prelim','Prelim'), ('final', 'Final'), ('review', 'Sunset Review')])
    ad_investigation_number = StringField('AD Investigation Number(s), separate with commas')
    ad_determination = SelectField('AD Determination', choices=[('','None'), ('affirmative', 'Affirmative'), ('negative', 'Negative'), ('terminated', 'Terminated')])
    cvd_investigation_number = StringField('CVD Investigation Number(s), separate with commas')
    cvd_determination = SelectField('CVD Determination', choices=[('','None'), ('affirmative', 'Affirmative'), ('negative', 'Negative'), ('terminated', 'Terminated')])
    itc_investigator_name = StringField('Investigator', validators=[DataRequired()])
    itc_analyst_name = StringField('Analyst')
    itc_economist_name = StringField('Economist')
    itc_accountant_name = StringField('Accountant')
    itc_statistician_name = StringField('Statistician')
    itc_attorney_name = StringField('Attorney')
    itc_sup_investigator_name = StringField('Supervisory Investigator')
    itc_staff_name = StringField('Other, Name')
    itc_staff_role = StringField('Other, Role')
    hearing_date = DateField('Hearing Date', format='%m-%d-%Y', validators=[DataRequired()])
    submit = SubmitField('Submit')
