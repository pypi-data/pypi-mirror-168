#!/usr/bin/env python3

# Copyright 2022 Louis Paternault
#
# This file is part of Chval.
#
# Chval is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chval is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with Chval.  If not, see <http://www.gnu.org/licenses/>.

"""Parallel `getmail` calls, with progress bars"""

import argparse
import io
import pathlib
import re
import subprocess
import sys
import threading
import time
import unicodedata

from rich.console import Console
from rich.progress import Progress
from rich.text import Text

console = Console()

VERSION = "1.0.0"
NAME = "chval"
CONFIG = pathlib.Path("~/.config/getmail").expanduser()
PREFIX = "getmailrc-"
GETMAIL = ["getmail", "--rcfile"]
DELAY = 1

# Set DEBUG to True to log a lot of things
DEBUG = False

RE_MESSAGE = re.compile(r"msg (?P<sub>\d+)/(?P<total>\d+) \(\d+ bytes\) delivered")
RE_END = re.compile(
    r"(?P<messages>\d+) messages \(\d+ bytes\) retrieved, (\d+) skipped"
)


def parse_getmail(task, process, progress, completion):
    """Parse the output of `getmail`.

    :param rich.TaskID task: ID of the corresponding :class:`rich.progress.Progress`.
    :param subprocess.Popen process: Process running `getmail`.
    :param rich.progress.Progress progress: Shared progress bar.
    :param list completion: Shared list to store (sub, total):
        `sub` messages have been fetched out of `total` messages.
        This function (run in a thread) is expected to set the values of this list,
        so that the calling thread can access the results.
        A list is not thread safe, but nobody will write this variable but this function,
        and nobody will read this variable until after this function has completed.
    """
    start = None
    while True:
        # Unbuffer standard output
        line = process.stdout.readline()
        if not line:
            break

        if DEBUG:
            console.log(f"[green]{task}[/green] {line.strip()}")
        if match := RE_MESSAGE.search(line):
            sub = int(match.group("sub"))
            total = int(match.group("total"))
            if start is None:
                progress.start_task(task)
                start = sub
            progress.update(task, total=total - start + 1, completed=sub - start + 1)
            completion[0] = sub - start + 1
            completion[1] = total - start + 1
        elif match := RE_END.search(line):
            pass

    if process.returncode:
        # `getmail` exited with an error
        progress.stop_task(task)
    else:
        if start is None:
            # `getmail` exited with no error, but not a single message has been fetched
            # Trick progress into showing 100% completion
            progress.start_task(task)
            progress.update(task, total=1, completed=1)


def getmail(keywords):
    """Run getmail calls, and display a progress bar.

    :param List[str] keywords: List of getmailrc keyword
        (a keyword `foo` references a getmail configuration file CONFIG/getmailrc-foo).
    """
    calls = {}

    with Progress() as progress:
        if DEBUG:
            progress.stop()
        for rcfile in keywords:
            task = progress.add_task(rcfile, start=False, total=0)

            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                # Uncomment to debug
                # [str(pathlib.Path(__file__).parent / "bin" / "fake-getmail.py"), rcfile],
                GETMAIL + [PREFIX + rcfile],
                text=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            time.sleep(DELAY)

            completion = [0, 0]
            thread = threading.Thread(
                target=parse_getmail,
                kwargs={
                    "task": task,
                    "process": process,
                    "progress": progress,
                    "completion": completion,
                },
            )
            thread.start()

            calls[rcfile] = {
                "process": process,
                "thread": thread,
                "stderr": io.TextIOWrapper(process.stderr),
                "task": task,
                "progress": completion,
            }

        for call in calls.values():
            call["process"].wait()
            call["thread"].join()

    # Display errors
    # and replace wrapper to error to actual error message
    for getmailrc, call in calls.items():
        call["stderr"] = "".join(call["stderr"].buffer.readlines()).strip()
        if call["process"].returncode:
            console.rule(Text(f"\u26A0\uFE0F {getmailrc}"))
            console.print(call["stderr"])

    # Display summary
    console.rule(Text(f"""{unicodedata.lookup("PARTY POPPER")} Summary"""))
    for getmailrc, call in calls.items():
        if call["process"].returncode:
            lastline = call["stderr"].split("\n")[-1]
            console.print(
                # pylint: disable=line-too-long
                f"""\u274C [red][{call["progress"][0]}/{call["progress"][1]}] {getmailrc}[/red] {lastline}"""
            )
        else:
            console.print(
                # pylint: disable=line-too-long
                f"""\u2714\uFE0F [green][{call["progress"][0]}/{call["progress"][1]}] {getmailrc}[/green]"""
            )

    if any(call["process"].returncode for call in calls.values()):
        return 1
    return 0


def _type_choice(available):
    def wrapped(txt):
        if txt in available:
            return txt
        raise argparse.ArgumentTypeError(
            f""""{txt}" must be one of : {", ".join(available)}."""
        )

    return wrapped


def main():
    """Main function."""
    # Gather list of configuration files
    available = set(
        filename.name[len(PREFIX) :]
        for filename in CONFIG.glob(f"{PREFIX}*")
        if not str(filename).endswith("~")
    )

    # Parse command line
    parser = argparse.ArgumentParser(
        description="Parallel `getmail` calls, with progress bars",
        prog="chval",
        epilog=f"All getmailrc files must be in the default directory {CONFIG}.",
    )
    parser.add_argument(
        "--version",
        help="Show version and exit.",
        action="version",
        version=f"{NAME} {VERSION}",
    )
    parser.add_argument(
        "GETMAILRC",
        nargs="*",
        # Workaround to bug https://bugs.python.org/issue27227
        # "type=str, choices=available" would have been better
        type=_type_choice(available),
        help=(
            "List of getmailrc files to process. "
            f"""Calling "chval foo" will process configuration file "{CONFIG/"getmailrc-foo"}". """
            "Leave blank to process all getmailrc files."
        ),
    )
    options = parser.parse_args()
    if not options.GETMAILRC:
        options.GETMAILRC = list(sorted(available))

    # Call getmail
    return getmail(options.GETMAILRC)


if __name__ == "__main__":
    sys.exit(main())
