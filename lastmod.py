import subprocess as sp
from subprocess import PIPE, Popen


# calculates the current line number of the .bash_history to check how many commands need to be executed
# wc -l < /Users/kiranv/.bash_history
def last_line_num():
	with open('/Users/kiranv/.bash_history', 'rb') as in_f:
		p_ln = Popen(['wc', '-l'], stdin=in_f, stdout=PIPE, stderr=PIPE)
		output, err = p_ln.communicate(b'')
		line_num = output.strip()
		print line_num
		return int(line_num)

# calculates how many seconds since the last edit of the .bash_history
def last_edit_time():
	p1 = Popen(['date', '+%s'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	o1, e1 = p1.communicate(b'')
	p2 = Popen(['stat', '-f%c', '/Users/kiranv/.bash_history'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	o2, e2 = p2.communicate(b'')
	print o1
	print o2
	d = int(o1.strip())
	s = int(o2.strip())
	print d
	print s
	return d - s

