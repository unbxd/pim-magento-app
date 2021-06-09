from django.conf import settings
import requests
from math import floor


def get_pim_domain():
    return getattr(settings, "PIM_BASE_URL")


class Properties(object):

    def __init__(self, pim_prop, cache_count=100):
        self.pim_prop = pim_prop
        self.cache_count = cache_count
        self.adapter = self.get_adapter()

    def __iter__(self):
        self.n = 0
        response = self.get(count=0)
        if "data" not in response or "total" not in response["data"]:
            raise ValueError("Invalid response returned by PIM")

        self.max = response["data"]["total"]
        return self

    def __next__(self):
        if self.n < self.max:
            index = self.n % self.cache_count
            if index == 0:
                page = floor(self.n / self.cache_count) + 1
                response = self.get(count=self.cache_count, page=page)
                if "data" not in response or "entries" not in response["data"]:
                    raise ValueError("Invalid response returned by PIM")

                properties = response["data"]["entries"]
                self.cache = properties
            self.n += 1
            if len(self.cache) > index:
                return self.cache[index]
        else:
            raise StopIteration

    def get_adapter(self, count=10, page=1):
        url = "{}/v1/channelAdapterList/".format(get_pim_domain())
        headers = {
            'Content-Type': "application/json",
            'Authorization': self.pim_prop.api_key,
        }
        req = {
            "count": count,
            "page": page
        }
        response = requests.post(url, headers=headers, json=req)
        if response.status_code != 200:
            raise ValueError("Pim property fetch failed due non 200 status " + response.text)

        if "data" not in response.json():
            raise ValueError("Pim fields API failed due to data expectation")
        adapter_data = response.json()
        return adapter_data['data']['entries'][0]

    def get(self, count=100, page=1):
        url = "{}/v1/channelAdapter/{}/properties".format(get_pim_domain(), self.adapter['id'])
        headers = {
            'Content-Type': "application/json",
            'Authorization': self.pim_prop.api_key,
        }
        req = {
            "count": count,
            "page": page
        }
        response = requests.post(url, headers=headers, json=req)
        if response.status_code != 200:
            raise ValueError("Pim adapters fetch failed due non 200 status " + response.text)

        if "data" not in response.json() or "entries" not in response.json()["data"]:
            raise ValueError("Pim fields API failed due to data expectation")

        return response.json()
