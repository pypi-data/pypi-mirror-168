#!/usr/bin/python
from  .file_handle import *  
from .ot_class import *  


class OT_client : 
    def __init__(self,key,base_url):
        self.key= key
        self.base_url = base_url
        self.ot_instance = ot(self.key,self.base_url)

    # Method 1 : Adding domains for scan in the One Trust interface from a CSV file:
    def scan_sites(self,col_num_site,col_num_org,number_of_pages):
        self.ot_instance.get_scan_sites(col_num_site = col_num_site, col_num_org = col_num_org, number_of_pages = number_of_pages)

    # Method 2 : Retrieving API-keys for scanned domains and writing to a  CSV file :
    def retrieve_api(self,col_num,script_type,write_to_file):
        self.ot_instance.get_api_key_retrieve(col_num = col_num,script_type = script_type ,write_to_file = write_to_file)
        
    # Method 3: Fetching information or attributes of scanned domains and writing to a CSV file :
    def site_attributes(self,extract_attr,write_to_file,search_domain_list):
        self.ot_instance.get_site_attributes(extract_attr = extract_attr ,write_to_file= write_to_file,search_domain_list = search_domain_list)
    # Method 4 : Publishing a script from a CSV file :

    def publish_ot_script(self,col_num,script_type):
        self.ot_instance(col_num = col_num ,script_type = script_type) 
 
