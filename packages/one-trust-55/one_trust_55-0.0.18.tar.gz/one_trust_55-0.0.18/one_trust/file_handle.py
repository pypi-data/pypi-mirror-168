from csv import reader
import os
import csv 
import pandas as pd 

# class to handle read/write operations with the CSV file 
class file_handle:
    def __init__(self,file_name):
        self.file_name=file_name

# Method to append dictionary to csv file
    def append_dict(self,site_info,header_list):
        if isinstance(site_info,dict):
            writer_header = False
            if not os.path.isfile(self.file_name):
                writer_header = True
            with open (self.file_name,mode='a',newline='') as f :
                fieldnames = header_list
                writer = csv.DictWriter( f,fieldnames=fieldnames)
                if writer_header == True:
                    writer.writeheader()  
                writer.writerow(site_info)    
        else:
            for site_dict in site_info:
                self.append_dict(site_dict,header_list)
# Method to read by column from csv file (ignores the first row ==headers)
    def read_by_col(self,col_num) :
        result_list=[]
        with open (self.file_name,mode='r',newline='') as f :
            fhandle=reader(f)
            fhandle=list(fhandle)
            fhandle = fhandle[1:]
            try:
                for col in fhandle:
                    result_list.append(col[col_num-1])
            except IndexError as error :
                print (f'The column(s) selected in the method argument is incorrect or Unused rows/empty cells are found in the CSV file {error}')  
                exit()             
            return result_list

# Method to read by headers from csv file (first row == headers)
    def get_file_headers(self):
        header_list = []
        with open (self.file_name,mode='r',newline='') as f :
            fhandle=reader(f)
            fhandle=list(fhandle)
            fhandle = fhandle[0]
            for row in fhandle:
                header_list.append(row)
            return header_list


# Method to write new column to csv file (used for log -- pandas used)
    def write_to_column(self, header_name, write_list,header_list):
        data_dict= {}
        key_list =[] 
        for index, header in enumerate (header_list):
            data_dict[header] = self.read_by_col(index+1)
        for key in write_list:
            key_list.append(key)
        data_dict[header_name] = key_list
        try:
            data_frame = pd.DataFrame(data_dict)
            data_frame.to_csv(self.file_name, mode='w',index=False)
        except ValueError as error :
            print (f'nothing to log {error} ') 
            exit()
 
# print (f' This module is {__name__}')