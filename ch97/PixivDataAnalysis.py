import json
import pytz
import requests
import time
import re
import datetime
import pandas as pd
from tqdm import tqdm
import os
import concurrent.futures
import statistics
import argparse
from bs4 import BeautifulSoup



class PixivDataAnalysis():

    def __init__(
                    self,
                    *, 
                    uid : str, 
                    cookie : str,
                    output_path : str, 
                    proxies = None,
                    sleep_time,
                    quick_mode = False,
                ):
        self.quick_mode = quick_mode
        self.sleep_time = sleep_time
        self.start_time = time.time()
        self.uid = uid
        self.session = requests.Session()
        self.path = output_path
        self.headers = {
            "referer": "https://www.pixiv.net/ranking.php",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
            'cookie' : cookie
        }
        
        self.proxies = proxies
        self.data = {}
        if not self.path.endswith('/') and not self.path.endswith('\\'):
            self.path += '/'

        text = self.session.get(f'https://www.pixiv.net/users/{self.uid}', headers=self.headers, proxies=self.proxies).text
        self.name = re.findall('meta property="og:title" content="(.*?)"', text)[0]

        print(f'Uid:{self.uid}, Name:{self.name}')

    def get_pages(self) -> list:
        illustration_url = f'https://www.pixiv.net/ajax/user/{self.uid}/profile/all'
        response = self.session.get(illustration_url, headers=self.headers, proxies=self.proxies)
        response.raise_for_status()
        img_urls = list(response.json()['body']['illusts'].keys())
        return img_urls
    def read_data_from_url(self, url_id : str, index : int, pbar : tqdm) -> dict:
        response = self.session.get(f'https://www.pixiv.net/artworks/{url_id}', headers=self.headers, proxies=self.proxies)
        pbar.set_description(f'Pid {url_id}')
        text = response.text
        view = re.findall('"viewCount":(.*?),', text)[0]
        bookmarkCount = re.findall('"bookmarkCount":(.*?),"', text)[0]
        r18 = re.findall('"tag":"(.*?)","locked"', text)[0] if len(re.findall('"tag":"(.*?)","locked"', text)) > 0 else ''
        soup = BeautifulSoup(response.text, "html.parser")
        total = len(self.session.get(f'https://www.pixiv.net/ajax/illust/{url_id}/pages', headers=self.headers, proxies=self.proxies).json()['body'])
        content = soup.find("meta", {"id": "meta-preload-data"})["content"]
        json_data = json.loads(content)
        unformatted_time = json_data['illust'][url_id]['createDate']
        delta_time = self.get_utc_timestamp() - self.convert_to_utc_timestamp(unformatted_time)
        self.data[index] = [
            url_id,
            delta_time,
            view,
            bookmarkCount,
            int(view) / delta_time * 3600 * 24,
            float(bookmarkCount) / float(view) * 100,
            r18 == 'R-18',
            total
        ]
    def get_utc_timestamp(self):
        utc_time = datetime.datetime.utcnow()
        utc_timestamp = int(utc_time.timestamp())
        return utc_timestamp
    def convert_to_utc_timestamp(self,time_str):
        time_obj = datetime.datetime.fromisoformat(time_str)
        tz_offset = time_obj.utcoffset()
        time_zone = pytz.FixedOffset(tz_offset.seconds // 60)
        utc_time = time_zone.normalize(time_obj.astimezone(pytz.utc))
        return int(utc_time.timestamp())
    def read_data_from_urls(self, urls : list, threshold : int):
        try:
            if self.quick_mode or len(urls) <= threshold:
                with tqdm(total=len(urls), leave=False) as pbar, \
                    concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
                    futures = []
                    for index, img_id in enumerate(urls):
                        futures.append(executor.submit(self.read_data_from_url, img_id, index, pbar))
                    for future in concurrent.futures.as_completed(futures):
                        pbar.update(1)
                        future.result()
            else:
                with tqdm(enumerate(urls), total=len(urls), leave=False) as pbar:
                    for index, url in pbar:
                        time.sleep(self.sleep_time)
                        self.read_data_from_url(url, index, pbar)
        finally:
            return self.data
    
    def save_data(self, data : dict, log):
        a_data=pd.DataFrame(columns=('pid', 'delta_time', 'view', 'like', 'view/day', 'like/view', 'isR18', 'num_of_pages'))
        for i, (_, value) in enumerate(data.items()):
            a_data.loc[i + 1] = value
        t = time.localtime(time.time())
        rsu = '{}-{}-{}_{}-{}-{}'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        name = '{}-{}'.format(self.name, rsu)
        name = self.replace_invalid_chars(name)
        a_data.to_excel(f"{self.path}{name}.xlsx")
        file = open(f'{self.path}{name}.txt', 'w', encoding='utf-8')
        file.write(log)
        output = os.path.join(self.path, name)
        print(f'已保存至 "{output}.xlsx"')
    def show_data(self, data: dict):
        num_of_pages_list = [int(value[7]) for value in data.values()]
        view_list = [int(value[2]) for value in data.values()]
        bookmark_list = [int(value[3]) for value in data.values()]
        R18_num = sum(1 for value in data.values() if value[6])
        delta_time_list = [value[1] for value in data.values()]
        delta_time_list = sorted(delta_time_list)
        last_time = max(delta_time_list) + time.time() - self.get_utc_timestamp()
        first_time = min(delta_time_list)+ time.time() - self.get_utc_timestamp()
        delta_time_list = [delta_time_list[i+1] - delta_time_list[i] for i in range(len(delta_time_list)-1)]
        avg_delta_time = sum(delta_time_list) / len(delta_time_list)
        max_view_pid = max(data.items(), key=lambda x: int(x[1][2]))[1][0]
        max_bookmark_pid = max(data.items(), key=lambda x: int(x[1][3]))[1][0]
        min_view_pid = min(data.items(), key=lambda x: int(x[1][2]))[1][0]
        min_bookmark_pid = min(data.items(), key=lambda x: int(x[1][3]))[1][0]
        total_page, total_view, total_bookmark, total_num_of_pages = len(data), sum(view_list), sum(bookmark_list), sum(num_of_pages_list)
        bookmark_dev_view_list = [float(bookmark_list[i]) / view_list[i] for i in range(len(bookmark_list))]
        if R18_num > 0:
            log = f'总投稿数:{total_page}\tR18投稿数:{R18_num}\t总阅读:{total_view}\t总收藏:{total_bookmark}\t总图片数:{total_num_of_pages}\t'
            log += f'R18投稿占比:{float(R18_num) / total_page * 100:.3f}%\n'
        else:
            log = f'总投稿数:{total_page}\t总阅读:{total_view}\t总收藏:{total_bookmark}\t总图片数:{total_num_of_pages}\n'
        log += f'平均阅读:{float(total_view) / total_page:.3f}\n平均收藏:{float(total_bookmark) / total_page:.3f}\n平均图片数:{float(total_num_of_pages) / total_page:.3f}\n'
        log += f'收藏/阅读(整体):{float(total_bookmark) / total_view * 100:.3f}%\n收藏/阅读(平权):{float(sum(bookmark_dev_view_list)) / total_page * 100:.3f}%\n'
        log += f'最高阅读:{max(view_list)}\tpid:{max_view_pid}\t最低阅读:{min(view_list)}\tpid:{min_view_pid}\n'
        log += f'最高收藏:{max(bookmark_list)}\tpid:{max_bookmark_pid}\t最低收藏:{min(bookmark_list)}\tpid:{min_bookmark_pid}\n'
        log += f'阅读量(每投稿)\tmean:{statistics.mean(view_list):.3f}\tmed:{statistics.median(view_list):.3f}\tstd:{statistics.stdev(view_list):.3f}\n'
        log += f'收藏量(每投稿)\tmean:{statistics.mean(bookmark_list):.3f}\tmed:{statistics.median(bookmark_list):.3f}\tstd:{statistics.stdev(bookmark_list):.3f}\n'
        log += f'平均投稿间隔:{self.timestamp2str(avg_delta_time)}\t中位投稿间隔:{self.timestamp2str(statistics.median(delta_time_list))}\t距离最近投稿:{self.timestamp2str(first_time)}\t距离首次投稿:{self.timestamp2str(last_time)}'
        print(log)
        return log
    def timestamp2str(self, timestamp: float) -> str:
        timestamp = int(timestamp)
        time_units = [(31536000, "年"), (86400, "日"), (3600, "时"), (60, "分"), (1, "秒")]
        output = ""
        for unit, unit_str in time_units:
            if timestamp >= unit:
                num_units = int(timestamp // unit)
                timestamp %= unit
                if num_units >= 1:
                    output += str(num_units) + unit_str
        if output == "":
            output += "0秒"
        return output
    def replace_invalid_chars(self, s: str) -> str:
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        new_s = ''
        for c in s:
            if c in invalid_chars:
                new_s += '_'
            else:
                new_s += c

        return new_s

def main(uid, output_dir, cookie, sleep_time, quick_mode):
    
    os.makedirs(output_dir, exist_ok=True)
    p = PixivDataAnalysis(  
                            uid=uid,
                            cookie=cookie,
                            output_path=output_dir,
                            proxies=PROXIES,
                            sleep_time=sleep_time,
                            quick_mode=quick_mode)

    img_urls = p.get_pages()
    data = p.read_data_from_urls(img_urls, 50)
    log = p.show_data(data)
    p.save_data(data, log)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uid', type=str, required=True)
    parser.add_argument('-c', '--cookie', type=str, default='')
    parser.add_argument('-o', '--output_dir', type=str, default='output/')
    parser.add_argument('-s', '--sleep_time', type=float, default=1.5)
    parser.add_argument('-q', '--quick_mode', default=False, action='store_true')
    args = parser.parse_args()
    PROXIES = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }   
    main(args.uid, args.output_dir, args.cookie, args.sleep_time, args.quick_mode)