import requests
from app_mgr.models import PimProp
import json
from math import floor
import logging

from common.utils.exceptions import PimProductException

logger = logging.getLogger("pim_catalog.models")
from django.conf import settings
from common.utils.utility import get_pim_app_domain, get_pas_domain, get_pim_domain


class Import(object):
    def __init__(self, pim_prop):
        self.pim_prop = pim_prop

    def import_to_pim(self, file_path):
        url = "{}/v1/imports".format(get_pim_domain())

        payload = dict()
        payload["url"] = file_path

        headers = {
            'Content-Type': "application/json",
            'Authorization': self.pim_prop.api_key,
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            logger.error(
                "Pim Product Pull failed due non 200 status data:  {} status_code {} ".format(
                    response.status_code, response.text
                )
            )
            raise ValueError("Pim Product Pull failed due non 200 status " + response.text)
        if "data" not in response.json() or "import_id" not in response.json()["data"]:
            raise ValueError("Pim Product Pull failed due to data expectation")

        return response.json()["data"]["import_id"]


class Product(object):
    def __init__(
            self, pim_prop, reference_id=None, properties=[], group_by_parent=None, parent_id=None, q=None,
            cache_count=10, app_id=None
    ):
        self.pim_prop = pim_prop
        self.properties = properties
        self.group_by_parent = self.pim_prop.group_by_parent if group_by_parent is None else group_by_parent
        self.q = q
        self.cache_count = cache_count
        self.cache = []
        self.reference_id = reference_id
        self.app_id = app_id
        self.parent_id = parent_id

    def __iter__(self):
        self.n = 0
        response = self.get(count=10)

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
                if "data" not in response or "products" not in response["data"]:
                    raise ValueError("Invalid response returned by PIM")
                products = response["data"]["products"]
                self.cache = products
            self.n += 1
            if len(self.cache) > index:
                return self.cache[index]
        else:
            raise StopIteration

    def get(self, count=10, page=1):
        url = "{}v1/products".format(get_pim_domain())
        headers = {
            'Content-Type': "application/json",
            'Authorization': self.pim_prop.api_key,
        }
        req = {
            "page": page,
            "count": count,
            "groupByParent": self.group_by_parent,
            "properties": self.properties,
            "q": self.q,
            "referenceId": self.reference_id,
            "parentId": self.parent_id
        }
        logger.info("Requesting URL {}".format(url))
        logger.info("Request for PIM products : {}".format(str(json.dumps(req))))
        response = requests.post(url, headers=headers, json=req)
        if response.status_code != 200:
            raise PimProductException(
                "Pim Product Pull failed due non {} response body {} - reason {} ==> Request Object >> {}".format(
                    response.status_code, response.text, response.reason, str(req)
                )
            )
        if "data" not in response.json() or "products" not in response.json()["data"]:
            raise PimProductException("Pim Product Pull failed due to data expectation")

        return response.json()




