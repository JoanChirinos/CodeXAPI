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
    user_p = subprocess.run(['/usr/local/bin/python3', '/home/joan/code/{}.py'.format(filename)], capture_output=True, timeout=10)
    return str(user_p.stdout.decode()), str(user_p.stderr.decode()).replace('{}.py'.format(filename), real_filename)
