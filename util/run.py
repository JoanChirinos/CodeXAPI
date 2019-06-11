import subprocess, uuid, os


def code_is_unsafe(code):
    keywords = ['import', 'exec', 'eval', 'compile', 'open', 'input', '__import__', 'user_outputs', 'correct_outputs', 'file', 'execfile', 'stdin', '__builtins__', 'globals', 'locals']
    for keyword in keywords:
        if keyword in code:
            return True, keyword
    return False, None


def go(user_code, real_filename):
    unsafe, keyword = code_is_unsafe(user_code)
    if unsafe:
        return '#Unsafe code! I can\'t run that!', False
    filename = str(uuid.uuid4())
    with open('/var/www/XAPI/XAPI/util/{}.py'.format(filename), 'w') as f:
        f.write(user_code)
    my_stdout = open('/var/www/XAPI/XAPI/util/{}_stdout.txt'.format(filename), 'w')
    my_stderr = open('/var/www/XAPI/XAPI/util/{}_stderr.txt'.format(filename), 'w')
    user_p = subprocess.run(['sudo', '/usr/bin/python3', '/var/www/XAPI/XAPI/util/{}.py'.format(filename)], stdout=my_stdout, stderr=my_stderr, timeout=1)
    try:
        user_p.wait()
    except:
        pass
    my_stdout.close()
    my_stderr.close()
    with open('/var/www/XAPI/XAPI/util/{}_stdout.txt'.format(filename)) as f:
        my_stdout = f.read()
    with open('/var/www/XAPI/XAPI/util/{}_stderr.txt'.format(filename)) as f:
        my_stderr = f.read()
    os.remove('/var/www/XAPI/XAPI/util/{}_stderr.txt'.format(filename))
    os.remove('/var/www/XAPI/XAPI/util/{}_stdout.txt'.format(filename))
    os.remove('/var/www/XAPI/XAPI/util/{}.py'.format(filename))
    return str(my_stdout), str(my_stderr).replace('{}.py'.format(filename), real_filename)

##out, err = go('print("works!")', 'testcode.py')
##print(out)
##print(err)
