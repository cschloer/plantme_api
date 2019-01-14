from flask import Blueprint, request, jsonify
from ..models import Tree, TreeSpeciesVote, TreeImage
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete
from ..database import db
from ..helpers import transform_species_votes


tree_bp = Blueprint("tree", __name__)

@tree_bp.route('/', methods=('GET', 'POST'))
def tree():
    if request.method == 'GET':
        return index(Tree, request.args.to_dict())
    if request.method == 'POST':
        # A custom POST to allow all of the objects to be added at the same time
        species_votes = request.json.pop('species_votes', None)
        images = request.json.pop('images', None)
        tree = create(Tree, request.json, False, False)
        tree_id = tree['id']

        # Create species votes
        vote_dicts = []
        if species_votes:
            for vote_request in species_votes:
                vote_request['tree_id'] = tree_id
                vote = create(TreeSpeciesVote, vote_request, False, False)
                vote_dicts.append(vote)
        tree['species_votes'] = transform_species_votes(vote_dicts)

        # Create images
        image_dicts = []
        if images:
            for image_request in images:
                image_request['tree_id'] = tree_id
                image = create(TreeImage, image_request, False, False)
                image_dicts.append(image)
        tree['images'] = image_dicts

        db.session.commit()

        return jsonify(tree)


@tree_bp.route('/<int:id_>', methods=('GET', 'PUT', 'DELETE'))
def tree_id(id_):
    if request.method == 'GET':
        return get(Tree, id_)
    if request.method == 'PUT':
        if request.json.get('user_id'):
            raise FormError(f'The user_id of a tree object ({id_}) cannot be changed')
        return update(Tree, request.json, id_)
    if request.method == 'DELETE':
        return delete(Tree, id_)
