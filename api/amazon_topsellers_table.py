from db_connection import DBconnection
from sqlalchemy import Column, String, Integer, Numeric, Date, Text
from sqlalchemy_utils import ArrowType

db_conn = DBconnection("locafox_config.yaml", "marketing")
db_eng = db_conn.get_engine()
session = db_conn.get_session()
hash_id = db_conn.get_hash_id
time_stamp = db_conn.get_date

class amazon_topseller(db_conn.get_base()):
    __tablename__ = 'amazon_topsellers'

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = db_conn.get_hash_id(kwargs['date_time'], kwargs['category'], kwargs['gtin'], kwargs['asin'], kwargs['rank'])
            self.id = kwargs['id']
        super(amazon_topseller, self).__init__(**kwargs)
            
    date_time = Column(ArrowType, default=db_conn.get_date("YYYY-MM-DD HH:mm:ss"))
    category = Column(String(255))
    asin = Column(String(255))
    gtin = Column(String(255))
    amazon_price = Column(Integer)
    marketplace_price = Column(Integer)
    rank = Column(Integer)
    id = Column(String(32), primary_key=True)
    category_level = Column(Integer)
    product_name = Column(Text)
    product_url = Column(Text)
    parent = Column(Text)



def create_amazon_topseller_tables():
    db_conn.get_metadata().create_all()
        
if __name__ == '__main__':
    create_amazon_topseller_tables()
