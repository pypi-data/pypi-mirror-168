#!/usr/bin/env python3

import argparse
import copy
import curses
import hashlib
import logging
import math
import os
import re
import signal
import time
from logging.handlers import SocketHandler
from threading import Lock
from typing import Dict, Tuple

import colorama
from sh import bash
from yaml import load

import socket


try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', type=str, default='just-compose.yaml', help='A job definition')
parser.add_argument('--jobs', '-j', type=str, default='+all', metavar='name', required=False, nargs='+',
                    help='What to run. User +job, +tag to include a jobs by tag or a job.'
                         'Use _job, _tag to exclude jobs.'
                         'Use special keyword all to match all jobs')
parser.add_argument("--dry", action='store_true')

pgids = []
stop = False


def signal_handler(sig, frame):
    print("CTRL+C Detected, please wait for all processes to exit...")

    global stop
    stop = True

    for pgid in pgids:
        try:
            os.killpg(pgid, 2)
        except Exception:
            pass


signal.signal(signal.SIGINT, signal_handler)


# Logging Handle
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
result = sock.connect_ex(('127.0.0.1', 19996))
sock.close()

logger_server = result == 0

socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
loggers = {}

def create_logger(level: int = 1, namespace=None):
    log = logging.getLogger(namespace)
    log.setLevel(level)
    log.addHandler(socket_handler)
    return log

# Create root logger
loggers["jcompose"] = create_logger(namespace="jcompose")


class StdoutPrinter:

    def __init__(self, stdscr):
        self.stdsrc = stdscr
        colors = [value for name, value in list(vars(colorama.Fore).items())]
        colors.remove(colorama.Fore.RESET)
        colors.remove(colorama.Fore.BLACK)
        colors.remove(colorama.Fore.LIGHTBLACK_EX)
        colors.remove(colorama.Fore.LIGHTWHITE_EX)
        colors.remove(colorama.Fore.WHITE)

        colorama.init()
        self.colors = colors

        self.logs = {}
        self.assigned_colors = {}

        self.mutex = Lock()

        if "TERM" not in os.environ:
            os.environ["TERM"] = "xterm-256color"

        self.windows = {}

    def prepare(self, compose):

        stdscr = self.stdsrc
        rows, cols = stdscr.getmaxyx()

        rows_per_job = rows // len(compose['services'])
        rows_per_job *= 2

        cols_per_job = cols // 2

        serv_len = len(compose['services'])

        table_columns = 2
        table_rows = math.ceil(serv_len / 2)

        column = 0
        row = 0

        for i, job in enumerate(compose['services']):
            color = self.colors[compose['services'][job]['hash'] % len(self.colors)] if compose is not None else ''
            self.assigned_colors[job] = color
            self.colors.remove(color)

            self.logs[job] = []
            self.windows[job] = curses.newwin(rows_per_job, cols_per_job, row * rows_per_job, column * cols_per_job)
            self.windows[job].border(' ', ' ', '-', ' ', '+', '+', ' ', ' ')
            self.windows[job].addstr(0, 4, f"{job}")
            self.windows[job].refresh()
            stdscr.refresh()

            column += 1

            if column >= table_columns:
                column = 0
                row += 1

    def process_output_paned(self, job, compose, line, err=False):
        self.mutex.acquire()

        if logger_server:
            if job not in loggers:
                loggers[job] = create_logger(namespace=f"jcompose.{job}")
            
            if not err:
                loggers[job].info(line)
            else:
                loggers[job].warn(line)

        if line.endswith('\n'):
            line = line[0:len(line) - 1]

        def escape_ansi(l):
            ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
            return ansi_escape.sub('', l)

        line = escape_ansi(line)

        window = self.windows[job]
        rows, cols = window.getmaxyx()
        rows -= 1
        cols -= 2

        lines = [line[i:i + cols] for i in range(0, len(line), cols)]

        self.logs[job] += lines
        self.logs[job] = self.logs[job][-rows:]

        window.clear()
        self.windows[job].border(' ', ' ', '-', ' ', '+', '+', ' ', ' ')
        self.windows[job].addstr(0, 4, f"{job}")
        for i, line in enumerate(self.logs[job]):
            window.addstr(i + 1, 1, line)

        window.refresh()

        self.mutex.release()

    def process_output(self, job, compose, line, err=False):
        if line.endswith('\n'):
            line = line[0:len(line) - 1]

        if job not in self.assigned_colors:
            color = self.colors[compose['services'][job]['hash'] % len(self.colors)] if compose is not None else ''
            self.assigned_colors[job] = color
            self.colors.remove(color)
        else:
            color = self.assigned_colors[job]

        self.mutex.acquire()
        print(color + job + colorama.Fore.RESET, end=' ')
        print("| " + (colorama.Fore.RED if err else '') + line + colorama.Fore.RESET)
        self.mutex.release()


def run_service(compose, service_name, services, printer):
    definition = compose['services'][service_name]

    stdin = ";\n".join(compose['pre']) + ";\n"

    stdin += f"cd {definition['working_dir']};\n"
    stdin += definition["command"] + ";\n" if definition['command'] else ''
    stdin += ";\n".join(definition["commands"]) + ";\n" if definition['commands'] else ''

    stdin += ";\n".join(compose['post']) + ";\n"

    service = bash(_in=stdin,
                   _out=(lambda j: (lambda line: printer.process_output_paned(j, compose, line, False)))(service_name),
                   _err=(lambda j: (lambda line: printer.process_output_paned(j, compose, line, True)))(service_name),
                   _bg=True,
                   _new_session=False)

    global pgids
    pgids += [service.pgid]
    services += [service]
    return service.pgid


def healthcheck_ok(compose, service_name):
    if "healthcheck" not in compose["services"][service_name]:
        return True

    stdin = ";\n".join(compose['pre']) + ";\n"
    stdin += compose["services"][service_name]["healthcheck"] + ";\n"
    stdin += "echo -n $?;\n"

    code = [-1]

    def set_code(c):
        c = str(c).replace("\n", "")
        try:
            code[0] = int(c)
        except Exception:
            pass

    bash(_in=stdin, _out=lambda line: set_code(line))

    while code[0] == -1:
        time.sleep(0.5)

    return code[0] == 0


def run(stdscr, compose):
    printer = StdoutPrinter(stdscr)
    printer.prepare(compose)

    service_names = []
    services = []
    started_at = {}
    k_pgids = {}
    healthcheck_fails = {}

    for service_name in compose["services"]:
        pgid = run_service(compose, service_name, services, printer)
        started_at[service_name] = time.time()
        k_pgids[service_name] = pgid
        healthcheck_fails[service_name] = 0
        service_names += [service_name]

    while not stop:

        for service_name in compose["services"]:
            if time.time() - started_at[service_name] > 60:

                ok = healthcheck_ok(compose, service_name)

                if ok:
                    healthcheck_fails[service_name] = 0
                else:
                    healthcheck_fails[service_name] += 1
                    printer.process_output_paned(service_name, compose,
                                                 f"=== HEALTH CHECK FAILED === ({healthcheck_fails[service_name]} / 3)",
                                                 err=True)

                if healthcheck_fails[service_name] >= 3:
                    printer.process_output_paned(service_name, compose, f"=== RESTARTING ===", err=True)

                    try:
                        os.killpg(k_pgids[service_name], 9)
                    except Exception:
                        pass

                    time.sleep(1)
                    pgid = run_service(compose, service_name, services, printer)
                    started_at[service_name] = time.time()
                    k_pgids[service_name] = pgid

        c = stdscr.getch()

        if c != -1:

            try:
                n = int(chr(c))
            except:
                continue

            service_name = service_names[n]
            try:
                os.killpg(k_pgids[service_name], 9)
            except Exception:
                pass
            time.sleep(1)

            printer.process_output_paned(service_name, compose, f"=== RESTARTING ===", err=True)
            pgid = run_service(compose, service_name, services, printer)
            started_at[service_name] = time.time()
            k_pgids[service_name] = pgid

        time.sleep(1)

    for service in services:
        service.wait()


def filter_jobs(compose, jobs) -> Tuple[bool, str, Dict]:
    filtered_compose = copy.deepcopy(compose)
    filtered_compose['services'] = {}

    for name in jobs:
        mode = 'remove' if name[0] == '-' or name[0] == '_' else 'append'

        if name[0] == '+' or name[0] == '-' or name[0] == '_':
            name = name[1:]

        if name in compose['services']:

            if mode == 'append':
                filtered_compose['services'][name] = compose['services'][name]
            elif mode == 'remove':
                filtered_compose['services'].pop(name, None)

        else:
            found = False

            for service_n in compose['services']:
                service = compose['services'][service_n]

                if name in service['tags']:
                    if mode == 'append':
                        filtered_compose['services'][service_n] = compose['services'][service_n]
                    elif mode == 'remove':
                        filtered_compose['services'].pop(service_n, None)

                    found = True

            if not found:
                return False, f"Failed to find job / tag {name}", {}

    return True, '', filtered_compose


def validate(compose) -> Tuple[bool, str]:
    compose['pre'] = compose['pre'] if 'pre' in compose else []
    compose['post'] = compose['post'] if 'post' in compose else []
    compose['visible'] = 0

    for job in compose['services']:
        definition = compose['services'][job]

        definition['command'] = definition['command'] if 'command' in definition else ''
        definition['commands'] = definition['commands'] if 'commands' in definition else []

        definition['working_dir'] = definition['working_dir'] if 'working_dir' in definition else '.'

        definition['hash'] = int(hashlib.sha1(job.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        definition['tags'] = definition['tags'] if 'tags' in definition else []
        definition['tags'] += ['all']

        definition['bg'] = definition['bg'] if 'bg' in definition else False

        if not definition['bg']:
            compose['visible'] += 1

    return True, ''


def print_jobs(compose):
    prnt = ""

    for service in compose['services']:
        definition = compose['services'][service]

        prnt += colorama.Style.BRIGHT
        prnt += f"== {service} =="
        prnt += colorama.Style.RESET_ALL + "\n"

        for command in compose['pre']:
            prnt += command + "\n"

        prnt += f"cd {definition['working_dir']}\n"

        if 'command' in definition and definition['command']:
            prnt += (definition['command'] + "\n")

        for command in definition['commands']:
            prnt += (command + "\n")

        for command in compose['post']:
            prnt += (command + "\n")

        prnt += "\n\n"

    return prnt


def main(stdscr, args):
    stdscr.nodelay(True)

    with open(args.file, 'r') as f:
        compose = load(f, Loader=Loader)

    ok, err = validate(compose)

    if not ok:
        return ok, err

    if type(args.jobs) is not list:
        args.jobs = [args.jobs]

    ok, err, compose = filter_jobs(compose, args.jobs)

    if not ok:
        return ok, err

    if args.dry:
        return True, print_jobs(compose)

    run(stdscr, compose)

    return True, ""


def entrypoint():
    args = parser.parse_args()
    ok, err = curses.wrapper(main, args)

    print(f"Finished with ok status: {ok}")
    print(err)


if __name__ == '__main__':
    entrypoint()
