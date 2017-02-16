#!/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
import arrow
import math
import sys
import yaml

class DBconnection():
    def __init__(self, config_file, schema=None):
        self.__config_file = config_file
        self.__schema = schema
        self.__db_config = self.__load_config(self.__config_file)
        try:
            self.__db_user = self.__db_config.get("db_user")
            self.__db_passwd = self.__db_config.get("db_passwd")
            self.__db_name = self.__db_config.get("db_name")
            self.__db_host = self.__db_config.get("db_host")
        except KeyError:
            print "one of the config values is missing. Please check the config file."
            sys.exit(1)
        self.__engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (self.__db_user, self.__db_passwd, self.__db_host,
                                                                             self.__db_name))
        self.__metadata = MetaData(self.__engine, schema=self.__schema)
        self.__Base = declarative_base(metadata=self.__metadata)
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

    def get_engine(self):
        return self.__engine

    def get_base(self):
        return self.__Base

    def get_metadata(self):
        return self.__metadata

    def get_session(self):
        return self.__session

    def __load_config(self, config_path):
        try:
            with open(config_path, 'r') as db_connection:
                try:
                    return yaml.load(db_connection)
                except yaml.YAMLError as e:
                    sys.exit("Error {0}) : {1}".format(e.errno, e.strerror))
        except IOError as e:
            print config_path
            sys.exit("Error {0}) : {1}".format(e.errno, e.strerror))

    @staticmethod
    def get_hash_id(*args):
        tomd5 = "".join(str(args))
        id_hash = hashlib.md5(tomd5).hexdigest()
        return id_hash

    @staticmethod
    def get_date(date_format="", **kwargs):
        if kwargs is None:
            return arrow.now('Europe/Berlin') if date_format == "" else arrow.now('Europe/Berlin').format(date_format)
        else:
            return arrow.now('Europe/Berlin').replace(**kwargs) if date_format == "" else arrow.now('Europe/Berlin').replace(**kwargs).format(date_format)

			
class MySQLDBconnection():
    def __init__(self, config_file, schema=None):
        self.__config_file = config_file
        self.__schema = schema
        self.__db_config = self.__load_config(self.__config_file)
        try:
            self.__db_user = self.__db_config.get("db_user")
            self.__db_passwd = self.__db_config.get("db_passwd")
            self.__db_name = self.__db_config.get("db_name")
            self.__db_host = self.__db_config.get("db_host")
            self.__charset = self.__db_config.get("charset")
        except KeyError:
            print "one of the config values is missing. Please check the config file."
            sys.exit(1)
        self.__engine = create_engine('mysql+pymysql://%s:%s@%s/%s?%s' % (self.__db_user, self.__db_passwd, self.__db_host,
                                                                             self.__db_name, self.__charset))
        self.__metadata = MetaData(self.__engine, schema=self.__schema)
        self.__Base = declarative_base(metadata=self.__metadata)
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

    def get_engine(self):
        return self.__engine

    def get_base(self):
        return self.__Base

    def get_metadata(self):
        return self.__metadata

    def get_session(self):
        return self.__session

    def __load_config(self, config_path):
        try:
            with open(config_path, 'r') as db_connection:
                try:
                    return yaml.load(db_connection)
                except yaml.YAMLError as e:
                    sys.exit("Error {0}) : {1}".format(e.errno, e.strerror))
        except IOError as e:
            print config_path
            sys.exit("Error {0}) : {1}".format(e.errno, e.strerror))

    @staticmethod
    def get_hash_id(*args):
        tomd5 = "".join(str(args))
        id_hash = hashlib.md5(tomd5).hexdigest()
        return id_hash

    @staticmethod
    def get_date(date_format="", **kwargs):
        if kwargs is None:
            return arrow.now('Europe/Berlin') if date_format == "" else arrow.now('Europe/Berlin').format(date_format)
        else:
            return arrow.now('Europe/Berlin').replace(**kwargs) if date_format == "" else arrow.now('Europe/Berlin').replace(**kwargs).format(date_format)
