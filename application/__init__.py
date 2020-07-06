from flask import Flask


app = Flask(__name__)
app.static_folder = 'static'


from application import routes


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)