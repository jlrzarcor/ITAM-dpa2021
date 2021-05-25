### Chicago Food Inspections, pass/fail predictions API.
### ITAM, Data Product Arquitecture, Spring 2021.
### Paty Urriza, Octavio Fuentes, Uriel Rangel, Carlos Román, José Luis R. Zárate

# ================================= LIBRARIES  ================================= #

# FLASK imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields

# gral libraries
import os
#import psycopg2



# Special routing for importing custom libraries

# Modify path
old_path = os.getcwd()
path = os.path.realpath('../..')

# Get imports
from src.utils.general import get_pg_service
pg = get_pg_service(path + '/conf/local/credentials.yaml')

#import src.utils.constants as ks
#from src.utils.general import get_db_conn_sql_alchemy


# Reset path
os.path.realpath(old_path)


# ================================= API ================================= #

# Connection to RDS-Postgress chicagofoodinsp db
#db_conn_str = 'postgresql://jl:alan_turing.13@rds-dpa-project.cudydvgqgf80.us-west-2.rds.amazonaws.com:5432/chicagofoodinsp'

# Connection to RDS-Postgress chicagofoodinsp db
#pg = get_pg_service('../../conf/local/credential.yaml')
#db_conn_str = 'postgresql://' + pg['user'] + ':' + pg['password'] + '@' + pg['host'] + ':' + str(pg['port']) + '/' + pg['dbname']
db_conn_str = 'postgresql://{}:{}@{}:{}/{}'.format(pg['user'], pg['password'], pg['host'], str(pg['port']), pg['dbname'])


# create flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn_str
api =  Api(app)

db = SQLAlchemy(app)

# deploy.scores
class Match(db.Model):
    __table_args__ = {'schema':'api'}
    __tablename__ = 'scores'

    ingest_date = db.Column(db.DateTime)
    index = db.Column(db.Integer, primary_key = True)
    aka_name = db.Column(db.String)
    license = db.Column(db.String)
    score = db.Column(db.Float)
    prediction = db.Column(db.Integer)
    
    def __repr__(self):
        return(u'<{self,__class__,__name__}:{self.id}>'.format(self=self))
    

# ======= ======= =======   Models   ======= ======= =======    
# swagger model, marshall outputs    
model = api.model("scores_table", {
    'ingest_date' : fields.DateTime,
    'index' : fields.Integer,
    'aka_name' : fields.String,
    'license' : fields.String,
    'score' : fields.Float,
    'prediction' : fields.Integer
})    


# outputs
model_customer = api.model("search_by_customer", {
    'predictions' : fields.Nested(model)
})


model_insp_dates = api.model("search_by_insp_date", {
    'ingest_date' : fields.DateTime,
    'predictions' : fields.Nested(model)
})

    
# ======= ======= =======   Endpoints   ======= ======= =======
@api.route('/cfi')
class Chicago(Resource):
    def get(self):
        return{'Hello':'Hello World'}
    
    
@api.route('/cfi_license/<string:license>')
class Chicago(Resource):
    @api.marshal_with(model_customer, as_list = True)
    def get(self, license):
        match = Match.query.filter_by(license=license).order_by(Match.score.desc()).limit(1).all()
        predictions = []
        for element in match:
            predictions.append({'ingest_date' : element.ingest_date,
                                'index' : element.index,
                                'aka_name' : element.aka_name,
                                'license' : element.license,
                                'score' : element.score,
                                'prediction' : element.prediction})
        
        return{'license':license,'predictions':predictions}



@api.route('/cfi_prediction_date/<string:ingest_date>')
class Chicago(Resource):
    @api.marshal_with(model_insp_dates, as_list = True)
    def get(self, ingest_date):
        match = Match.query.filter_by(ingest_date=ingest_date).order_by(Match.score.desc())
        predictions = []
        for element in match:
            predictions.append({'ingest_date' : element.ingest_date,
                                'index' : element.index,
                                'aka_name' : element.aka_name,
                                'license' : element.license,
                                'score' : element.score,
                                'prediction' : element.prediction})
        
        return{'license':license,'predictions':predictions}



if __name__ == '__main__':
    app.run(debug = True)
    