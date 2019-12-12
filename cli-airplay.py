import airplay
import argparse
import json
import sys
import os
import yaml

argv = sys.argv
parser = argparse.ArgumentParser(description="Command line interface for AirTable")
parser.add_argument("table_name", help="Table name")
parser.add_argument("action", help="Chose an action", choices=["ins", "mod", "del", "get"])
parser.add_argument("-payload", help="Payload dictionary", type=json.loads)
parser.add_argument("-target_id", help="Target ID")
parser.add_argument("-c", help="Config file path")
args = parser.parse_args()


def chk_config_():
    if os.path.isfile('config.yaml'):
        cf = 'config.yaml'
    elif '-c' in sys.argv:
        cf = args.c
    else:
        cf = None
        tbl = None
        print("Missing or invalid configuration file")
    if cf is not None:
        with open(cf, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            tbl = airplay.Table(config['base_key'], args.table_name, config['api_key'])
    return tbl


def actions():
    if chk_config_() is not None:
        tbl = chk_config_()
        if args.action == "ins":
            print(tbl.insert(**args.payload))
        if args.action == "get":
            print(tbl.get())
            return tbl.get()
        if args.action == "mod":
            print(tbl.modify(args.target_id, **args.payload))
        if args.action == "del":
            print(tbl.delete(args.target_id))
    else:
        pass


actions()
