from decimal import Decimal
from http import HTTPStatus
from flask import Flask, g, request, json
from flasgger import Swagger
from api import endpoints
from pymssql import connect as mssql_connect

class CustomJSONEncoder(json.JSONEncoder):
   def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

app = Flask(__name__)
app.config.from_json('../config.json')
app.json_encoder = CustomJSONEncoder
[app.register_blueprint(endpoint) for endpoint in endpoints()]
Swagger(app)

@app.errorhandler(500)
def internal_server_errror(error):
    if '/api/' in request.path:
        return { 'message': str(error.original_exception) }

@app.before_request
def before_request():
    if '/api/' in request.path:
        g.wbc_db = mssql_connect(
            server=app.config['WBC']['HOST'],
            user=app.config['WBC']['USER'],
            password=app.config['WBC']['PASSWORD'],
            database=app.config['WBC']['DATABASE'],
            as_dict=True
        )

@app.teardown_appcontext
def teardown_appcontext(error):
    if hasattr(g, 'wbc_db'):
        g.wbc_db.close()

if __name__ == '__main__':
    app.run()
