from datetime import datetime, timedelta

def getTime(t):
    return datetime.strptime(t, '%Y-%m-%dT%H:%M:%S+0000')
def getFromTime():
	return datetime.now() - timedelta(days=7)
