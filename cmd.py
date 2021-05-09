import parse
import os


a = False
b = False


# Internal change-directory command.
def shell_cd (dir):
	# TODO - execute cd
	if len(dir) != 1:
		os.chdir(dir[1])


# Internal exit/quit command.
def shell_exit ():
	# TODO - execute sys.exit()

	os._exit(0)
	pass


# Execute simple command
def run_simple_command (simple_commands_list, father_command):
	# TODO - extract command and arguments; ATTENTION! not all commands are simple_commands

	# TODO - extract redirects from father_command

	# TODO - fork parent process

	# TODO - execute child

	# TODO - wait for child

	# TODO - return exit status

	inF = father_command.input
	outF = father_command.output
	errF = father_command.err
	appOutF = father_command.append_out
	appErrF = father_command.append_err
	cmd = []

	for i in range(len(simple_commands_list)):
		cmd.append(simple_commands_list[i].word)

	if cmd[0] == "cd":
		shell_cd(cmd[1])
	elif cmd[0] == "exit" or cmd[0] == "quit":
		shell_exit()
	elif inF != None:
		inpF(inF)
	else:
		pid = os.fork()
		if pid == 0:
			if outF != None:
				if appOutF == True:
					appendOutFile(outF, cmd)
				elif errF != None:
					if outF != errF:
						outAndErrorDifF(outF, errF, cmd)
					else:
						outAndErrorSameF(outF, cmd)
				else:
					outputF(outF, cmd)
			if errF != None:
				if appErrF == True:
					appendErrorFile(errF, cmd)
				else:
					errorF(errF, cmd)
			else:
				os.execvp(cmd[0], cmd)
		else:
			(r,w) = os.waitpid(pid, 0)
			return os.WEXITSTATUS(w)


def inpF(file):
	fd = os.open(file, os.O_RDONLY, 0o644)
	text = os.read(fd, 1000000)
	text = str(text, "utf-8")
	text = text.rstrip()
	print(text)
	os.close(fd)


def outputF(file, cmd):
	fd = os.open(file, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o644)
	os.dup2(fd, 1)
	os.execvp(cmd[0], cmd)
	os.close(fd)


def appendOutFile(file, cmd):
	fd = os.open(file, os.O_RDWR | os.O_CREAT | os.O_APPEND, 0o644)
	os.dup2(fd, 1)
	os.execvp(cmd[0], cmd)
	os.close(fd)


def outAndErrorDifF(file1, file2, cmd):
	fd = os.open(file1, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o644)
	fd1 = os.open(file2, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o644)
	os.dup2(fd, 1)
	os.dup2(fd1, 2)
	os.execvp(cmd[0], cmd)
	os.close(fd)
	os.close(fd1)


def outAndErrorSameF(file, cmd):
	fd = os.open(file, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o644)
	os.dup2(fd, 1)
	os.dup2(fd, 2)
	os.execvp(cmd[0], cmd)
	os.close(fd)


def appendErrorFile(file, cmd):
	fd = os.open(file, os.O_RDWR | os.O_CREAT | os.O_APPEND, 0o644)
	os.dup2(fd, 2)
	os.execvp(cmd[0], cmd)
	os.close(fd)


def errorF(file, cmd):
	fd = os.open(file, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o644)
	os.dup2(fd, 2)
	os.execvp(cmd[0], cmd)
	os.close(fd)


def do_cond_zero(cmd1, cmd2, father_command):

	global a
	if cmd2.com1 == None:
		st = run_simple_command(cmd1.commands, cmd1)
		if st == 0:
			a = False
		else:
			if cmd2 == None:
				pass
			else:
				a = False
				run_simple_command(cmd2.commands, cmd2)
	else:
		if cmd1 == None:
			pass
		else:
			st = run_simple_command(cmd1.commands, cmd1)
			if st == 0:
				a = False
			else:
				if a == True:
					a = False
					run_simple_command(cmd2.commands, cmd2)
				else:
					if cmd2 != None:
						a = True
						do_cond_zero(cmd2.com1, cmd2.com2, cmd2)
	pass

def do_cond_nzero(cmd1, cmd2, father_command):

	global b
	if cmd2.com1 == None:
		st = run_simple_command(cmd1.commands, cmd1)
		if st != 0:
			b = False
		else:
			if cmd2 == None:
				pass
			else:
				b = False
				run_simple_command(cmd2.commands, cmd2)
	else:
		if cmd1 == None:
			pass
		else:
			st = run_simple_command(cmd1.commands, cmd1)
			if st != 0:
				b = False
			else:
				if b == True:
					b = False
					run_simple_command(cmd2.commands, cmd2)
				else:
					if cmd2 != None:
						b = True
						do_cond_nzero(cmd2.com1, cmd2.com2, cmd2)

def do_sequential(cmd1, cmd2, father_command):

	if cmd1 != None:
		run_simple_command(cmd1.commands, cmd1)
	if cmd2 != None:
		do_sequential(cmd2.com1, cmd2.com2, cmd2)
	else:
		run_simple_command(father_command.commands, father_command)


# Process two commands in parallel, by creating two children.
def do_in_parallel (cmd1, cmd2, father_command):
	# TODO - execute cmd1 and cmd2 simultaneously
	pass


def do_on_pipe (cmd1, cmd2, father_command):
	# TODO - redirect the output of cmd1 to the input of cmd2
	pass


#Parse and execute a command.
def parse_command (command):

	if command.op == parse.OP_NONE:
		return run_simple_command (command.commands, command)
	elif command.op == parse.OP_SEQUENTIAL:
		# TODO - execute the commands one after the other
		return do_sequential(command.com1, command.com2, command)
	elif command.op == parse.OP_PARALLEL:
		# TODO - execute the commands simultaneously
		return do_in_parallel(command.com1, command.com2, command)
	elif command.op == parse.OP_CONDITIONAL_NZERO:
		# TODO - execute the second command only if the first one returns non zero
		return do_cond_nzero(command.com1, command.com2, command)
	elif command.op == parse.OP_CONDITIONAL_ZERO:
		# TODO - execute the second command only if the first one returns zero
		return do_cond_zero(command.com1, command.com2, command)
	elif command.op == parse.OP_PIPE:
		# TODO - redirect the output of the first command to the input of the second
		return 0 # TODO - replace with actual exit code of command


try:
	while True:
		line = input('$ ')
		command = parse.parse(line)
		# print the resulting object, for debugging only
		#parse.dump(command)
		# TODO - delete the line before submitting the homework
		parse_command (command)
except EOFError:
		pass
