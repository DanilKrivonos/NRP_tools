#!/bin/env python

import json, glob, os, sys, re
from datetime import date

## Note, this will break on files of size 0 so runs
##	$ find mibigdir/ -size  0 -print0 |xargs -0 rm
## on the mibig json dir

os.system( 'find ' + sys.argv[1] + ' -size 0 -print0|xargs -0 rm 2> /dev/null' )
khayatt = date(2013,03,19) # set now to post-khayatt, can be changed in the future
dayssince = (date.today() - khayatt).days
for j in glob.glob( sys.argv[1] + '/*.json'):
	data_file  = open(j)
	try:
		data = json.load(data_file)
		for c in data['cluster']['biosyn_class']:
			if 'NRP' in c and 'publications' in data['cluster']:
				waszero = 0
				if 'pubmed' in [data['cluster']['publications']][0][0]:
					for pub in [data['general_params']['publications']]:
						for p in str(pub).split(','):
							if( not (re.search('\.', str(p) )) ): ## ignore non uid entries
								q = re.sub(r'\D', "", p)
								cmd = 'esearch -db pubmed -query "' + str(q) + '[uid]" | efilter -days ' + str(dayssince) + ' > tmp'
								os.system(cmd)
								tfh = open('tmp')
								content = tfh.readlines()
								count = re.search(r'<Count>(\d+)', str(content)).group(1)
								if(int(count) == 0):
									waszero = 1
				if(waszero == 0):
					print j
	except:
			sys.stderr.write( "Issue parsing " + j + "\n")
os.system('rm tmp')
