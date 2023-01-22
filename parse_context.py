class EBAY:
    def __init__(self):
        self.ebay_lists = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_old = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_nosw = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_old_nosw = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_both = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_old_both = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }


class WG:
    def __init__(self):
        self.wg_base_url = "https://www.wg-gesucht.de"
        self.wg_swap = {
            -1: "",
            0: "&exc=2",
            1: "&exc=1"
        }
        self.wg_lists = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
        }
        self.wg_lists_old = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
        }
        self.wg_city_start = {
            "Berlin": "Berlin.8.1",
            "Hamburg": "Hamburg.55.1",
            "Muenchen": "Munchen.90.1",
            "Frankfurt_main": "Frankfurt-am-Main.41.1",
            "Hannover": "Hannover.57.1",
            "Leipzig": "Leipzig.77.1",
            "Dresden": "Dresden.27.1",
            "Dortmund": "Dortmund.26.1",
            "Koeln": "Koeln.73.1",
            "Duesseldorf": "Dusseldorf.30.1",
            "Bremen": "Bremen.17.1",
            "Stuttgart": "Stuttgart.124.1",
            "Nuernberg": "Nurnberg.96.1",
            "Essen": "Essen.35.1",
            "Bonn": "Bonn.13.1",
        }
        self.wg_city_end = {
            "Berlin": "&city_id=8",
            "Hamburg": "&city_id=55",
            "Muenchen": "&city_id=55",
            "Frankfurt_main": "&city_id=41",
            "Hannover": "&city_id=57",
            "Leipzig": "&city_id=77",
            "Dresden": "&city_id=27",
            "Dortmund": "&city_id=26",
            "Koeln": "&city_id=73",
            "Duesseldorf": "&city_id=30",
            "Bremen": "&city_id=17",
            "Stuttgart": "&city_id=124",
            "Nuernberg": "&city_id=96",
            "Essen": "&city_id=35",
            "Bonn": "&city_id=13",
        }


class PARSE_CONTEXT:
    def __init__(self):
        self.locations = [
            "Berlin",
            "Hamburg",
            "Muenchen",
            "Frankfurt_main",
            "Hannover",
            "Leipzig",
            "Dresden",
            "Dortmund",
            "Koeln",
            "Duesseldorf",
            "Bremen",
            "Stuttgart",
            "Nuernberg",
            "Essen",
            "Bonn",
        ]
        self.ebay = EBAY()
        self.wg = WG()
