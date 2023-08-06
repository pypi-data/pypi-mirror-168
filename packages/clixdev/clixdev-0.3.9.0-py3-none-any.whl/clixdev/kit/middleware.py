import os
import json
from django.conf import settings
from django.http import JsonResponse


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("\ncustom middleware before next middleware/view")

        # has_errors = False
        # errors = {
        #     "request": [],
        #     "headers": [],
        # }

        # import clixdev
        # wrk_dr = clixdev.__path__[0] + "/apps/clix/"
        # if not os.path.exists(wrk_dr):
        #     raise Exception('Please Sync your project')

        # f = open(wrk_dr + 'validations.json')
        # validations = json.load(f)
        # f.close()

        # for v in validations:
        #     if str(request.META['PATH_INFO']) == '/' + v[1] + '/' + v[2]:
        #         if str(request.META['REQUEST_METHOD']) == str(v[0]):
                    # for header in v[3]:
                    #     h = 'HTTP_' + header[0].replace('-', '_').upper()
                    #     if h not in request.META.keys():
                    #         has_errors = True
                    #         errors['headers'].append(f"header {header[0]} is missing")
        #             pass
        #         else:
        #             has_errors = True
        #             errors['request'].append(f"request {request.META['REQUEST_METHOD']} is not allowed")

        # if has_errors:
        #     return JsonResponse({"errors": errors}) if settings.DEBUG else JsonResponse(False, safe=False)

        response = self.get_response(request)
        # print("custom middleware after response or previous middleware\n")

        return response
