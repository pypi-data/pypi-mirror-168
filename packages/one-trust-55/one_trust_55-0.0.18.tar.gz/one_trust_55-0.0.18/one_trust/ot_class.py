from itertools import zip_longest
from requests import Session 
import re 
from  .file_handle import *  



FILE_NAME = 'ot_sites - Copy.csv'
file = file_handle(FILE_NAME)
logger = [] 


class ot:
    def __init__(self,token,base_url):   
        self.url= base_url 
        # 'https://app-fr.onetrust.com'

        self.session=Session()
        self.session.headers.update( {
                    "Content-Type": "application/json",
                    "Authorization": 'Bearer' + token
                     })     

        
    # API doc : https://developer.onetrust.com/onetrust/reference/requestbulkadddomainusingpost
    def get_scan_sites(self,col_num_site,col_num_org,number_of_pages):
        site_list = file.read_by_col(col_num_site)[:14]
        org_list = file.read_by_col(col_num_org)[:14]
        url= self.url + '/api/cookiemanager/v2/websites'
        site_org_map= (list((zip_longest(site_list, org_list))))
        for site in site_org_map:
            site_to_scan=(site[0]).split(' ')
            org_to_scan = (site[1])
            payload = {
                'domainsList': site_to_scan,
                "externalOrgId": org_to_scan,
                "includedQueryParams": "string",
                "keepExistingData": True,
                "numberOfPages": number_of_pages,
                "scanRequired": True,
            }
            print(site_to_scan)
            r=self.session.post(url,json=payload)
            if (r.status_code == 200) :
                print ('Success : ', r.status_code)
                responses = r.json()
                for response in responses:
                    print(response['message'])
                    logger.append(response['message'])


            else:
                print (f'Error: {r.status_code} API key has probably expired or BASE_URL is incorrrect. Create a new API key on the OT interface/modify BASE_URL and try again') 
                exit()  
              
        file.write_to_column ('Log',logger,file.get_file_headers())  


    # API doc :  https://developer.onetrust.com/onetrust/reference/publishtositeusingput
    def publish_script(self,col_num,script_type): 
        sites = file.read_by_col(col_num)  
        url= self.url + '/api/cookiemanager/v2/websites/publish'    
        payload={
        "languageDetectionEnabled": True,
        "languageDetectionHtml": True
        
            }
        for site in sites:
            r=self.session.request("PUT", url, json=payload,params={"website":site,"scriptType":script_type})
            if (r.status_code == 200) :
                print ('Success : ', r.status_code)
                logger.append(r.json()['responseMsg'])
                
            else:
                print (f'Error: {r.status_code} API key has probably expired or BASE_URL is incorrrect. Create a new API key on the OT interface/modify BASE_URL and try again')  
                exit()   
        file.write_to_column ('Log',logger,file.get_file_headers())

    # API doc : https://developer.onetrust.com/onetrust/reference/getscriptforwebsiteusingget
    def get_api_key_retrieve(self,col_num,script_type,write_to_file):
        site_list = file.read_by_col(col_num)
        key_list=list ()
        url= self.url + '/api/cookiemanager/v2/websites/scripts'
        for site in site_list:
            query_params={"website":site,"scriptType":script_type}
            r=self.session.get(url,params=query_params)
            if (r.status_code == 200) :
                print ('Success : ', r.status_code)
                data = r.text
                data_line= data.split("\n")
                for line in data_line:
                    results=re.findall('data-domain-script="(.*-{0,5})"',line)
                    for result in results:
                        if (len(result) >0):
                            key_list.append(result)
            else:
                print (f'Error: {r.status_code} API key has probably expired or BASE_URL is incorrrect. Create a new API key on the OT interface/modify BASE_URL and try again') 
                exit() 
        if write_to_file == 'yes': 
            print (f'writing to file:{FILE_NAME}')  
            file.write_to_column('API-Key',key_list,file.get_file_headers())         
            # return key_list
        else:
            print('writing to console ...')
            print (key_list)

    # API doc : https://developer.onetrust.com/onetrust/reference/getdomainsscannedbysortusingget
    def get_site_attributes (self,extract_attr,write_to_file,search_domain_list):
        for domain in search_domain_list: 
            site_list=[]
            attr_dict = {}
            url= self.url + '/api/cookiemanager/v2/websites'
            query_params = {'searchStr': domain}
            r=self.session.get(url,params=query_params)
            if (r.status_code == 200) :
                if not r.json()['content']:
                    print ('No content to be retrieved for {}'.format(domain))
                    continue
                print ('Success : ', r.status_code)
                sites_scanned= r.json()['content']
                for sites in sites_scanned:
                    for attr in extract_attr:
                        try:
                            attr_dict[attr]=sites[attr]
                        except:
                            print ('{} does not exist'.format(attr))    
                            continue
                    site_list.append (attr_dict.copy())
                if write_to_file == 'yes':
                    print (f'writing to file:{FILE_NAME}')    
                    file.append_dict(site_list,extract_attr)
                
                else:
                    print('writing to console ...')
                    print (site_list)
            else:
                print (f'Error: {r.status_code} API key has probably expired or BASE_URL is incorrrect. Create a new API key on the OT interface/modify BASE_URL and try again') 
                exit()   
# print (f' This module is {__name__}')            