from bs4 import BeautifulSoup
import requests
import parse_context
import random

# Debug
# import json
# import logging
# import socket
# from logging.handlers import SysLogHandler

class ITEM:
    def __init__(self, url="", price=0, address="-", description="-", img="-"):
        self.url = url
        self.price = price
        self.address = address
        self.description = description
        self.img = img


class PARSER:

    ####################################
    # PRIVATE
    ####################################

    def __init__(self, parseData, logger):
        self.context = parse_context.PARSE_CONTEXT()
        self.parseData = parseData
        self.logger = logger

    def __search_in_list(self, list, search_item):
        for item in list:
            if item.url == search_item.url:
                if item.price == search_item.price:
                    return True
        return False

    def __diff_list(self, item_list, new_list):
        new_items = []
        for item in new_list:
            isOld = self.__search_in_list(item_list, item)
            if not isOld:
                new_items.append(item)
        return new_items

    def __save_html(self, page):
        soup = BeautifulSoup(page.text, "html.parser")
        html = soup.prettify("utf-8")
        with open("parseResult.html", "wb") as file:
            file.write(html)

        print("Parse result is saved")

    def print_list(self):
        for item in self.itemsList:
            print(item.price, item.url)

    def log_list(self, list):
        for item in list:
            string = "      " + item.price + ", " + item.address
            self.logger.info(string)

    def getData(self, site, partName):
        return self.parseData[site][partName]

    def get_list(self, site, location, swap):
        self.logger.info("#")
        self.logger.info("#")
        self.logger.info("#")
        self.logger.info("getting parsed data...")
        diff_items = []
        if site == "ebay":
            if swap == 0:
                self.logger.info("#")
                self.logger.info("  Old list:")
                self.log_list(self.context.ebay.ebay_lists_old_nosw[location])
                self.logger.info("#")
                self.logger.info("  New list:")
                self.log_list(self.context.ebay.ebay_lists_nosw[location])

                diff_items = self.__diff_list(self.context.ebay.ebay_lists_old_nosw[location],
                                              self.context.ebay.ebay_lists_nosw[location])
            elif swap == 1:
                self.logger.info("#")
                self.logger.info("Old list:")
                self.log_list(self.context.ebay.ebay_lists_old[location])
                self.logger.info("#")
                self.logger.info("New list:")
                self.log_list(self.context.ebay.ebay_lists[location])

                diff_items = self.__diff_list(self.context.ebay.ebay_lists_old[location],
                                              self.context.ebay.ebay_lists[location])
            elif swap == 2:
                self.logger.info("#")
                self.logger.info("Old list:")
                self.log_list(self.context.ebay.ebay_lists_old_both[location])
                self.logger.info("#")
                self.logger.info("New list:")
                self.log_list(self.context.ebay.ebay_lists_both[location])

                diff_items = self.__diff_list(self.context.ebay.ebay_lists_old_both[location],
                                              self.context.ebay.ebay_lists_both[location])
            else:
                self.logger.info("#")
                self.logger.info("Error: wrong SWAP parameter in function parse.get_list()")
                self.logger.info("#")
        elif site == "wggesucht":
            diff_items = self.__diff_list(self.context.wg.wg_lists_old[location], self.context.wg.wg_lists[location])
        else:
            self.logger.info("Error: wrong site parameter in function get_list")
        self.logger.info("#")
        self.logger.info("Diff:")
        self.log_list(diff_items)
        return diff_items

    def proxy_request(self, request_type, url, **kwargs):
        ip = ["8.219.97.248:80"]
        ip_addresses = ["159.197.250.171:3128", "193.104.189.68:3128", "157.100.12.138:999", "8.219.97.248:80"]

        try:
            raise Exception
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            self.logger.info("Request was made without proxies")
        except:
            self.logger.info("Error. Looking for proxy....")
            while True:
                try:
                    proxy = random.randint(0, len(ip_addresses) - 1)
                    proxies = {"http": ip_addresses[proxy], "https": ip_addresses[proxy]}
                    response = requests.get(url, proxies=proxies, timeout=5, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, **kwargs)
                    print(f"Proxy currently being used: {proxy}")
                    break
                except:
                    print("Error, looking for another proxy: ", proxy)
        return response

    ################
    # Ebay parsing process
    ################

    def __ebay_get_items_in_list(self, page, location, swap):
        resultList = []
        templist = []
        soup = BeautifulSoup(page.text, 'lxml')
        for item in soup.findAll("li", {"class": "ad-listitem lazyload-item"}):
            resultList.append(item)
            print("########################################")
            print(item)
            print("########################################")


        for item in resultList[:5]:
            try:
                item_url = "https://www.ebay-kleinanzeigen.de"  # JSON
                item_url += item.find("a", href=True)["href"]
                price = item.find("p", {"class": "aditem-main--middle--price-shipping--price"}).text.strip()
                address = item.find("div", {"class": "aditem-main--top--left"}).text.strip()
                decrip = item.find("a", {"class": "ellipsis"}).text.strip()
                img = item.find("div", {"class": "imagebox srpimagebox"})["data-imgsrcretina"].split()[0]
                item_data = ITEM(url=item_url, price=price.split()[0], address=address, description=decrip, img=img)
                templist.append(item_data)
            except Exception:
                pass

        self.logger.info("#")
        self.logger.info("#")
        self.logger.info("  Parsed list:")
        for item in templist:
            string = "      " + item.price + ", " + item.address
            self.logger.info(string)

        if templist:
            if swap == "0":
                self.context.ebay.ebay_lists_old_nosw[location] = self.context.ebay.ebay_lists_nosw[location]
                self.context.ebay.ebay_lists_nosw[location] = templist
            elif swap == "1":
                self.context.ebay.ebay_lists_old[location] = self.context.ebay.ebay_lists[location]
                self.context.ebay.ebay_lists[location] = templist
            elif swap == "2":
                self.context.ebay.ebay_lists_old_both[location] = self.context.ebay.ebay_lists_both[location]
                self.context.ebay.ebay_lists_both[location] = templist
            else:
                self.logger.info("#")
                self.logger.info("Error. Wrong SWAP parameter in method parse.make()")
                self.logger.info("#")
        else:
            self.logger.info("          Parsed list is empty")
            if swap == "0":
                self.context.ebay.ebay_lists_old_nosw[location] = self.context.ebay.ebay_lists_nosw[location]
            elif swap == "1":
                self.context.ebay.ebay_lists_old[location] = self.context.ebay.ebay_lists[location]
            elif swap == "2":
                self.context.ebay.ebay_lists_old_both[location] = self.context.ebay.ebay_lists_both[location]
            else:
                self.logger.info("#")
                self.logger.info("Error. Wrong SWAP parameter in method parse.make()")
                self.logger.info("#")

    def __ebay_create_url(self, location, priceOt, priceDo, swap):
        url = self.getData('ebay', 'base_url')

        if location != "":
            url += self.getData('ebay', 'city_start')[location]

        url += self.getData('ebay', 'price_base_url') + str(priceOt) + ":" + str(priceDo)

        if location != "":
            url += self.getData('ebay', 'city_end')[location]
        else:
            url += "/c203"

        url += self.getData('ebay', 'swap')[swap]

        self.logger.info(url)
        return url

    def __ebay_parse(self, location, priceOt, priceDo, swap):
        url = self.__ebay_create_url(location, priceOt, priceDo, swap)
        # page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        page = self.proxy_request(self, url=url)
        # print(page.text)
        code = "Request code: " + str(page.status_code)
        self.logger.info(code)

        if page.status_code == 200:
            self.__ebay_get_items_in_list(page=page, location=location, swap=swap)

        else:
            self.logger.info("Error while Parsing")
            self.logger.info(BeautifulSoup(page.text, "html.parser").text)

        ################
        # WG Gesucht parsing process
        ################

    def __wg_get_items_in_list(self, page, location):
        resultList = []
        templist = []
        html = page.text
        soup = BeautifulSoup(html, 'lxml')

        for item in soup.findAll("div", {"class": "wgg_card offer_list_item"}):
            resultList.append(item)

        for item in resultList[:5]:
            print("--------------------------")
            print(item)
            print("--------------------------")
            try:
                item_url = self.getData('wg', 'base_url')
                item_url += item.find("a", href=True)["href"]
                price = item.find("div", {"class": "col-xs-3"}).find("b").text.strip()

                address = item.find("div", {"class": "col-xs-11"}).find("span").text
                print("@############################")
                a = address.replace(address[0], "")
                print(a.replace(a[0], ""))
                print(a.replace(a[0], ""))
                print("@############################")
                index1 = address.find("|") + 1
                address = address[index1:]
                index2 = address.find("|") + 1
                street = address[index2:].strip()
                bezirk = address.split("|")[0].strip()

                description = item.find("a", {"class": "detailansicht"}).find("b").text
                img = item.find("a")["style"][22:-2]

                item_data = ITEM(item_url, price.split()[0], address=street, description=description, img=img)
                templist.append(item_data)
            except Exception:
                print("Error")
                pass

        self.context.wg.wg_lists_old[location] = self.context.wg.wg_lists[location]
        self.context.wg.wg_lists[location] = templist

    def __wg_create_url(self, location, priceDo=100000, swap=2):
        #  &sort_column=0&sort_order=&noDeact=1&dFr=&dTo=&radLat=&radLng=&clear_vu=&autocompinp=Berlin+%28Berlin%29&country_code=de&city_name=Berlin&categories%5B%5D=1&categories%5B%5D=2&rent_types%5B%5D=0&sMin=&rMax=&pu=&hidden_dFrDe=&hidden_dToDe=&radAdd=&radDis=&wgSea=&wgMnF=&wgMxT=&wgAge=&wgSmo=&rmMin=&rmMax=&fur=&pet=&sin=&exc=&kit=&flo=
        # url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-"  # opportunity for Flats-Typ Selection
        url = self.getData('wg', 'base_url') + "/1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-"
        url += self.getData('wg', 'city_start')[location]
        # url += "+2.1.0.html?csrf_token=&offer_filter=1"  # 1 Room Flat + Flats
        url += "+3.1.0.html?csrf_token=&offer_filter=1"  # 1 Room Flat + Flats
        url += self.getData('wg', 'city_end')[location]
        url += "&sort_column=0&noDeact=1&categories%5B%5D=1&categories%5B%5D=2&rent_types%5B%5D=2&rMax="
        url += str(priceDo)
        url += self.getData('wg', 'swap')[swap]

        print(url)
        return url

    def __wg_parse(self, location, priceDo, swap):
        url = self.__wg_create_url(location=location, priceDo=priceDo, swap=swap)
        page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

        print("Request code: ", page.status_code)
        if page.status_code == 200:
            self.__wg_get_items_in_list(page=page, location=location)
        else:
            print("Error while Parsing")
            print(BeautifulSoup(page.text, "html.parser").text)

    def make(self, site="ebay", location="", priceOt="", priceDo="", swap=2):
        self.logger.info("start parsing...")
        if site == "all":
            self.__ebay_parse(location, priceOt, priceDo, str(swap))
            self.__wg_parse(location, priceDo, swap)
        elif site == "ebay":
            self.__ebay_parse(location, priceOt, priceDo, str(swap))
        elif site == "wggesucht":
            self.__wg_parse(location, priceDo, str(swap))

# Debug

# class ContextFilter(logging.Filter):
#     hostname = socket.gethostname()
#     def filter(self, record):
#         record.hostname = ContextFilter.hostname
#         return True
#
# def loggerInit():
#     syslog = SysLogHandler(address=('logs6.papertrailapp.com', 52605))
#     syslog.addFilter(ContextFilter())
#     format = '%(asctime)s %(hostname)s LOG: %(message)s'
#     formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
#     syslog.setFormatter(formatter)
#     logger = logging.getLogger()
#     logger.addHandler(syslog)
#     logger.setLevel(logging.INFO)
#
#     return logger
#
#
#
# with open('config_parse.json') as file:
#     parseData = json.load(file)
#
#
# logger = loggerInit()
# request = PARSER(parseData, logger)
# site = "ebay"
# location = "Berlin"
# swap=0
#
# request.make(site=site, location=location, priceDo=1500, swap=swap)  # Wg gesucht - 10k geht nicht
# a = request.get_list(site, location, swap=swap)
#
# print("List:")
# for el in a:
#     print(el.url)
#     print(el.price)
#     print(el.description)
#     print(el.address)
#     print("\n")
