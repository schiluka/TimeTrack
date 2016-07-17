# MYSQL
mysql_db_username = 'san'
mysql_db_password = 'local'
mysql_db_name = 'tt'
mysql_db_hostname = 'localhost'

DEBUG = True
PORT = 5500
HOST = "localhost"
SQLALCHEMY_ECHO = False
SECRET_KEY = "secret21"

# MySQL
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://san:local@localhost/tt".format(
		DB_USER=mysql_db_username,
		DB_PASS=mysql_db_password,
		DB_ADDR=mysql_db_hostname,
		DB_NAME=mysql_db_name)
# Email Server Configuration

MAIL_DEFAULT_SENDER = "san@localhost"

PASSWORD_RESET_EMAIL = """
Hi,

Please click on the link below to reset your password

<a href="/resetpassword/{token}> Reset Password </a>

--TimeTrack"""
