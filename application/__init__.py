from flask import Flask
from flask_mail import Mail

mail = Mail()

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'autoqpcr@gmail.com'
app.config["MAIL_PASSWORD"] = 'neuroeddu'
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

from application import routes


if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost', port=8080)