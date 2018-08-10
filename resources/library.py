from flask_restful import Resource
from models.library import LibraryModel

class Library(Resource):
    def get(self, name):
        library = LibraryModel.find_by_name(name)
        if library:
            return library.json()
        return {'message': 'Library not found'}, 404

    def post(self, name):
        if LibraryModel.find_by_name(name):
            return {'message': "A library with name '{}' already exists.".format(name)}, 400

        library = LibraryModel(name)
        try:
            library.save_to_db()
        except:
            return {'message': 'An error occurred while creating the library.'}, 500

        return library.json(), 201

    def delete(self, name):
        library = LibraryModel.find_by_name(name)
        if library:
            library.delete_from_db()

        return {'message': 'Library deleted'}

class LibraryList(Resource):
    def get(self):
        return {'libraries': [library.json() for library in LibraryModel.query.all()]}
