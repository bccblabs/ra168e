import glob, json, pickle, re

urls = []
for x in glob.glob ('*.json'):
	with open (x, 'rb') as f:
		data = json.load (f, strict=False)
		for url in data['Series']:
				urls.append (re.sub ('[^A-Za-z0-9/-]', '', url['Value']['ActionUrl']))
print len (urls)
pickle.dump (urls, open ('iihs_urls.p', 'wb'))