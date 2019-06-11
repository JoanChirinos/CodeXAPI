from subprocess import Popen, PIPE
from time import sleep
from uuid import uuid4
from os import remove

def code_is_unsafe(code):
    keywords = ['import', 'exec', 'eval', 'compile', 'open', 'input', '__import__', 'user_outputs', 'correct_outputs', 'file', 'execfile', 'stdin', '__builtins__', 'globals', 'locals']
    lines = code.split('\n')
    for line_number in range(len(lines)):
        for keyword in keywords:
            if keyword in lines[line_number]:
                return True, keyword, line_number + 1
    return False, None, None


def go(user_code, real_filename):
    unsafe, keyword, line_number = code_is_unsafe(user_code)
    if unsafe:
        return '# Unsafe code on line {}: {}'.format(line_number, keyword), False
    filename = str(uuid4())

    with open('/var/www/XAPI/XAPI/util/{}.py'.format(filename), 'w') as f:
        f.write(user_code)

    p = Popen('sudo', '/usr/bin/python3', '/var/www/XAPI/XAPI/util/{}.py'.format(filename), stdout=PIPE, stderr=PIPE)
    for t in range(50):
        sleep(0.1)
        if p.poll() is not None:
            stdout, stderr = p.communicate()
            return str(stdout), str(stderr).replace('{}.py'.format(filename), real_filename)
    p.kill()
    return '# Timeout error (~5 seconds).\n# Are you using too much recursion?\n# Please run this code on your own machine', False

##def go(user_code, real_filename):
##    unsafe, keyword = code_is_unsafe(user_code)
##    if unsafe:
##        return '#Unsafe code! I can\'t run that!', False
##    filename = str(uuid.uuid4())
##    with open('/var/www/XAPI/XAPI/util/{}.py'.format(filename), 'w') as f:
##        f.write(user_code)
##    my_stdout = open('/var/www/XAPI/XAPI/util/{}_stdout.txt'.format(filename), 'w')
##    my_stderr = open('/var/www/XAPI/XAPI/util/{}_stderr.txt'.format(filename), 'w')
##    user_p = subprocess.run(['sudo', '/usr/bin/python3', '/var/www/XAPI/XAPI/util/{}.py'.format(filename)], stdout=my_stdout, stderr=my_stderr, timeout=1)
##    try:
##        user_p.wait()
##    except:
##        pass
##    my_stdout.close()
##    my_stderr.close()
##    with open('/var/www/XAPI/XAPI/util/{}_stdout.txt'.format(filename)) as f:
##        my_stdout = f.read()
##    with open('/var/www/XAPI/XAPI/util/{}_stderr.txt'.format(filename)) as f:
##        my_stderr = f.read()
##    os.remove('/var/www/XAPI/XAPI/util/{}_stderr.txt'.format(filename))
##    os.remove('/var/www/XAPI/XAPI/util/{}_stdout.txt'.format(filename))
##    os.remove('/var/www/XAPI/XAPI/util/{}.py'.format(filename))
##    return str(my_stdout), str(my_stderr).replace('{}.py'.format(filename), real_filename)

##out, err = go('print("works!")', 'testcode.py')
##print(out)
##print(err)
