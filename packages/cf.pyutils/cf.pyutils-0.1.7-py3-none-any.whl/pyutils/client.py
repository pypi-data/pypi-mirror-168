#!/usr/bin/env python3
import os
import sys
import time
import psutil
import select
import logging
import asyncio
import subprocess


from scp import SCPClient
from paramiko import SSHClient, AutoAddPolicy
from websocket_server import WebsocketServer
from utils import main, parse_args, register, has_hidden
from http.server import HTTPServer, CGIHTTPRequestHandler
from threading import Thread

import pyinotify
import pychrome

SITE=os.path.basename(os.getcwd())
USER="p1810569"
PATH="matthieu.jacquemet"
REMOTE="lifasr2.univ-lyon1.fr"
IGNORE=["grille.txt", "score.txt", "jeu-2048.log"]

@main(**parse_args(sys.argv))
class ClientAgent:

    def __init__(self, path, command=None, *args, **kwargs):
        for name in dir(self):
            method = getattr(self, name)
            id = getattr(method, "_id", None)
            if id == command:
                method(**kwargs)
    
    def _handler(self, event):
        if (os.path.islink(event.pathname) or
            has_hidden(event.pathname) or 
            os.path.basename(event.pathname) in IGNORE):
            return
        # if hasattr(self, "scp"):
        #     print(os.path.relpath(event.pathname))
        #     self.scp.put(os.path.relpath(event.pathname),
        #         SITE, os.path.isdir(event.pathname))
        #     self._reload_page("remote")
        #     print("no")
        # else:
        if os.path.splitext(event.pathname)[-1] == ".css":
            message = "refreshcss"
        else:
            message = "reload"
        self.server.send_message_to_all(message)
    
    @register("log")
    def _diplay_logs(self, mode="local", **kwargs):
        if mode == "remote":
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(REMOTE, username=USER)
            _, stdout, _ = client.exec_command(f"tail -f {SITE}/{SITE}.log")
            while not stdout.channel.exit_status_ready():
                data = stdout.read(1)
                sys.stdout.write(data.decode("utf-8"))
                sys.stdout.flush()
        elif mode == "local":
            subprocess.run(("tail", "-f", f"{SITE}.log"))

    @register("watch")
    def _start_watcher(self, **kwargs):

        wm = pyinotify.WatchManager()
        wm.add_watch(".", pyinotify.IN_CLOSE_WRITE, rec=True)
        handler = pyinotify.ProcessEvent()
        handler.process_IN_CLOSE_WRITE = self._handler
        notifier = pyinotify.ThreadedNotifier(wm, handler)
        notifier.start()

        self.server = WebsocketServer(5600, host='localhost')
        self.server.run_forever()
        # CGIHTTPRequestHandler.cgi_directories = ["/"]
        # httpserver = HTTPServer(("", 80), CGIHTTPRequestHandler)
        # httpserver.handle_request()
        # httpserver.serve_forever()
    
        # if mode == "remote":
        #     client = SSHClient()
        #     client.set_missing_host_key_policy(AutoAddPolicy())
        #     client.connect(REMOTE, username=USER)
        #     self.scp = SCPClient(client.get_transport())
        # elif mode == "local":
        # else:
            # exit(1)
    
    @register("commit")
    def _commit(self, **_):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(REMOTE, username=USER)

        with SCPClient(client.get_transport()) as scp:
            for entity in os.listdir():
                if entity.startswith(".") or os.path.islink(entity):
                    continue
                scp.put(entity, SITE, os.path.isdir(entity))
    
    @register("test")
    def _reload_page(self, mode="local", **_):
        if mode == "remote":
            url = f"https://{REMOTE}/{PATH}/{SITE}"
        elif mode == "local":
            url = f"http://{SITE}.localhost"
        else:
            exit(1)
        browser = pychrome.Browser()
        try:
            _ = browser.version()
        except: pass
            #self._run_brower(url)
        else:
            for tab in browser.list_tab():
                tab_url = tab._kwargs.get("url")
                if tab_url.startswith(url):
                    tab.start()
                    tab.Page.reload(ignorecache=True)
                    browser.activate_tab(tab)
                    break
            else: browser.new_tab(url)
    
    def _run_brower(self, url=""):
        for proc in psutil.process_iter():
            if proc.name().startswith("chromium-browser"):
                proc.kill()
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect("localhost")
        
        client.exec_command(
            f"DISPLAY=:0 nohup chromium-browser \
            --remote-debugging-port=9222 {url} &>/dev/null &")
        client.close()