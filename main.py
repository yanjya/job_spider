import job_spider

key_word = '商業分析'
spider = job_spider.JobSpider(key_word)
spider.get_job_data()
data = spider.get_job_details()
data.drop(columns = ['job_link'], inplace = True)
data.to_csv('job_data.csv', index = False)