urls = [
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-1-0&bsId=20211&crSrtFlds=stkTypId-feedSegId-mkId-mdId&feedSegId=28705&isDealerGrouping=false&mdId=21179&mkId=20019&photoId=46724&requestorTrackingInfo=RTB_SEARCH&rpp=50&sf1Dir=DESC&sf1Nm=actualPhotoCount&sf2Dir=DESC&sf2Nm=price&stkTypId=28881&yrId=20199&yrId=20198&yrId=20143&zc=92612&rd=250&searchSource=UTILITY",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&PMmt=1-1-0&zc=92612&rd=100000&mdId=54539&mkId=20019&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=feedSegId-mkId-mdId&pgId=2102&rpp=100",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=100&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&PMmt=1-1-0&zc=92612&rd=100000&mdId=54539&mkId=20019&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=feedSegId-mkId-mdId&pgId=2102&rn=100",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=100000&mdId=52108&mkId=20019&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId-mdId&pgId=2102&rpp=100",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=100&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=100000&mdId=52108&mkId=20019&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId-mdId&pgId=2102&rn=100",
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-1-0&crSrtFlds=stkTypId-feedSegId-mkId&feedSegId=28705&isDealerGrouping=false&rpp=100&sf1Dir=DESC&sf1Nm=price&sf2Dir=ASC&sf2Nm=miles&zc=92612&rd=100000&stkTypId=28881&mkId=20019&mdId=21153&photoId=46724&bsId=20211&searchSource=GN_REFINEMENT",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=100&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-1-0&zc=92612&rd=100000&bsId=20211&mdId=21153&mkId=20019&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId&pgId=2102&rn=100",
"http://www.cars.com/for-sale/searchresults.action?PMmt=1-0-0&crSrtFlds=stkTypId-feedSegId-mkId&feedSegId=28705&isDealerGrouping=false&rpp=100&sf1Dir=DESC&sf1Nm=price&sf2Dir=ASC&sf2Nm=miles&zc=92612&rd=100000&stkTypId=28881&mkId=20019&bsId=20211&photoId=46724&mdId=21236&mdId=21279&mdId=21236&searchSource=GN_REFINEMENT",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=100&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-2-0&zc=92612&rd=100000&bsId=20211&mdId=21236&mdId=21279&mkId=20019&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId&pgId=2102&rn=100",
"http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&rpp=100&photoId=46724&sf2Nm=miles&requestorTrackingInfo=RTB_SEARCH&sf1Nm=price&sf2Dir=ASC&stkTypId=28881&PMmt=1-2-0&zc=92612&rd=100000&bsId=20211&mdId=21236&mdId=21279&mkId=20019&sf1Dir=DESC&searchSource=UTILITY&crSrtFlds=stkTypId-feedSegId-mkId&pgId=2102&rn=200"
]


import pickle

batch_size = len(urls) / 4
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
