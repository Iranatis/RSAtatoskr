from json import load


GLOBAL_VARS = None

def read_json(path = "../config.json"):
    global GLOBAL_VARS
    if GLOBAL_VARS == None:
        GLOBAL_VARS = load(open(path))
        
def get(*strings):
    if GLOBAL_VARS == None:
        read_json()
    d = GLOBAL_VARS
    not_found = False
    for s in strings:
        try:
            if s in d:
                d = d[s]
            else:
                not_found = True
        except:
            not_found = True
        if not_found:
            print("/!\\Can't find the config " + str(strings))
            return None
    return d