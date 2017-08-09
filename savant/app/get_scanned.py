import os
from bassist.parser import host as parser_host
import logging
import logging.config
from app import record

def get_scanner_directory():
	os.chdir("/home/josiah/Documents/Doveps/mono/scanner/local/33.33.33.50/")

	scanner_directory = str(os.getcwd())
	print "get_scanner_directory: ", scanner_directory
	return scanner_directory

def parse():
	logger = logging.getLogger(__name__)
	scanner_directory = get_scanner_directory()
	print "Scanner_directory: ", scanner_directory
	
	logger.debug('importing parsers')
	parsed_host = parser_host.Host(scanner_directory)
	logger.debug('finished importing parsers')

	for parser in parsed_host.parsers:
		logger.debug('parser log: %s', parser.log)
		logger.debug('parsing: %s', parser.path)
		parser.parse()

	print "recording"
	for parser in parsed_host.parsers:
		print('Recording %s'%parser)
	
	record.record_all()

    