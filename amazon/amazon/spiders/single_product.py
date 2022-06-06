import scrapy
from scrapy.http import TextResponse


class SingleProductSpider(scrapy.Spider):
    name = 'single_product'
    allowed_domains = ['www.amazon.com']
    start_urls = [
        'https://www.amazon.com/Ingredients-Activated-Charcoal-Therapeutic-Essential/dp/B00S5HIZZC/ref=sr_1_8?qid=1649600527&rnid=11060901&s=beauty&sr=1-8'
    ] # Change me! (can be more than one link in the list)

    def parse(self, response: TextResponse) -> scrapy.Request:
        '''
        Accepts the content of the page in "start_urls". Extracts the name, url and ingredients of the product.
        It then extracts and follows a link to the product's reviews, to be processed in the parse_reviews() function.

        Args:
        response: holds the url page's content

        yield: a request object for the review's url
        '''

        product_url = response.url
        product_name = response.xpath("normalize-space(//span[@id='productTitle']/text())").get()
        product_ingredients = response.xpath(
            "//div[@id='important-information']/div/h4[contains(text(), 'Ingredients')]/following-sibling::node()/text()").get()
        
        # extract a link to the product's reviews page:
        reviews_url = response.xpath("(//a[@data-hook='see-all-reviews-link-foot']/@href)[1]").get()

        # follow the link to the reviews page for further scraping:
        yield response.follow(url=reviews_url,
                              callback=self.parse_reviews,
                              meta={"product_name": product_name, "product_url": product_url,
                                    "product_ingredients": product_ingredients}
                              )

    def parse_reviews(self, response: TextResponse) -> dict:
        '''
        Accepts the content of the reviews page and the meta data from the function that originated the request.
        Extracts the title, body and rating from each review.
        Follows a link to the next page to repeat the process (if there is a next page).

        Args:
        response: holds the url page's content and meta data from the function that originated the request.

        yield: a dictionary containing the scraped data for each review
        '''

        # access meta data:
        product_name = response.request.meta['product_name']
        product_url = response.request.meta['product_url']
        product_ingredients = response.request.meta['product_ingredients']

        # find all reviews in the page:
        reviews = response.xpath("//div[@data-hook='review']/div/div")

        # Extract the title, body and rating from each review:
        for review in reviews:

            review_title = review.xpath(".//div/a[@data-hook='review-title']/span/text()").get()
            review_body = ' '.join(
                ''.join(review.xpath(".//div/span[@data-hook='review-body']/span/text()").getall()).split())
            rating = float(
                review.xpath(".//div/a/i[@data-hook='review-star-rating']/span/text()").get().replace('out of 5 stars',

                                                                                                      ''))
            # yield the scraped data for each review in dict form:
            yield {
                'product_name': product_name,
                'product_url': product_url,
                'product_ingredients': product_ingredients,
                'review_title': review_title,
                'review_body': review_body,
                'rating': rating
            }


        # pagination for a single product's reviews:
        next_page = response.xpath("(//ul[@class='a-pagination']/li)[2]/a/@href").get()
        
        # If a next page link exists, follow it and repeat scraping procedure.
        if next_page:
            yield scrapy.Request(url='https://www.amazon.com' + next_page,
                                 callback=self.parse_reviews,
                                 meta={"product_name": product_name, "product_url": product_url,
                                       "product_ingredients": product_ingredients})
