urls = [
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-1-0&crSrtFlds=feedSegId-mkId-mdId&feedSegId=28705&isDealerGrouping=false&rpp=250&sf1Dir=DESC&sf1Nm=actualPhotoCount&sf2Dir=DESC&sf2Nm=price&zc=92612&rd=99999&mkId=20072&mdId=21197&photoId=46724&searchSource=GN_REFINEMENT",
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-0-0&crSrtFlds=feedSegId-mkId&feedSegId=28705&isDealerGrouping=false&rpp=250&sf1Dir=DESC&sf1Nm=actualPhotoCount&sf2Dir=DESC&sf2Nm=price&zc=92612&rd=99999&mkId=20072&photoId=46724&mdId=21814&searchSource=GN_REFINEMENT",
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-1-0&crSrtFlds=feedSegId-mkId-mdId&feedSegId=28705&isDealerGrouping=false&rpp=50&sf1Dir=DESC&sf1Nm=actualPhotoCount&sf2Dir=DESC&sf2Nm=price&zc=92612&rd=100000&mkId=20049&mdId=22159&yrId=58487&searchSource=GN_REFINEMENT",

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