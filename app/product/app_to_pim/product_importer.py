from app_mgr.models import AppUserProp
from .denormalisation import Transformer


class ProductImporter(object):

    def __init__(self, user, request_id):
        self.user = user
        self.request_id = request_id
        self.app_name= "CUSTOM_APP"
        properties = AppUserProp.get_properties_by_user(user=user)
        # TODO Product level common config initialisation


    def __del__(self):
        # Call the delete or garbage clear
        print("Do Cleanup")

    def pull_channel_products(self, reference_id):
        transformer = Transformer('app_template/product/app_to_pim/denormalisation.json')
        #TODO API calls to Pull products from your channel and merge all the relevant properties to it
        # store the raw object from platform in final_product_list array and update transformations in denormalisation config

        final_product_list = []
        products_list = []
        for product in final_product_list:
            counter = counter + 1
            # TODO Manage the product level cleanup and final expected custom channel format
            product = transformer.transform(product)
            products_list.append(product)

        #TODO Done processing the Denormalisation

        if len(products_list) > 0:
            return products_list
            zip_file_name = self.write_feed_file(file_dir, final_product_list)
            return "{}/{}/{}".format(self.user.app.name, self.user.identifier, zip_file_name)



