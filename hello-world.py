#!/etc/bin/env python
# -*- coding: utf-8 -*-
#

class hello(object):
	
	def __init__(self, str='world'):
		self._name = str
		
	def __str__(self):
		return 'hello {}'.format(self._name)
		
	__repr__ = __str__
	
if __name__ == '__main__':
	
	print hello()
	print hello('friend!')