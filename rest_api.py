from flask import Flask, request, Response
import airplay
import yaml
from jsonschema import validate, ValidationError
import logging

app = Flask(__name__)

with open(r'base_config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


@app.route('/api/<table>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def methods(table):
    tbl = airplay.Table(config['base_key'], table, config['api_key'])
    ##########################################################################################
    # create formulas string with args
    formulas = []
    for arg in request.args:
        if request.args.get(arg).isnumeric():
            formulas.append(f'''{arg}={request.args.get(arg)}''')
        else:
            formulas.append(f'''FIND("{request.args.get(arg)}", {arg})''')
    filter_by_formula = str("AND({})".format(",".join(formulas)))
    ##########################################################################################
    if request.method == 'GET':
        if len(request.args) > 0:
            return tbl.items(filters=filter_by_formula)
        else:
            return tbl.items()
    if request.method == 'POST':
        data = request.get_json()
        logging.info(data)
        if validate_schema(table, data) is not None:
            result = validate_schema(table, data)
            logging.warning(Response(result, 400))
            return Response(result, status=400)
        else:
            return tbl.insert(**data)
    if request.method == 'PATCH':
        data = request.get_json()
        if validate_schema(table, data) is not None:
            result = validate_schema(table, data)
            return Response(result, status=400)
        else:
            target_id = data['id']
            data.pop('id')
            return tbl.modify(target_id, **data)
    if request.method == 'DELETE':
        data = request.get_json()
        if validate_schema(table, data) is not None:
            result = validate_schema(table, data)
            return Response(result, status=400)
        else:
            target_id = data['id']
            return tbl.delete(target_id)


@app.route('/api/<table>/<target_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_id(table, target_id):
    tbl = airplay.Table(config['base_key'], table, config['api_key'])
    if request.method == 'GET':
        return tbl.get_id(target_id)
    if request.method == 'PATCH':
        data = request.get_json()
        return tbl.modify(target_id, **data)
    if request.method == 'DELETE':
        return tbl.delete(target_id)


def validate_schema(table, data=""):
    try:
        schema_ = config['schema']
        validate(data, schema_[table])
        return None
    except ValidationError as ex:
        logging.info(ex.args[0])
        return ex.message


if __name__ == '__main__':
    app.run

# curl -X GET  localhost:5000/api?table=Albums
# curl -X POST -H "Content-Type: application/json" -d "{\"Track\": \"sound\"}" localhost:5000/api/Tracks
# curl -X PATCH -H "Content-Type: application/json" -d "{\"id\":\"reclfUY48qDMTnmXl\",\"Artist\": \"tommy\"}" localhost:5000/api/Albums
# localhost:5000/api?name=Albums
# curl http://localhost:5000/api/Albums?Artist=Daft
# curl -X PATCH -H "Content-Type: application/json" -d "{\"Profile\": \"a good boy\"}" http://localhost:5000/api/Artists/rec5V36WuIX4XsDUe
