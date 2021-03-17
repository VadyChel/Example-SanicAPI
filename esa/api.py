from esa.core.config import Config
from esa.core.exceptions import *
from esa.core.database import Database
from sanic import response, Blueprint

bp = Blueprint("api", url_prefix='/v2', version="v2")


@bp.listener('before_server_start')
async def setup_db(app, loop):
    app.database = Database()
    await app.database.prepare()


@bp.get('/users')
async def get_users(request):
    return response.json(await request.app.get_users())


@bp.get('/users/<user_id>')
async def get_user(request, user_id):
    try:
        data = await request.app.get_user(user_id=user_id)
    except UserNotFound:
        return response.json(Config.MESSAGES["error_user_not_found"])
    else:
        return response.json(data)


@bp.post('/users')
async def create_user(request):
    fields = ["password", "username", "email"]
    if request.json is None or sorted(request.json.keys()) == sorted(fields):
        return response.json(Config.MESSAGES["error_invalid_json"])

    if not Config.EMAIL_REGEX.match(request.json.get("email")):
        return response.json(Config.MESSAGES["error_invalid_email"])

    try:
        await request.app.create_user(
            password=request.json.get("password"),
            username=request.json.get("username"),
            email=request.json.get("email")
        )
    except UserAlreadyExists:
        return response.json(Config.MESSAGES["error_email_already_used"])
    else:
        return response.json(Config.MESSAGES["successfully_create_user"])


@bp.delete('/users/<id>')
async def delete_user(request, id):
    if request.json is None:
        return response.json(Config.MESSAGES["error_invalid_json"])

    if "password" not in request.json.keys():
        return response.json(Config.MESSAGES["error_invalid_json"])

    try:
        await request.app.delete_user(
            user_id=id,
            password=request.json.get("password")
        )
    except UserNotFound:
        return response.json(Config.MESSAGES["error_user_not_found"])
    except InvalidPassword:
        return response.json(Config.MESSAGES["error_invalid_password"])
    else:
        return response.json(Config.MESSAGES["successfully_delete_user"])


@bp.patch('/users/<user_id>')
async def edit_user(request, user_id):
    if request.json is None:
        return response.json(Config.MESSAGES["error_invalid_json"])

    if "password" not in request.json.keys():
        return response.json(Config.MESSAGES["error_invalid_json"])

    if "email" in request.json.keys():
        if not Config.EMAIL_REGEX.match(request.json.get("email")):
            return response.json(Config.MESSAGES["error_invalid_email"])

    try:
        await request.app.edit_user(
            user_id=user_id,
            params=request.json
        )
    except InvalidPassword:
        return response.json(Config.MESSAGES["error_invalid_password"])
    except UserNotFound:
        return response.json(Config.MESSAGES["error_user_not_found"])
    else:
        return response.json(Config.MESSAGES["successfully_edit_user"])
