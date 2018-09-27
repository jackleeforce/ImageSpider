# -*- coding: utf-8 -*-
import json
from multiprocessing.pool import Pool

from selenium import webdriver

from func import *


def get_google_image_links(main_keyword, second_keyword, link_files_dir):
    link_file = link_files_dir + second_keyword

    if not os.path.exists(link_files_dir):
        os.makedirs(link_files_dir, exist_ok=True)

    image_urls = set()

    driver = webdriver.Chrome()

    keyword = main_keyword + ' ' + second_keyword

    url = url = "https://www.google.com/search?q=" + keyword + "&source=lnms&tbm=isch"
    driver.get(url)

    for i in range(20):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(1)

        try:
            driver.find_element_by_xpath('//*[@id=“smb”]').click()
        except Exception as e:
            print("%s already get list all image" % (second_keyword))
            break;

    imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')

    for image in imges:
        image_url = json.loads(image.get_attribute('innerHTML'))["ou"]
        image_urls.add(image_url)

    driver.quit()

    print("%s %s got %d image links" % (main_keyword, second_keyword, len(image_urls)))

    with open(link_file, 'w') as wf:
        for url in image_urls:
            wf.write(url + '\n')

    print('Store all the links in file {0}'.format(link_file))


if __name__ == "__main__":
    main_keyword = '游泳'

    second_keywords = ['蝶泳', '自由泳', '仰泳', '蛙泳']
    # second_keywords = ['butterfly']

    download_dir = './image/google/' + main_keyword + '/'

    link_files_dir = './linkfile/google/' + main_keyword + '/'

    log_dir = './logs/'

    if not os.path.exists(link_files_dir):
        os.makedirs(link_files_dir, exist_ok=True)

    if not os.path.exists(download_dir):
        os.makedirs(download_dir, exist_ok=True)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    init_ssl()

    p = Pool()
    for i in range(len(second_keywords)):
        p.apply_async(get_google_image_links,
                      args=(main_keyword, second_keywords[i], link_files_dir))
    p.close()
    p.join()

    p = Pool()
    for keyword in second_keywords:
        p.apply_async(download_images, args=(link_files_dir + keyword, download_dir + keyword, log_dir))

    p.close()
    p.join()

    print('Finish downloading all images')
