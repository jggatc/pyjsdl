#!/usr/bin/env python

#Pyjsdl - Copyright (C) 2013
#Released under the MIT License

"""
Pyjsdl App

Script launches HTML app on desktop using Gtk/Webkit.
Copy app script to the application root and optionally rename.
Run the script once to create an ini file and edit to configure.

Tested under Linux Gnome desktop with the installed packages:
gir1.2-webkit2-4.0, python-gi (py2), python3-gi (py3).
On other OS, additional installation steps may be required.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
import multiprocessing
import os.path
import sys

if sys.version_info.major >= 3:
    from socketserver import TCPServer
    from http.server import SimpleHTTPRequestHandler
else:
    from SocketServer import TCPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class Server(TCPServer):

    allow_reuse_address = True

    def __init__(self, port):
        TCPServer.__init__(self, ("", port), SimpleHTTPRequestHandler)
        self.process = multiprocessing.Process(target=self.serve_forever)

    def initiate(self):
        self.process.daemon = True
        self.process.start()

    def terminate(self):
        self.process.terminate()


class QuietServer(Server):
    def __init__(self, port):
        TCPServer.__init__(self, ("", port), QuietHandler)
        self.process = multiprocessing.Process(target=self.serve_forever)


class QuietHandler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass


class App(object):

    def __init__(self, config):
        self.config = config
        self.window = Gtk.Window()
        self.window.resize(self.config.width+16,self.config.height+16)
        if self.config.app_name is not None:
            self.window.set_title(self.config.app_name)
        else:
            title = self.config.app_uri.split('/')[-1].split('.')[0]
            self.window.set_title(title.capitalize())
        self.window.connect('destroy', Gtk.main_quit)
        self.web = None
        self.server = None

    def webview_setup(self):
        self.web = WebKit2.WebView()
        uri = 'http://%s:%d/%s' % (self.config.server_ip,
                                   self.config.server_port,
                                   self.config.app_uri)
        self.web.load_uri(uri)
        self.window.add(self.web)

    def webview(self):
        self.webview_setup()
        self.window.show_all()
        Gtk.main()

    def server_enable(self):
        if not self.server:
            if self.config.server_log:
                self.server = Server(self.config.server_port)
            else:
                self.server = QuietServer(self.config.server_port)
            self.server.initiate()

    def server_disable(self):
        if self.server:
            self.server.terminate()


class Config(object):

    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 8000
        self.server_log = False
        self.app_uri = None
        self.app_name = None
        self.width = 500
        self.height = 500
        self.config_name = sys.argv[0].split('.')[0]+'.ini'
        if os.path.exists(self.config_name):
            cfg_setting = self.read_ini()
        else:
            self.create_ini()
            print('Enter configuration info in %s.' % self.config_name)
            sys.exit()
        for setting in cfg_setting:
            if setting == 'app_uri':
                self.app_uri = cfg_setting['app_uri'].strip()
            if setting == 'app_name':
                self.app_name = cfg_setting['app_name'].strip()
            if setting == 'window_width':
                self.width = int(cfg_setting['window_width'].strip())
            if setting == 'window_height':
                self.height = int(cfg_setting['window_height'].strip())
            if setting == 'server_ip':
                self.server_ip = cfg_setting['server_ip'].strip()
            if setting == 'server_port':
                self.server_port = int(cfg_setting['server_port'].strip())
            if setting == 'server_log':
                server_log = cfg_setting['server_log'].strip().lower()
                self.server_log = {'true':True, 'false':False}[server_log]

    def create_ini(self):
        f = open(self.config_name, 'w')
        f.write('#App Configuration\n\n')
        f.write('app_uri output/app.html\n\n')
        f.write('app_name App\n\n')
        f.write('window_width 500\n\n')
        f.write('window_height 500\n\n')
        f.write('server_ip localhost\n\n')
        f.write('server_port 8000\n\n')
        f.write('server_log false\n\n')
        f.close()

    def read_ini(self):
        cfg_file = open(self.config_name)
        cfg = [ln.strip().split(' ',1) for ln in cfg_file if ln[:1].isalpha()]
        cfg = dict(cfg)
        cfg_file.close()
        return cfg


def main():
    config = Config()
    app = App(config)
    app.server_enable()
    app.webview()
    app.server_disable()


if __name__ == '__main__':
    main()

