from time import sleep
from subprocess import Popen, PIPE

def popen_t(command, timeout):
	p = Popen(command, stdout=PIPE, stderr=PIPE)
	for t in range(timeout * 10):
		sleep(0.1)
		if p.poll() is not None:
			return p.communicate()
	p.kill()
	return False

print(popen_t(['/usr/local/bin/python3', 'test.py'], 1))
