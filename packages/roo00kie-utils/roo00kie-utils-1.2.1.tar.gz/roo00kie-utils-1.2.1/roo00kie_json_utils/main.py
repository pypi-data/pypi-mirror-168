import json


def j_print(j):
	print(json.dumps(j, indent=4, ensure_ascii=False))
