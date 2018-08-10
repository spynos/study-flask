import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.case import CaseModel

class Case(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('birth',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('library_id',
        type=int,
        required=True,
        help="Every case should have a library id!"
    )

    @jwt_required()
    def get(self, name):
        case = CaseModel.find_by_name(name)
        if case:
            return case.json()
        return {'message': 'Case not found'}, 404

    def post(self, name):  #error first approach
        if CaseModel.find_by_name(name):
            return {'message': "An case with name '{}' is aleady exist.".format(name)}, 400 #bad request

        data = Case.parser.parse_args()

        case = CaseModel(name, **data)

        try:
            case.save_to_db()
        except:
            return {"message": "An error occured inserting the case."}, 500 #internal server error

        return case.json(), 201 #created

    def delete(self, name):
        case = CaseModel.find_by_name(name)
        if case:
            case.delete_from_db()

        return {'message': 'Case deleted'}

    def put(self, name):
        data = Case.parser.parse_args()

        case = CaseModel.find_by_name(name)

        if case is None:
            case = CaseModel(name, **data)
        else:
            case.birth = data['birth']

        case.save_to_db()

        return case.json()


class CaseList(Resource):
    def get(self):
        return {'cases': [x.json() for x in CaseModel.query.all()]} #list(map(lambds x: x.json(), CaseModel.query.all()))
