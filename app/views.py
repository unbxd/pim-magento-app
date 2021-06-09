import logging
import json
from traceback import print_exc

from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.template import loader
from rest_framework.views import APIView
# from PAS.models import AppUser, App, PimProp

from .installer import Installer
from common.utils.utility import get_pim_app_domain, get_pas_domain
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger("shopify.views")


from django.conf import settings
from common.PAS.app import App, AppUser
from common.PIM.pim import Installer as PIMInstaller

app_id = "PIM_MAGENTO2_APP"
app = App(app_id)
class PIMInstall(APIView):
    """
        Class that handlers shopify install calls
    """
    def __init__(self):
        self.installer = Installer()


    @csrf_exempt
    def post(self, request):
        """
            Method  that is called when user clicks the install button on shopify app store .
        :param request: (object)
        :return:  Redirects the user to the shopify auth page
        """
        try:
            req_data = json.loads(request.body)
            identifier = req_data["pim"]["siteName"]
            appUser = AppUser(app_id=app.app_data.name, identifier=identifier)
            appUser.create(app_id=app.app_data.name, identifier=identifier, **{req_data[app_id]["data"]})

            if app.app_name not in req_data or "data" not in req_data[app.app_name]:
                return HttpResponse("No Custom Channel name sent", status=400)

            #TODO Call App based install/OAuth methods
            app_creds = self.installer.install()
            app_creds = {**app_creds, **req_data[app_id]["data"]}
            app.create_app_user(app=app.app_data.name, identifier=identifier, **app_creds)
            cookie = request.COOKIES.get('_un_sso_uid')
            source = request.headers.get("referer")
            pim_data = req_data["pim"]
            pim_data["cookie"] = cookie
            PIMInstaller(pim_data)
            redirect_url = get_pim_app_domain() + "/#/network/orgId=" +pim_data['orgKey']+ ";primaryTab=channels;secondaryTab=installedChannels"
            return JsonResponse({"redirect_url": redirect_url}, status = 200)
        except ValueError as e:
            print_exc()
            logger.error("Shopify - Validation error : {}".format(str(e)))
            return JsonResponse({"msg": "Bad request: {}".format(str(e))}, status=400)

        #TODO Templatise to use PAS-sdk urls




class Install(APIView):
    """
        Class that handlers shopify install calls
    """
    def __init__(self):
        self.installer = Installer()


    @csrf_exempt
    def post(self, request):
        """
            Method  that is called when user clicks the install button on shopify app store .
        :param request: (object)
        :return:  Redirects the user to the shopify auth page
        """
        try:
            req_data = json.loads(request.body)
            identifier = req_data["pim"]["siteName"]
            appUser = AppUser(app_id=app.app_data.name, identifier=identifier)
            appUser.create(app_id=app.app_data.name, identifier=identifier, **{req_data[app_id]["data"]})

            if app.app_name not in req_data or "data" not in req_data[app.app_name]:
                return HttpResponse("No Custom Channel name sent", status=400)

            #TODO Call App based install/OAuth methods
            app_creds = self.installer.install()
            app_creds = {**app_creds, **req_data[app_id]["data"]}
            app.create_app_user(app=app.app_data.name, identifier=identifier, **app_creds)
            cookie = request.COOKIES.get('_un_sso_uid')
            source = request.headers.get("referer")
            pim_data = req_data["pim"]
            pim_data["cookie"] = cookie
            PIMInstaller(pim_data)
            redirect_url = get_pim_app_domain() + "/#/network/orgId=" +pim_data['orgKey']+ ";primaryTab=channels;secondaryTab=installedChannels"
            return JsonResponse({"redirect_url": redirect_url}, status = 200)
        except ValueError as e:
            print_exc()
            logger.error("Shopify - Validation error : {}".format(str(e)))
            return JsonResponse({"msg": "Bad request: {}".format(str(e))}, status=400)

        #TODO Templatise to use PAS-sdk urls



class Uninstall(APIView):

    def get(self, request):
        """
            Method that is being called upon user clicking the Uninstall button on the Bigcommerce.
        :param request:
        :return:
        """
        try:
            data = request.GET.get('data', None)
            if data is None:
                raise ValueError("Uninstall API : Invalid number of parameters received.")
            logger.info("Uninstall API: signed payload - {}".format(data))
            self.installer.uninstall(data)
            return HttpResponseRedirect("https://pimapps.unbxd.io/login?appId=ENRICHMENT_PIM_DONDE_V!")
        except ValueError as e:
            logger.error("Uninstall API - value error: {}".format(str(e)))
            print_exc()
            return HttpResponse(status=500)

        except Exception as e:
            logger.error("Uninstall API - exception : {}".format(str(e)))
            print_exc()
            return HttpResponse(status=500)


class Health(APIView):
    def get(self, request):
        """
            Method that is being called upon user clicking the Uninstall button on the Bigcommerce.
        :param request:
        :return:
        """

        return JsonResponse({"msg": "I am kicking some"}, safe=False, status=401)

    def post(self, request):
        """
            Method  that is called when user clicks the install button on shopify app store .
        :param request: (object)
        :return:  Redirects the user to the shopify auth page
        """
        req_data = json.loads(request.body)

        return JsonResponse({"data": "Succesuufully finished processing it"}, safe=False, status=200)




def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())
