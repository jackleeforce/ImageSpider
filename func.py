import os
import ssl
import time
import urllib.request
import urllib.error
from urllib.parse import urlparse

from user_agent import generate_user_agent


def init_ssl():
    ssl._create_default_https_context = ssl._create_unverified_context


def download_images(link_file_path, download_dir, log_dir):
    print('Start downloading with link file:%s' % (link_file_path))

    second_keyword = link_file_path.split('/')[-1]

    count = 0
    headers = {}
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with open(link_file_path, 'r') as rf:
        for link in rf:
            try:
                o = urlparse(link)
                ref = o.scheme + '://' + o.hostname
                ua = generate_user_agent()
                headers['User-Agent'] = ua
                headers['referer'] = ref

                req = urllib.request.Request(link.strip(), headers=headers)
                response = urllib.request.urlopen(req)

                data = response.read()
                file_path = download_dir + "/" + '{0}.jpg'.format(count)
                with open(file_path, 'wb') as wf:
                    wf.write(data)

                count += 1
                if count % 10 == 0:
                    print('Process-{0} is sleeping'.format(second_keyword))
                    time.sleep(5)

            except urllib.error.URLError as e:
                print('URLError:'+link)
                print(repr(e))

                continue
            except urllib.error.HTTPError as e:
                print('HTTPError:'+link)
                print(repr(e))

                continue
            except Exception as e:
                print('Unexpected Error:'+link)
                print(repr(e))


                continue
