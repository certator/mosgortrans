import fnmatch
import os
import json
import re

matches = []
for root, dirnames, filenames in os.walk('out'):
    for filename in fnmatch.filter(filenames, '*.json'):
        matches += [root + '/' + filename]

data = []

for m in matches:
    with open(m) as f:
        data += [json.load(f)]
        
rr = {}

for d in data:
    r = rr.setdefault(d['route'], {})
    dy = r.setdefault(d['day'], {})
    dy[d['direction']] = d

tq = {}
tt = []

metros = [u'Каширская' , u'Кантемировская', u'Царицыно']
def hs_to_ts(s):
    return (int(s[0:2]), int(s[3:5]))

for route, r in rr.items():
    if not '1111100' in r:
        print 'not work wp', route
        continue
    for dr, wp in r['1111100'].items():
        metro_idx = None
        metro_wp = None
        metro_idx_t = None
        metros = [u'Каширская' , u'Кантемировская', u'Царицыно']
        home_idx = None
        home_wp = None
        for k in sorted(wp['waypoints_list']):
            idx = re.match(r'(\d+).*', k).groups()[0] 

            if u'Метро' in k:
                for m in metros:
                    if m in k:
                        #print route, dr, idx, k
                        metro_idx = idx
                        metro_idx_t = m
                        metro_wp = k                    
            
            if u'Бирюлевская' in k:
                #print route, dr, idx, k
                home_idx = idx
                home_wp = k
            if u'Элеваторная' in k:
                #print route, dr, idx, k
                home_idx = idx
                home_wp = k
        #print route, dr, metro_idx, home_idx
        if metro_idx is None or home_idx is None:
            print '---no home'
            continue
        if int(metro_idx) > int(home_idx):
            continue
        print '+++to home', route, metro_idx_t
        for t in wp['waypoints'][metro_wp]:
            t = hs_to_ts(t)
            q = int((t[0]*60 + t[1])/15)
            k = (q, metro_idx_t, t, route)
            

            tt += [k]
            
        

#build flat table
rt = []
tq = {}


for q, metro_idx_t, t, route in sorted(tt):
    #print q, metro_idx_t
    ti = tq.setdefault(q, {})
    ti.setdefault(metro_idx_t, [])
    ti[metro_idx_t] += ['%d-%d/%s' % (t[0], t[1], route)]

print '\t', '\t'.join(metros)
    
for q in sorted(tq.keys()):
    print q, '\t',
    for i in range(0, 3):
        print ', '.join(tq[q].get(metros[i], [])), '\t',
    print ''

