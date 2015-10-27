urls = [
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&yrId=20196&yrId=20195&yrId=20194&yrId=20139&yrId=20138&yrId=20140&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=99999&mdId=21906&mkId=20028&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId-mdId&pgId=2102&rpp=250"
]


import pickle

batch_size = len(urls) / 1
for x in range(0, len(urls), batch_size):
	sub_arr = urls[x:x+batch_size]
	pickle.dump (sub_arr, open('urls_%d.p' %(x/batch_size), 'wb'))

# import glob, pickle
# test = []
# for x in glob.glob ('*.p'):
# 	for y in pickle.load(open(x, 'rb')):
# 		test.append (y)
# print len (test)
# print set(urls).difference(set(test))
