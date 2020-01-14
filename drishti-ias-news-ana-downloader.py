import os
import datetime
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path


def fetchingWebpage(url):
    try:
        local_webpage = requests.get(base_url)
        return local_webpage
    except Exception as e:
        print('Cannot fetch the webpage...')
        print(e)


def createDirectories(cwd):
    folder_name = 'drishti-ias-crnt-aff'
    folder_path = Path(cwd + '/' + folder_name)
    if os.path.exists(folder_path) != True:
        print('Creating base directory...')
        os.mkdir(folder_path)
    else:
        print('Directory already exixts...')
        return None


def creatingSoup(webpage):
    local_soup = bs(webpage.text, features='html.parser')
    return local_soup


def fetchingPdf(date, soup):
    pdf_link = soup.select('.btn-group a')
    if len(pdf_link) != 0:
        pdf_link = pdf_link[2]['href']
        return pdf_link
    else:
        print('File ' + date + ' not available...')
        return None


def creatingFile(date, cwd):
    file_name = date + '.pdf'
    file_path = Path(cwd + '/' + 'drishti-ias-crnt-aff' +
                     '/' + file_name)
    if os.path.exists(file_path) != True:
        print('Creating file ' + date + '.pdf...')
        pdf_file = open(file_path, 'wb')
        return pdf_file
    else:
        print('File already exists...')
        return None


def downloadingFile(file, pdf_url):
    pdf_raw = requests.get(pdf_url)
    if pdf_raw.status_code != 200:
        print('Error downloading file...')
    else:
        print('Saving the file...')
        for chunks in pdf_raw.iter_content(100000):
            file.write(chunks)


if __name__ == '__main__':
    print('*****Drishti IAS News Analysis PDF Downloader*****')
    download_option = input(
        'Press T to download Latest PDF \nPress P to download Previous PDFs\n')

    date_today = datetime.date.today()  # Getting present date

    # Fetching Current Working Directory
    base_path = os.path.abspath(os.getcwd())

    day_delta = datetime.timedelta(days=1)  # Days Delta For Reversing the Date
    start_date = end_date = date_today

    if download_option.lower() == 't':
        end_date = start_date + 1*day_delta
    elif download_option.lower() == 'p':
        end_date = start_date + \
            int(input('Enter the number of days: '))*day_delta
    else:
        print('Try again...')

    createDirectories(base_path)  # Creating the base folder

    for i in range((end_date - start_date).days):
        date = start_date - i*day_delta
        date = date.strftime('%d-%m-%Y')  # Correcting the format
        base_url = 'https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis/' + date

        webpage = fetchingWebpage(base_url)

        soup = creatingSoup(webpage)
        pdf_url = fetchingPdf(date, soup)

        if pdf_url != None:
            file = creatingFile(date, base_path)
        else:
            file = None

        if file != None:
            downloadingFile(file, pdf_url)

    print('Scraping Successful...')
