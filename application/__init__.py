from flask import Flask


app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


from application import routes


if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1', port=5000)