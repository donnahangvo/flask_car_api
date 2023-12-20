from flask import Blueprint, render_template
from flask_login import current_user

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    user = current_user
    return render_template('profile.html', user = user)