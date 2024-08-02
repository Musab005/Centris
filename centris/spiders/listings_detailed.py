import json
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


# ctrl + alt + l
# to format json file on pycharm

class ListingsSpider(scrapy.Spider):
    name = "listings_detailed"
    allowed_domains = ["www.centris.ca"]

    # first page on the pagination index
    position = {
        "startPosition": 0
    }

    # sort number for "Recent Publications"
    dropdown_sort = {
        "sort": 3
    }

    # splash script to render the html of the summary page of each listing
    summary_script = '''
        function main(splash, args)
            splash:on_request(function(request)
                if request.url:find('css') then
                    request.abort()
                end
            end)
            splash.images_enabled = false
            splash.js_enabled = false

            splash:set_viewport_full()
            splash:go(splash.args.url)
            splash:wait(5)

            return splash:html()
        end
    '''

    # code starts executing here
    def start_requests(self):
        # The query variable contains the request payload copied from the XHR request UpdateQuery.
        # It contains the following filters:
        # Location: Montréal (Island)
        # Features: 2 beds, 2 baths
        # Price: $1750 - $2500
        # Category: Residential, for rent
        query = {
            "query": {
                "UseGeographyShapes": 0,
                "Filters": [
                    {
                        "MatchType": "GeographicArea",
                        "Text": "Montréal (Island)",
                        "Id": "GSGS4621"
                    }
                ],
                "FieldsValues": [
                    {
                        "fieldId": "GeographicArea",
                        "value": "GSGS4621",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "Category",
                        "value": "Residential",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SellingType",
                        "value": "Rent",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "Rooms",
                        "value": "2",
                        "fieldConditionId": "IsResidentialNotLot",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "BathPowderRooms",
                        "value": "2+",
                        "fieldConditionId": "IsResidentialNotLot",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "LandArea",
                        "value": "SquareFeet",
                        "fieldConditionId": "IsLandArea",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 1750,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 2500,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    }
                ]
            },
            "isHomePage": True
        }

        # This method makes the API request to the UpdateQuery endpoint.
        yield scrapy.Request(
            url="https://www.centris.ca/property/UpdateQuery",  # url to send the request to
            method='POST',
            # body = payload. Need to send as string so convert the json object to string  using `dumps`
            body=json.dumps(query),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.update_sort  # go to this method after execution completes
        )

    def update_sort(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/property/UpdateSort",
            method="POST",
            body=json.dumps(self.dropdown_sort),  # The sort number for "Recent publications"
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.get_inscriptions
        )

    def get_inscriptions(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/Property/GetInscriptions",
            method="POST",
            body=json.dumps(self.position),  # Send the start position as payload so that it starts from the first page.
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.parse
        )

    def parse(self, response):
        # this is the actual response from the get_inscriptions method:
        # {
        #     "d": {
        #         "Message": "",
        #         "Result": {
        #             "html": "..."
        #         },
        #         "Succeeded": true
        #     }
        # }

        # convert it to a python dict:
        response_dict = json.loads(response.body)
        # print(type(response_dict))

        # we only need the html response so that we can start scraping
        html = response_dict.get('d').get('Result').get('html')

        # convert the html to a selector object so that we can use xpath. The html is just a string.
        sel = Selector(text=html)

        # Container for the listings
        listings = sel.xpath('//div[@class="property-thumbnail-item thumbnailItem col-12 col-sm-6 col-md-4 col-lg-3"]')

        for listing in listings:
            # no. of beds and baths
            beds = listing.xpath('.//div[@class="cac"]/text()').get()
            baths = listing.xpath('.//div[@class="sdb"]/text()').get()
            features = f"{beds} beds, {baths} baths"

            # price in $
            price = listing.xpath('.//div[@class="price"]/span/text()').get()
            price = price.replace('\xa0', '').split(' ')
            f_price = f'${price[0]}'

            # url that leads to the detailed info about the listing
            summary_url = listing.xpath(
                './/div[@class="thumbnail property-thumbnail-feature legacy-reset"]/a/@href').get()
            abs_summary_url = f'https://www.centris.ca{summary_url}'
            abs_summary_url = abs_summary_url.replace('fr', 'en')

            # Use the code below if you need to exclude listings from specific street addresses
            # if any(x in address for x in (
            #         'Chemin Bates', 'Avenue Madison', 'boulevard Décarie', 'Place Northcrest', 'Avenue Lennox',
            #         'Place des Jardins-des-Vosges', 'Chemin du Golf', 'Avenue des Pins Ouest', 'Rue Cartier')):
            #     pass
            # else:

            # execute the Splash request
            yield SplashRequest(
                url=abs_summary_url,
                endpoint='execute',
                callback=self.parse_summary,
                args={
                    'lua_source': self.summary_script
                },
                meta={  # send this argument to the parse_summary method
                    'features': features,
                    'price': f_price,
                    'url': abs_summary_url
                }
            )

        count = response_dict.get('d').get('Result').get('count')
        increment = response_dict.get('d').get('Result').get('inscNumberPerPage')

        if self.position["startPosition"] <= count:
            self.position["startPosition"] += increment
            yield scrapy.Request(
                url="https://www.centris.ca/Property/GetInscriptions",
                method='POST',
                body=json.dumps(self.position),
                headers={
                    'Content-Type': 'application/json'
                },
                callback=self.parse
            )

    def parse_summary(self, response):
        # meta = {  # send this argument to the parse_summary method
        #     'features': features,
        #     'price': f_price,
        #     'url': abs_summary_url
        # }

        # retrieve from splash response:

        # Category (apartment/condo/townhouse)
        category = response.xpath('//span[@data-id="PageTitle"]/text()').get()

        address = response.xpath('//h2[@itemprop="address"]/text()').get()
        if address is not None:
            address = response.xpath('//h2[@itemprop="address"]/text()').get().strip()
        else:
            address = "empty"

        area = response.xpath("//div[@class='col-lg-3 col-sm-6 carac-container' and div[@class='carac-title' and "
                              "text()='Net area']]//div[@class='carac-value']/span/text()").get()
        if area is None:
            area = "Not specified"

        description = response.xpath("//div[@itemprop='description']/text()").get()
        if description is not None:
            description = response.xpath("//div[@itemprop='description']/text()").get().strip()
        else:
            description = "empty"

        # Create the key value pairs for the listing
        yield {
            'category': category,
            'address': address,
            'features': response.request.meta['features'],
            'price': response.request.meta['price'],
            'area': area,
            'description': description,
            'summary_url': response.request.meta['url']
        }
