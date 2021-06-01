'''
Base url:
https://www.moviestillsdb.com/movies?year=2019
'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import urllib.request
from tqdm import tqdm
import time
from random import randint
import threading

opts = Options()
opts.headless = True
browser = webdriver.Firefox(options=opts)
time.sleep(0.1)

def get_images_from_url(driver, url):
    images = []
    browser.get(url)
    for element in browser.find_elements_by_xpath("//div[@class=\"image\"]/img"):
        images.append(element.get_attribute("style")[23:][:-3])
    return images

def get_movies_from_url(driver, url):
    movies = []
    browser.get(url)
    for element in browser.find_elements_by_xpath("//td[@class=\"title\"]/a"):
        movies.append(element.get_attribute("href"))
    return movies

def random_name():
    return str(randint(1000000,9999999))

def download_image(url, folder, filename):
    path = folder+"/m"+filename+".jpg"
    urllib.request.urlretrieve(url, path)
    #wget.download(url, folder+"/m"+filename+".jpg")

def multi_file_downloader(urls, folder):
    for url in urls:
        download_image(url, folder, random_name())

def threaded_downloader(links, folder):
    pbar = tqdm(total=len(links))
    remaining = links[:]
    THREADS_MAX = 16
    while len(remaining) > 0:
        threads = []
        BATCH_SIZE = 24
        for _ in range(THREADS_MAX):
            batch = remaining[-BATCH_SIZE:]
            remaining = remaining[:-BATCH_SIZE]
            thread = threading.Thread(target=multi_file_downloader, args=(batch, folder))
            thread.start()
            threads.append(thread)
        
        for t in threads: # Wait for all threads, then next batch
            t.join()

        pbar.update(len(remaining))
        #print("Remaining:", len(remaining))
    pbar.close()

try:
    base_url = "https://www.moviestillsdb.com/movies"
    for year in range(2020, 2022):
        for page in range(1, 16):
            print("[-]  Scraping year", year, "on page", page)
            year_url = base_url+"?year="+str(year)+"&page="+str(page)
            movies = get_movies_from_url(browser, year_url)
            images = []

            for url in tqdm(movies):
                images.extend(get_images_from_url(browser, url))
            print("Found", len(images), "images on this page")
            print("Downloading",len(images),"files...")

            try:
                threaded_downloader(images, "./images")
            except Exception as e:
                print("[!!!] ERROR: downloader failed :", e)
finally:
    time.sleep(0.1)
    print("Bye bye!")
    browser.quit()