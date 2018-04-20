#!/usr/bin/env python

from icalendar import Calendar, vText
from datetime import datetime
import urllib2, pytz

def get_cal(url=None,fn=None):

	if url:
		usock = urllib2.urlopen(url,timeout=10)
		full = usock.read()
		usock.close()
	elif fn:
		with open(fn) as fp:
			full = fp.read()
	else:
		raise Exception("No calendar URL or fn given")
	
	return Calendar.from_ical(full)

def clear_road_locs(cal):
	EMPTY = vText('')
	for ev in cal.walk('vevent'):
		if '@' in ev.decoded('summary'):
			ev['location'] = EMPTY
	return cal

def clear_desc_boilerplate(cal):
	for ev in cal.walk('vevent'):
		desc = ev.decoded('description')
		ev['description'] = vText(desc[0:desc.find('Buy tickets here:')])
	return cal

def field_replacements(cal,field_to_dicts):
	for ev in cal.walk('vevent'):
		for field in field_to_dicts:
			text = ev.decoded(field)
			repls = field_to_dicts[field]
			for src in repls:
				text = text.replace(src,repls[src])
			ev[field] = vText(text)
	return cal

def clear_old_locs(cal):
	EMPTY = vText('')
	utcnow = pytz.utc.localize(datetime.utcnow())
	for ev in cal.walk('vevent'):
		if ev.decoded('dtstart') < utcnow:
			ev['location'] = EMPTY
	return cal	

def test():
	salem = get_cal('https://www.stanza.co/api/schedules/milb-salemredsox/milb-salemredsox.ics')
	salem = clear_road_locs(salem)
	salem = clear_desc_boilerplate(salem)
	teamsubs = { 'summary': { 'Red Sox':'SalemSox', 'Nationals':'P-Nats'} }
	salem = field_replacements(salem,teamsubs)
	return salem.to_ical()
	
"""
>>> import icalendar
>>> with open("squirrels.ics") as fp:
...     sq = fp.read()
... 
>>> cal = icalendar.Calendar.from_ics(sq)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: type object 'Calendar' has no attribute 'from_ics'
>>> cal = icalendar.Calendar.from_ical(sq)
>>> len(cal.walk('vevent'))
140
>>> opener = cal.walk('vevent')[0]
>>> from icalendar import vDatetime
>>> from datetime import datetime
>>> dtnow = datetime.now()
>>> dtnow
datetime.datetime(2018, 4, 18, 22, 32, 56, 439493)
>>> opener.decoded('dtstart')
datetime.datetime(2018, 4, 5, 23, 0, tzinfo=<UTC>)
>>> dtnow < opener.decoded('dtstart')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't compare offset-naive and offset-aware datetimes
>>> dtutc = datetime.utcnow()
>>> import pytz
>>> dtutc = pytz.utc.localize(dtutc)
>>> dtutc
datetime.datetime(2018, 4, 19, 3, 15, 28, 408115, tzinfo=<UTC>)
>>> opener.decoded('dtstart') < dtutc
True

"""
