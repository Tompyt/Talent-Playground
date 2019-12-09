import airplay
import multiprocessing
import old_airplay
import random
import string
import yaml
import os
os.getcwd()


with open(r'C:\Users\tommy.TIGERITALIA\PycharmProjects\airtest\config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


def random_str(typo, nr_char):
    letters = string.ascii_letters
    numbers = string.digits
    if typo == "l":
        char = letters
    else:
        char = numbers
    output = [y for nr in range(nr_char) for y in random.choice(list(char))]
    try:
        return int(''.join(output))
    except ValueError:
        return ''.join(output)


def rand_item(count=1):
    res = []
    for _ in range(count):
        res.append({'Name': random_str("l", 10), 'Code': random_str("n", 10)})
    return res


def _wrap_insert(x):
    tbl, item = x
    return tbl.insert(**item)


def test_concurrency():
    tbl = airplay.Table(config['base_key'], config['table_name'], config['api_key'])
    p = multiprocessing.Pool(20)
    items = rand_item(30)
    res = p.map(_wrap_insert, [(tbl, item) for item in items])
    p.close()
    p.join()
    if res[0] != 200:
        return res


def test_class():
    tbl = airplay.Table(config['base_key'], config['table_name'], config['api_key'])
    rsp0 = tbl.get()
    assert rsp0[0] == 200
    rsp1 = tbl.insert(Name='Items00', Code=100)
    assert rsp1[0] == 200
    rsp3 = tbl.get()
    #assert len(rsp3[1]) == len(rsp0[1]) + 1  # verifica inserimento in tabella
    my_id = list(rsp3[1].keys())[0]
    rsp4 = tbl.modify(my_id, Name='RenameItem00', Code=200)
    assert rsp4[0] == 200
    tbl.delete(my_id)
    rsp5 = tbl.get
    #assert len(rsp5[1]) == len(rsp0[1])  # verifica eliminazione da tabella


def test_all():
    resp_ins = old_airplay.table_insert(Name='item01', Code=200)
    assert resp_ins[0] == 200
    assert resp_ins[1] is not None

    resp_get = old_airplay.table_get()
    assert resp_get is not None
    assert len(resp_get) == 2

    resp_mod = old_airplay.table_modify(resp_ins[1], Name='rename_item01', Code=200)
    assert resp_mod[0] == 200
    assert resp_mod[1] == resp_ins[1]

    resp_get = old_airplay.table_get()
    assert resp_get is not None
    assert len(resp_get) == 2

    resp_del = old_airplay.table_del(resp_ins[1])
    assert resp_del is not None
    assert resp_del[0] == 200
    assert resp_del[1] == resp_ins[1]
