import airplay
import argparse
import json
import sys
import os
import yaml
from http import HTTPStatus

argv = sys.argv
parser = argparse.ArgumentParser(description="Command line interface for AirTable")
parser.add_argument("table_name", help="Table name")
parser.add_argument("action", help="Chose an action", choices=["ins", "mod", "del", "get"])
body_group = parser.add_argument_group(title='Requests body')
body_group.add_argument("-payload", help="Payload dictionary", type=json.loads)
body_group.add_argument("-target_id", help="Item id number")
body_group.add_argument("-c", help="Config file path")
args = parser.parse_args()


def chk_config_():

    if '-c' in sys.argv:
        cf = args.c
    elif os.path.isfile('config.yaml'):
        cf = 'config.yaml'
    else:
        cf = None
        tbl = None
        print("Configuration file not found")
    if cf is not None:
        with open(cf, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            try:
                tbl = airplay.Table(config['base_key'], args.table_name, config['api_key'])
            except KeyError:
                print("Missing attributes in configuration file")
                tbl = None
    return tbl


def actions():
    if chk_config_() is not None:
        tbl = chk_config_()
    try:
        if args.action == "ins":
            print(tbl.insert(**args.payload))
        if args.action == "get":
            print(tbl.items())
        if args.action == "mod":
            print(tbl.modify(args.target_id, **args.payload))
        if args.action == "del":
            print(tbl.delete(args.target_id))
    except airplay.HTTPStatusCodeException as ex:
        print(HTTPStatus(ex.status).phrase)
    else:
        pass


actions()
