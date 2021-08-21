# Url shortener



## Dependencies
    - Python > 3.6
    - Sqlite

# Quickstart
1. Clone repository from Github:
```bash
git clone https://github.com/ayanami142/url-shortener.git
```
2. For easy install the dependencies, you can use Makefile commands
```bash
make Makefile setup
make Makefile migrate

make Makefile run-dev  # for local development
or
make Makefile run-prod  # for production
```
or you can do it manually:
```bash
 python3 -m virtualenv env
 source env/bin/activate
 pip install -U pip ./env/bin/pip 
 install -r requirements.txt
 
 cd src
 flask db upgrade
 
 python run.py 
 or 
 gunicorn -w 4 run:app
```

3. (Optional)
```
Check other useful commands in Makefile for development
    make Makefile help
```

# API Documentation
### 1. Convert url to shorten:
```http
POST /shorten_url
Content-Type: application/json
Status code: 201 or 400 if url is not valid or empty
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `url` | `string` | **Required**. Website url |

Example response:
```javascript
{
  "shorten_url": "https://app-domain.com/short_code"
}
```

Example of valid urls:
```
https://www.domain.dom:5000/hello
www.test.test
google.com
localhost
```

### 2. Convert shorten url to base url and redirect to this url:
```http
GET /<url_code>
Status code: 301 if url code is valid or 400 if not valid
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `<url_code>` | `string` | **Required**. Short url code |


### 3. Get number of shorten urls:
```http
GET /shortened_urls_count
Content-Type: application/json
Status code: 200
```
Example response:
```javascript
{
  "Number of shortened urls": 2021
}
```
<i>Note: Result includes only unique urls with unique ip addresses</i>  

### 4. Get top 10 urls ordered by views count and sorted by desc:
```http
GET /top10
Content-Type: application/json
Status code: 200
```
Example response:
```javascript
{
  "Most popular urls": "www.google.com, www.amazon.com, www.ebay.com, www.yahoo.com"
}
```



# Notes by developer:
#### 1. I made a decision to use b64encode to shorten URL for optimizing database and do not convert the same URL address. So this is similar to cache and get better performance.
#### 2. At the beginning I was getting only first 8 chars from b64 encode, but after tests I got that the similar URLs like google.com and goosgle.com has the same b64 in the start. After this, I made a decision to get the last 8 chars instead of the first.
#### 3. About performance:
By default, Flask uses a single synchronous process, which means at most 1 request is being processed at a time.
But when we will use Gunicorn in production, we can set the number of workers via --workers key.
It helps us to works with i.e 4 workers and scale handling requests by 4 times (depends on CPU)

Also, we can use Async workers like Greenlets, but we should adapt our application and database for this.
#### 4. I used Sqlite instead of Postgres or MySql because it's to easier and faster for development. In real situation Postgres would be better :)


## TODO
- Unit tests