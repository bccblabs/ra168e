def parseFloat (field):
	try:
		return float (Decimal (re.sub(r'[^\d.]', '', field)))
	except:
		return None

def cleanseField (field):
	try:
		return re.sub (r'\s\s+', ' ',field.encode ('ascii', 'ignore')).strip()
	except:
		return ''

def parseContent (fields):
	contentList = parseAlnum (fields)
	return ' '.join (contentList)

def parseMedia (mediaType, urlStrings):
	return [{'type': mediaType, 'link': x} for x in urlStrings]

def parseAlnum (fields):
	return filter (lambda item: len(item.strip()) > 0, [cleanseField (x) for x in fields])

def parseFirst (fieldSelector):
	try:
		return fieldSelector.extract()[0]
	except:
		return None