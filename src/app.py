import flask
import functools
import click
import os
import glob
import subprocess
import dateutil.parser

from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader
from datetime import datetime
from pytz import timezone

# import utils.database as database
# import utils.logger as logger
# import utils.request as request
# import utils.response as response
# import utils.session as session

class App(Flask):

    def __init__(self):

        super().__init__(__name__, static_folder='assets')

        self.directory = os.path.dirname(os.path.abspath(__file__))
        click.secho(' * Bootstrapping application from directory {0}'.format(self.directory), fg='green')

        default_config_file = os.path.join(self.directory, 'app.config')
        click.secho(' * Loading default config file {0}'.format(default_config_file))
        self.config.from_pyfile(default_config_file)

        for alternative_config_file in glob.glob(os.path.join(self.directory, 'app.*.config')):

            click.secho(' * Loading alternative config file {0}'.format(alternative_config_file))
            self.config.from_pyfile(alternative_config_file)

        self.timezone = timezone(self.config['TIMEZONE'])

    def setup(self):

        macros_path = os.path.join(self.directory, 'macros')
        macros_paths = [ macros_path, *glob.glob(os.path.join(macros_path, '*' + os.path.sep)) ]

        template_path = os.path.join(self.directory, 'templates')
        template_paths = [ template_path, *glob.glob(os.path.join(template_path, '*' + os.path.sep)) ]

        click.secho(' * Registering macros {0}'.format(', '.join(macros_paths)))
        click.secho(' * Registering templates {0}'.format(', '.join(template_paths)))

        jinja_loaders = [ self.jinja_loader ]
        jinja_loaders.append(FileSystemLoader(macros_paths))
        jinja_loaders.append(FileSystemLoader(template_paths))

        self.jinja_loader = ChoiceLoader(jinja_loaders)

        # for pathname in ('LOGS', 'TEMP', 'TRASH', 'BACKUP', 'FLYER'):

        #     if not os.path.isabs(self.config[pathname]):

        #         self.config[pathname] = os.path.join(self.directory, self.config[pathname])

        #     if not os.path.exists(self.config[pathname]):

        #         click.secho(' * Creating {0} directory {1}'.format(pathname, self.config[pathname]))

        #         os.makedirs(self.config[pathname])

        # logger.setup(self)
        # database.setup(self)

app = App()
