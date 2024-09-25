import requests
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import traceback

class JobSpider:
    def __init__(self):
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                'Referer': 'https://www.104.com.tw/'}
        self.area_code_url = 'https://static.104.com.tw/category-tool/json/Area.json'
        self.industry_code_url = 'https://static.104.com.tw/category-tool/json/Indust.json'

    #get all job data from 104 website
    def get_all_job_data(self)-> None:

        print('Start to get job data')
        area_code = self.get_area_code()
        industry = self.get_industry_code()
        job_info = self.get_job_info(area_code, industry)
        job_info.to_csv('job_info.csv', index=False)
        print('job_info.csv has been saved')
    

    #get area code
    def get_area_code(self) -> pd.DataFrame:

        area_code = pd.DataFrame(requests.get(self.area_code_url).json()[0]['n'])
        area_code = area_code.explode('n')
        area_code['des2'] = area_code['n'].apply(lambda x: x['des'])
        area_code['no2'] = area_code['n'].apply(lambda x: x['no'])
        area_code = area_code[['des', 'no', 'des2', 'no2']]
        # area_code.to_csv('area_code.csv', index=False)

        return area_code

    
    # get industry code
    def get_industry_code(self) -> pd.DataFrame:

        industry = pd.DataFrame(requests.get(self.industry_code_url).json())
        industry = industry.explode('n')
        industry['des2'] = industry['n'].apply(lambda x: x['des'])
        industry['no2'] = industry['n'].apply(lambda x: x['no'])
        industry['n2'] = industry['n'].apply(lambda x: x['n'])
        industry = industry.explode('n2')
        industry['des3'] = industry['n2'].apply(lambda x: x['des'])
        industry['no3'] = industry['n2'].apply(lambda x: x['no'])
        industry = industry[['des', 'no', 'des2', 'no2', 'des3', 'no3']]
        # industry.to_csv('industry.csv', index=False)
        return industry

    #get job information
    def get_job_info(self, area_code, industry) -> pd.DataFrame:


        df = []
        for area in area_code['no2'].unique():
            for indcat in industry['no2'].unique():
                page = 1
                while page <= 100:
                    try:
                        url = f'https://www.104.com.tw/jobs/search/list?ro=1&indcat={indcat}&area={area}&order=11&asc=0&page={page}&mode=l'
                        response = requests.get(url, headers=self.headers)
                        ndf = pd.DataFrame(response.json()['data']['list'])
                        print(ndf)
                        df.append(ndf)
                        if ndf.shape[0] < 30:
                            break
                        page = page + 1
                    except KeyboardInterrupt:
                        print('Interrupted by "cntrl+c" ')
                        break
                    except Exception as e:
                        print('Exception occurred: ', e)
                        traceback.print_exc()
                        print('==================== Error and retry ====================')

        df = pd.concat(df, ignore_index=True)
        return df