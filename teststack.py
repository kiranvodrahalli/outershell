## Kiran Vodrahalli
## July 17, 2015
## OuterShell - works as a layer on top of whatever shell you're using 
##              and gives you additional power by giving access to Python process running in background
##            - supports any data structure / saving data / easy customization of functions.
## 30 lines of code gives you all this extra power in customizing your terminal workflow!
## moreover, you're bootstrapping all of this on TOP of whatever shell you already have working! it's completely independent and seamless.


from subprocess import Popen, PIPE
from time import sleep

# this basically is a very simple hack to enable you to easily hack on top of a bash shell additional functionality through writing Python.
# it's a bit more complicated than this though! this also allows you to persist your own datastructures and so on! this is not possible in bash to my knowledge 
# i.e. you cannot have all your commands be aware of some defined data structures/objects - this is possible here! and it's possible to use with other libraries as well!

## Usage: python teststack.py 
##  Then, in some other shell window, enter the commands as you wish and watch them appear. 

## Usage(2): nohup python teststack.py &
##  Runs the process in the background. Need to be sure to save the pid so that you can kill -9 the process when you want to shut it down. 



## neccessities for setup:
## 1) modify your .bash_profile to have the following lines:
##
##         shopt -s histappend  # append to history, don't overwrite it
##         export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
##
## This allows the .bash_history to be updated automatically.

# 0) Save this on github!
## TODO: 1) implement a save (i.e. pickle relevant data structures - data structures are still TBD)
##       2) for the commands defined in the supported commands, give them aliases to "" or make them some function in .bash_profile
##         so that they don't spit out "command not recognized"
##       3) additionally, enable some bash scripts to automatically start/status/stop this (i.e. nohup python teststack.py &, save the pid, be able to kill it and save the new one to a common file)
##       4) along the lines of 1): figure out what the primary data structures and functions should be, and enable an easy way of adding to it
##       5) test if when you close the bash shell, the nohup background python program stops too - it should not! (i.e. it should persist). need the equivalent of netstat -tnlp to see the process...
##          (note: since this isn't on a network, we just need to find the command that displays all active processes/pids and then grep for python, probably. 
##           (actually we are going to store the pid of the process when we start it))



stack = []
i = 0
old_line_num = 0 # to be set later
started = False # if this has not started running
while(True):
	with open('/Users/kiranv/.bash_history', 'rb') as in_f:
		p_ln = Popen(['wc', '-l'], stdin=in_f, stdout=PIPE, stderr=PIPE)
		output, err = p_ln.communicate(b'')
		line_num = int(output.strip())
		if not started:
			old_line_num = line_num -1
			started = True
		if line_num > old_line_num:
			num_commands = line_num - old_line_num # number of unprocessed commands
			cmd_str = '-' + str(num_commands)
			p = Popen(['tail', cmd_str], stdin=in_f, stdout=PIPE, stderr=PIPE)
			output, err = p.communicate(b"")
			commands = map(lambda line: line.strip(), output.split("\n"))
			for command in commands:
				# Currently supported command options
				if command == "":
					continue
				if command == "hellotherekiran":
					stack.append(i)
					i += 1
				elif command == "pausedkiran":
					# for testing that it can correctly execute the missed commands
					sleep(10)
					stack.append(5555555)
				elif command == "printitkiran":
					print(str(stack))
			old_line_num = line_num # we are caught up!

#########################################################

#from lastmod import last as last_edit
#import time

# The old time-based solution to handle checking if there is a new command (rather than the same old one sitting around)
'''
stack = []
i = 0
loop_elapse = 1
while(True):
	# if commands take too long, may be some bugs (i.e. it might forget about a command)
	if last_edit() < loop_elapse + 0.0000001:
		start = time.time()
		p = Popen(['tail', '-1', '/Users/kiranv/.bash_history'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate(b"")
		rc = p.returncode
		command = output.strip()
		if command == "hellotherekiran":
			stack.append(i)
			i += 1
		elif command == "printitkiran":
			#sp.call(["echo", str(stack)])
			print(str(stack))
		end = time.time()
		loop_elapse = 1 + int(end - start)
'''
# Upgrading to the line number based solution
# Keep track of the line number in .bash_history of the last command parsed
# check new line number - if it's +1 the old number, execute it and update the old_line_number
# if it's 1 (i.e. .bash_history got reset), execute it and reset old_line_number to 1
# if its +n the old number, you have to read the commands that had not been parsed and execute them in order.











