from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
#from flask.ext.jsonpify import jsonify
from flask import jsonify

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID



class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Places(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select placename,hotelname,hoteldesc,rating,hotellink from places p , hotels s where p.placeid=s.placeid") # This line performs query and returns json result
        return {'places': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} # Fetches first column that is Employee ID   

parser = reqparse.RequestParser()
parser.add_argument('placename', type = str)

class Places_Name(Resource):
    def get(self, placename):
        conn = db_connect.connect() # connect to database
        #query = conn.execute("select placename,hotelname,hoteldesc,rating,hotellink from places p , hotels s where p.placeid=s.placeid and  p.placename ='pune'") # This line performs query and returns json result
        query = conn.execute("select placename,hotelname,hoteldesc,rating,hotellink from places p , hotels s where p.placeid=s.placeid and  p.placename ='" + placename + "'") # This line performs query and returns json result
        print(query)
        return {'places': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} # Fetches first column that is Employee ID        

class Places_Tag(Resource):
    def get(self, placename):
        conn = db_connect.connect() # connect to database
        #query = conn.execute("select placename,hotelname,hoteldesc,rating,hotellink from places p , hotels s where p.placeid=s.placeid and  p.placename ='pune'") # This line performs query and returns json result
        query = conn.execute("select placename as place,hotelname as tagname,hoteldesc as tagdesc,rating as tagrating,hotellink as taglink,'hotel' as tag from places p , hotels s where p.placeid=s.placeid and  p.placename ='" + placename + "' union select placename as place,templename as tagname,templedesc as tagdesc,'0' as tagrating,templelink as taglink,'historic' as tag from places p , temples s where p.placeid=s.placeid and  p.placename ='" + placename + "'")
        # This line performs query and returns json result
        return {'places': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} # Fetches first column that is Employee ID        


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
api.add_resource(Places, '/places') # Route_4
api.add_resource(Places_Name, '/places/<placename>') # Route_5
api.add_resource(Places_Tag, '/placestag/<placename>') # Route_5


if __name__ == '__main__':
     app.run(port='5002')
     