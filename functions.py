def	strToInt(string):
	ret = 0
	for letter in string:
		if letter.isnumeric():
			number = int(letter)
			ret = ret * 10
			ret = ret + number
	return ret