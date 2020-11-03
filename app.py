import json

from sanic import response
from sanic import Sanic
from sanic_session import Session
from api import bp as API_v1

app = Sanic(__name__)
app.register_blueprint(API_v1)
session = Session(app)

@app.get('/users')
async def get_users(request):
    users = {}
    if request.ctx.session['users']:
        for key, value in request.ctx.session['users'].items():
            users.update({
                value['name']:{
                    'id': key, 
                    'e-mail': value['e-mail'], 
                    'pass-hash': value['pass-hash']
                }
            })
        return response.json(users)
    else:
        return response.text('Users has not been created yet')


@app.get('/users/<id>')
async def get_user(request, id):
    if request.ctx.session.get('users'):
        return response.json(request.ctx.session.get('users')[id])
    else:
        return response.text('There is no such user')


@app.post('/users')
async def create_user(request):
    if request.ctx.session.get('users'):
        if request.json:
            request.ctx.session.get('users').update(request.json)
            return response.json({
                'message': {'succefly':
                    'Creating user was sucefly'
                }
            })
        else:
            return response.json({
                'message': {'error':
                    'There is a valid json data'
                }
            })
    else:
        if request.json:
            users = {}
            users.update(request.json)
            request.ctx.session['users'] = users
            return response.json({
                'message': {'succefly':
                    'Creating user was sucefly'
                }
            })
        else:
            return response.json({
                'message': {'error':
                    'There is a valid json data'
                }
            })

@app.delete('/users/<id>')
async def delete_user(request, id):
    pass


@app.patch('/users/<id>')
async def edit_user(request, id):
    pass


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)