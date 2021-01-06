from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    render_template('home.html', title = 'home')