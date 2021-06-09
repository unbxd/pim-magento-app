import logging
import json
import traceback
import requests

from urllib.parse import urlencode
from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.views import APIView

from app_mgr.models import AppUser, PimProp, App
from common.pim_catalog.installer import Installer
from common.pim_catalog.serializer import PimPropSerializer
from django.conf import settings

logger = logging.getLogger("pim_catalog.views")
PIM_APP_NAME = "unbxd_pim"
from common.utils.utility import get_pim_app_domain, get_pas_domain, get_pim_domain

class AppInstall(APIView):
    """
        Class to handle oauth flow.
    """

    def prepare_redirect_url(self, app_type, store_name):
        query_params = dict()
        query_params['appId'] = app_type
        if app_type == 'BIGCOMMERCE_PIM_V1':
            query_params['store_hash'] = store_name
        elif app_type == 'PIM_BRIGHTPEARL_APP':
            query_params['accountCode'] = store_name
        elif app_type == "AMAZON_PIM_APP":
            query_params['seller_id'] = store_name
        else:
            raise ValueError("{} app not supported".format(app_type))
        return "{}/dashboard?{}".format(get_pim_domain(), urlencode(query_params))

    @staticmethod
    def validate(data):
        if (
                not data.get('orgKey') or
                not data.get("identifier") or
                not data.get("authToken")
        ):
            raise ValueError("App Install: Pimcreds request is wrong")

        if "appId" not in data:
            raise ValueError("App Install: appId property is missing with appCreds")

    @csrf_exempt
    def post(self, request):
        """
            Method to handle Pim installation along with access_token of the installing app.
        :param request:
        :return: (json) Installation status.
        """
        try:
            try:
                data = json.loads(request.body)
            except ValueError as e:
                logger.error("Wrong request has been passed to installation API, " + str(e))
                return JsonResponse(
                    {"data": {}, "error": ["Invalid request " + str(e)]}, safe=False, status=400
                )
            self.validate(data)
            app_id = data["appId"]
            try:
                user = AppUser.objects.get(app__label=app_id, identifier=data["identifier"])
            except ObjectDoesNotExist:
                logger.error("Wrong User is passed for installation: {}".format(app_id))
                return JsonResponse({"msg": "User doesnt exists"}, safe=False, status=401)

            # Install the Pim application on the pim catalog
            pim_installer = Installer()
            pim_installer.install(
                org_key=data["orgKey"],
                site_name=data["identifier"],
                auth_token=data["authToken"],
                group_by_parent=data.get("group_by_parent", True),
                app_id=app_id, user=user
            )

            return JsonResponse(
                {"status": "success", "data": {"identifier": data["identifier"], "appId": data['appId']}},
                safe=False, status=200
            )
        except ValueError as e:
            traceback.print_exc()
            logger.error("Error : {}".format(str(e)))
            return JsonResponse(
                    {"data": {}, "errors": ["Bad request: {}".format(str(e))]}, safe=False, status=400)
        except Exception as e:
            traceback.print_exc()
            logger.error("Error : {}".format(str(e)))
            return JsonResponse(
                    {"data": {}, "errors": ["Internal error : {}".format(str(e))]}, safe=False, status=500
                )


class Installer(APIView):

    # def install(self, org_key, site_name, auth_token, app_id, identifier, cookie=None, source=None):
    def post(self, request):
        data = json.loads(request.body)
        org_key = data["org_key"]
        site_name = data["site_name"]
        app_id = data["app_id"]
        identifier = data["identifier"]
        cookie = data["cookie"]
        app = App.objects.get(name=app_id)
        app_custom_id = app.label
        user = AppUser.objects.get(identifier=identifier)

        pim_installer = Installer()
        pim_installer.install(
            org_key=org_key,
            site_name=site_name,
            cookie=cookie,
            group_by_parent=data.get("group_by_parent", True),
            app_id=app_id, user=user
        )

        return JsonResponse(
            {"status": "success", "data": {"identifier": data["identifier"], "appId": data['appId']}},
            safe=False, status=200
        )


class Import(generics.RetrieveAPIView):

    def post(self, request, **kwargs):
        import_id = kwargs.get('import_id')
        req = json.loads(request.body)
        identifier = req.get("identifier")
        app_id = req.get("appCustomId")
        page = int(req.get("page", 1))
        count = int(req.get("count", 10))
        try:
            pim_prop = PimProp.objects.get(user__identifier__exact=identifier, user__app__label__exact=app_id)
        except ObjectDoesNotExist:
            logger.debug("No pim authorization properties existed from account: " + str(identifier))
            return JsonResponse({"msg": "Pim authorization did not happen"}, status=401)
        api_key = pim_prop.api_key

        headers = {
            "content-type": "application/json",
            "Authorization": api_key
        }

        if import_id is None:
            url = get_pim_domain() + "/pim/v1/imports/details"
            pim_req = {"page": page, "count": count}
            response = requests.post(url=url, headers=headers, json=pim_req)
        else:
            url = get_pim_domain() + "/pim/v1/imports/" + import_id + "/status"
            response = requests.get(url=url, headers=headers)

        return JsonResponse(response.json(), status=response.status_code)

class PimConf(ListAPIView, UpdateAPIView):
    serializer_class = PimPropSerializer
    lookup_field = "user__identifier"

    def get_queryset(self):
        username = self.kwargs['user__identifier']
        return PimProp.objects.filter(user__identifier=username)

class Login(APIView):


    def get(self, request):
        is_loggedin = '1'
        return render(request, "templates/login.html", {'isLogin':is_loggedin, "pim_domain": get_pim_app_domain()})

    def post(self, request):
        keys = request.POST.keys()
        if 'email' in keys:
            app = request.GET.get('app')
            identifier = request.GET.get('identifier')
            userEmail = request.POST['email']
            password = request.POST['password']
            response = pimLogin(userEmail, password)

            response_json = json.loads(response.text)
            if response_json['errors'] != []:
                error_flag = 1
                return render(request, "templates/login.html", {'isLogin': '1', 'error_flag':error_flag , "pim_domain": get_pim_app_domain()})
            else:
                auth_token = response_json['data']['auth_token']
                options = response_json['data']['org_list']
                is_loggedin = '0'
                return render(request, "templates/login.html", {'options':options, 'isLogin':is_loggedin, 'auth_token':auth_token, 'app':app, "pim_domain": get_pim_app_domain()})

        else:
            identifier = request.GET.get('identifier')
            app_id = request.GET.get('app')
            login_callback = request.GET.get('login_callback')
            org_key = request.POST['Organisation']
            # market_place_id = request.POST['region']
            #

            auth_token = request.POST['auth_token']
            site_name = request.POST['siteName']
            app = App.objects.get(name=app_id)
            app_custom_id = app.label
            user = AppUser.objects.get(identifier=identifier)
            pim_installer = Installer()
            pim_installer.install(
                org_key=org_key,
                site_name=site_name,
                auth_token=auth_token,
                group_by_parent=True,
                app_id=app_custom_id, user=user
            )


            return redirect(login_callback + f"?identifier={identifier}")

def pimLogin(userEmail, password):
    url = get_pim_domain() + "/v1/login"

    payload = json.dumps({
        "email": userEmail,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response
