from __future__ import print_function
import sys

import dbdb


OK = 0
BAD_ARGS = 1
BAD_VERB = 2
BAD_KEY = 3


def usage():
    print("Usage:", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME get KEY", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME set KEY VALUE", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME delete KEY", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME help", file=sys.stderr)


def help_function():
    print("Dog Bed Database CLI")
    print("---------------------")
    print("This command-line interface allows you to interact with a database storing information about dog beds.")
    print("You can perform the following operations:")
    print("1. Get a value associated with a key: 'get KEY'")
    print("2. Set a value for a key: 'set KEY VALUE'")
    print("3. Delete a key-value pair: 'delete KEY'")
    print("4. Get help: 'help'")
    print("\nTips:")
    print("- Ensure the database is initialized and contains the necessary schema.")
    print("- Use descriptive keys for better organization.")
    print("- Remember that keys are case-sensitive.")


def main(argv):
    if not (4 <= len(argv) <= 5):
        usage()
        return BAD_ARGS

    dbname, verb, key, value = (argv[1:] + [None])[:4]
    if verb == 'help':
        help_function()
        return OK

    if verb not in {'get', 'set', 'delete'}:
        usage()
        return BAD_VERB

    db = dbdb.connect(dbname)
    try:
        if verb == 'get':
            sys.stdout.write(db[key] + '\n')
        elif verb == 'set':
            db[key] = value
            db.commit()
            print(f"Set {key} to {value}")
        else:
            del db[key]
            db.commit()
            print(f"Deleted {key}")
    except KeyError:
        print("Key not found", file=sys.stderr)
        return BAD_KEY
    return OK


if __name__ == '__main__':
    sys.exit(main(sys.argv))
