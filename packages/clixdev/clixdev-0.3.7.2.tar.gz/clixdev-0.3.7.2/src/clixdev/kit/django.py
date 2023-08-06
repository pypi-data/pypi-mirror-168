import json
from django.conf import settings
from django.http import JsonResponse


class Django:
    def __init__(self, get_response):
        self.get_response = get_response
        self.endpoints = [
            {"uri": "user/all/", "method": "GET",
                "headers": {"Content-Type": "application/json"}}
        ]

    def __call__(self, request):
        print("custom middleware before next middleware/view")
        # our work is here mostly
        # if debug is true, add self.messages ro response

        has_errors = False
        errors = {
            "request": [],
            "headers": [],
            "params": [],
            # "response": []
        }

        print(
            request.method,
            request.path,
            request.body,
            request.headers,
            request.content_type,
        )

        f = open('../../../usr/clix.json', 'r')
        res = json.load(f)
        f.close()

        # print(res[0]['endpoints'][0]['request']['method'])

        for header in list(res[0]['endpoints'][0]['headers']['body'].values()):
            if header[0] not in request.headers.keys():
                has_errors = True
                errors['headers'].append(f"header {header[0]} is missing")

        if str(request.method) != str(res[0]['endpoints'][0]['request']['method']):
            has_errors = True
            errors['request'].append(f"request {request.method} is not allowed")

        # only if there are errors
        if has_errors:
            return JsonResponse({"errors": errors}) if settings.DEBUG else JsonResponse(False, safe=False)

        response = self.get_response(request)

        # if response.status_code == 500:
        #     current_url = resolve(request.path_info).view_name
        #     content = response.content
        #     ExceptionHandlerModel.objects.create(url=current_url, stacktrace=content, ...)

        print("custom middleware after response or previous middleware")
        # print('\nresponse ', response)
        return response
