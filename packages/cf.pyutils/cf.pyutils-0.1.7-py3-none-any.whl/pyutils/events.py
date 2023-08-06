import os
import inspect
import inotify
import threading

from inotify.constants import IN_ALL_EVENTS
from inotify.adapters import Inotify, InotifyTree

from . import thread

class FileSystemEvent():
    CREATED     = 1
    DELETED     = 1<<1
    MODIFIED    = 1<<2
    MOVED       = 1<<3
    ANY         = (1<<4)-1


class ThreadedNotifier(threading.Thread):

    def __init__(self, handler, mask=IN_ALL_EVENTS,
            recursive=False, path=[]):
        
        self._handler = handler
        self._stop_event = threading.Event()

        assert not (recursive and not path)

        if recursive:
            self.watcher = InotifyTree(path, mask)
        else:
            self.watcher = Inotify(path)
        
        super().__init__()

    def start(self):

        if not self.is_alive():
            self._stop_event.clear()
            super().start()
        
    def stop(self):

        if self.is_alive():
            self._stop_event.set()

    def run(self):

        for event in self.watcher.event_gen(yield_nones=False):
            if self._stop_event.is_set():
                break
            heander, *_ = event
            self._handler(event)

def on_filesystem_event(path, mask=IN_ALL_EVENTS, recursive=False):

    def factory(handler):
        register_event_handler(handler, path, mask, recursive)
        return handle
    return factory

def register_event_handler(handler, path, mask=IN_ALL_EVENTS, recursive=False):
    
    watcher = ThreadedNotifier(handler, mask, recursive, path)
    watcher.start()

    return watcher

#################### OLD ONE #######################

def on_any(*paths, recursive=False):
    def factory(handle):
        return filesystemevent(
            *paths,
            handle=handle,
            recursive=recursive
        )
    return factory

def on_modified(*paths, recursive=False):
    def factory(handle):
        return filesystemevent(
            *paths, 
            handle=handle,
            event_type=FileSystemEvent.MODIFIED,
            recursive=recursive
        )
    return factory

def on_created(*paths, recursive=False):
    def factory(handle):
        return filesystemevent(
            *paths,
            handle=handle,
            event_type=FileSystemEvent.CREATED,
            recursive=recursive
        )
    return factory

def on_moved(*paths, recursive=False):
    def factory(handle):
        return filesystemevent(
            *paths,
            handle=handle,
            event_type=FileSystemEvent.MOVED,
            recursive=recursive
        )
    return factory

def on_deleted(*paths, recursive=False):
    def factory(handle):
        return filesystemevent(
            *paths,
            handle=handle,
            event_type=FileSystemEvent.DELETED,
            recursive=recursive
        )
    return factory

def filesystemevent(*paths,
                    handle,
                    event_type=FileSystemEvent.ANY,
                    recursive=False):
    watchers = list()
    from watchdog.observers import Observer
    from watchdog import events
    
    for path in paths:
        fpath = path
        callback = handle
        observer = Observer()

        class _file_wrapper:
            def __init__(self, path):
                self.path = path
            def __call__(self, event):
                if event.src_path == self.path:
                    handle(event)
        
        if os.path.isfile(path):
            fpath = os.path.dirname(path)
            if callable(handle):
                callback = _file_wrapper(path)

        if (inspect.isclass(handle) and
            issubclass(handle, events.FileSystemEventHandler)):
            handler = handle()
        else:
            handler = events.FileSystemEventHandler()
            cases =("on_created","on_deleted","on_modified","on_moved")
            if event_type == FileSystemEvent.ANY:
                handler.on_any_event = callback
            else:
                for i,member in enumerate(cases):
                    if (event_type >> i) & 0x1:
                        setattr(handler, member, callback)
        
        observer.schedule(handler, fpath, recursive)
        observer.start()
        watchers.append(observer)

    return watchers