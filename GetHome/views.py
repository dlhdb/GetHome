
from flask import request, Response
from flask import render_template


from GetHome import app
from GetHome.modules import house_parser
from GetHome.modules.house_data_manager import LocalMongoDB, serialize_object

mydb = LocalMongoDB()

# home page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("user", "")
    pw = request.form.get("pw", "")

    # get user info from db
    # RSA decrypt and check info
    # if pass redirect to home page
    # else return access denied page

    return True
    

# get house list
@app.route("/house", methods=["Get"])
def get_houses():
    ls = mydb.get_house_list()
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
        insert_data = mydb.insert_house_data(parse_res)
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
    if mydb.update_house_data(id, data):
        return Response(status=200)
    else:
        return Response(status=500)

# delete house data
@app.route("/house", methods=["DELETE"])
def delete_house_data():
    id = request.args.get('id')
    if mydb.del_house_data(id):
        return Response(status=200)
    else:
        return Response(status=500)