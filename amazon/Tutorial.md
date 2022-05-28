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

In the command line/Anaconda prompt/termianl, navigate into the folder where you wish to create your project and type in:

```
scrapy startproject <project_name> [project_dir]
```

This command generates a new folder called [project_dir]. This is the project's root directory and within it are the "scrapy.cfg" file (containing configuration parameters) and another folder called <project_name>.
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

**"items.py"** - used to define dict-like subclasses for the scraped items.

**"middlewares.py"** - used to define models with custom functionality that process the requests/responses from/to a website or a spider.

**"pipelines.py"** - used to post-process the scraped items (duplicate removal, storing in a database etc.)

**"settings.py"** - used to customize the behaviour of all scrapy components (core, extensions, pipelines and the spiders themselves).

Note that since we're building a very basic spider, we won't actually change too much in these files.

There is a also a folder called **"spiders/"** that doesn't contain any spiders yet.

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
    start_urls = ['http://www.domainname.com/']

    def parse(self, response):
        pass
```        

A spider class that inherits from scrapy's base spider class, "scrapy.Spider", is created.

**"name" -** The spider's unique name.

**"allowed_domains" -** contains a list of the domains we're interested in scraping. It will prevent our spider from following links that lead outside of the specified domains during scraping. Do not add "https://" in the begining!

**"start_urls" -** contains the urls of the pages we would like to start scraping from. Scrapy automatically adds "http://" to the url we inputed. Make sure to change that it "https://" if that is the case for your url. Scrapy will send sequential requests to these specified urls and the response downloaded from each url will be passed on to the **"parse()"** method to be processed (The "response" holds the url page's content and it has many helpful methods to process said content).

**"parse() -"** This method is used to extract the scraped data and find new urls to follow and send new requests to.

## Extract scraped data

As mentioned above, the act of extracting useful data is done through the **"parse()** method. To extract data from the response, we'll use scrapy's Selectors:

```python
scraped_data = response.xpath("xpath_expression").get()
```
or
```python
scraped_data = response.css("css_expression").get()
```

XPath is a language used to identify parts in an XML document (but works with HTML as well). CSS is a language used to apply styles to HTML documents. Both are equally useful for identifying relevent sections in a web page.The choice of using xpath or css depends on whether the user is more familiar with XPath expressions or with CSS.

To those who are familiar with neither and/or are short on time, this chrome extension, https://selectorgadget.com/, is a useful tool that will find the css/xpath expression for you just by clicking on the desired content in the web page.

Both the xpath() and css() methods return a list of selectors. Each selector in the list references a section of the document that matches the css/xpath expression. In order to access the textual data within these selectors, we need to use the selector **get()** or **getall()** methods. **get()** will return the textual contant of the first match (or None if there is no match), and **getall()** will return a list of all the results.

Alternatively, we can use nested selectors. i.e. call the selection methods on the results of the previouse selection. For example:

```python
items = response.xpath("xpath_expression")
    
    for item in items:

        item_title = item.xpath(".xpath_expression").get()
        item_ingredients = item.xpath(".xpath_expression").getall()
        item_rating = item.xpath(".xpath_expression").get()
```
