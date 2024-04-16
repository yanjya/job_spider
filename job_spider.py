from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os
import warnings
import logging
warnings.filterwarnings('ignore')


class JobSpider:
    def __init__(self, key_word):
        """
        Initialize the JobSpider class.

        Parameters:
        - key_word (str): The keyword used for job search.
        """
        self.key_word = key_word
        self.data = pd.DataFrame(columns=['job_name','company_name','job_industry','job_link','job_description','toolkit','good_to_have','salary'])

    def get_job_data(self)-> pd.DataFrame:
        """
        Get job data from the 104 website.

        Returns:
        - data (DataFrame): The job data in a pandas DataFrame.
        """
        #let user to get into the 104 web
        data_len_check = 1
        start_page = 1
        total_page = 100

        #get job data
        for page in range(start_page,total_page):
            page_number = page
            url = f'https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword={self.key_word}&mode=s&page={page_number}'
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
                    
                    print('index: ',len(self.data))
                    print('job: ',company_name,job_name)
                    print('job link: ',job_link)
                    #insert data into dataframe
                    self.data.loc[len(self.data)] = [job_name, company_name, job_industry,job_link, None, None, None, None]

            # Handle exceptions and log errors
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                continue  # Use continue instead of pass to skip to the next iteration
            
            time.sleep(1)
            current_data_len = len(self.data)
            if current_data_len == data_len_check:
                logging.info('No new data')
                break
            else:
                data_len_check = current_data_len
            logging.info('Changing to next page')
        return self.data

    def get_job_details(self)-> pd.DataFrame:
        """
        Get job details for each job in the data.

        Returns:
        - data (DataFrame): The job data with job details added.
        """
        for i in range(0,len(self.data)): 

            url = self.data['job_link'][i]
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            job_content = soup.find(name = 'p', class_="mb-5 r3 job-description__content text-break").text
            toolkit_elements = soup.find_all(name= 'u', attrs = {'data-v-7850ec4d': True})        
            toolkit = str([i.text for i in toolkit_elements]).strip('[]')     
            good_to_have = soup.find_all('p', class_ ='m-0 r3 w-100')
            salary_elements = soup.find_all('div', class_='row')


            try:
                print(job_content)
                print('-'*20)
                print(toolkit)
                print('-'*20)
                print(good_to_have[0].text)
                print('-'*20)
                print(salary_elements[4].text)
                
                self.data.loc[i, 'job_description'] = job_content
                self.data.loc[i, 'toolkit'] = toolkit
                self.data.loc[i, 'good_to_have'] = good_to_have[0].text
                self.data.loc[i, 'salary'] = salary_elements[4].text
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                continue
            
        return self.data


    def save_to_csv(self, filename)-> None:
        """
        Save the job data to a CSV file.

        Parameters:
        - filename (str): The name of the CSV file to save the data to.
        """
        self.data.to_csv(filename)