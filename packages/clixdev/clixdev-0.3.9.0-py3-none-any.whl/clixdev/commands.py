import os
import json
import shutil
import requests
from .trace import MANAGE, WSGI, SETTINGS, BASE_SETTINGS, VIEWS, BASE_MODELS, APP_URLS, DEF


class Commands:
    def __init__(self, terminal_token, project_token, path, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.user_dir = path
        self.project_token = project_token
        self.terminal_token = terminal_token
        self.messages = []
    

    # returns True if project already exists
    def generate(self):
        try:
            _dir = os.getcwd()
            _res = requests.post('https://clix.dev/api/package/generate',
            data=json.dumps({
                'terminal_token': self.terminal_token,
                'project_token': self.project_token,
                'local_path': _dir + '/' + self.user_dir + '/' if self.user_dir else _dir + '/',
            })).json()

            if _res == False:
                print('Please check your tokens and try again.\n')
                return False

            if _res.get('misc').get('project_path'):
                if _res.get('misc').get('project_name') != _res.get('misc').get('last_generated_name'):
                    if os.path.exists(_res.get('misc').get('project_path') + _res.get('misc').get('last_generated_name') + "/"):
                        # rename project
                        os.chdir(_res.get('misc').get('project_path'))
                        os.rename(_res.get('misc').get('last_generated_name'), _res.get('misc').get('project_name'))
                        print('Warning: Project renamed. Please sync your project.')
                        return True
                elif _res.get('misc').get('project_name') == _res.get('misc').get('last_generated_name'):
                    if os.path.exists(_res.get('misc').get('project_path') + _res.get('misc').get('project_name') + "/"):
                        print('\nWarning: Project already exists. Please sync your project instead.\n')
                        return True
            
            print('\nGeneration started.')

            project_name = _res.get('misc').get('project_name')
            working_dir = _dir + '/' + self.user_dir + '/' + project_name + '/' if self.user_dir else _dir + '/' + project_name + '/'
            # TODO some logic needed here
            if os.path.exists(working_dir):
                shutil.rmtree(working_dir)
            os.makedirs(working_dir)
            
            base_file_tree = {
                'manage.py': MANAGE(project_name),
                project_name + '/': [('__init__.py', ''), ('wsgi.py', WSGI(project_name)), ('settings.py', SETTINGS(_res.get('settings'),))],
                'db.sqlite3': '',
            }
                # ('urls.py', URLS(_res.get('apps')))
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

            self.sync()

            print('Generation successful.\n')
            return True
        except Exception as e:
            print(e)
            # raise Exception('base template error')
            print('Something went wrong; please try again.\n')
            return False


    # sync doesn't remove a function if you remove it from the dashboard
    # sync does remove the endpoint url tho
    def sync(self):
        try:
            _res = requests.post('https://clix.dev/api/package/sync',
                                data=json.dumps({
                                    'terminal_token': self.terminal_token,
                                    'project_token': self.project_token,
                                })).json()
            
            if _res == False:
                print('Please check your tokens and try again.\n')
                return False                
            
            _project_dir = _res.get('misc').get('last_generated_name')

            if _res.get('misc').get('project_path'):
                if _res.get('misc').get('project_name') != _project_dir:
                    if os.path.exists(_res.get('misc').get('project_path') + _project_dir + "/"):
                        # rename project
                        os.chdir(_res.get('misc').get('project_path'))
                        os.rename(_project_dir, _res.get('misc').get('project_name'))
                        print('Warning: Project renamed.')
                        _project_dir = _res.get('misc').get('project_name')
                        # SYNC
                    elif os.path.exists(_res.get('misc').get('project_path') + _res.get('misc').get('project_name') + "/"):
                        _project_dir = _res.get('misc').get('project_name')
                        # SYNC
                    else:
                        print('Error: Project cannot be found. Please generate your project first.')
                        return False
                elif _res.get('misc').get('project_name') == _project_dir:
                    if not os.path.exists(_res.get('misc').get('project_path') + _res.get('misc').get('project_name') + "/"):
                        print("no project")
                        return False
                    # else:
                        # SYNC
            else:
                print('Error: Project cannot be found. Please generate your project first.')
                return False
            
            print('Sync started.')
            
            import clixdev
            if not os.path.exists(clixdev.__path__[0] + '/apps'):
                os.makedirs(clixdev.__path__[0] + '/apps/clix/migrations', 0o777)
            if not os.path.exists(clixdev.__path__[0] + '/apps/clix'):
                os.makedirs(clixdev.__path__[0] + '/apps/clix/migrations', 0o777)
            if not os.path.exists(clixdev.__path__[0] + '/apps/clix/migrations'):
                os.makedirs(clixdev.__path__[0] + '/apps/clix/migrations', 0o777)
            
            f = open(clixdev.__path__[0] + '/apps' + '/__init__.py', 'w')
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps' + '/__init__.py', 0o777)

            f = open(clixdev.__path__[0] + '/apps/clix' + '/__init__.py', 'w')
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps/clix' + '/__init__.py', 0o777)
            
            f = open(clixdev.__path__[0] + '/apps/clix/migrations' + '/__init__.py', 'w')
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps/clix/migrations' + '/__init__.py', 0o777)
            # urls
            f = open(clixdev.__path__[0] + '/apps/clix' + '/urls.py', 'w')
            f.write(APP_URLS(_res.get('apps')[0]))
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps/clix' + '/urls.py', 0o777)

            # models
            f = open(clixdev.__path__[0] + '/apps/clix' + '/models.py', 'w')
            f.write(BASE_MODELS(_res.get('apps')[0]))
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps/clix' + '/models.py', 0o777)
            
            # settings
            f = open(clixdev.__path__[0] + '/apps/clix' + '/settings.py', 'w')
            f.write(BASE_SETTINGS(_res.get('misc').get('project_name'), _res.get('misc').get('secret_key')))
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps/clix' + '/settings.py', 0o777)

            # apps
            f = open(clixdev.__path__[0] + '/apps/clix' + '/apps.py', 'w')
            f.write("""from django.apps import AppConfig\n\nclass AppConfig(AppConfig):\n\tname = 'clixdev.apps.clix'\n""")
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps/clix' + '/apps.py', 0o777)

            # TODO
            if os.path.exists(_res.get('misc').get('project_path') + _project_dir + "/" + 'clix/views.py'):
                f = open(_res.get('misc').get('project_path') + _project_dir + "/" + 'clix/views.py', 'r+')
                content = f.read()
                missing_def = []
                for endpoint in _res.get('apps')[0].get('endpoints'):
                    if 'def ' + endpoint.get('misc').get('token') not in content:
                        missing_def.append(endpoint)
                
                for md in missing_def:
                    f.write(DEF(md))
                f.close()
            else:
                print('Error: Views cannot be found.')
                return False
            
            f = open(clixdev.__path__[0] + '/apps/clix/validations.json', 'w')
            f.write(json.dumps(_res.get('validations')))
            f.close()
            os.chmod(clixdev.__path__[0] + '/apps/clix' + '/validations.json', 0o777)

            print('Sync successful.')
            return True
        except Exception as e:
            print(e)
            # raise Exception('base template error')
            print('Something went wrong; please try again.\n')
            return False


    def docs(self):
        try:
            _res = requests.post('https://clix.dev/api/package/docs',
                                data=json.dumps({
                                    'terminal_token': self.terminal_token,
                                    'project_token': self.project_token,
                                })).json()

            if _res == False:
                print('Please check your tokens and try again.\n')
                return False
            
            print('Docs started.')
            
            if _res.get('misc').get('project_path') and os.path.exists(_res.get('misc').get('project_path')):
                f = open(_res.get('misc').get('project_path') + '/docs.json', 'w')
                f.write(json.dumps(_res.get('docs'), indent=4))
                f.close()
                os.chmod(_res.get('misc').get('project_path') + '/docs.json', 0o777)
            else:
                print('Error: Project cannot be found. Please generate your project first.')
                return False
            
            return True
        except Exception as e:
            print(e)
            return False

