from sanic import Blueprint
from sanic.response import *

bp = Blueprint('api', url_prefix='/api/v1', version='v1')

@bp.route('/users')
async def get_all_users(request):
    return json({
            value['name']:{
                'id': key, 
                'e-mail': value['e-mail'], 
                'pass-hash': value['pass-hash']
            }
            for key, value in request.ctx.session.get('users').items()
        }
    )

@bp.route('/user/<id>')
async def get_user_by_id(request, id):
    return json(request.ctx.session.get('users')[id])