# Amazon Web Scraper

This scraper contains two similar spiders, both aimed at scraping customer reviews from Amazon products, and located at the amazon/spiders/ folder:

1. "reviews" - takes in a link to search results and returns the reviews for all products that were found.
2. "single_product" - takes in a link to a single product's page and returns its reviews.

both spiders collect the following information: product_name, product_url, product_ingredients, review_title, review_body, rating.

## Usage Instructions:

first, install the scraping library and its associated user-agent utility library:
```
pip install Scrapy
pip install scrapy-user-agents
```

To set the link you wish to scrape, open the suitable spider, and replace the link in the "start_urls" variable with the link of your choice.
```
start_urls = [
        'https://www.amazon.com/Ingredients-Activated-Charcoal-Therapeutic-Essential/dp/B00S5HIZZC/ref=sr_1_8?qid=1649600527&rnid=11060901&s=beauty&sr=1-8'
    ]
```
Next, in your terminal, cd into the folder that contains the "scrapy.cfg" file.

In the terminal, type in:
```
scrapy crawl <spider_name>
```
This will run the spider.

This will either create a new SQLite database called amazon.db, or add the scraped reviews to an existing one.

If you prefer using MySQL, go to "settings.py" and comment/uncomment the appropriate pipeline:
```
ITEM_PIPELINES = {
   # 'amazon.pipelines.SQLlitePipeline': 300,
   'amazon.pipelines.mySQLPipeline': 300,
}
```
Then go to "piplines.py" and fill in your details:
```python
class mySQLPipeline(object):

    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='input_your_password here',
            database='name_of_our_db'  # create it in mySQL beforehand
        )
```
Alternatively, you can comment out both pipelines and use scrapy's built in function to generate a csv or json file:
```
scrapy crawl <spider_name> -o database.csv
```
or
```
scrapy crawl <spider_name> -o database.json
```
