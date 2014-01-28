Installation
============
pip install loggingd

or 

easy_install loggingd

Introduction
============

Loggingd is based on decorated (https://github.com/CooledCoffee/decorated).

Code without logging:

	def divide(a, b):
	    return a / b
	    
Old style logging:

	import logging
	
	def divide(a, b):
	    logging.info('Calculating %d / %d ...' % (a, b))
	    try:
	        result = a / b
	        logging.info('Result is %d.' % result)
	    except Exception as e:
	        logging.warn('Failed to calc. Error is "%s".' % e, exc_info=True)
	        raise
	
	logging.getLogger().setLevel(logging.DEBUG)
	logging.basicConfig()
	divide(2, 1)
	
Using loggingd:

	from loggingd import log_enter, log_return, log_error
	import loggingd
	
	@log_enter('Calculating {a} / {b} ...')
	@log_return('Result is {ret}.')
	@log_error('Failed to calc. Error is "{e}".', exc_info=True)
	def divide(a, b):
	    return a / b
	
	loggingd.init(loggingd.DEBUG)
	loggingd.add_console_handler(loggingd.DEBUG)
	divide(2, 1)
	
Specify logging level:

	from loggingd import log_enter, log_return, log_error
	
	@log_enter('[INFO] Calculating {a} / {b} ...')
	@log_return('[DEBUG] Result is {ret}.')
	@log_error('[ERROR] Failed to calc. Error is "{e}".', exc_info=True)
	def divide(a, b):
	    return a / b
	
	loggingd.init(loggingd.DEBUG)
	loggingd.add_console_handler(loggingd.DEBUG)
	divide(2, 1)
	    
Conditional logging:

	from loggingd import log_enter
	
	@log_enter('This is going to fail.', condition='b == 0')
	def divide(a, b):
	    return a / b
	
	loggingd.init(loggingd.DEBUG)
	loggingd.add_console_handler(loggingd.DEBUG)
	divide(2, 0)

Log exit:

	from loggingd import log_exit

	@log_exit('This is going to log on return and on exception.')
	def divide(a, b):
	    return a / b
	
	loggingd.init(loggingd.DEBUG)
	loggingd.add_console_handler(loggingd.DEBUG)
	divide(2, 1)

Python3 Support
===============
Loggingd is tested under python 2.7 and python 3.3.
