import sys
import random
import time
import redis
import datetime

r = redis.Redis(host="localhost", port=6379)

s_test_name = 'test'
# s_tracker_name = 'tracker'
s_tracker_name = 'ST:TRACKER::::'
s_articles_name = 's-articles'
s_enrich_name = 's-enrich'
ps_metrics_page = 'pb-page-metrics'

# xadd "tracker" "*" "url" "https://www.rtl.lu/meenung/carte-blanche/a/1874304.html" "uui" "ipdigl0jjm5kwusf5zyg8x6n" "ua" "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1" "lang" "fr-fr" "dt" "2022-03-09T12:35:01.977Z"
# xadd "tracker" "*" "url" "https://www.rtl.lu/news/international/a/1877030.html" "uui" "ipdigl0ja4pko3l94bm3atkz" "ua" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" "lang" "en-US,en;q=0.9" "dt" "2022-03-09T12:35:02.072Z"
# xadd "tracker" "*" "url" "https://www.rtl.lu/mobiliteit/news/a/1877195.html" "uui" "ipdigkwnlnbcwsw0qx1622" "ua" "Mozilla/5.0 (Linux; Android 11; M2007J20CG Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/356.0.0.28.112;]" "lang" "en-GB,en;q=0.9,fr-LU;q=0.8,fr;q=0.7,de-DE;q=0.6,de;q=0.5,en-US;q=0.4" "dt" "2022-03-09T12:35:02.355Z"
# xadd "tracker" "*" "url" "https://5minutes.rtl.lu/actu/monde/a/1877034.html?didomiConfig.notice.enable=false" "uui" "ipdigkwklyvx9gp53bo5n2o" "ua" "Mozilla/5.0 (Linux; Android 12; SM-A528B Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36" "lang" "it-IT,it;q=0.9,fr-FR;q=0.8,fr;q=0.7,de-DE;q=0.6,de;q=0.5,en-GB;q=0.4,en-US;q=0.3,en;q=0.2" "dt" "2022-03-09T12:35:01.880Z"
# xadd "tracker" "*" "url" "https://www.rtl.lu/sport/auto-moto-sport/a/1877315.html" "uui" "ipdigkuzvet7lowu3fgz2de" "ua" "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1" "lang" "de-DE,de;q=0.9" "dt" "2022-03-09T12:35:02.505Z"
# xadd "tracker" "*" "url" "https://www.rtl.lu/news/international/a/1877198.html" "uui" "ipdigl08he4ecn19s1nsebbt" "ua" "Mozilla/5.0 (Linux; Android 11; SM-A705FN Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.58 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/356.0.0.28.112;]" "lang" "en-GB,en-US;q=0.9,en;q=0.8" "dt" "2022-03-09T12:35:01.978Z"
# xadd "tracker" "*" "url" "https://www.rtl.lu/news/national/a/1876697.html" "uui" "ipdigkv195auv4zc50x7imjo" "ua" "Mozilla/5.0 (SMART-TV; Linux; Tizen 5.5) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.0 Chrome/69.0.3497.106 TV Safari/537.36" "lang" "fr-FR" "dt" "2022-03-09T12:35:03.893Z"
# xadd "tracker" "*" "url" "https://www.rtl.lu/news/national/a/1876686.html?didomiConfig.notice.enable=false" "uui" "null" "ua" "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148" "lang" "de-DE,de;q=0.9" "dt" "2022-03-09T14:32:55.741Z"
# xadd "tracker" "*" "url" "https://www.rtl.lu/news/national/a/1876686.html" "uui" "null" "ua" "Mozilla/5.0 (Linux; Android 11; SM-A705FN Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.58 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/356.0.0.28.112;]" "lang" "de-DE,de;q=0.9" "dt" "2022-03-09T14:31:55.741Z"


urls = [
    'https://www.rtl.lu/meenung/carte-blanche/a/1874304.html',
    'https://www.rtl.lu/news/international/a/1877030.html',
    'https://www.rtl.lu/mobiliteit/news/a/1877195.html',
    'https://5minutes.rtl.lu/actu/monde/a/1877034.html',
    'https://www.rtl.lu/news/international/a/1877198.html',
    # 'https://today.rtl.lu/news/luxembourg/a/1963501.html',
    # 'https://www.eldo.lu/aktuell/news/a/119006.html'
]

uuis = [
    'ipdigl0jjm5kwusf5zyg8x6n',
    'ipdigkwnlnbcwsw0qx1622',
    'ipdigkuzvet7lowu3fgz2de',
    'ipdigkv195auv4zc50x7imjo'
]


def create_record():
    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = round(datetime.datetime.now().timestamp() * 1000)
    return {
        'url': 'https://www.rtl.lu/news/international/a/1877030.html',
        'uui': 'ipdigl0jjm5kwusf5zyg8x6n',
        'dt': now,
        'metadata': {
            'schema_version': 1,
            'schema_name': 'TRACKER',
            'object_name': 'TRACKER'
        }
    }


def create_random_record():
    url = random.choice(urls)
    uui = random.choice(uuis)
    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = round(datetime.datetime.now().timestamp() * 1000)

    return {
        'url': url,
        'uui': uui,
        'dt': now
    }


def main():
    while True:
        record = create_random_record()
        # record = create_record()
        interval = random.randint(0, 2)
        # r.xadd(s_test_name, record)
        r.xadd(s_tracker_name, record)
        dt = record['dt']
        print(f'{interval} => XADD {s_tracker_name} {record} ({type(dt)})')
        time.sleep(interval)
        # time.sleep(1)


if __name__ == '__main__':
    sys.exit(main())