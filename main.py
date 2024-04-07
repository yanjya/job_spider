from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os

key_word = '商業分析'

#get job data and store in csv
def get_job_data(key_word:str)-> None:
    #let user to get into the 104 web
    data_len_check = 1
    start_page = 1
    total_page = 100

    #check weather "job data csv" exits
    if os.path.exists('job_data.csv'):
        data = pd.read_csv('job_data.csv')
        print('job data csv exist')
    else:
       data  = pd.DataFrame(columns=['job_name','company_name','job_link','job_demand','toolkit'])

    #find num of total pages
    def get_url_soup(key_word: str, page_number:int = 1)-> BeautifulSoup:
        url = f'https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword={key_word}&mode=s&page={page_number}'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')   
         
        return soup

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
                data.loc[len(data)] = [job_name, company_name, job_link, None, None]

        #print error log
        except Exception as e:
            print(e)
            print(f'page {page_number} error')
            pass
        
        time.sleep(1)
        current_data_len = len(data)
        if current_data_len == data_len_check:
            print('no new data')
            break
        else:
            data_len_check = current_data_len
        print('changing to next page')
    
    #save data to csv    
    data.to_csv(f'104_{key_word}_job_data.csv',index=False)


    
get_job_data(key_word)