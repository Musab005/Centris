# Centris.ca
A web scraping project that scrapes rental listings from the Centris.ca website using a web spider that runs on Scrapy. 
These filters were applied: Location: Montréal (Island). Features: 2 beds, 2 baths. Price: $1750 - $2500. Category: Residential, for rent.
Two spiders are available, `listings.py` and `listings_detailed.py`.
The `listings_detailed.py` spider runs a Splash script on top of scrapy to retrieve additional information about the listings that was
available on the summary webpage of each listing. Splash was used because these web pages had javascript enabled.

## project setup - Scrapy
1. Install Anaconda from `https://www.anaconda.com/` and create a virtual environment.
2. Activate your virtual environment from the command line `conda activate {virtual env name}` or from the Anaconda GUI application.
3. Install these packages: `conda install -c conda-forge scrapy`, `conda install -c conda-forge protego`
4. `git clone` this project to your local machine and open it with your preferred IDE.
5. On your IDE, set up the python interpreter path to the `python.exe` file located in your anaconda virtual environment directory.
6. Run the script directly `scrapy crawl listings` from the terminal or `python gui.app.py` to run the GUI application that can be used to run the script.
7. To get the results as json or csv file, run `scrapy crawl listings -o {file_name}.{json/csv}`.
The GUI application has an option return a .json or .csv file to the chosen path.

## project setup - Splash
1. Follow the steps 1-5 from above
2. Download Docker: https://www.docker.com/products/docker-desktop/
3. Install Splash from the terminal: `docker pull scrapinghub/splash`
4. Start the Splash container from the Docker GUI application.
5. Run the script directly `scrapy crawl listings_detailed` from the terminal or `python gui.app.py` to run the GUI application that can be used to run the script.
6. To get the results as json or csv file, run `scrapy crawl listings_detailed -o {file_name}.{json/csv}`. 
The GUI application has an option return a .json or .csv file to the chosen path.


