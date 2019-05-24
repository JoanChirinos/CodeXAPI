import subprocess, uuid


def code_is_unsafe(code):
    keywords = ['import', 'exec', 'eval', 'compile', 'open', 'input', '__import__', 'user_outputs', 'correct_outputs', 'file', 'execfile', 'stdin', '__builtins__', 'globals', 'locals']
    for keyword in keywords:
        if keyword in code:
            return True, keyword
    return False, None


def go(user_code, real_filename):
    unsafe, keyword = code_is_unsafe(user_code)
    if unsafe:
        return 'Unsafe code! I can\'t run that!'
    filename = str(uuid.uuid4())
    with open('/home/joan/code/{}.py'.format(filename), 'w') as f:
        f.write(user_code)
    my_stdout = open('{}_stdout.txt'.format(filename), 'w')
    my_stderr = open('{}_stderr.txt'.format(filename), 'w')
    user_p = subprocess.run(['/usr/bin/python3', '/home/joan/code/{}.py'.format(filename)], stdout=my_stdout, stderr=my_stderr, timeout=10)
    my_stdout.close()
    my_stderr.close()
    with open('{}_stdout.txt'.format(filename)) as f:
        my_stdout = f.read()
    with open('{}_stderr.txt'.format(filename)) as f:
        my_stderr = f.read()

    return str(my_stdout), str(my_stderr).replace('{}.py'.format(filename), real_filename)

##out, err = go('print("works!")', 'testcode.py')
##print(out)
##print(err)
