from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os
import warnings
warnings.filterwarnings('ignore')

key_word = '商業分析'

#get job data and store in csv
def get_job_data(key_word:str)-> pd.DataFrame:
    #let user to get into the 104 web
    data_len_check = 1
    start_page = 1
    total_page = 100

    #create dataframe
    data  = pd.DataFrame(columns=['job_name','company_name','job_industry','job_link','job_description','toolkit','good_to_have'])

    #get job data
    for page in range(start_page,total_page):
        page_number = page
        url = f'https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword={key_word}&mode=s&page={page_number}'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Find all the elements
        elements = soup.find_all(name = 'article', class_="b-block--top-bord job-list-item b-clearfix js-job-item")
        job_link_elements = soup.find_all(name='a', class_='js-job-link')
        try:
            for element in elements:
                
                #get job name / company name
                job_name = element['data-job-name']
                company_name = element['data-cust-name']
                job_industry = element['data-indcat-desc']

                #get job link
                job_link = [link for link in job_link_elements if link.text == job_name]
                job_link = 'https:' +job_link[0]['href']
                
                print('index: ',len(data))
                print('job: ',company_name,job_name)
                print('job link: ',job_link)
                #insert data into dataframe
                data.loc[len(data)] = [job_name, company_name, job_industry,job_link, None, None, None]

        #print error log
        except Exception as e:
            print(e)
            pass
        
        time.sleep(1)
        current_data_len = len(data)
        if current_data_len == data_len_check:
            print('no new data')
            break
        else:
            data_len_check = current_data_len
        print('changing to next page')
        
    return data

def get_job_details(data:pd.DataFrame)-> pd.DataFrame:
    for i in range(0,len(data)): 

        url = data['job_link'][i]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        job_content = soup.find(name = 'p', class_="mb-5 r3 job-description__content text-break").text
        toolkit_elements = soup.find_all(name= 'u', attrs = {'data-v-7850ec4d': True})        
        toolkit = str([i.text for i in toolkit_elements]).strip('[]')     
        good_to_have = soup.find_all('p', class_ ='m-0 r3 w-100')

        try:
            print(job_content)
            print('-'*20)
            print(toolkit)
            print('-'*20)
            print(good_to_have[0].text)
            
            data['job_description'][i] = job_content
            data['toolkit'][i] = toolkit
            data['good_to_have'][i] = good_to_have[0].text
        except Exception as e:
            print(e)
            pass
        
    return data
    
data = get_job_data(key_word)
data = get_job_details(data)
data.to_csv('aaa.csv')