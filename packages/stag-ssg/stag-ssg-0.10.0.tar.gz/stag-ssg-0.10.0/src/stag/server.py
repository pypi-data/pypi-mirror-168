# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2021 Michał Góral.

from typing import Set, Dict, List

import os
import sys
import glob
import queue
import multiprocessing as mp
import traceback
from contextlib import contextmanager
from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging

from stag.utils import chdir

log = logging.getLogger(__name__)


class Process(mp.Process):
    def __init__(self, *a, **kw):
        self._queue = mp.Queue()
        super().__init__(*a, **kw)

    def run(self):
        try:
            super().run()
        except Exception as e:
            tb = traceback.format_exc()
            self._queue.put((e, tb))

    @property
    def exception(self):
        try:
            e = self._queue.get_nowait()
            return e
        except queue.Empty:
            return None


# This function is intended to be run in a separate process
def run_http_server(directory, port):
    with chdir(directory):
        log.info(f"Running simple HTTP server on http://localhost:{port}.")
        log.info(f"Serving files from '{directory}'.")
        server_address = ("", port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()


def get_timestamps(watch_patterns):
    stamps = {}
    for pat in watch_patterns:
        for path in glob.iglob(pat, recursive=True):
            mtime = os.stat(path).st_mtime
            stamps[path] = mtime
    return stamps


@contextmanager
def run_server(serve_directory, port):
    server = Process(target=run_http_server, args=(serve_directory, port))
    try:
        server.start()
        yield server
    finally:
        log.info("Terminating HTTP server.")
        server.terminate()
        server.join()
        server.close()


def get_differing_files(
    stamps: Dict[str, float], newstamps: Dict[str, float]
) -> Set[str]:
    stamps_set = set(stamps.items())
    newstamps_set = set(newstamps.items())
    diff = set.symmetric_difference(stamps_set, newstamps_set)
    return set(k for k, _ in diff)


def serve_until_changed(
    serve_directory: str, port: int, watch_patterns: List[str]
) -> set[str]:
    poll_delay = 1

    stamps = get_timestamps(watch_patterns)
    fl = len(stamps)
    log.info(f"Watching {fl} files.")

    with run_server(serve_directory, port) as server:
        while True:
            newstamps = get_timestamps(watch_patterns)
            diff = get_differing_files(stamps, newstamps)
            if diff:
                return diff

            server.join(poll_delay)

            e = server.exception
            if e:
                raise e[0]

            if server.exitcode is not None:
                return set()
