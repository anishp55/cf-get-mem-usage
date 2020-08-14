from flask import render_template, flash, redirect, json
from app import app
from app.forms import LoginForm
import json
import helpers as helper


@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    vcap_data = json.loads(app.config['VCAP_APPLICATION'])
    loginUrl = vcap_data['cf_api'].replace("api","login") + '/oauth/token'
    apiUrl = vcap_data['cf_api'] + '{}'
    form = LoginForm()
    if form.validate_on_submit():
        flash(
                'Login requested for user {}'.format(
                 form.username.data, 
                 )
            )
        authHeader = helper.createAuthHeader(helper.getAuth(
                                              loginUrl=loginUrl,
                                              user=form.username.data,
                                              password=form.password.data
                                            )['access_token'])
        return render_template("quota-summary.html", 
                                object=helper.getOrgsSummary(header=authHeader,apiUrl=apiUrl), 
                                quotaData=helper.getQuotas(header=authHeader,apiUrl=apiUrl)
                              )
    return render_template('login.html', title='Sign In', form=form)

@app.route("/health", methods=['GET'])
@app.route("/healthz", methods=['GET'])
def health():
    return "OK"