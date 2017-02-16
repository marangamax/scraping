# -*- coding: utf-8 -*-
from lxml import html
from amazonproduct import API
import amazonproduct
import requests
import re
import sys
import time
from amazon_topseller_tables import amazon_topseller
from db_connection import DBconnection


AWS_KEY = 'AKIAIJ42FBEUQPGK4T5Q'
SECRET_KEY = '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'
ASSOCIATE_TAG = 'locafox09-21'
db_config = 'locafox_config.yaml'
psql_schema = 'marketing'


def add_to_database(catASINGTINpriceMPpriceRankProductNameURL):
    db_conn = DBconnection(db_config, psql_schema)
    session = db_conn.get_session()
    time_stamp = db_conn.get_date("YYYY-MM-DD hh:mm:ss")
    
       
    
    rows_to_insert = []
    

    for row in catASINGTINpriceMPpriceRankProductNameURL:
        entry = amazon_topseller(date_time = DBconnection.get_date("YYYY-MM-DD HH:mm:ss"), category = row[0], asin = row[1], gtin = row[2], amazon_price = int(row[3]), marketplace_price = int(row[4]), rank = int(str(row[5])), product_name = row[6], product_url = row[7], category_level = 1 if row[0] == 'Elektronik' else 2, parent = 'Elektronik')
        rows_to_insert.append(entry)
        
    session.add_all(rows_to_insert)
    
    
    print " %s - %s new entries were added to the database" % (time_stamp, len(rows_to_insert))

    session.commit()

def get_amazon_api_data_EAN(catASINranks):

    api = API(AWS_KEY, SECRET_KEY, 'de', ASSOCIATE_TAG)
    catASINGTINranks = []
    
    for ASIN in catASINranks:
        try:
            productEANs = api.item_lookup(str(ASIN[1]),IdType='ASIN',ResponseGroup='ItemAttributes')
            if hasattr(productEANs.Items[0].Item[0].ItemAttributes[0],'EAN'):
                catASINGTINranks.append((ASIN[0],ASIN[1],str(productEANs.Items[0].Item[0].ItemAttributes[0].EAN),ASIN[2]))
            else:
                catASINGTINranks.append((ASIN[0],ASIN[1],-1,ASIN[2]))
    
        except :
            catASINGTINranks.append((ASIN[0],ASIN[1],-1,ASIN[2]))
    
	   
    get_amazon_api_data_price(catASINGTINranks)

def get_amazon_api_data_price(catASINGTINranks):
    
    api = API(AWS_KEY, SECRET_KEY, 'de', ASSOCIATE_TAG)
    catASINGTINpriceranks = []
    
    for ASIN in catASINGTINranks:
        try:
            productPrices = api.item_lookup(str(ASIN[1]),IdType = 'ASIN', ResponseGroup='Offers')
            if hasattr(productPrices,'Items'):
                if hasattr(productPrices.Items[0],'Item'):
                    if hasattr(productPrices.Items[0].Item[0],'Offers'):
                        if hasattr(productPrices.Items[0].Item[0].Offers[0],'TotalOffers'):
                            if int(productPrices.Items[0].Item[0].Offers[0].TotalOffers) > 0 :
				if hasattr(productPrices.Items[0].Item[0].Offers[0].Offer[0].OfferListing[0],'SalePrice'):
                                    catASINGTINpriceranks.append((ASIN[0],ASIN[1],ASIN[2],str(productPrices.Items[0].Item[0].Offers[0].Offer[0].OfferListing[0].SalePrice[0].Amount),ASIN[3]))
				else:
                                    catASINGTINpriceranks.append((ASIN[0],ASIN[1],ASIN[2],str(productPrices.Items[0].Item[0].Offers[0].Offer[0].OfferListing[0].Price[0].Amount),ASIN[3]))
                            else:
                                catASINGTINpriceranks.append((ASIN[0],ASIN[1],ASIN[2],-1,ASIN[3]))

        except :
            catASINGTINpriceranks.append((ASIN[0],ASIN[1],ASIN[2],-1,ASIN[3]))
    
                 
    get_amazon_api_data_marketplaceprice(catASINGTINpriceranks)

def get_amazon_api_data_marketplaceprice(catASINGTINpriceranks):
    
    api = API(AWS_KEY, SECRET_KEY, 'de', ASSOCIATE_TAG)
    catASINGTINpriceMPpriceranks = []
    
    for ASIN in catASINGTINpriceranks:
        try:
            productPrices = api.item_lookup(str(ASIN[1]),IdType = 'ASIN', ResponseGroup='OfferSummary')
            if hasattr(productPrices,'Items'):
                if hasattr(productPrices.Items[0],'Item'):
                    if hasattr(productPrices.Items[0].Item[0],'OfferSummary'):
                        if hasattr(productPrices.Items[0].Item[0].OfferSummary[0],'LowestNewPrice'):
                            catASINGTINpriceMPpriceranks.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],str(productPrices.Items[0].Item[0].OfferSummary[0].LowestNewPrice[0].Amount),ASIN[4]))
                        else:
                            catASINGTINpriceMPpriceranks.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],-1,ASIN[4]))
        except :
            catASINGTINpriceMPpriceranks.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],-1,ASIN[4]))
    
    
    get_amazon_api_data_productname(catASINGTINpriceMPpriceranks)
    #for alldetail in catASINGTINpriceMPpriceranks:
        #print alldetail[0],alldetail[1],alldetail[2],alldetail[3],alldetail[4],alldetail[5]

def get_amazon_api_data_productname(catASINGTINpriceMPpriceranks):
    
    api = API(AWS_KEY, SECRET_KEY, 'de', ASSOCIATE_TAG)
    catASINGTINpriceMPpriceRankProductName = []
    
    for ASIN in catASINGTINpriceMPpriceranks:
        try:
            time.sleep(0.2)
            productName = api.item_lookup(str(ASIN[1]), IdType = 'ASIN', ResponseGroup='ItemAttributes')
            if hasattr(productName.Items[0].Item[0].ItemAttributes[0],'Title'):
		title = u''+productName.Items[0].Item[0].ItemAttributes[0].Title
                catASINGTINpriceMPpriceRankProductName.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],ASIN[4],ASIN[5],title))
            else:
                catASINGTINpriceMPpriceRankProductName.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],ASIN[4],ASIN[5],-1))
        
        except:
            catASINGTINpriceMPpriceRankProductName.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],ASIN[4],ASIN[5],-1))
            
	
    get_amazon_api_data_productURL(catASINGTINpriceMPpriceRankProductName)
            
def get_amazon_api_data_productURL(catASINGTINpriceMPpriceRankProductName):
    
    api = API(AWS_KEY, SECRET_KEY, 'de', ASSOCIATE_TAG)
    catASINGTINpriceMPpriceRankProductNameURL = []
    
    for ASIN in catASINGTINpriceMPpriceRankProductName:
        try:
            time.sleep(0.2)
	    productURL = api.item_lookup(str(ASIN[1]), IdType = 'ASIN', ResponseGroup='ItemAttributes')
            if hasattr(productURL.Items[0].Item[0],'DetailPageURL'):
                url = u''+productURL.Items[0].Item[0].DetailPageURL 
                catASINGTINpriceMPpriceRankProductNameURL.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],ASIN[4],ASIN[5],ASIN[6],url))
            else:
                catASINGTINpriceMPpriceRankProductNameURL.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],ASIN[4],ASIN[5],ASIN[6],-1))
        
        except:
            catASINGTINpriceMPpriceRankProductNameURL.append((ASIN[0],ASIN[1],ASIN[2],ASIN[3],ASIN[4],ASIN[5],ASIN[6],-1))
            
    add_to_database(catASINGTINpriceMPpriceRankProductNameURL)		

def scrape_amazon(cat,url):
    htmltext = requests.get(url)
    
    xpath_ranks = '//span[@class="zg_rankNumber"]/text()'
    tree = html.fromstring(htmltext.text)
    ranks = tree.xpath(xpath_ranks)

    ranklist = []
    for rank in ranks:
        rankarr = str(rank).split('.')
        ranklist.append(str(rankarr[0]))
    
    
    xpath_products = '//div[@class="zg_itemImageImmersion"]/a/@href'
    products = tree.xpath(xpath_products)

    i = 0

    catASINranks = []
    for product in products:
        productwonewline = str(product).replace("\n","")
        #print productwonewline
        asin = productwonewline.split('dp/')
        if(len(asin)>1):
            catASINranks.append((cat,str(asin[1]),ranklist[i]))
        i= i + 1

    get_amazon_api_data_EAN(catASINranks)
    #for catASINrank in catASINranks:
        #print catASINrank[0],catASINrank[1],catASINrank[2]
        

        
def getPagesAndScrape(cat,URL):
    htmlCatText = requests.get(URL)
    treeCat =  html.fromstring(htmlCatText.text)
    
    xpath_nextpages = '//ol[@class="zg_pagination"]/li/a/@href'
    nextpages = treeCat.xpath(xpath_nextpages)
    
    for nextpage in nextpages:
        #print nextpage
        scrape_amazon(cat,nextpage)



    
if __name__ == '__main__':

	urlmain = 'http://www.amazon.de/gp/bestsellers/ce-de'
	catURLs = []
	catURLs.append(('Elektronik',urlmain))
	htmltextmain = requests.get(urlmain)
	treemain = html.fromstring(htmltextmain.text)

	xpath_subCats = '//div[@id="zg_left_col2"]/ul[@id="zg_browseRoot"]/ul/ul/li/a/text()'
	subcats = treemain.xpath(xpath_subCats)
	#print len(subcats)
	
	#for subcat in subcats:
	#    print subcat
	
	xpath_subCatURLs = '//div[@id="zg_left_col2"]/ul[@id="zg_browseRoot"]/ul/ul/li/a/@href'
	subcatURLs = treemain.xpath(xpath_subCatURLs)
	
	#for subcatURL in subcatURLs:
	#    print subcatURL
	
	for i in range(0,len(subcatURLs)):
		catURLs.append((subcats[i],subcatURLs[i]))

	for catURL in catURLs:
		#print catURL
		getPagesAndScrape(catURL[0],catURL[1])
