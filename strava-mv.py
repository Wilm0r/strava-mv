#!/usr/bin/python

import datetime
import dbm

from stravalib.client import Client
from stravalib.attributes import LatLon
import units

LOGIN = file("access_token").read().strip()
BIKES = {
	"Madone": "b1258359",
	"Secteur": "b1708741",
	"Random": "b1209450",
}
# Strava rounds to two decimals which isn't terribly precise but at least easy
# for comparisons.
WORK = LatLon(lat=51.49, lon=-0.15)

client = Client()
client.access_token = LOGIN

def build_updates(act):
	ret = {}

	if act.type != act.RIDE:
		if (act.start_latlng == WORK and
		    act.start_date_local.weekday() <= 4):
			ret["name"] = "Walking commute"
			ret["commute"] = True
			ret["activity_type"] = act.WALK

		# I don't record walks that often anyway.
		return
	
	segments = [se.segment.id for se in act.segment_efforts]

	if act.location_country == "United Kingdom":
		if act.average_cadence is not None:
			# Only my Trek has a candence sensor.
			ret["gear_id"] = BIKES["Madone"]
		# Else it's my Gazelle or a Santander, how to guess?
	else:
		# Outside my home country it's usually not my own bike.
		ret["gear_id"] = BIKES["Random"]
		if (act.location_country == "Netherlands" and
		    act.average_cadence is not None):
			# Oh, or maybe the Secteur in .nl?
			ret["gear_id"] = BIKES["Secteur"]

	if (act.start_date_local.weekday() > 4):
		# Weekend. No clue, what do I do then? :>
		ret["name"] = "Weekend ride"
		pass
	else:
		# Weekday. Sooo... commute?
		if (act.distance > units.unit("km")(5)):
			# Longer than usual. Where was I going?
			pass
		elif (1594398 in segments):
			ret["name"] = "Morning commute"
			ret["commute"] = True
		elif (1547949 in segments):
			ret["name"] = "Evening commute"
			ret["commute"] = True

	if "name" in ret and not (act.name.endswith("rit") or act.name.endswith(" Ride")):
		# May already not be the default name anymore.
		del ret["name"]

	return ret

seen = dbm.open("seen", "c")

after = datetime.datetime.now() - datetime.timedelta(days=2)
for act in act for act in client.get_activities(after=after, limit=5):
	if str(act.id) in seen:
		continue
	full = client.get_activity(act.id)
	print full
	updates = build_updates(full)
	print updates
	seen[str(act.id)] = "1"
	if updates:
		updates["activity_id"] = act.id
		print client.update_activity(**updates)
