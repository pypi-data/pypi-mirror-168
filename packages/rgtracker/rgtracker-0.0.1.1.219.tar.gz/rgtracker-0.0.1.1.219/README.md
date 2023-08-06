## Redis Naming Convention

### Redis Key

TYPE:NAME:DIMENSION:ID:TIMESTAMP:METRIC  
__Example__ :
* JSON -> J::P:001::
* TS   -> TS:5MINUTES:S:001::UD

```python
@unique
class RedisNC(IntEnum):
    TYPE = 0,
    NAME = 1,
    DIMENSION = 2,
    RECORD_ID = 3,
    TS = 4,
    METRIC = 5
```

```python
@unique
class Type(Enum):
    STREAM = 'ST'
    HASH = 'H'
    JSON = 'J'
    INDEX = 'I'
    TIMESERIES = 'TS'
    BLOOM = 'B'
    SORTEDSET = 'SS'
    SET = 'S'
    LIST = 'L'
    CHANNEL = 'C'
    CMS = 'CMS'
    HLL = 'HLL'
```

```python
NAME = "custom_dev_choice"
```

```python
@unique
class Dimension(Enum):
    WEBSITE = 'W'
    SECTION = 'S'
    PAGE = 'P'
    DEVICE = 'D'
    AUDIO = 'A'
    VIDEO = 'V'
    PODCAST = 'PC'
    METRIC = 'M'
```

```python
ID = "unique_key_identifier" # hash
```

```python
TIMESTAMP = "timestamp_key" # int
```

```python
@unique
class Metric(Enum):
    PAGEVIEWS = 'PG'
    DEVICES = 'D'
    UNIQUE_DEVICES = 'UD'
```


### Redis JSON

__Website__ 
```json
{
    "id": "28be7218962bea2626e3dd6c72186b3218221819ae09", (string - hash)
    "name": "RTL", (string - uppercase)
    "last_visited": 17218562426214, (numeric - timestamp)
    "sections": [
        {
            "id": "c218c622181bbe062bd4410d5b625dd21893fd632188", (string - hash)
            "pretty_name": "actu/monde", (string) -TODO-> "name": "actu/monde"
            "last_visited": 1721842180218218, (numeric - timestamp)
        }
    ], (tracker Section object)
    "pages": [
        {
            "id": "f0362c3463d7e27218db1f3218e9a4d218628a5eebd", (string - hash)
            "url": "https://5minutes.rtl.lu/actu/monde/a/218218218.html", (string - url without query params)
            "article_id": 218218218, (numeric)
            "last_visited": 1721842180218218, (numeric - timestamp)
        }
    ] (tracker Page object)
}
```

__Section__ 
```json
{
    "id": "", (string - hash)
    "pretty_name": "", (string)
    "level_0": "", (string) -> "levels": {"level_0": "", "level_n": "n"}
    "level_1": "", (string)
    "level_2": "", (string)
    "level_3": "", (string)
    "level_4": "", (string)
    "last_visited": 1721856272182182, (numeric - timestamp)
    "website": {
        "id": "", (string - hash)
        "name": "", (string)
    },
    "pages": [
        {
            "id": "f0362c3463d7e27218db1f3218e9a4d218628a5eebd", (string - hash)
            "url": "https://5minutes.rtl.lu/actu/monde/a/218218218.html", (string - url without query params)
            "article_id": 218218218, (numeric)
            "last_visited": 1721842180218218, (numeric - timestamp)
        }
    ]
}
```

__Page__ 
```json
{
    "id": "", (string - hash)
    "url": "", (string - url without query params)
    "article_id": "", (numeric)
    "last_visited": 17218626236220, (numeric, timestamp)
    "metadata": {
        "title": "", (string)
        "kicker": "", (string)
        "display_data": 17218626236220
    },
    "website": {
        "id": "",
        "name": ""
    },
    "section": {
        "id": "", (string - hash)
        "pretty_name": "", (string) -TODO-> "name": "" (string)
        "levels": {
            "level_0": "", (string)
            "level_1": "", (string)
            "level_2": "", (string)
            "level_3": "", (string)
            "level_4": "", (string)
        }
    }
}
```



### Redis Index

__Website__ on prefix = J::W: on JSON  
   - id TAG as id,  
   - name TAG as name,  
   - last_visited NUMERIC as last_visited, -TODO-> last_visited NUMERIC as last_visited SORTABLE true,  
   - sections[*].id TAG as section_id,  
   - sections[*].pretty_name TAG as section_pretty_name, -TODO-> sections[*].name TAG as section_name,  
   - pages[*].id TAG as page_id  


__Section__ on prefix = J::S: on JSON  
   - id TAG as id,  
   - pretty_name TAG as pretty_name SEPARATOR '/', -TODO-> name TAG as name SEPARATOR '/',  
   - level_0 TAG as level_0, -TODO-> levels.level_0 TAG as level_0  
   - level_1 TAG as level_1,  
   - level_2 TAG as level_2,  
   - level_3 TAG as level_3,  
   - level_4 TAG as level_4,  
   - last_visited NUMERIC as last_vistited SORTABLE true  
   - website.id TAG as website_id,  
   - website.name TAG as website_name  


__Page__ on prefix = J::P: on JSON  
   - id TAG as id,  
   - url TEXT as url,  
   - metadata.title TEXT as title,  
   - metadata.kicker TEXT as kicker,  
   - last_visited NUMERIC as last_visited,  
   - website.id TAG as website_id,  
   - website.name TAG as website_name,  
   - section.id TAG as section_id,  
   - section.pretty_name TAG as section_pretty_name SEPARATOR '/',  
   - section.levels.level_0 TAG as section_level_0,  
   - section.levels.level_1 TAG as section_level_1,  
   - section.levels.level_2 TAG as section_level_2,  
   - section.levels.level_3 TAG as section_level_3,  
   - section.levels.level_4 TAG as section_level_4  


### Redis TimeSeries

__Website__  
   - ts_name: 5MINUTES, 10MINUTES, etc.  
   - dimension: W, S, P  
   - M: PG, UD  
   - website_id: dbc218622189a62c7218fb1f62c362f2ad162646c2e, ...  
   - name: RTL, ...  


__Section__    
   - ts_name: 5MINUTES, 10MINUTES, etc.  
   - dimension: W, S, P  
   - M: PG, UD  
   - section_id: 46f3218321846f2187a2189e4dbeb63f14a162e2181a, ...  
   - pretty_name: meenung/carte-blanche, ...  -TODO-> section_name: meenung/carte-blanche
   - website_id: dbc218622189a62c7218fb1f62c362f2ad162646c2e, ...  
   - website_name: RTL, ...  


__Page__  
   - ts_name: 5MINUTES, 10MINUTES, etc.  
   - dimension: W, S, P   
   - M: PG, UD  
   - page_id: 6272182b62cd179ca7afa1eebc721872184ed2bff218, ...  
   - website_id: dbc218622189a62c7218fb1f62c362f2ad162646c2e, ...  
   - website_name: RTL, ...  
   - section_id: 46f3218321846f2187a2189e4dbeb63f14a162e2181a, ...  
   - section_pretty_name: meenung/carte-blanche, ...   -TODO-> section_name: meenung/carte-blanche


## Pythonic Redis Backend

### Build Python project
change version in pyproject.toml
delete /dist files
python3 -m build

### Upload Python package
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*

### Update Local Python Package
pip install rgtracker==0.0.1.1.219

##  Run RedisGears Jobs
### Requirements Job
python src/jobs/create_requirements.py

### Main Loop Job
gears-cli run --host localhost --port 6379 src/jobs/bigbang.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas requests

### Rotate Jobs 
#### 92 merged keys + 5 not merged keys (1 minute key) + 5 timeseries keys (1 pageviews, 4 unique devices) = 102 keys by recrods
#### Run the job every 5 minutes to rotate 5 key of 1 minute each. Expire new merged key after 30 minutes, i.e. keep 6 merged keys of 5 minutes each.
30 minutes requests
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/1to5/rotate_pg_website_1to5.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/1to5/rotate_pg_section_1to5.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/1to5/rotate_pg_page_1to5.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/1to5/rotate_ud_website_1to5.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/1to5/rotate_ud_section_1to5.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/1to5/rotate_ud_page_1to5.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  

#### Run the job every 10 minutes to rotate 2 key of 5 minutes each. Expire new merged key after 60 minutes, i.e. keep 6 merged keys of 10 minutes each.
1 hour requests
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/5to10/rotate_pg_website_5to10.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/5to10/rotate_pg_section_5to10.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/5to10/rotate_pg_page_5to10.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/5to10/rotate_ud_website_5to10.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/5to10/rotate_ud_section_5to10.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/5to10/rotate_ud_page_5to10.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas

#### Run the job every 60 minutes to rotate 6 key of 10 minutes each. Expire new merged key after 24 hours, i.e keep 24 merged keys of 1 hour each.
24 hours requests
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/10to60/rotate_pg_website_10to60.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/10to60/rotate_pg_section_10to60.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/10to60/rotate_pg_page_10to60.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/10to60/rotate_ud_website_10to60.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/10to60/rotate_ud_section_10to60.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/10to60/rotate_ud_page_10to60.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas

#### Run the job every 3 hours to rotate 3 key of 1 hour each. Expire new merged key after 7 days, i.e keep 56 merged keys of 3 hour each.
7 days request
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/60to180/rotate_pg_website_60to180.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/60to180/rotate_pg_section_60to180.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/60to180/rotate_pg_page_60to180.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/60to180/rotate_ud_website_60to180.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/60to180/rotate_ud_section_60to180.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas  
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/60to180/rotate_ud_page_60to180.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas

### Enrich Jobs
gears-cli run --host localhost --port 6379 src/jobs/enrich.py REQUIREMENTS rgtracker==0.0.1.1.219 pandas requests

### Notes
https://stackoverflow.com/questions/2221821862/how-to-apply-hyperloglog-to-a-timeseries-stream  
https://redis.com/blog/7-redis-worst-practices/  
https://redis.com/blog/streaming-analytics-with-probabilistic-data-structures/  
https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/  
https://www.peterbe.com/plog/best-practice-with-retries-with-requests  