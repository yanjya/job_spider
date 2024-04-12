import job_spider

key_word = '商業分析'
spider = job_spider.JobSpider(key_word)
spider.get_job_data()
spider.get_job_details()
spider.save_to_csv('aaa.csv')
