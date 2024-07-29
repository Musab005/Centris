# Centris.ca
A web scraping project that scrapes rental listings from the Centris.ca website using a web spider that runs on Scrapy. Filters were applied (Montreal, QC, sort by most recent, 2 beds, 2 baths, $1.5k-$2.5k and neighbourhood filters).
Optionally, a Splash script can be executed to retrieve the detailed information that is stored on a webpage that runs javascript. 

The code that runs the Scrapy + Splash script is pasted in the `splash_working.txt` file. To use that script, simply copy and paste it into the `listings.py` file. (Need to install Splash and Docker to be able to run a Splash script).

A deaktop app GUI is available to facilitate running the script. Simply run `python gui.app.py` from the parent directory.

To run the the spider `listings.py` from the terminal:

1. Install scrapy
2. Install Anaconda
3. Activate the anaconda virtual environment: `conda activate {virtual env name}`
4. run `scrapy crawl listings -o listings.json`
