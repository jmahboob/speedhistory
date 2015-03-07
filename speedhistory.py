import speedtest_cli
import sys, os
import sqlite3
import time

# At the moment, this main function from the library initializes a few global variables
# related to threads that are necessary to cleanly ctrl-c
# Either need to clean this up so this can be removed or strip the functionality from the library
speedtest_cli.speedtest()

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

ulsizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
ulsizes = []
for ulsize in ulsizesizes:
	for i in range(0, 25):
		ulsizes.append(ulsize)


# Time to actually do this
for i in range(10):

	epoch = int(time.time())

	sys.stdout.write("Downloading...")
	dlspeed = speedtest_cli.downloadSpeed(urls, False)
	convdl = (dlspeed / 1000 / 1000) * 8
	print "Speed - %0.2f Mbit/s" % convdl

	sys.stdout.write("Uploading...")
	ulspeed = speedtest_cli.uploadSpeed(best['url'], ulsizes, False)
	convul = (ulspeed / 1000 / 1000) * 8
	print "Speed - %0.2f Mbit/s\n" % convul

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
	line = (epoch, best['latency'], best['name'], best['lon'], best['lat'], dlspeed, ulspeed, convdl, convul)

	c = conn.cursor()

	try:
		c.execute (''' create table tests
			(int epoch,
			real latency,
			name text,
			lon real,
			lat real,
			rawdl real,
			rawul real,
			convdl real,
			convul real)
		''')
	except sqlite3.OperationalError:
		pass

	c.execute('insert into tests values (?,?,?,?,?,?,?,?,?)', line)

	conn.commit()

c.close()
