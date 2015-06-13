import os
from datetime import datetime


#check existance of log file --------------
def isLogFile(logfile):
	if os.path.isfile(logfile):
		return True
	else:
		return False


#write message to log file ----------------
def writeLog(logfile, msg):
	if not logfile.endswith(".txt"):
		logfile += ".txt"

	log = open(logfile, 'a')
	logmsg = '[' + str(datetime.now()) + ']'

	if isinstance(msg, str):
		logmsg += msg + "\n"
	else:
		logmsg += str(msg) + "\n"

	log.write(logmsg)
	log.close()

#add message to log file ------------------
def addLog(logfile, msg):
	if not logfile.endswith(".txt"):
		logfile += ".txt"

	log = open(logfile, 'a')
	logmsg = '[' + str(datetime.now()) + ']'

	if isinstance(msg, str):
		logmsg += msg
	else:
		logmsg += str(msg)

	log.write(logmsg)
	log.close()
