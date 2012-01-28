from datetime import datetime, timedelta

"""convert a facebook time string to a datetime object.  Optionally include the UTC timezone offset, which defaults to -8 (Pacific Time)"""
def getTime(t, timezone=-8):
    return datetime.strptime(t, '%Y-%m-%dT%H:%M:%S+0000') + timedelta(hours=timezone)

def getFromTime():
	return datetime.now() - timedelta(days=7)
