Introduction
============

Loggingd is a logging framework based on <a href="https://github.com/CooledCoffee/decorated" target="_blank">decorated</a>

Code without logging:

	def divide(a, b):
	    return a / b
	    
Old style logging:

	import logging
	
	def divide(a, b)
	    logging.info('Calculating %d / %d ...' % (a, b))
	    try:
	        result = a / b
	        logging.info('Result is %d.' % result)
	    except Exception as e:
	        logging.warn('Failed to calc. Error is "%s".' % e, exc_info=True)
	        raise
	
Using loggingd:

	from loggingd import log_enter, log_return, log_error
	
	@log_enter('Calculating {a} / {b} ...')
	@log_return('Result is {ret}.')
	@log_error('Failed to calc. Error is "{e}".', exc_info=True)
	def divide(a, b):
	    return a / b
	    
Conditional logging:

	from loggingd import log_enter
	
	@log_enter('This is going to fail.', condition='b == 0')
	def divide(a, b):
	    return a / b
	    
Installation
============
pip install loggingd

or 

easy_install loggingd

Author
======

Mengchen LEE: <a href="https://plus.google.com/117704742936410336204" target="_blank">Google Plus</a>, <a href="https://cn.linkedin.com/pub/mengchen-lee/30/8/23a" target="_blank">LinkedIn</a>
