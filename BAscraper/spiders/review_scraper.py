import scrapy

class review_spider(scrapy.Spider):
    name = 'review_spider'

    def start_requests(self):
        
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}

        urls = ['https://www.airlinequality.com/airline-reviews/british-airways']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        for review in response.css('article[itemprop=review]'):

            table = review.css('table.review-ratings')

            yield{
                'title': review.css('h2.text_header::text').get(),
                'rating': review.css('div.rating-10').css('span[itemprop=ratingValue]::text').get(),
                'text': review.css('div.text_content').css('::text').getall()[-1],
                'date': review.css('time[itemprop=datePublished]::text').get(),
                'aircraft_type': table.xpath('.//td[contains(text(), "Aircraft")]/following-sibling::td[1]/text()').get(),
                'traveller_type': table.xpath('.//td[contains(text(), "Type Of Traveller")]/following-sibling::td[1]/text()').get(),
                'seat_type': table.xpath('.//td[contains(text(), "Seat Type")]/following-sibling::td[1]/text()').get(),
                'route': table.xpath('.//td[contains(text(), "Route")]/following-sibling::td[1]/text()').get(),
                'date_flown': table.xpath('.//td[contains(text(), "Date Flown")]/following-sibling::td[1]/text()').get(),
                'seat_comfort_rating': None if table.xpath('.//td[contains(text(), "Seat Comfort")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall() == []
                                        else table.xpath('.//td[contains(text(), "Seat Comfort")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall().pop(),
                'cabin_staff_rating': None if table.xpath('.//td[contains(text(), "Cabin Staff Service")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall() == []
                                        else table.xpath('.//td[contains(text(), "Cabin Staff Service")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall().pop(),
                'food_beverage_rating': None if table.xpath('.//td[contains(text(), "Food & Beverage")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall() == []
                                        else table.xpath('.//td[contains(text(), "Food & Beverage")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall().pop(),
                'entertainment_rating': None if table.xpath('.//td[contains(text(), "Inflight Entertainment")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall() == []
                                        else table.xpath('.//td[contains(text(), "Inflight Entertainment")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall().pop(),
                'ground_service_rating': None if table.xpath('.//td[contains(text(), "Ground Service")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall() == []
                                        else table.xpath('.//td[contains(text(), "Ground Service")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall().pop(),
                'wifi_rating': None if table.xpath('.//td[contains(text(), "Wifi & Connectivity")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall() == []
                                        else table.xpath('.//td[contains(text(), "Wifi & Connectivity")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall().pop(),
                'value_for_money_rating': None if table.xpath('.//td[contains(text(), "Value For Money")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall() == []
                                        else table.xpath('.//td[contains(text(), "Value For Money")]/following-sibling::td[1]/child::span[@class="star fill"]/text()').getall().pop(),
                'recommended': table.xpath('.//td[contains(text(), "Recommended")]/following-sibling::td[1]/text()').get(),
            }
        
        next_page_link = response.selector.xpath('//a[text()=">>"]/@href').get()

        if next_page_link is not None:
           yield response.follow('https://www.airlinequality.com' + next_page_link, callback=self.parse)
