from flask import Blueprint, jsonify, request

from . import db_session
from .product import Product

blueprint = Blueprint(
    'product_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/product')
def get_product():
    db_sess = db_session.create_session()
    product = db_sess.query(Product).all()
    return jsonify(
        {
            'product':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in product]
        }
    )


@blueprint.route('/api/product/<int:product_id>', methods=['GET'])
def get_one_product(product_id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).get(product_id)
    if not product:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'product': product.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/product', methods=['POST'])
def create_product():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    product = Product(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(product)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/product/<int:news_id>', methods=['DELETE'])
def delete_product(product_id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).get(product_id)
    if not product:
        return jsonify({'error': 'Not found'})
    db_sess.delete(product)
    db_sess.commit()
    return jsonify({'success': 'OK'})
