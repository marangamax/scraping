from amazon_tables import engine, session, AmazonProducts
from db_connection import DBconnection

import pandas as pd
import pandas.io.sql as sql

try:
	amazon_db = sql.read_sql("SELECT * FROM analytics.amazon_db", con = engine)
	amazon_data = sql.read_sql("SELECT * FROM analytics.amazon_data", con = engine)
except:
	print "fail querying the data"

try:
	new_amazon_products = amazon_db[['gtin', 'ASIN', 'name']].drop_duplicates().reset_index(drop=True)
	new_amazon_products_2 = new_amazon_products.merge(amazon_data[['ASIN', 'parentASIN', 'has_reviews', 'binding', 'brand']], how='outer', on='ASIN')
except:
	print "fail joining data"

try:
	ff_conn = DBconnection("foxfeed_mySql_config.yaml")
	ff_engine = ff_conn.get_engine()

	product_ids = sql.read_sql("SELECT id, gtin FROM products", con=ff_engine)
	final_amazon_products = product_ids.merge(new_amazon_products_2, how='right', on='gtin')
except:
	print "fail making connection to database"

try:
	final_amazon_products['API_method'] = final_amazon_products.ASIN.apply(lambda x: 'itemLookup' if x != '-1' else '-1')
	final_amazon_products.drop_duplicates(inplace=True)
	final_amazon_products.drop_duplicates('id', inplace=True)
except:
	print "fail dropping duplicates"

try:
	def chunks(l, n):
	    """Yield successive n-sized chunks from l."""
	    for i in xrange(0, len(l), n):
	        yield l[i:i+n]
	        
	list_df = list()
	n_loc = 1000
	for _ in range(len([i for i in chunks(final_amazon_products, 1000)])):
	    list_df.append(final_amazon_products.iloc[n_loc-1000: n_loc, :])
	    n_loc += 1000

	count = 0
	for df in list_df:
		df["created_at"] = ff_conn.get_date("YYYY-MM-DD hh:mm:ss")
		df.to_sql("amazon_products", con=engine, schema="analytics", if_exists="append", index=False)
		count += 1
		print "%s out of %s inserted" % (count, str(len(list_df)))

except:
	print "fail inserting data"
	print final_amazon_products
