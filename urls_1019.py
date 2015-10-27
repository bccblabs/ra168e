urls = [
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=99999&mdId=20427&mkId=20008&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId-mdId&pgId=2102&rpp=250",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=99999&mdId=20648&mkId=20008&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId-mdId&pgId=2102&rpp=250",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=250&photoId=46724&requestorTrackingInfo=RTB_SEARCH&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=99999&mdId=20896&mkId=20008&searchSource=SORT_USED&crSrtFlds=stkTypId-feedSegId-mkId&pgId=2102&sf1Nm=actualPhotoCount&sf1Dir=DESC&sf2Nm=price&sf2Dir=DESC",
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-0-0&crSrtFlds=stkTypId-feedSegId-mkId&feedSegId=28705&isDealerGrouping=false&rpp=250&sf1Dir=DESC&sf1Nm=actualPhotoCount&sf2Dir=DESC&sf2Nm=price&zc=92612&rd=99999&stkTypId=28881&mkId=20008&photoId=46724&mdId=21801&mdId=20865&mdId=21801&searchSource=GN_REFINEMENT"
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