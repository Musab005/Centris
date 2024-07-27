import json
import scrapy
from scrapy.selector import Selector


# ctrl + alt + l
# to format json file on pycharm


class ListingsSpider(scrapy.Spider):
    name = "listings"
    allowed_domains = ["www.centris.ca"]

    # item number
    position = {
        "startPosition": 0
    }

    # sort number for "Recent Publications"
    dropdown_sort = {
        "sort": 3
    }

    # code starts executing here
    def start_requests(self):
        # This variable contains the request payload copied from the XHR request UpdateQuery. It contains the filters.
        query = {
            "query": {
                "UseGeographyShapes": 0,
                "Filters": [
                    {
                        "MatchType": "CityDistrict",
                        "Text": "Montréal (Ville-Marie)",
                        "Id": 843
                    },
                    {
                        "MatchType": "CityDistrict",
                        "Text": "Montréal (Verdun/Île-des-Soeurs)",
                        "Id": 819
                    },
                    {
                        "MatchType": "CityDistrict",
                        "Text": "Montréal (Rosemont/La Petite-Patrie)",
                        "Id": 844
                    },
                    {
                        "MatchType": "CityDistrict",
                        "Text": "Montréal (Le Sud-Ouest)",
                        "Id": 839
                    },
                    {
                        "MatchType": "CityDistrict",
                        "Text": "Montréal (Le Plateau-Mont-Royal)",
                        "Id": 842
                    },
                    {
                        "MatchType": "CityDistrict",
                        "Text": "Montréal (LaSalle)",
                        "Id": 820
                    },
                    {
                        "MatchType": "CityDistrict",
                        "Text": "Montréal (Côte-des-Neiges/Notre-Dame-de-Grâce)",
                        "Id": 838
                    }
                ],
                "FieldsValues": [
                    {
                        "fieldId": "CityDistrict",
                        "value": 843,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "CityDistrict",
                        "value": 819,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "CityDistrict",
                        "value": 844,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "CityDistrict",
                        "value": 839,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "CityDistrict",
                        "value": 842,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "CityDistrict",
                        "value": 820,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "CityDistrict",
                        "value": 838,
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
            body=json.dumps(self.dropdown_sort),  # payload is the sort number for "Recent publications"
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.get_inscriptions
        )

    def get_inscriptions(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/Property/GetInscriptions",
            method="POST",
            body=json.dumps(self.position),  # payload is the listing number so that it starts from the first page
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.parse
        )

    def parse(self, response):
        # the response is a JSON object that is interpreted as a String:
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
        # print(type(response_dict))
        response_dict = json.loads(response.body)

        # we only need the html response
        html = response_dict.get('d').get('Result').get('html')
        # we will scrap this html response, so save it as a separate file for easy lookup
        # with open('centris.html', 'w') as f:
        #     f.write(html)

        # convert the html to a selector object so that we can use xpath. The html is just a string
        sel = Selector(text=html)
        listings = sel.xpath('//div[@class="property-thumbnail-item thumbnailItem col-12 col-sm-6 col-md-4 col-lg-3"]')

        for listing in listings:

            # category (condo/apartment/townhouse)
            category = listing.xpath('.//span[@class="category"]/div/text()').get()
            if category is not None:
                category = category.strip()

            # no. of beds and baths
            beds = listing.xpath('.//div[@class="cac"]/text()').get()
            baths = listing.xpath('.//div[@class="sdb"]/text()').get()
            features = f"{beds} beds, {baths} baths"

            # price in $
            price = listing.xpath('.//div[@class="price"]/span/text()').get()
            price = price.replace('\xa0', '').split(' ')
            f_price = f'${price[0]}'

            # complete address
            add1 = listing.xpath(".//span[@class='address']/div[1]/text()").get()
            add2 = listing.xpath(".//span[@class='address']/div[2]/text()").get()
            add3 = listing.xpath(".//span[@class='address']/div[3]/text()").get()
            address = f"{add1}, {add2}, {add3}"

            # url that leads to the detailed info about the listing
            summary_url = listing.xpath(
                './/div[@class="thumbnail property-thumbnail-feature legacy-reset"]/a/@href').get()
            abs_summary_url = f'https://www.centris.ca{summary_url}'
            # For some reason, I still get the French listings
            abs_summary_url = abs_summary_url.replace('fr', 'en')

            # if any(x in address for x in (
            #         'Montréal (Mercier/Hochelaga-Maisonneuve)', 'Montréal (Anjou)', 'Montréal (Saint-Laurent)',
            #         'Montréal (Lachine)', 'Montréal (Villeray/Saint-Michel/Parc-Extension)',
            #         'Montréal (Pierrefonds-Roxboro)', 'Pointe-Claire', 'Dollard-des-Ormeaux')):
            #     pass
            # else:
            yield {
                'category': category,
                'features': features,
                'address': address,
                'price': f_price,
                'url': abs_summary_url
            }

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
