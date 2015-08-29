import pymongo, zipfile, zlib, os.path
from pymongo.son_manipulator import SONManipulator
from pymongo import MongoClient

client_host = "localhost"
client_port = 27017

client = MongoClient (client_host, client_port)

for x in client['pure_images'].images.find({}):
	file_name = x['label'] + '_batch_' + str(len(x['ext'])) + '.zip'
	zip_file = zipfile.ZipFile (file_name, mode='w')
	for image_path in x['ext']:
		image_name = image_path.split('/')[-1]
		zip_file.write (filename=image_path, arcname=image_name, compress_type=zipfile.ZIP_DEFLATED)
	zip_file.close()
	print "[Zipped %s] with %d images" %(file_name, len(x['ext']))
