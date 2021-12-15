import datetime

def	strToInt(string):
	ret = 0
	for letter in string:
		if letter.isnumeric():
			number = int(letter)
			ret = ret * 10
			ret = ret + number
	return ret

def myPrint(*args):
	#Add log
    print("[" + str(datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")) + "]" +" ".join(map(str,args)))