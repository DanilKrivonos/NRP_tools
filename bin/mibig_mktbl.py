#!/bin/env python

import json, glob, re, sys

bgclist = [line.rstrip('\n') for line in open(sys.argv[1])]
print('\t'.join(['Cluster', 'Module', 'Evidence', 'Specificity', 'Gene']))
for bgcp in bgclist:
	with open(bgcp) as data_file:
		data = json.load(data_file)
		if 'nrp' in data['cluster']:
			p = re.split('/', bgcp)
			p[-1] = p[-1].replace('.json', '')
			if 'nrps_genes' in data['cluster']['nrp']:
				for d in data['cluster']['nrp']['nrps_genes']:
					for m in d['modules']:
						if 'a_substr_spec' in m:
							mod = str(d['modules'])
							a = m['a_substr_spec']
							spec, evid = 'none', 'none'
							if 'evidence' in a:
								evid = a['evidence']
							if 'nonproteinogenic' in a:
								spec = a['nonproteinogenic']
							elif 'proteinogenic' in a:
								spec = a['proteinogenic']
							if (evid != 'none') and (spec != 'none'):
								if evid != 'Sequence-based prediction':
									print('\t'.join([p[-1], str(mod), str(evid), str(spec), d['gene_id'] ]))
								else:
									if 'compound' in data['cluster']:
										print('\t'.join([p[-1], str(mod), str(evid), str(spec), d['gene_id'] ]))
