# How To create your own basic spider

This is a tutorial aimed to help you create your own very basic spider with scrapy.
What it is not, is an HTML/CSS tutorial. Basic knowledge is required, though, and some useful links will be provided.

## Install necessary libraries

This includes the scraping library itself and its associated user-agent utility library:

```
pip install Scrapy
pip install scrapy-user-agents
```

## Generate a project

In the command line/Anaconda prompt/terminal, navigate into the folder where you wish to create your project and type in:

```
scrapy startproject <project_name> [project_dir]
```

This command generates a new folder called [project_dir]. This is the project's root directory and within it are the **"scrapy.cfg"** file (containing configuration parameters) and another folder called <project_name>.
The <project_name> folder contains the following files:

```
<project_name>/
    __init__.py
    items.py
    middlewares.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
```

This is the scaffold on top of which we will build our spider.

**"items.py"** - used to define dict-like classes for the scraped items.

**"middlewares.py"** - used to define models with custom functionality that process the requests/responses from/to a website or a spider.

**"pipelines.py"** - used to post-process the scraped items (duplicate removal, storing in a database etc.)

**"settings.py"** - used to customize the behavior of all scrapy components (core, extensions, pipelines and the spiders themselves).

Note that since we're building a very basic spider, we won't actually change too much in these files.

There is also a folder called **"spiders/"** that doesn't contain any spiders yet.

## Generate a spider

To create a basic spider, first navigate into the [project_dir] folder, then type in:

```
scrapy genspider <spider_name> <domain or url>
```
Note that the <spider_name> should be unique for each spider that we create within the project.

This will create a "spider_name.py" file in the "spiders" folder, which will contain the following skeleton for us to fill:

```python
import scrapy


class SpiderNameSpider(scrapy.Spider):
    name = 'spider_name'
    allowed_domains = ['www.domainname.com']
    start_urls = ['http://www.domainname.com/page-we-want-to-scrape']

    def parse(self, response):
        pass
```        

A spider class that inherits from scrapy's base spider class, "scrapy.Spider", is created.

**"name" -** The spider's unique name.

**"allowed_domains" -** contains a list of the domains we're interested in scraping. It will prevent our spider from following links that lead outside of the specified domains during scraping. Do not add "https://" in the beginning!

**"start_urls" -** contains the urls of the pages we would like to start scraping from. Scrapy automatically adds "http://" to the url we inputted. Make sure to change it to "https://" if that is the case for your url. Scrapy will send sequential requests to these specified urls and the response downloaded from each url will be passed on to the **"parse()"** method to be processed (The "response" holds the url page's content and it has many helpful methods to process said content).

**"parse() -"** This method is used to extract the scraped data and find new urls to follow and send new requests to.

## Extract scraped data

As mentioned above, the act of extracting useful data is done through the **"parse()** method. To extract data from the response, we'll use scrapy's Selectors:

```python
scraped_data = response.xpath("//xpath_expression").get()
```
or
```python
scraped_data = response.css("css_expression").get()
```

XPath is a language used to identify parts in an XML document (but works with HTML as well). CSS is a language used to apply styles to HTML documents. Both are equally useful for identifying relevant sections in a web page. The choice of using xpath or css depends on whether the user is more familiar with XPath expressions or with CSS.

To those who are familiar with neither and/or are short on time, this chrome extension, https://selectorgadget.com/, is a useful tool that will find the css/xpath expression for you just by clicking on the desired content in the web page. That said, I do recommend obtaining even just a passing familiarity with one of the options.

Both the xpath() and css() methods return a list of selectors. Each selector in the list references a section of the document that matches the css/xpath expression. In order to access the textual data within these selectors, we need to use the selector **get()** or **getall()** methods. **get()** will return the textual content of the first match (or None if there is no match), and **getall()** will return a list of all the results.

Alternatively, we can use nested selectors. i.e. continue to use the selection methods to extract data from each of the document sections that where selected previously. For example:

```python
def parse(self, response):

    # select the relevant sections in the HTML document:
    items = response.xpath("//xpath_expression")

        for item in items:

            # select data to scrape within each section:
            item_title = item.xpath(".//xpath_expression").get()
            item_ingredients = item.xpath(".//xpath_expression").getall()
            item_rating = item.xpath(".//xpath_expression").get()

            # send the scraped data to be processed:
            yield {
                'item_title': item_title,
                'item_ingredients': item_ingredients,
                'item_rating': item_rating,
            }
```
Note that when we use an xpath expression to search within a selected object instead of a response object, we need to start the expression with ".//" instead of "//".

If pipelines were defined in **"pipelines.py"** (not mandatory), then the dictionary that contains the scraped data is passed forward through these pipelines to be processed further. The order of the pipelines is determined in **"settings.py"** like this:

```python
ITEM_PIPELINES = {
   'project_name.pipelines.FirstPipelineName': 300,
   'project_name.pipelines.SecondPipelineName': 400,
}
```

The lower the number, the higher the priority of execution.

## Following links

Sometimes we won't find all the information we want to scrape within one document. Instead, we'd like to follow a link within the document and scrape additional information from there.

There are actually several ways to do this, but the one I find simplest is to use the response's **"follow()"** method. This method takes in several important arguments:

**url** - The url we scraped from the original document and which we wish to follow. This url can be either an absolute url or relative to the url of the current document.

**callback** - The follow method sends a request to the scraped url; The returned response needs to be processed by some other function. The callback parameter determines which function the response is sent to.

**meta** - Any information that was scraped within the **parse()** method can be passed forward to the next parsing function through a dictionary in the meta parameter.

For example:

```python
def parse(self, response):
    
    # scrape data from the current page:
    item_url = response.url
    item_name = response.xpath("//xpath_expression").get()
    item_ingredients = response.xpath("//xpath_expression").get()
    
    # get link to another page (for example, a reviews page):
    link = response.xpath("//xpath_expression").get()
    
    # follow link to another page and parse its content:
    yield response.follow(url=link,
                          callback=self.parse_reviews,
                          meta={"item_url": item_url,
                                "item_name": item_name,
                                "item_ingredients": item_ingredients
                                }
                          )

# define a new function for parsing reviews:
def parse_reviews(self, response):
    
    # access the scraped data that was passed through the meta argument:
    item_url = response.request.meta['item_url']
    item_name = response.request.meta['item_name']
    item_ingredients = response.request.meta['item_ingredients']
    
    # select all the separate reviews in the page:
    reviews = response.xpath("//xpath_expression")
    
    # iterate over the reviews:
    for review in reviews:
        
        # scrape the title and text of the review:
        review_title = review.xpath(".//xpath_expression").get()
        review_body = review.xpath(".//xpath_expression").get()
        
        # yield all the scraped data from one review in dict form:
        yield {
            'item_name': item_name,
            'item_url': item_url,
            'item_ingredients': item_ingredients,
            'review_title': review_title,
            'review_body': review_body,
        }
```

## Pagination
What happens if we want to scrape something that spans several pages? For example, calling back to the previous example, when we have several pages of reviews.
The solution is actually similar to what we just did: we follow the link to the next page from our current one, until there is no link to scrape because we reached the last page.
```python
next_page_link = response.xpath("//xpath_expression").get()
```
When we reach the last page the selector will return **None** when it won't find a match.

If there is a valid link to the next page, we'll follow it and send the response to the same **parse_reviews()** function (don't forget to pass the relevant data you want to pass forward through the **meta** argument).
```python
if next_page_link:
    yield scrapy.follow(url=next_page_link,
                        callback=self.parse_reviews,
                        meta={"item_url": item_url,
                              "item_name": item_name,
                              "item_ingredients": item_ingredients
                              }
                        )
```

And to see it all together:
```python
import scrapy

class SpiderNameSpider(scrapy.Spider):
    name = 'spider_name'
    allowed_domains = ['www.domainname.com']
    start_urls = ['http://www.domainname.com/page-we-want-to-scrape']

    def parse(self, response):

        # scrape data from the current page:
        item_url = response.url
        item_name = response.xpath("//xpath_expression").get()
        item_ingredients = response.xpath("//xpath_expression").get()

        # get link to another page (for example, a reviews page):
        link = response.xpath("//xpath_expression").get()

        # follow link to another page and parse its content:
        yield response.follow(url=link,
                              callback=self.parse_reviews,
                              meta={"item_url": item_url,
                                    "item_name": item_name,
                                    "item_ingredients": item_ingredients
                                    }
                              )

    # define a new function for parsing reviews:
    def parse_reviews(self, response):

        # access the scraped data that was passed through the meta argument:
        item_url = response.request.meta['item_url']
        item_name = response.request.meta['item_name']
        item_ingredients = response.request.meta['item_ingredients']

        # select all the separate reviews in the page:
        reviews = response.xpath("//xpath_expression")

        # iterate over the reviews:
        for review in reviews:

            # scrape the title and text of the review:
            review_title = review.xpath(".//xpath_expression").get()
            review_body = review.xpath(".//xpath_expression").get()

            # yield all the scraped data from one review in dict form:
            yield {
                'item_name': item_name,
                'item_url': item_url,
                'item_ingredients': item_ingredients,
                'review_title': review_title,
                'review_body': review_body,
            }

        # scrape the link for the next page:
        next_page_link = response.xpath("//xpath_expression").get()

        # if a next page exists, follow the link and process the next page using the same parse_reviews() function:
        if next_page_link:
            yield scrapy.follow(url=next_page_link,
                                callback=self.parse_reviews,
                                meta={"item_url": item_url,
                                      "item_name": item_name,
                                      "item_ingredients": item_ingredients
                                      }
                                )
```

## Spoofing headers

With everything we've done until now, we actually already have a nice functional spider. The only problem is that most websites that we would like to scrape would block our spider when they'd recognize that the requests are coming from scrapy. Furthermore, even if we change scrapy's default user-agent to our own personal one, we are still likely to get blocked if we want to scrape many pages.

Luckily, there are actually many ways to get around this problem, either by using rotating user-agents or by using proxies. 
The easiest solution that worked for me simply required the installation of the scrapy-user-agent package (https://pypi.org/project/scrapy-user-agents/), and adding these lines to **settings.py**:
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}
```

And nothing more than that is required. Now you have a functional spider that won't get blocked immediately.

## running the spider

Running our finished spider is extremely simple. In the command line/terminal/anaconda prompt, navigate into the project_directory that contains the **"scrapy.cfg"** file, then type in the following:

```
scrapy crawl <spider_name>
```

## Exporting the scraped data

The simplest way to export our scraped data is to use scrapy's built-in function when running the spider. 

To save the data in csv format:
```
scrapy crawl <spider_name> -o file_name.csv
```
And in json format:
```
scrapy crawl <spider_name> -o file_name.json
```

## Optional additions

As you can see above, creating a functional and useful spider doesn't actually require much. However, scrapy has a lot of additional functionality we could make use of. I won't get into the details, just mention a few options:

1. Scrapy actually has 5 types of spiders we can inherit from, not just the basic spider we used here. Depending on the type of data you want to scrape, consider looking into the other options. For example, I found the crawlSpider class very useful for automating and streamlining pagination and following many links.
2. Use the pipelines.py file to create data cleaning methods and/or to send the scraped data to a database of your choice (SQL, MongoDB, etc.)
3. Use the items.py file to define a class for the scraped data (instead of passing it through a simple dictionary).
4. Utilize the scrapy shell for interactive selection - useful for testing out expressions and the like.

## Useful links
1. https://docs.scrapy.org/ - Scrapy's documentation.
2. https://www.udemy.com/course/web-scraping-in-python-using-scrapy-and-splash/ - A useful udemy course that goes over all the basics.
3. https://youtube.com/playlist?list=PLhTjy8cBISEqkN-5Ku_kXG4QW33sxQo0t - A helpful course on YouTube.
