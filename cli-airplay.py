import airplay
import argparse
import json
import sys

argv = sys.argv

parser = argparse.ArgumentParser(description="Command line interface for AirTable")
parser.add_argument("table", type=str, help="Table name")
parser.add_argument("base", type=str, help="Base key")
parser.add_argument("apikey", type=str, help="API key")
parser.add_argument("action", type=str, help="Chose an action", choices=["ins", "mod", "del", "get"])
parser.add_argument("-payload", type=str, help="Payload dictionary")
parser.add_argument("-target_id", type=str, help="Target ID")
# parser.set_defaults(payload={'Name':'test', 'Code':100})
args = parser.parse_args()
tbl = airplay.Table(args.base, args.table, args.apikey)


def actions():
    if args.action == "ins":
        dd = json.loads(args.payload)
        print(tbl.insert(**dd))
    if args.action == "get":
        print(tbl.get())
        return tbl.get()
    if args.action == "mod":
        pass
        dd = json.loads(args.payload)
        print(tbl.modify(args.target_id, **dd))
    if args.action == "del":
        print(tbl.delete(args.target_id))


actions()
