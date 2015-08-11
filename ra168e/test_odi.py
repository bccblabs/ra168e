
import json
json_path = '/Users/bski/Project/image_training/ra168e/ra168e/json/'
def construct_odi_url (year, make, model, model_id):
	url = "http://www-odi.nhtsa.dot.gov/owners/SearchResults?prodType=V&searchType=PROD&targetCategory=A&searchCriteria.model=%s&searchCriteria.model_yr=%s&searchCriteria.make=%s&searchCriteria.prod_ids=%s" %(model, year, make, model_id)
	return url

def parse_odi_json (json_file_name):



parse_odi_json("2013-16.json")