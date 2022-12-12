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
    phase = SelectField('Investigation Phase', choices=[('prelim','Prelim'), ('final', 'Final'), ('review', 'Sunset Review')], validators=[DataRequired()])
    investigation_number = StringField('AD Investigation Number(s), separate with commas', validators=[DataRequired()])
    determination = SelectField('AD Determination', choices=[('','None'), ('affirmative', 'Affirmative'), ('negative', 'Negative'), ('terminated', 'Terminated')], validators=[DataRequired()])
    itc_investigator_name = StringField('Investigator', validators=[DataRequired()])
    itc_analyst_name = StringField('Analyst', validators=[DataRequired()])
    itc_economist_name = StringField('Economist', validators=[DataRequired()])
    itc_accountant_name = StringField('Accountant', validators=[DataRequired()])
    itc_statistician_name = StringField('Statistician', validators=[DataRequired()])
    itc_attorney_name = StringField('Attorney', validators=[DataRequired()])
    itc_sup_investigator_name = StringField('Supervisory Investigator', validators=[DataRequired()])
    itc_staff_name = StringField('Other, Name')
    itc_staff_role = StringField('Other, Role')
    hearing_date = DateField('Hearing Date')
    submit = SubmitField('Submit')
