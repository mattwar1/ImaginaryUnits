
import logging
from flask import Flask, request, render_template                                    
from flask_restful import Resource, Api, reqparse, inputs                            

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.

# Flask & Flask-RESTful instance variables
app = Flask(__name__) # Core Flask app.                                              
api = Api(app) # Flask-RESTful extension wrapper                                     



# --------------------------------- database -------------------------------------------

state = { 
    0:{},1:{},2:{},3:{} 
    # 0: {
    #       "0013A20040E442D6" : 0,
    #       "0113A20040E442D7" : 1,
    #       "0213A20040E442D8" : 1,
    #       "0313A20040E442D9" : 0,
    # 1: {
    #       "0013B20040E442DA" : 0,
    #       "0013C20040E442DB" : 1,
    #       "0013D20040E442DC" : 1,
    #       "0013E20040E442DD" : 0,
}



# --------------------------------- index site ------------------------------------------


@app.route('/', methods=['GET'])                                                    
def index():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('', data=state)               
    # return 'OK'



# --------------------------------- classes ------------------------------------------

# -------- /v1/parking --------------------

class Parking(Resource):

    def __init__(self):
        self.args_parser = reqparse.RequestParser()                                 
        self.args_parser.add_argument(
            name='floor',  # Name of arguement
            required=True,  # Mandatory arguement
            type=int,                
            help='Parking floor nr here needed',
            default=None)

    def get(self):
        """ Returns all floors of the parking."""
        try:
            return {"floor" : list(state.keys())}
        except:
            return None, 404

    def post(self):
        """Adds new floor. Returns new floor ID."""
        global state    
        args = self.args_parser.parse_args()
        if args.floor in state.keys():
            logger.info("Floor with - ID: " + str(args.floor)+" already exists")
            return None, 409
        state[args.floor] = {}    
        logger.info("Added new floor with - ID: " + str(args.floor))
        return {"floor": args.floor}


# -------- /v1/parking/<floor> ------------

class ParkingFloor(Resource):

    def __init__(self):
        self.args_parser = reqparse.RequestParser()                                 

        self.args_parser.add_argument(
            name='place',  # Name of arguement
            required=True,  # Mandatory arguement
            type=str,                
            help='Parking place adress here needed',
            default=None)

        self.args_parser.add_argument(
            name='status',  # Name of arguement
            required=True,  # Mandatory arguement
            type=inputs.int_range(0, 1),  # Allowed range 0..1                
            help='Parking places status here needed',
            default=None)

    def get(self, floor):
        """ Returns all places from <floor>."""  
        try:
            return {"floor" : state[int(floor)]}
        except:
            return None, 404


    def post(self, floor):
        """Adds new place to <floor>. Returns new places's addres and it's status."""
        global state    

        args = self.args_parser.parse_args() # level, color

        try:
            if args.place in list(state[int(floor)].keys()):
                return "Parking place with such addres already exists", 409
            state[int(floor)][args.place] = args.status
            logger.info("Added new place - ID: " + str(floor) + ", place: " + str(args.place) +", status: " + str(args.status))
            return {args.place : args.status}
        except:
            return None, 404

    def delete(self, floor):
        """Deletes floor <floor>."""
        global state    

        try:
            state.pop(int(floor))
            logger.info("Deleted floor - ID: " + str(floor))
            return {}
        except:
            logger.info("ERROR: There is not floor - ID: " + str(floor))
            return {}, 404



# -------- /v1/parking/<floor>/<place> ------------

class ParkingPlace(Resource):

    def __init__(self):
        self.args_parser = reqparse.RequestParser()                                 

        self.args_parser.add_argument(
            name='status',  # Name of argument
            required=True,  # Mandatory argument
            type=inputs.int_range(0, 1),  # Allowed range 0..100                  
            help='Parking places status here needed',
            default=None)

    def get(self, floor, place):
        """ Returns <place> status from <floor> floor."""
        try:
            return {"place" : state[int(floor)][place]}
        except:
            return None, 404

    def post(self, floor, place):
        """Sets <place> status to <floor> floor. Returns <place> status from <floor> floor."""
        global state    

        args = self.args_parser.parse_args() # status, place
        
        try:
            if place not in list(state[int(floor)].keys()):
                return None, 404

            state[int(floor)][place] = args.status
            return {"place" : state[int(floor)][place]}
        except:
            return None, 404


    def delete(self, floor, place):
        """Deletes <place> from floor <floor>."""
        global state    

        try:
            state[int(floor)].pop(place)
            logger.info("Deleted place " + str(place) + " from floor - ID: " + str(floor))
            return {}
        except:
            logger.info("ERROR: There is not place - ID" + str(place) + " in floor - ID: " + str(floor))
            return {}, 404



# ------------------------------------ register URIs ----------------------------------------

# Register Flask-RESTful resource and mount to server end points
api.add_resource(Parking, '/v1/parking')
api.add_resource(ParkingFloor, '/v1/parking/<floor>') 
api.add_resource(ParkingPlace, '/v1/parking/<floor>/<place>')                          



# ------------------------------------ run server -------------------------------------------------

if __name__ == '__main__':
    app.run(host="192.168.1.107", debug=True)                                            
