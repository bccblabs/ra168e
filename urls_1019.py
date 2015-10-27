urls = ["http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=250&photoId=46724&requestorTrackingInfo=RTB_SEARCH&yrId=20199&yrId=20198&yrId=20197&yrId=20143&yrId=20142&yrId=20141&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=99999&mdId=21906&mkId=20028&searchSource=SORT_USED&crSrtFlds=stkTypId-feedSegId-mkId-mdId&pgId=2102&sf1Nm=actualPhotoCount&sf1Dir=DESC&sf2Nm=price&sf2Dir=DESC",
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-1-0&crSrtFlds=stkTypId-feedSegId-mkId-mdId&feedSegId=28705&isDealerGrouping=false&rpp=250&sf1Dir=DESC&sf1Nm=actualPhotoCount&sf2Dir=DESC&sf2Nm=price&zc=92612&rd=99999&stkTypId=28881&mkId=20028&mdId=21906&photoId=46724&yrId=20194&yrId=20139&yrId=20195&yrId=20140&yrId=20196&yrId=20194&searchSource=GN_REFINEMENT"
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-1-0&crSrtFlds=stkTypId-feedSegId-mkId-mdId&feedSegId=28705&isDealerGrouping=false&rpp=250&sf1Dir=DESC&sf1Nm=actualPhotoCount&sf2Dir=DESC&sf2Nm=price&zc=92612&rd=99999&stkTypId=28881&mkId=20028&mdId=21906&photoId=46724&yrId=20138&searchSource=GN_REFINEMENT",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=250&photoId=46724&sf2Nm=price&requestorTrackingInfo=RTB_SEARCH&yrId=20193&sf1Nm=actualPhotoCount&sf2Dir=DESC&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=99999&mdId=21906&mkId=20028&sf1Dir=DESC&searchSource=GN_BREADCRUMB&crSrtFlds=stkTypId-feedSegId-mkId-mdId&pgId=2102"
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