from subprocess import Popen, PIPE
from time import sleep
from uuid import uuid4
from os import remove
import re

SAFE_IMPORTS = {'math', 'string', 're', 'difflib', 'textwrap', 'stringprep', 'datetime',
                'calendar', 'deque', 'ChainMap', 'Counter', 'OrderedDict', 'UserDict',
                'UserList', 'UserString', 'heapq', 'bisect', 'array', 'copy', 'pprint', '',
                'enum', 'cmath', 'decimal', 'fractions', 'random', 'statistics', 'itertools',
                'functools', 'operator', 'hashlib', 'hmac', 'secrets', 'time', 'json', 're',
                'base64', 'binascii', 'html', 'html.parser', 'html.entites', 'colorsys', 'uuid'}
UNSAFE_KEYWORDS = {'exec', 'eval', 'compile', 'open', 'input', '__import__', 'stdin', 'stdout',
                   'stderr' '__builtins__', 'globals', 'locals', '.read', '.write'}

def code_is_safe(code):
    # check imports
    import_from = re.compile(r'^[ \t]*from[ \t]+([\w.]+)[ \t]+import[ \t][\w, \t.]+\s*$', re.M)
    import_any = re.compile(r'^[ \t]*import[ \t]+[\w, \t.]+$', re.M)
    imports = import_from.findall(code) + [item for sublist in [[b.strip() for b in i] for i in [x[x.find('import')+6:].split(',') for x in import_any.findall(code)]] for item in sublist]
    for i in imports:
        if i not in SAFE_IMPORTS:
            return False, '# Unsafe import: {}'.format(i)

    #check other stuff
    lines = code.split('\n')
    for line_number in range(len(lines)):
        for keyword in UNSAFE_KEYWORDS:
            if keyword in lines[line_number]:
                before, after = lines[lines_number]
                return False, '# Unsafe code on line {}: {}'.format(line_number, keyword)
    return True, None


def go(user_code, real_filename):
    safe, message = code_is_safe(user_code)
    if not safe:
        return '', message
    filename = str(uuid4())

    with open('/var/www/XAPI/XAPI/util/{}.py'.format(filename), 'w') as f:
        f.write(user_code)

    p = Popen(['sudo', '/usr/bin/python3', '/var/www/XAPI/XAPI/util/{}.py'.format(filename)], stdout=PIPE, stderr=PIPE)
    pid = p.pid
    for t in range(50):
        sleep(0.1)
        if p.poll() is not None:
            stdout, stderr = p.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()
            try:
                Popen(['sudo', 'rm', '{}.py'.format(filename)])
            except:
                pass
            finally:
                return stdout, stderr.replace('/var/www/XAPI/XAPI/util/{}.py'.format(filename), real_filename)
    try:
        Popen(['sudo', 'rm', '{}.py'.format(filename)])
        Popen(['sudo', 'kill', str(pid)])
    except:
        pass
    finally:
        return '', '# Timeout error (~5 seconds).\n# Are you using too much recursion?\n# Please run this code on your own machine'
