import re
from collections import namedtuple
import sys

Token=namedtuple('Token',['typ','content','bounds'])

reserved_words=set(['class','struct','module','func',
'for','sequential','persistent','task',
'export','rasterize','import','type'])

tokrestr=r'(?P<number>\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|(?P<comment1>/\*.*\*/)|//(?P<comment2>.*?)$|(?P<punctuation>[^\w\s])|(?P<symbol>\w+)'
tokre=re.compile(tokrestr,re.M | re.S)
def tokenizer(source):
	for mo in tokre.finditer(source):
		for k,v in mo.groupdict().items():
			if(v):
				ko,vo=k,v
		content=vo
		typ=ko
		if(typ=='comment1' or typ=='comment2'):
			typ='comment'
		if(typ=='symbol' and content in reserved_words):
			typ='reserved'
		yield Token(typ=typ,content=content,bounds=mo.span())


if(__name__=="__main__"):
	for t in tokenizer(sys.stdin.read()):
		print(t)

