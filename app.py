#!/usr/bin/env python

#Pyjsdl - Copyright (C) 2013
#Released under the MIT License

"""
Pyjsdl App

Script launches HTML app on desktop using Webkit.
To use, copy script and run once to create app.ini.
Edit app.ini with the necessary information:
app_name, app_size, server_ip, server_port.

Tested under Linux, required python-webkit installation.
On other OS, additional installation steps may be required.
"""


import webkit, gtk
import SocketServer
import SimpleHTTPServer
import requests
import multiprocessing
import os.path
import sys


class Server(SocketServer.TCPServer):

    allow_reuse_address = True

    def __init__(self, port):
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        SocketServer.TCPServer.__init__(self, ("", port), Handler)
        self.process = multiprocessing.Process(target=self.serve_forever)

    def initiate(self):
        self.process.daemon = True
        self.process.start()

    def terminate(self):
        self.process.terminate()


class App(object):

    def __init__(self, config):
        self.config = config
        self.window = gtk.Window()
        w, h = self.config.app_size
        self.window.resize(w,h)
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.scroller = gtk.ScrolledWindow()
        self.window.add(self.scroller)
        self.web = None
        self.server = None

    def webview(self):
        self.web = webkit.WebView()
        url = 'http://%s:%d/%s' % (self.config.server_ip, self.config.server_port, self.config.app_name)
        self.web.open(url)
        self.scroller.add(self.web)
        self.window.show_all()
        gtk.main()

    def server_enable(self):
        if not self.server:
            self.server = Server(self.config.server_port)
            self.server.initiate()

    def server_disable(self):
        if self.server:
            self.server.terminate()


class Config(object):

    def __init__(self):
        if os.path.exists('app.ini'):
            cfg_setting = self.read_ini()
        else:
            self.create_ini()
            print('Enter configuration info in app.ini.')
            sys.exit()
        for setting in cfg_setting:
            if setting == 'app_name':
                self.app_name = cfg_setting['app_name'].strip()
            if setting == 'app_size':
                size = cfg_setting['app_size'].strip().split('x')
                self.app_size = (int(size[0].strip()),int(size[1].strip()))
            if setting == 'server_ip':
                self.server_ip = cfg_setting['server_ip'].strip()
            if setting == 'server_port':
                self.server_port = int(cfg_setting['server_port'].strip())

    def create_ini(self):
        f = open('app.ini', 'w')
        f.write('#App Configuration\n\n')
        f.write('app_name output/app.html\n\n')
        f.write('app_size 500x500\n\n')
        f.write('server_ip localhost\n\n')
        f.write('server_port 8000\n\n')
        f.close()

    def read_ini(self):
        config_file = open('app.ini')
        cfg_setting = [line.strip().split(' ',1) for line in config_file if line[:1].isalpha()]
        cfg_setting = dict(cfg_setting)
        config_file.close()
        return cfg_setting


def main():
    config = Config()
    app = App(config)
    app.server_enable()
    app.webview()
    app.server_disable()


if __name__ == '__main__':
    main()

