import sys, os, time, atexit
from signal import SIGTERM

class Daemon:
	def __new__(cls, *args, **kwargs):
		daemon = super().__new__(cls)
		daemon.__init__(*args, **kwargs)
		if len(sys.argv) == 2:
			_, command = sys.argv
			if command == "start":
				daemon.start()
			elif command == "stop":
				daemon.stop()
			elif command == "restart":
				daemon.restart()
			else:
				print("Unknown command")
				sys.exit(2)
			return daemon
		else:
			print(f"usage: {sys.argv[0]} start|stop|restart")
			sys.exit(2)

	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile


	def daemonize(self):
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError as e:
			sys.stderr.write(f"fork #1 failed: {e.errno} ({e.strerror})\n")
			sys.exit(1)

		os.chdir("/")
		os.setsid()
		os.umask(0)

		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError as e:
			sys.stderr.write(f"fork #2 failed: {e.errno} ({e.strerror})\n")
			sys.exit(1)

		# sys.stdout.flush()
		# sys.stderr.flush()

		# si = open(self.stdin, 'r')
		# so = open(self.stdout, 'a+')
		# se = open(self.stderr, 'a+',0)

		# os.dup2(si.fileno(), sys.stdin.fileno())
		# os.dup2(so.fileno(), sys.stdout.fileno())
		# os.dup2(se.fileno(), sys.stderr.fileno())


		atexit.register(self.delpid)
		with open(self.pidfile,'w+') as file:
			file.write(f"{os.getpid()}\n")

	def delpid(self):
		print("removing", flush=True)
		os.remove(self.pidfile)

	def start(self):
		try:
			with open(self.pidfile,'r') as file:
				pid = int(file.read().strip())
		except IOError:
			pid = None

		if pid:
			message = "pidfile %s already exist. Daemon already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)

		self.daemonize()
		self.run()

	def stop(self):
		try:
			with open(self.pidfile,'r') as file:
				pid = int(file.read().strip())
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stderr.write(message % self.pidfile)
			return

		try:
			while True:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print(str(err))
				sys.exit(1)

	def restart(self):
		self.stop()
		self.start()

	def run(self):
		"""
		You should override this method when you subclass Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""
		pass