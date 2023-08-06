import os
import json
import shutil
import requests
from pathlib import Path

from .trace import MANAGE, REQUIREMENTS, WSGI, URLS, SETTINGS, VIEWS, MODELS, ADMIN, README


def generate(terminal_token, project_token, *args):
    try:
        res = requests.post('https://api.clix.dev/api/package/sync',
        data=json.dumps({
            'terminal_token': terminal_token,
            'project_token': project_token,
        })).json()

        secret_key = res.get('misc').get('secret_key')
        project_name = res.get('misc').get('project_name')
        working_dir = os.getcwd() + '/' + args[0] + '/' + project_name + '/' if args[0] else os.getcwd() + '/' + project_name + '/'
        
        if os.path.exists(working_dir):
            # sync()
            # return True
            shutil.rmtree(working_dir)
        os.makedirs(working_dir)
        
        base_file_tree = {
            'README.md': README(),
            'manage.py': MANAGE(project_name),
            'requirements.txt': REQUIREMENTS(),
            'db.sqlite3': '',
            'static/': [],
            project_name + '/': [('__init__.py', ''), ('wsgi.py', WSGI(project_name)), ('settings.py', SETTINGS(project_name, res.get('apps'), res.get('settings'), secret_key)), ('urls.py', URLS(res.get('apps')))],
        }
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
        # removed ('urls.py', APP_URLS(app)) because of beta
        for app in res.get('apps'):
            file_extensions = {
                '': [('__init__.py', ''), ('models.py', MODELS(app)), ('admin.py', ADMIN(app)), ('apps.py', f"from django.apps import AppConfig\n\n\nclass AppConfig(AppConfig):\n\tname = '{app.get('name')}'"), ('tests.py', 'from django.test import TestCase'), ('views.py', VIEWS(app))],
                'migrations/': [('__init__.py', '')],
            }
            for k, v in file_extensions.items():
                working_d = working_dir + app.get('name') + '/' + k
                os.mkdir(working_d)
                for file_name, file_content in v:
                    with open(working_d + file_name, 'w') as ff:
                        ff.write(file_content)

                return True
    
        return True
    except Exception as e:
        print(e)
        raise Exception('base template error')


# syncs usr/local/.clix/project_token folder
def sync(terminal_token, project_token, *args):
    res = requests.post('https://api.clix.dev/api/package/sync',
                        data=json.dumps({
                            'terminal_token': terminal_token,
                            'project_token': project_token,
                        })).json()
    
    if not os.path.exists('projects'):
        os.mkdir('projects')
    
    if not os.path.exists('projects/'):
        os.mkdir('projects/')

    f = open('projects/' + '/__init__.py', 'w')
    f.write("")
    f.close()

    # write urls based on res -> api.clix.dev
    f = open('projects/' + '/_urls.py', 'w')
    f.write(APP_URLS(res.get('apps')[0]))
    f.close()

    f = open('projects/' + '/_models.py', 'w')
    f.write(MODELS(res.get('apps')[0]))
    f.close()

    # not sure about views yet
    f = open('projects/' + '/_validators.txt', 'w')
    f.write(json.dumps("""[{"name": "API", "base_url": "api", "endpoints": [{"misc": {"endpoint_id": "ae0937d9-95e4-4ea1-9ff5-76312209e948", "is_draft": false, "token": "rcxxday", "name": "Get all users", "description": "The description", "base_url": "api"}, "request": {"method": "GET", "host": "localhost", "uri": "users/all"}, "headers": {"authorization": true, "body": {"0": ["auth-token", "str"]}}, "params": {"0": ["d", "uuid"]}, "body": {"type": "none", "payload": {}}, "response": {"code": "200", "message": "OK"}}], "models": [{"table_name": "User", "fields": {"0": ["D372D1", "id", "UUIDField", null, null, false, false, false, true, true], "1": ["F8B9D7", "f_name", "CharField", null, null, true, true, true, false, false], "2": ["D0BA20", "l_name", "CharField", null, null, true, true, true, false, false], "3": ["21341C", "created_at", "DateTimeField", null, null, false, false, true, false, false]}}]}]"""))
    f.close()

    # f = open('/usr/local/.clix/projects.txt', 'w')
    # f.write(json.dumps("""[{"name": "API", "base_url": "api", "endpoints": [{"misc": {"endpoint_id": "ae0937d9-95e4-4ea1-9ff5-76312209e948", "is_draft": false, "token": "rcxxday", "name": "Get all users", "description": "The description", "base_url": "api"}, "request": {"method": "GET", "host": "localhost", "uri": "users/all"}, "headers": {"authorization": true, "body": {"0": ["auth-token", "str"]}}, "params": {"0": ["d", "uuid"]}, "body": {"type": "none", "payload": {}}, "response": {"code": "200", "message": "OK"}}], "models": [{"table_name": "User", "fields": {"0": ["D372D1", "id", "UUIDField", null, null, false, false, false, true, true], "1": ["F8B9D7", "f_name", "CharField", null, null, true, true, true, false, false], "2": ["D0BA20", "l_name", "CharField", null, null, true, true, true, false, false], "3": ["21341C", "created_at", "DateTimeField", null, null, false, false, true, false, false]}}]}]"""))
    # f.close()

    return True
