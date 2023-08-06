import yake
from removedor import removedor

def removedordepalavraschaves(t):
	text = removedor(t)

	language = "pt-br"
	max_ngram_size = 3
	deduplication_threshold = 0.9
	deduplication_algo = 'seqm'
	windowSize = 1
	numOfKeywords = 20

	custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
	keywords = custom_kw_extractor.extract_keywords(text)

	devolver = None

	for kw in keywords:
		x = 0
		for k in kw:
			x += 1
			if x == 1:
				if devolver == None:
					devolver = f"'{k}'"
				else:
					devolver = f"{devolver}, '{k}'"
			else:
				x = 0

	return devolver