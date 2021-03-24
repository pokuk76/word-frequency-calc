"""
Now we’ll be able to import the appropriate config class based on the
current environment. Thus, we can use environment variables to choose which
settings we’re going to use based on the environment - e.g., local, staging,
production.
"""

import os

# set the basedir variable as a relative path from any place we call it to 
# this file
basedir = os.path.abspath(os.path.dirname(__file__))

class Config (object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'this-really-needs-to-be-changed'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	""" How would we go about having different databases for development 
		and production/staging? """

class ProductionConfig(Config):
	DEBUG =  False

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	TESTING = True

