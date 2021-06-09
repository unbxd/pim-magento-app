from django.core.exceptions import ObjectDoesNotExist
from app_mgr.models import PimProp
from common.app_template.product.app_to_pim.product_importer import ProductImporter
from common.app_template.product.pim_to_app.product_exporter import ProductExporter
import logging
from common.PIM.models import Import as ImportIntoPIM
from django.conf import settings

from common.utils.file_operations import write_feed_file
from viper.settings import DUMP_DIR

logger = logging.getLogger(__name__)

class ProductSync(object):
    def product_import(self, request_id, user, reference_id=None):
        try:
            pim_prop = PimProp.objects.get(user=user)
            if pim_prop is None:
                raise ValueError("Pim properties for the app installation is not set")
            import_product = ProductExporter(user, pim_prop, request_id)
            import_product.pullPimProducts(reference_id)
            return True

        except ObjectDoesNotExist:
            pass

    def get_viper_domain(self):
        return getattr(settings, "PIM_BASE_URL")

    def product_export(self, request_id, user, reference_id=None):
        try:
            export_product = ProductImporter(user, request_id)
            products = export_product.pull_channel_products(reference_id)
            file_dir = "{}/{}/{}".format(DUMP_DIR, user.app.name, user.identifier)
            zip_file_name = write_feed_file(file_dir, products)
            dist_link = "{}/{}/{}".format(self.user.app.name, self.user.identifier, zip_file_name)
            pim_prop = PimProp.objects.get(user=user)
            pim_import = ImportIntoPIM(pim_prop)
            import_id = pim_import.import_to_pim(self.get_viper_domain() + "/export/{}".format(dist_link))
            logger.info("Product export Custom APp: Export completed")
            return import_id
        except ObjectDoesNotExist:
            pass
