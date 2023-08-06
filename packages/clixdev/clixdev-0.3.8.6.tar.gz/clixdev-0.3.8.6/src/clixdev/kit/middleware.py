import os
import json
from django.conf import settings
from django.http import JsonResponse
# from clixdev.apps.clix import validators


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("custom middleware before next middleware/view")
        # print(
        #     request.method,
        #     request.path,
        #     request.body,
        #     request.headers,
        #     request.content_type,
        # )

        # has_errors = False
        # errors = {
        #     "request": [],
        #     "headers": [],
        #     "params": [],
        #     "body": [],
        # }

        # wrk_dr = "/usr/local/.clix/CDBCB8/"

        # if not os.path.exists(wrk_dr) or \
        #     not os.path.exists(wrk_dr + '/' + prj_tkn) or \
        #     not os.path.exists(wrk_dr + '/' + prj_tkn + '/' + '_urls.txt') or \
        #     not os.path.exists(wrk_dr + '/' + prj_tkn + '/' + '_models.txt') or \
        #     not os.path.exists(wrk_dr + '/' + prj_tkn + '/' + '_validators.txt'):
        #     raise Exception('Sync your project using: clixdev sync')

        # f = open(wrk_dr + '_validators.txt')
        # app = json.load(f)
        # f.close()
        # app = json.loads(app)[0]

        # request = detecting correct endpoint details based on Request URI (if not in list pass)

        """
    Sudo code:
        if uri:
            if method:
                check headers (1.exist 2.type check)
                check params (1.exist 2.type check)
                check body*
                check response*
            else:
                error method not allowed
        else:
            let django handle (endpoint doesn't exist)
        """

        # validating request method
        # if str(request.method) != str(app['endpoints'][0]['request']['method']):
        #     has_errors = True
        #     errors['request'].append(
        #         f"request {request.method} is not allowed")

        # validating request headers
        # for header in list(app['endpoints'][0]['headers']['body'].values()):
        #     if header[0] not in request.headers.keys():
        #         has_errors = True
        #         errors['headers'].append(
        #             f"{header[0]} is missing from headers")
        #     else:
        #         if type(request.headers.keys()) != header[1]:
        #             has_errors = True
        #             errors['headers'].append(
        #                 f"{header[0]} should be {header[1]}")

        # validating request body type & payload
        # for body_payload in list(app['endpoints'][0]['body']['payload'].values()):
        #     if body_payload[0] not in request.body.keys():
        #         has_errors = True
        #         errors['body'].append("")

        # validating request params
        # for param in list(app['endpoints'][0]['params'].values()):
        #     if param[0] not in request.headers.keys():
        #         has_errors = True
        #         errors['params'].append("")

        # if has_errors:
        #     return JsonResponse({"errors": errors}) if settings.DEBUG else JsonResponse(False, safe=False)

        response = self.get_response(request)
        print("custom middleware after response or previous middleware")

        return response
