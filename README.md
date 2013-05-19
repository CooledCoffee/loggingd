Introduction
============
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
	    
Specify logging level:

	from loggingd import log_enter, log_return, log_error
	
	@log_enter('[INFO] Calculating {a} / {b} ...')
	@log_return('[DEBUG] Result is {ret}.')
	@log_error('[ERROR] Failed to calc. Error is "{e}".', exc_info=True)
	def divide(a, b):
	    return a / b
	    
Conditional logging:

	from loggingd import log_enter
	
	@log_enter('This is going to fail.', condition='b == 0')
	def divide(a, b):
	    return a / b

Log exit:

	from loggingd import log_exit

	@log_exit('This is going to log on return and on exception.')
	def divide(a, b):
	    return a / b

Installation
============
pip install loggingd

or 

easy_install loggingd

Python3 Support
===============
Loggingd is tested under python 2.7 and python 3.3.
