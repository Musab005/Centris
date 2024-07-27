# Centris.ca
A web scraping project that scrapes rental listings from the Centris.ca website using a web spider that runs on Scrapy. Filters were applied (sort by most recent, 2 beds, 2 baths, price and location filters).
Optionally, a Splash script can be executed to retrieve the detailed information about the rental listings. The code that runs the Scrapy + Splash script is pasted the splash_working.txt file. The current script only runs on Scrapy.

A deaktop app GUI is available to facilitate running the script. Simply run `python gui.app.py` from the parent directory.

To run the Scrapy script from the terminal:

1. Install scrapy
2. Install Anaconda
3. Activate the anaconda virtual environment: `conda activate {virtual env name}`
4. run `scrapy crawl listings -o listings.json`
