from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import pandas as pd
import sys
#import importlib
#importlib.reload(sys)

#sys.setdefaultencoding('utf-8')

auth = Oauth1Authenticator(
    consumer_key= "TLjrYMWfFfrXVP2CuVdy9A",
    consumer_secret= "IMZ_nmrMUWbK-HpwiNZ9WrUkKVo",
    token= "u9Zl5Li6RdPq7nzDNZNpesCFGff4BZ6M",
    token_secret= "zZnqzXGrw5R8GvWfTPodtkZThBA"
)

def changeencode(data, cols):
    for col in cols:
        data[col] = data[col].str.decode('utf-8').str.encode('utf-8')
    return data 

client = Client(auth)

lead_records = []


# scraping params 

industries_csv = pd.read_csv('yelp_industries.csv', encoding='utf-8')
brown_cities_csv = pd.read_csv('yelp_brown_cities.csv', encoding='utf-8')
yellow_cities_csv = pd.read_csv('yelp_yellow_cities.csv', encoding='utf-8')
industries = industries_csv['industry'].tolist()
brown_cities = brown_cities_csv['city'].tolist()
yellow_cities = yellow_cities_csv['city'].tolist()


for industry in industries:
    
    print(industry)

    for city in yellow_cities:
        
        print(city)

        for i in range(0,30):

            params = {'term': industry, 'lang': 'de', 'sort' : 0, 'offset':i*20}

            response = client.search(city, **params)
    
            print(len(lead_records))
    
            for bus in response.businesses:
        
                lead = "None"
                neighborhood = "None"
                city = "None"
                postal_code = "None"
                address = "None"
                url = "None"
                phone = "None"
        
                if bus.name is not None:
                    lead = str(bus.name).encode('UTF-8', errors='replace')
            
                if bus.phone is not None:
                    phone = str(bus.phone).encode('utf-8', errors='replace')
            
                if bus.url is not None:
                    url = str(bus.url).encode('utf-8', errors='replace')
            
                if bus.location.postal_code is not None:
                    postal_code = str(bus.location.postal_code).encode('utf-8', errors='replace')
            
                if bus.location.address is not None:
                    iaddress = ""
            
                for i in range(0, len(bus.location.address)):
                    iaddress += str(bus.location.address[0])+", "
                    address = str(iaddress).encode('utf-8', errors='replace')
            
                if bus.location.city is not None:
                    city = str(bus.location.city).encode('utf-8', errors='replace')
        
        
                if bus.location.neighborhoods is not None:
                    if bus.location.neighborhoods[0] is not None:
                        neighborhood = str(bus.location.neighborhoods[0]).encode('utf-8', errors='replace')
       
                lead_records.append((lead, url, neighborhood, address, postal_code, city, phone))
        
        

set_final_leads = list(set(lead_records))

excel_df = pd.DataFrame(set_final_leads, columns=['lead', 'yelp_webaddress', 'neighborhood', 'address', 'postal_code', 'city', 'phone_no'])

excel_df.to_excel('yellow_cities_leads.xlsx', encoding='utf-8')
