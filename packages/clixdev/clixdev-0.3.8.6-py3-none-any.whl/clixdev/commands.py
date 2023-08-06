import os
import json
import shutil
import requests
# from pathlib import Path

# URLS, REQUIREMENTS, README, ADMIN
from .trace import MANAGE, WSGI, SETTINGS, BASE_SETTINGS, VIEWS, BASE_MODELS, APP_URLS


def generate(terminal_token, project_token, *args):
    try:
        _dir = os.getcwd()
        _res = requests.post('http://localhost:8000/api/package/sync',
        data=json.dumps({
            'terminal_token': terminal_token,
            'project_token': project_token,
            'local_path': _dir + '/' + args[0] + '/' if args[0] else _dir + '/',
        })).json()

        project_name = _res.get('misc').get('project_name')
        working_dir = _dir + '/' + args[0] + '/' + project_name + '/' if args[0] else _dir + '/' + project_name + '/'
        
        # TODO some logic needed here
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)
        os.makedirs(working_dir)
        
        base_file_tree = {
            'manage.py': MANAGE(project_name),
            project_name + '/': [('__init__.py', ''), ('wsgi.py', WSGI(project_name)), ('settings.py', SETTINGS(_res.get('settings'),))],
            'db.sqlite3': '',
        }
            # , ('urls.py', URLS(_res.get('apps')))
            # 'README.md': README(),
            # 'requirements.txt': REQUIREMENTS(),
            # 'static/': [],
            # 'templates/': [], removed at beta
            # 'templates/admin/': [('base_site.html', """{% extends "admin/base_site.html" %}{% load static %}{% block extrahead %}<link rel="stylesheet" href="https://api.clix.dev/static/admin.css" type="text/css" />{% endblock %}""")],

        # generating base file tree
        for k, v in base_file_tree.items():
            if type(v) is str:
                with open(working_dir + k, 'w') as ff:
                    ff.write(base_file_tree.get(k))
            else:
                os.mkdir(working_dir + k)
                for f in v:
                    with open(working_dir + k + f[0], 'w') as ff:
                        ff.write(f[1])
        
        # generate apps
        # removed ('urls.py', APP_URLS(app)), ('models.py', MODELS(app)), ('admin.py', ADMIN(app)), ('apps.py', f"from django.apps import AppConfig\n\n\nclass AppConfig(AppConfig):\n\tname = '{app.get('name')}'"), ('tests.py', 'from django.test import TestCase'), because of beta
        # removed 'migrations/': [('__init__.py', '')] for beta
        for app in _res.get('apps'):
            file_extensions = {
                '': [('__init__.py', ''), ('views.py', VIEWS(app))],
            }
            # TODO can make this much simpler
            for k, v in file_extensions.items():
                working_d = working_dir + 'clix' + '/' + k
                os.mkdir(working_d)
                for file_name, file_content in v:
                    with open(working_d + file_name, 'w') as ff:
                        ff.write(file_content)

        sync(terminal_token, project_token, args)

        return True
    except Exception as e:
        print(e)
        raise Exception('base template error')


# creates clixdev.__path__/apps/clix/*
def sync(terminal_token, project_token, *args):
    _res = requests.post('http://localhost:8000/api/package/sync',
                        data=json.dumps({
                            'terminal_token': terminal_token,
                            'project_token': project_token,
                        })).json()
    
    import clixdev
    if not os.path.exists(clixdev.__path__[0] + '/apps'):
        os.mkdir(clixdev.__path__[0] + '/apps/clix/migrations')
    if not os.path.exists(clixdev.__path__[0] + '/apps/clix'):
        os.mkdir(clixdev.__path__[0] + '/apps/clix/migrations')
    if not os.path.exists(clixdev.__path__[0] + '/apps/clix/migrations'):
        os.mkdir(clixdev.__path__[0] + '/apps/clix/migrations')
    
    f = open(clixdev.__path__[0] + '/apps' + '/__init__.py', 'w')
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps' + '/__init__.py', 777)

    f = open(clixdev.__path__[0] + '/apps/clix' + '/__init__.py', 'w')
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps/clix' + '/__init__.py', 777)
    
    f = open(clixdev.__path__[0] + '/apps/clix/migrations' + '/__init__.py', 'w')
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps/clix/migrations' + '/__init__.py', 777)

    # write urls based on _res -> api.clix.dev
    f = open(clixdev.__path__[0] + '/apps/clix' + '/urls.py', 'w')
    f.write(APP_URLS(_res.get('apps')[0]))
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps/clix' + '/urls.py', 777)

    f = open(clixdev.__path__[0] + '/apps/clix' + '/models.py', 'w')
    f.write(BASE_MODELS(_res.get('apps')[0]))
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps/clix' + '/models.py', 777)
    
    f = open(clixdev.__path__[0] + '/apps/clix' + '/settings.py', 'w')
    f.write(BASE_SETTINGS(_res.get('misc').get('project_name'), _res.get('misc').get('secret_key')))
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps/clix' + '/settings.py', 777)

    f = open(clixdev.__path__[0] + '/apps/clix' + '/apps.py', 'w')
    f.write("""from django.apps import AppConfig\n\nclass AppConfig(AppConfig):\n\tname = 'clixdev.apps.clix'\n""")
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps/clix' + '/apps.py', 777)

    # import clix
    os.chmod('/Users/ramtinmir/Programing/Clix/cli/project_1/clix' + '/views.py', 777)
    f = open(_res.get('misc').get('project_path') + '/clix/views.py', 'r+')
    lines = f.readlines()
    has_def = False
    for row in lines:
        word = 'def X4D20C'
        if row.find(word) == 0:
            has_def = True
    if not has_def:
        f.write(f"""\n@csrf_exempt\ndef X4D20C(request, *args, **kwargs):\n\t# body = json.loads(request.body)\n\n\treturn JsonResponse({{}})\n\n""")
    f.close()

    # not sure about views yet
    f = open(clixdev.__path__[0] + '/apps/clix' + '/validators.py', 'w')
    f.write(json.dumps("""[{"name": "API", "base_url": "api", "endpoints": [{"misc": {"endpoint_id": "ae0937d9-95e4-4ea1-9ff5-76312209e948", "is_draft": false, "token": "rcxxday", "name": "Get all users", "description": "The description", "base_url": "api"}, "request": {"method": "GET", "host": "localhost", "uri": "users/all"}, "headers": {"authorization": true, "body": {"0": ["auth-token", "str"]}}, "params": {"0": ["id", "uuid"]}, "body": {"type": "none", "payload": {}}, "response": {"code": "200", "message": "OK"}}], "models": [{"table_name": "User", "fields": {"0": ["D372D1", "id", "UUIDField", null, null, false, false, false, true, true], "1": ["F8B9D7", "f_name", "CharField", null, null, true, true, true, false, false], "2": ["D0BA20", "l_name", "CharField", null, null, true, true, true, false, false], "3": ["21341C", "created_at", "DateTimeField", null, null, false, false, true, false, false]}}]}]"""))
    f.close()
    os.chmod(clixdev.__path__[0] + '/apps/clix' + '/validators.py', 777)

    return True
