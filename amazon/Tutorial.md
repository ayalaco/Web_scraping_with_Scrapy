# How To create your own basic spider

This is a tutorial aimed to help you create your own very basic spider with scrapy.
What it is not, is an html/CSS tutorial. Basic knowledge is required, though, and some useful links will be provided.

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

"items.py" - used to define dict-like subclasses for the scraped items.

"middlewares.py" - used to define models with custom functionality that process the requests/responses from/to a website or a spider.

"pipelines.py" - used to post-process the scraped items (duplicate removal, storing in a database etc.)

"settings.py" - used to customize the behaviour of all scrapy components (core, extensions, pipelines and the spiders themselves).

Note that since we're building a very basic spider, we won't actually change too much in these files.

There is a also a folder called "spiders" that doesn't contain any spiders yet.

## Generate a spider

