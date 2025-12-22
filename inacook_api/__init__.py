import sys
try:
	import pymysql
	pymysql.install_as_MySQLdb()
	sys.stderr.write('INFO: PyMySQL shim installed (pymysql.install_as_MySQLdb)\n')
except Exception as e:
	# If pymysql isn't installed yet, leave a clear message in stderr so PA logs show it
	sys.stderr.write(f'INFO: PyMySQL shim NOT installed: {e}\n')

