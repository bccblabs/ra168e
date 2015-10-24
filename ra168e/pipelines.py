import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import numpy as np
import sys, glob
caffe_root = "/home/ubuntu/caffe/"
images_root = "/home/ubuntu/pure_images6/"

sys.path.insert (0, caffe_root + "/python")
import caffe
import numpy as np
caffe.set_mode_cpu()
blob = caffe.proto.caffe_pb2.BlobProto()
c0 = caffe.Classifier (
                caffe_root + "models/ext_int/gnet_deploy.prototxt",
                caffe_root + "models/ext_int/gnet_pre.caffemodel",
                channel_swap = (2,1,0),
                raw_scale = 255,
                image_dims = (256, 256)
)

class DownloadClassifyPipeline (ImagesPipeline):
	def get_media_requests (self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)
	def item_completed (self, results, item, info):
		images_path = [x['path'] for ok, x in results if ok]
		ext_images = []
		int_parts = []
		consec_int = 0
		for x in images_path:
			sample_path = images_root + x
			image = caffe.io.load_image(sample_path)
			resized_image = caffe.io.resize_image (image, (256,256,3))
			res = c0.predict ([resized_image])
			clz = np.argmax(res[0])
			print clz
			if consec_int > 3:
				break
			elif clz > 0:
				consec_int = consec_int + 1
				int_parts.append (sample_path)
			elif clz == 0:
				consec_int = 0
				ext_images.append (sample_path)
		item['ext'] = ext_images
		item['int_parts'] = int_parts
		return item

