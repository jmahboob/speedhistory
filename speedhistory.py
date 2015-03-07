import os
import sqlite3
import speedtest_cli
import time

# First connect to the local sqlite db
# File is created if it doesn't exist in the local directory
conn = sqlite3.connect('db.sqlite')

# Next we need to setup our speedtest_cli information
# Get the generic "config"
config = speedtest_cli.getConfig()
servers = speedtest_cli.closestServers(config['client'], False)
best = speedtest_cli.getBestServer(servers)
sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
urls = []
for size in sizes:
	for i in range(0, 4):
		urls.append('%s/random%sx%s.jpg' % (os.path.dirname(best['url']), size, size))
print sizes
print urls

# Time to actually do this
epoch = int(time.time())
dlspeed = speedtest_cli.downloadSpeed(urls, True)
#ulspeed = speedtest_cli.uploadSpeed(urls, sizes, True)
ulspeed = 0

# Build the tuple we'll be inserting into the table
# Table Structure
#	date - int
#	latency - real
#	name - text
#	lon - real
#	lat - real
#	rawdl - real
#	rawul - real
#	convdl - real
#	convul - real
line = (epoch, best['latency'], best['name'], best['lon'], best['lat'], dlspeed, ulspeed)

c = conn.cursor()

try:
	c.execute (''' create table tests
		(int epoch,
		real latency,
		name text,
		lon real,
		lat real,
		rawdl real,
		rawul real)
	''')
except sqlite3.OperationalError:
	pass

print 'Hurray\n'
print dlspeed

c.execute('insert into tests values (?,?,?,?,?,?,?)', line)

conn.commit()

c.close()
