#!/usr/bin/env python

from icalendar import Calendar, vText
from datetime import datetime, date
import urllib2, pytz

CAROLINA_LEAGUE_SUBS = { 'summary': { 'Red Sox':'SalemSox', 'Nationals':'P-Nats', 'Astros':'BC Astros'} }
EASTERN_LEAGUE_SUBS = { 'summary': { 'Flying Squirrels':'Squirrels'}}

TOKEN_TO_SUBSET = { 'salemredsox':CAROLINA_LEAGUE_SUBS, 'potomacnationals':CAROLINA_LEAGUE_SUBS, 'richmondflyingsquirrels':EASTERN_LEAGUE_SUBS,'lynchburghillcats':CAROLINA_LEAGUE_SUBS}


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
	oldtest = False
	for ev in cal.walk('vevent'):
		evtime = ev.decoded('dtstart')
		if evtime == None:
			continue
		if isinstance(evtime,date):
			# make it an evtime with midnight UTC
			evtime = pytz.utc.localize(datetime.combine(evtime,datetime.min.time()))
		if evtime < utcnow:
			ev['location'] = EMPTY
	return cal


def do_milb(teamtoken):
	cal = get_cal('https://www.stanza.co/api/schedules/milb-' + teamtoken  + '/milb-' + teamtoken + '.ics')
	cal = clear_road_locs(cal)
	cal = clear_old_locs(cal)
	cal = clear_desc_boilerplate(cal)
	if teamtoken in TOKEN_TO_SUBSET:
		cal = field_replacements(cal,TOKEN_TO_SUBSET[teamtoken])
	return cal.to_ical()
	
def test():
	return do_milb('salemredsox')
	
