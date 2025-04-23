from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from formularios.formulario_controller import FormularioController


formulario_bp = Blueprint('forms', __name__)

@formulario_bp.route('/<int:user_id>',methods=['POST'])
@jwt_required()
def register_formulario(user_id):
    return jsonify(FormularioController.register_form(user_id,request.get_json()))

@formulario_bp.route('/<int:user_id>',methods=['GET'])
@jwt_required()
def get_formulario(user_id):
    return FormularioController.get_form(user_id)

# @user_bp.route('/me',methods=['GET'])
# @jwt_required()
# def get_user():
#     user_id = get_jwt_identity()
#     return jsonify(UserController.get_user(user_id))

# @user_bp.route('/me/<int:user_id>',methods=['GET']) 
# @jwt_required()
# def get_user_route(user_id):
#     return jsonify(UserController.get_user(user_id))

# @user_bp.route('/me',methods=['PUT'])
# @jwt_required()
# def update_user():
#     user_id = get_jwt_identity()
#     return jsonify(UserController.update_user(user_id,request.get_json()))

# @user_bp.route('/me',methods=['DELETE'])
# @jwt_required()
# def delete_user():
#     user_id = get_jwt_identity()
#     return jsonify(UserController.delete_user(user_id))