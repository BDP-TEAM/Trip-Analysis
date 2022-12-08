import sys
import re
from konlpy.tag import Okt
from hanspell import spell_checker
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawProtocol

class CountryCount(MRJob):
	OUTPUT_PROTOCOL = RawProtocol
	idx  = 0
	def steps(self):
		return [
				MRStep(mapper = self.map_country_count,
					reducer = self.reduce_country_count)
				]
	def map_country_count(self,_,line):
		content = line.strip()
		con = re.compile('[가-힣]+').findall(content)
		content = ''
		for s in con:
			content = content + s + ' '
		han_spell = spell_checker.check(content)
		if han_spell.result:
			content = han_spell.checked
		okt = Okt()
		content = okt.pos(content)
		for i in content:
			key = i[0] + ',' + i[1]
			yield (key,1)
	def reduce_country_count(self,key,values):
		CountryCount.idx += 1
		output = str(CountryCount.idx)+','+key+','+str(sum(values))
		yield None, output

if __name__ == '__main__':
	CountryCount.run()
