
from db_connection import DBconnection
from sqlalchemy import Column, String, Integer, Numeric, Date
from sqlalchemy_utils import ArrowType

db_conn = DBconnection("locafox_config.yaml", "analytics")
db_eng = db_conn.get_engine()
session = db_conn.get_session()
hash_id = db_conn.get_hash_id
time_stamp = db_conn.get_date


class spot_scrapper(db_conn.get_base()):
    __tablename__ = 'spot_scrapper'

    def __init__(self, **kwargs):
        if 'api_id' not in kwargs:
            kwargs['api_id'] = db_conn.get_hash_id(kwargs['store_id_api'], kwargs['gtin_live'], kwargs['timestamp_live_check'],
                            kwargs['availability_live'])
            self.id = kwargs['api_id']
        super(spot_scrapper, self).__init__(**kwargs)
        
    api_id = Column(String(32), primary_key=True)
    store_id_api = Column(String(255))
    gtin_live = Column(String(255))
    price_live = Column(Integer)
    price_scraped = Column(Integer)
    availability_live = Column(String(255))
    availability_scraped = Column(String(255))
    timestamp_live_check = Column(ArrowType, default=db_conn.get_date("YYYY-MM-DD HH:mm:ss", hours=2))
    timestamp_scraped = Column(ArrowType, default=db_conn.get_date("YYYY-MM-DD HH:mm:ss", hours=2))
    store_name_api = Column(String(5000))
    url_api = Column(String(5000)) 
    product_name_api = Column(String(5000))
    
def create_analytics_tables():
    db_conn.get_metadata().create_all()
        
if __name__ == '__main__':
    create_analytics_tables()
