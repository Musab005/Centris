# Centris.ca (todo)
A web scraping project that scrapes rental listings from the Centris.ca website using a web spider that runs on Scrapy. These filters were applied: Montreal, QC, sort by most recent, 2 beds, 2 baths, $1.5k-$2.5k and specific neighbourhood filters...(todo)

## project setup - Scrapy (done)
1. Install Anaconda from `https://www.anaconda.com/download/success` and create a virtual environment.
2. Activate your virtual environment from the command line `conda activate {virtual env name}` or through the GUI application.
3. Install these packages: `conda install -c conda-forge scrapy`, `conda install -c conda-forge protego`
4. `git clone` this project to your local machine and open it with your preferred IDE.
5. On your IDE, set up the python interpreter path to the `python.exe` file located in your anaconda virtual environment directory.
7. Run the script directly `scrapy crawl listings` from the terminal or `python gui.app.py` to run the GUI application that can be used to run the script.
8. To get the results as json or csv file, run `scrapy crawl listings -o {file_name}.{json/csv}`. The GUI application will always return a .json or .csv file to the chosen path.

## project setup - Splash (todo)
Optionally, a Splash script can be executed to retrieve the detailed information that is stored on a webpage that runs javascript. 

The code that runs the Scrapy + Splash script is pasted in the `splash_working.txt` file. To use that script, simply copy and paste it into the `listings.py` file. (Need to install Splash and Docker to be able to run a Splash script).

A deaktop app GUI is available to facilitate running the script. Simply run `python gui.app.py` from the parent directory.

To run the the spider `listings.py` from the terminal:

