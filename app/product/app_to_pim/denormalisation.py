import json
import logging
from datetime import datetime, timezone


logger = logging.getLogger('shopify_catalog.product.transformer_graphql')


class Transformer:
    logger = logging.getLogger('shopify_catalog/product/app_to_pim/denormalisation.json')

    def __init__(self, configpath):
        self.logger.info('Loading transformer configuration from: %s', configpath)
        with open(configpath, 'r') as fp:
            self.config = json.load(fp)

    @staticmethod
    def _update_product(product, key, data):
        if type(data) is dict:
            product.update(data)
        else:
            product[key] = data

    def transform(self, product):
        changed_product = {}
        for fieldname in product:
            if fieldname in self.config:
                transformer = self.config[fieldname]
                helper_func = getattr(self, transformer['helper'])
                self._update_product(changed_product, transformer['key'], helper_func(product, fieldname))
            else:
                if product[fieldname] != None:
                    changed_product[fieldname] = product[fieldname]
        return changed_product

    @staticmethod
    def handler_datetime(product, key):
        if product[key] is not None:
            try:
                dt = datetime.fromisoformat(product[key])
            except ValueError:
                dt = datetime.utcnow()
            dt = dt.astimezone(tz=timezone.utc)
            return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            return None

    @staticmethod
    def handler_string(product, key):
        return str(product[key]).strip()

    @staticmethod
    def handler_id(product, key):
        return str(product[key]).split('/')[-1]

    @staticmethod
    def handler_decimal(product, key):
        try:
            value = float(product[key])
        except (ValueError, TypeError):
            value = None
        return value
