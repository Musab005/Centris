# Centris.ca
A web scraping project that scrapes rental listings from the Centris.ca website using a web spider that runs on Scrapy. 
Optionally, a Splash script can be executed to retrieve the detailed information about the rental listings. The code that runs both Scrapy and Splash is in the splash_working.txt file.

To run the Scrapy project:

1. Install scrapy
2. Install Anaconda
3. Activate the anaconda virtual environment: `conda activate {virtual env name}`
4. run `scrapy crawl listings -o listings.json`
