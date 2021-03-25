
from flask import request, Response, redirect
from flask import render_template
from flask_login import current_user, login_user, logout_user

from GetHome import app, logger
from GetHome.modules import house_parser
from GetHome.modules.house_data_manager import HouseManager, serialize_object
from GetHome.modules.user_manager import validate_google_token, User
from app_config import config

house_manager = HouseManager()

# home page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/google_signin", methods=["GET", "POST"])
def google_signin():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == 'GET':
        res = render_template(
            "login.html",
            client_id=config['env_vars']['google_oauth']['CLIENT_ID'],
            login_callback=request.host_url+"/google_signin") # callback url after google sign in
        return res
    elif request.method == 'POST':
        csrf_token_cookie = request.cookies.get('g_csrf_token')
        if not csrf_token_cookie:
            return Response('No CSRF token in Cookie.', status=400)
        csrf_token_body = request.form.get('g_csrf_token')
        if not csrf_token_body:
            return Response('No CSRF token in post body.', status=400)
        if csrf_token_cookie != csrf_token_body:
            return Response('Failed to verify double submit cookie.', status=400)

        id_token = request.form.get('credential')
        id_token_dec = validate_google_token(id_token)
        if id_token_dec:
            logger.info("validate id token success")
            
            user_id = "google-" + id_token_dec['email']
            user = User.get_user(user_id)
            if not user:
                # user has not signed in before, record user data
                user = User(
                    id=user_id, 
                    email=id_token_dec['email'],
                    email_verified=id_token_dec['email_verified']
                    )
                User.add_user(user)

            login_user(user)
            return redirect("/")
        else:
            logger.info("validate id token fail")
            return Response('validate id token fail', status=400)

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

# get house list
@app.route("/house", methods=["Get"])
def get_houses():
    ls = house_manager.get_house_list()
    jstr = serialize_object(ls)
    response = Response(jstr, status=200, mimetype='application/json')
    return response

# add house info. two ways:
# - parse web page info
# - input info manually
@app.route("/house", methods=["POST"])
def add_house_data():
    post_type = request.args.get('type')
    if post_type == "parse":
        url = request.form["url"]
        parse_res = house_parser.parse591(url)
        insert_data = house_manager.insert_house_data(parse_res)
        if insert_data:
            response = Response(serialize_object(insert_data), status=201, mimetype='application/json')
        else:
            response = Response("add data fail", status=500, mimetype='application/text')
        return response
    elif post_type == "manual":
        return "TODO"

# update house data
@app.route("/house", methods=["PUT"])
def update_house_data():
    id = request.args.get('id')
    data = request.form
    # TODO: parse form data to house data. not rely on under module data structure.
    if house_manager.update_house_data(id, data):
        return Response(status=200)
    else:
        return Response(status=500)

# delete house data
@app.route("/house", methods=["DELETE"])
def delete_house_data():
    id = request.args.get('id')
    if house_manager.del_house_data(id):
        return Response(status=200)
    else:
        return Response(status=500)