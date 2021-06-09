import logging

from common.app_template.product.pim_to_app.normalisation import Transformer
from app_mgr.models import AppUserProp
from common.PIM.models import Product as PimProductList
from common.utils.exceptions import PimProductException
from traceback import print_exc

logger = logging.getLogger('shopify_catalog.product.transformer_graphql')


class ProductExporter(object):

    def __init__(self, user, pim_prop, request_id):
        self.user = user
        self.request_id = request_id
        properties = AppUserProp.get_properties_by_user(user=user)
        # TODO Product level common config initialisation
        self.pim_prop = pim_prop
        self.request_id = request_id


    def __del__(self):
        # Call the delete or garbage clear
        print("Do Cleanup")


    # 1. Pulls products and variants from PIM
    def pullPimProducts(self, reference_id=""):
        self.reference_id = reference_id
        products_list = []
        # TODO property handler to handle property
        transformer = Transformer('app_template/product/pim_to_app/normalisation.json')
        counter = 1
        logger.info("Update from PIM to Shopify have begun for user: {} with reference_id: {}".
                    format(self.user.identifier, reference_id))
        try:
            for product in PimProductList(self.pim_prop, self.reference_id, group_by_parent=False):
                counter = counter + 1
                # TODO Manage the product level cleanup and final expected custom channel format
                product = transformer.transform(product)
                products_list.append(product)

            print("fetched all products", len(products_list))

            #TODO make product update to the system

            # TODO Update the celery thread to update job status

        except PimProductException as e:
            logger.error("Error : {} reason being {}".format("Could not fetch products from PIM", str(e)))
            raise e
        except Exception as e:
            print_exc()
            logger.error("Error : {} reason being {}".format("Could not fetch products from PIM", str(e)))
            raise e
