import scrapy


class SingleProductSpider(scrapy.Spider):
    name = 'single_product'
    allowed_domains = ['www.amazon.com']
    start_urls = [
        'https://www.amazon.com/Ingredients-Activated-Charcoal-Therapeutic-Essential/dp/B00S5HIZZC/ref=sr_1_8?qid=1649600527&rnid=11060901&s=beauty&sr=1-8'
    ]

    def parse(self, response):

        product_url = response.url
        product_name = response.xpath("normalize-space(//span[@id='productTitle']/text())").get()
        product_ingredients = response.xpath(
            "//div[@id='important-information']/div/h4[contains(text(), 'Ingredients')]/following-sibling::node()/text()").get()
        reviews_url = response.xpath("(//a[@data-hook='see-all-reviews-link-foot']/@href)[1]").get()

        yield response.follow(url=reviews_url,
                              callback=self.parse_reviews,
                              meta={"product_name": product_name, "product_url": product_url,
                                    "product_ingredients": product_ingredients}
                              )

    def parse_reviews(self, response):

        product_name = response.request.meta['product_name']
        product_url = response.request.meta['product_url']
        product_ingredients = response.request.meta['product_ingredients']

        reviews = response.xpath("//div[@data-hook='review']/div/div")

        for review in reviews:

            review_title = review.xpath(".//div/a[@data-hook='review-title']/span/text()").get()
            review_body = ' '.join(
                ''.join(review.xpath(".//div/span[@data-hook='review-body']/span/text()").getall()).split())
            rating = float(
                review.xpath(".//div/a/i[@data-hook='review-star-rating']/span/text()").get().replace('out of 5 stars',

                                                                                                      ''))

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

        if next_page:
            yield scrapy.Request(url='https://www.amazon.com' + next_page,
                                 callback=self.parse_reviews,
                                 meta={"product_name": product_name, "product_url": product_url,
                                       "product_ingredients": product_ingredients})
