#!/usr/bin/python3
# coding: utf-8

"""publish files on the internet"""

# This is a (partial) rewrite of weasel's "publish" program. See the
# `parse_args` function for details on the behavior changes and
# variations.

# Copyright (C) 2020 Antoine Beaupré <anarcat@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import argparse
import atexit
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import logging
import os.path
from pathlib import Path
import secrets  # python 3.6
import shutil
import subprocess
import sys
import tempfile
from typing import Optional, Tuple, Type
from urllib.parse import quote
import yaml

try:
    from shlex import join as shlex_join
except ImportError:
    import shlex

    # copied almost verbatim from python 3.8
    #
    # this triggers and error in mypy:
    #
    # error: All conditional function variants must have identical signatures  [misc]
    #
    # couldn't trace it, so i silence it. original version has no type
    # hints at all, and is nearly identical.
    def shlex_join(split_command):  # type: ignore[misc]
        return " ".join(shlex.quote(arg) for arg in split_command)


# we need GTK's event loop (or, more precisely, its clipboard support)
# to hold on to the clipboard long enough for it to work, but fallback
# on xclip if GTK is unavailable.
try:
    import gi  # type: ignore

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gdk, GdkPixbuf  # type: ignore
except ImportError:
    gi = None

__epilog__ = """ This program will upload the provided files on the internet and
notify the user when completed. The resulting URL will also be copied
to the clipboard. Preprocessors can do fancy things before (only
supports building an image gallery with sigal for now)."""


class LoggingAction(argparse.Action):
    """change log level on the fly

    The logging system should be initialized befure this, using
    `basicConfig`.
    """

    def __init__(self, *args, **kwargs):
        """setup the action parameters

        This enforces a selection of logging levels. It also checks if
        const is provided, in which case we assume it's an argument
        like `--verbose` or `--debug` without an argument.
        """
        kwargs["choices"] = logging._nameToLevel.keys()
        if "const" in kwargs:
            kwargs["nargs"] = 0
        super().__init__(*args, **kwargs)

    def __call__(self, parser, ns, values, option):
        """if const was specified it means argument-less parameters"""
        if self.const:
            logging.getLogger("").setLevel(self.const)
        else:
            logging.getLogger("").setLevel(values)


class ConfigAction(argparse._StoreAction):
    """add configuration file to current defaults.

    a *list* of default config files can be specified and will be
    parsed when added by ConfigArgumentParser.

    it was reported this might not work well with subparsers, patches
    to fix that are welcome.
    """

    def __init__(self, *args, **kwargs):
        """the config action is a search path, so a list, so one or more argument"""
        kwargs["nargs"] = 1
        super().__init__(*args, **kwargs)

    def __call__(self, parser, ns, values, option):
        """change defaults for the namespace, still allows overriding
        from commandline options"""
        for path in values:
            parser.set_defaults(**self.parse_config(path))
        super().__call__(parser, ns, values, option)

    def parse_config(self, path):
        """abstract implementation of config file parsing, should be overriden in subclasses"""
        raise NotImplementedError()


class YamlConfigAction(ConfigAction):
    """YAML config file parser action"""

    def parse_config(self, path):
        try:
            with open(os.path.expanduser(path), "r") as handle:
                logging.debug("parsing path %s as YAML" % path)
                return yaml.safe_load(handle) or {}
        except (FileNotFoundError, yaml.parser.ParserError) as e:
            raise argparse.ArgumentError(self, e)


class ConfigArgumentParser(argparse.ArgumentParser):
    """argument parser which supports parsing extra config files

    Config files specified on the commandline through the
    YamlConfigAction arguments modify the default values on the
    spot. If a default is specified when adding an argument, it also
    gets immediately loaded.

    This will typically be used in a subclass, like this:

            self.add_argument('--config', action=YamlConfigAction, default=self.default_config())

    >>> from tempfile import NamedTemporaryFile
    >>> c = NamedTemporaryFile()
    >>> c.write(b"foo: delayed\\n")
    13
    >>> c.flush()
    >>> parser = ConfigArgumentParser()
    >>> a = parser.add_argument('--foo', default='bar')
    >>> a = parser.add_argument('--config', action=YamlConfigAction, default=[c.name])
    >>> args = parser.parse_args([])
    >>> args.config == [c.name]
    True
    >>> args.foo
    'delayed'

    This is the same test, but with `--config` called earlier, which
    should still work (but doesn't, because the subsequent action
    changes the default).

    >>> from tempfile import NamedTemporaryFile
    >>> c = NamedTemporaryFile()
    >>> c.write(b"foo: quux\\n")
    10
    >>> c.flush()
    >>> parser = ConfigArgumentParser()
    >>> a = parser.add_argument('--config', action=YamlConfigAction, default=[c.name])
    >>> a = parser.add_argument('--foo', default='bar')
    >>> args = parser.parse_args([])
    >>> args.config == [c.name]
    True
    >>> args.foo
    'quux'
    >>> args = parser.parse_args(['--foo', 'baz'])
    >>> args.foo
    'baz'
    >>> parser = ConfigArgumentParser()
    >>> a = parser.add_argument('--config', action=YamlConfigAction, default=[c.name])
    >>> a = parser.add_argument('--foo', default='bar')
    >>> args = parser.parse_args(['--config', '/dev/null'])
    >>> args.foo
    'bar'
    >>> args = parser.parse_args(['--config', '/dev/null', '--foo', 'baz'])
    >>> args.foo
    'baz'
    >>> c.close()

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # a list of actions to fire with their defaults if not fired
        # during parsing
        self._delayed_config_action = []

    def _add_action(self, action):
        # this overrides the add_argument() routine, which is where
        # actions get registered in the argparse module.
        #
        # we do this so we can properly load the default config file
        # before the the other arguments get set.
        #
        # now, of course, we do not fire the action here directly
        # because that would make it impossible to *not* load the
        # default action. so instead we register this as a
        # "_delayed_config_action" which gets fired in `parse_args()`
        # instead
        action = super()._add_action(action)
        if isinstance(action, ConfigAction) and action.default is not None:
            self._delayed_config_action.append(action)

    def parse_args(self, args=None, namespace=None):
        # we do a first failsafe pass on the commandline to find out
        # if we have any "config" parameters specified, in which case
        # we must *not* load the default config file
        ns, _ = self.parse_known_args(args, namespace)

        # load the default configuration file, if relevant
        #
        # this will parse the specified config files and load the
        # values as defaults *before* the rest of the commandline gets
        # parsed
        #
        # we do this instead of just loading the config file in the
        # namespace precisely to make it possible to override the
        # configuration file settings on the commandline
        for action in self._delayed_config_action:
            if action.dest in ns and action.default != getattr(ns, action.dest):
                # do not load config default if specified on the commandline
                logging.debug("not loading delayed action because of config override")
                # action is already loaded, no need to parse it again
                continue
            try:
                action(self, ns, action.default, None)
                logging.debug("loaded config file: %s" % action.default)
            except argparse.ArgumentError as e:
                # ignore errors from missing default
                logging.debug("default config file %s error: %s" % (action.default, e))
        # this will actually load the relevant config file when found
        # on the commandline
        #
        # note that this will load the config file a second time
        return super().parse_args(args, namespace)

    def default_config(self):
        """handy shortcut to detect commonly used config paths"""
        return [
            os.path.join(
                os.environ.get("XDG_CONFIG_HOME", "~/.config/"), self.prog + ".yml"
            )
        ]


class PubpasteArgumentParser(ConfigArgumentParser):
    def __init__(self, *args, **kwargs):
        """
        override constructor to setup our arguments and config file
        """
        super().__init__(description=__doc__, epilog=__epilog__, *args, **kwargs)
        # This is the usage of weasel's publish:
        #
        # usage: publish [<src> [<src> ...]]
        #
        # copy the file <src> to a server and report the URL.
        #
        # OPTIONS:
        #    -8        Add a AddDefaultCharset UTF-8 .htaccess file.
        #    -c CF     Use config file CF.
        #    -H        Show the history.
        #    -l        Show last used token.
        #    -s FN     When reading data from stdin, use FN as filename to be published.
        #    -S        Make a screenshot of one window and publish.
        #    -h        Show this message.
        #    -n        no-do.  Just print what would have been done.
        #    -q        Produce a QR code.
        #    -r        Add --relative option to rsync so that path names of the given
        #              files are preserved at the remote host.
        #    -t days   time to live in days
        #    -R        re-publish (re-use last directory token)
        #    -T tag    directory name on the server (use this to re-publish under that name)
        #    -x        Publish the contents of the xclipboard.
        #    -u        Unpublish directory (only useful together with -T)
        #    -L        Follow symlinks
        self.add_argument(
            "-v",
            "--verbose",
            action=LoggingAction,
            const="INFO",
            help="enable verbose messages",
        )
        self.add_argument(
            "-d",
            "--debug",
            action=LoggingAction,
            const="DEBUG",
            help="enable debugging messages",
        )
        self.add_argument("--dryrun", "-n", action="store_true", help="do nothing")

        group = self.add_argument_group("history arguments")
        group.add_argument(
            "-t",
            "--ttl",
            help="how long to keep the entry, in days, default: %(default)s",
        )
        group = group.add_mutually_exclusive_group()
        group.add_argument("-T", "--token", help="secret token, default: generated")
        group.add_argument(
            "-R", "--republish", action="store_true", help="reuse previous secret token"
        )

        self.add_argument(
            "--follow-symlinks", "-L", action="store_true", help="follow symlinks"
        )
        self.add_argument(
            "-r",
            "--relative",
            action="store_true",
            help="consider all parts of the provided path, passed to rsync as --relative",
        )
        self.add_argument(
            "-s",
            "--stdin-name",
            metavar="NAME",
            default="stdin.txt",
            help="use NAME as filename when reading from stdin, default: %(default)s",
        )
        self.add_argument(
            "-o",
            "--output",
            help=argparse.SUPPRESS,  # only in configuration file
            default=None,
        )
        self.add_argument(
            "--url-prefix",
            help=argparse.SUPPRESS,  # only in configuration file
            default=None,
        )
        self.add_argument(
            "--base-dir",
            help=argparse.SUPPRESS,  # only in configuration file
            default=None,
        )
        self.add_argument(
            "--save-screenshots", help=argparse.SUPPRESS  # only in configuration file
        )
        self.add_argument(
            "--select",
            action="store_true",
            help="tell screenshot tool to let the user select an area, default: fullscreen",
        )
        commands_group = self.add_argument_group(
            "command arguments", description="what should be done, default: just upload"
        )
        group = commands_group.add_mutually_exclusive_group()
        group.add_argument(
            "-x",
            "--xselection",
            action="store_const",
            const="xselection",
            dest="command",
            help="publish the contents of the X PRIMARY selection",
        )
        group.add_argument(
            "-C",
            "--clipboard",
            action="store_const",
            const="xclipboard",
            dest="command",
            help="publish the contents of the X CLIPBOARD selection",
        )
        group.add_argument(
            "-S",
            "--screenshot",
            action="store_const",
            const="screenshot",
            dest="command",
            help="capture and upload a screenshot",
        )
        group.add_argument(
            "-g",
            "--gallery",
            action="store_const",
            const="gallery",
            dest="command",
            help="make a static image Sigal gallery from the files",
        )
        group.add_argument(
            "-l",
            "--last-token",
            action="store_const",
            const="last-token",
            dest="command",
            help="show the last token used and exit",
        )
        group.add_argument(
            "-H",
            "--show-history",
            action="store_const",
            const="show-history",
            dest="command",
            help="dump history file and exit",
        )
        group.add_argument(
            "-u",
            "--undo",
            action="store_const",
            const="undo",
            dest="command",
            help="delete uploaded token specified with -T or -R and exit",
        )
        group.add_argument(
            "-P",
            "--purge",
            action="store_const",
            const="purge",
            dest="command",
            help="purge old entries from remote server",
        )
        group.add_argument("--command", default="upload", help=argparse.SUPPRESS)

        self.add_argument(
            "--config",
            action=YamlConfigAction,
            default=self.default_config(),
            help="use alternatte config file path, default: %(default)s",
        )
        self.add_argument("files", nargs="*", help="files to upload")

    def parse_args(self, *args, **kwargs):
        res = super().parse_args(*args, **kwargs)
        if res.output and not res.output.endswith("/"):
            res.output += "/"
        if res.url_prefix and not res.url_prefix.endswith("/"):
            res.url_prefix += "/"
        if res.dryrun:
            if not res.files or "-" in res.files:
                self.error("cannot read from stdin in dryrun")
            if res.command in ("xselection", "xclipboard"):
                self.error("cannot read from x selection in dryrun")
        if res.files and res.command and res.command != "gallery":
            self.error(
                "command %s and files cannot be specified together" % res.command
            )
        if res.command and res.command == "purge" and args.base_dir is None:
            self.error("no --base-dir specified, cannot find files to purge")
        if res.command and res.command in ("xselection", "xclipboard") and res.relative:
            # this is to workaround a bug where the tmpfile path gets
            # propagated to the other side when using --relative
            # https://gitlab.com/anarcat/pubpaste/-/issues/1
            self.error("--relative and --xselection/--xclipboard do not make sense")

        return res


class Processor(object):
    def __init__(self, args, dryrun=False):
        self.args = args
        self.dryrun = dryrun

    def process(self, paths, tmp_dir):
        """process the given paths

        Returns the modified paths, or None if not modified. A tmp_dir
        is provided by the caller and automatically destroyed.
        """
        raise NotImplementedError()


class Sigal(Processor):
    """the Sigal processor will create a temporary gallery in the provided
    tmp_dir, after copying the provided files in the said
    directory. it returns only the "build" directory.
    """

    def process(self, paths, tmp_dir):
        output_dir = Path(tmp_dir) / Path(self.args.token)
        if not output_dir.exists() and not self.dryrun:
            logging.info("creating directory %s", output_dir)
            output_dir.mkdir(parents=True)

        pictures_dir = output_dir / "pictures"
        if not pictures_dir.exists() and not self.dryrun:
            logging.info("creating directory %s", pictures_dir)
            pictures_dir.mkdir(parents=True)
            # this removes the directory so that copytree works. this
            # can be removed once we depend on Python 3.8, which has
            # the `dirs_exist_ok` parameter
            pictures_dir.rmdir()

        conf_file = output_dir / "sigal.conf.py"
        if not conf_file.exists() and not self.dryrun:
            logging.info("creating config file %s", output_dir)
            with conf_file.open("w") as c:
                c.write(self.sigal_minimal_config())

        for path in paths:
            logging.info("copying %s into %s", path, pictures_dir)
            if not self.dryrun:
                shutil.copytree(
                    path, str(pictures_dir), symlinks=not self.args.follow_symlinks
                )

        build_dir = output_dir / "_build"
        command = (
            "sigal",
            "build",
            "--config",
            str(conf_file),
            str(pictures_dir),
            str(build_dir),
        )
        logging.info("building gallery with %r", shlex_join(command))
        if not self.dryrun:
            subprocess.check_call(command)
        return (str(build_dir),)

    @classmethod
    def sigal_minimal_config(cls):
        """a string representing a good minimal sigal configuration for our
        use case.

        sigal default settings are generally great, but i disagree on
        those.

        .. TODO:: allow users to provide their own config

        """
        return """
# theme: colorbox (default), galleria, photoswipe, or path to custom
theme = 'galleria'
# sort files by date (default: filename)
medias_sort_attr = 'date'
# "Standard HD", or 720p (default: (640, 480))
img_size = (1280, 720)
# "Standard HD", or 720p (default: (480, 360))
video_size = (1280, 720)
# skip first three seconds in video (default: 0)
thumb_video_delay = '3'
"""


class Maim(Processor):
    """The Main processor will take a screenshot and return the file after
    copying it to the temporary directory"""

    def __init__(self, args, dryrun=False, save_screenshots=False):
        super().__init__(args, dryrun=dryrun)
        if args.select:
            self.command = "maim --select --delay=3 '%s'"
        else:
            self.command = "maim --delay=3 '%s'"
        self.save_screenshots = save_screenshots

    def process(self, paths, tmp_dir):
        """wrap main around a timer, preview and prompt"""
        if self.save_screenshots:
            snaps_dir = Path(os.path.expanduser(self.save_screenshots))
            if not snaps_dir.exists():
                snaps_dir.mkdir()
        else:
            snaps_dir = Path(tmp_dir)
        snap_basename = Path(
            "snap-" + datetime.now().strftime("%Y%m%dT%H%M%S%Z") + ".png"
        )
        snap_path = snaps_dir / snap_basename
        # XXX: this is just horrible. can't the screenshot tool do the right thing here?
        #
        # TODO: at the very least, make our own popup, because right
        # now this doesn't catch errors from maim, as errors from the
        # subprocess are not trickled back up through xterm
        command = (
            "xterm",
            "-title",
            "pop-up",
            "-geometry",
            "80x3+5+5",
            "-e",
            self.command % snap_path,
        )
        logging.debug("running screenshot with %s", shlex_join(command))
        if not self.dryrun:
            success = subprocess.call(command) == 0
            if not success:
                notify_user("screenshot command failed, aborting")
                return []
        if not snap_path.exists():
            notify_user("snapshot file missing, is maim installed?")
            return []
        if snap_path.stat().st_size <= 0:
            notify_user("snapshot file is empty, aborting")
            snap_path.unlink()
            return []
        # we delegate the customization of this to XDG
        subprocess.Popen(("xdg-open", str(snap_path)))  # nowait
        # XXX: gah. we *could* just do GTK here?
        command = (
            "xmessage",
            "-buttons",
            "okay:0,cancel:1",
            "-center",
            "-default",
            "okay",
            "upload snapshot publically?",
        )
        try:
            retcode = subprocess.call(command)
        except OSError as e:
            logging.error("cannot find xmessage? %s", e)
            return []
        if retcode == 0:
            target = str(Path(tmp_dir) / snap_basename)
            if not self.save_screenshots:
                logging.debug("returning %s", tmp_dir)
                return (target,)
            shutil.copy(str(snap_path), target)
            # pass the resulting file back to the uploader
            logging.info("screenshot copied from %s to %s", snap_path, target)
            return (target,)
        elif retcode == 1:
            logging.info("user declined, aborting")
        elif retcode > 1:
            logging.error("unexpected error from xmessage")
        elif retcode < 0:
            logging.error("xmessage terminated by signal %s", -retcode)
        return []


class Uploader(object):
    """an abstract class to wrap around upload objects"""

    def __init__(self, target, dryrun=False, follow_symlinks=False):
        self.target = target
        self.dryrun = dryrun
        self.follow_symlinks = follow_symlinks

    def upload(self, paths, target=None, single=False):
        """upload the given path to the target

        "Single" is an indication by the caller of whether or not this
        is the only item in a list to upload.
        """
        raise NotImplementedError()


class RsyncUploader(Uploader):
    base_rsync_command = (
        "rsync",
        "--recursive",
        "--compress",
        "--times",
        "--chmod=u=rwX,go=rX",
    )

    def upload(self, path, target=None, single=False, cwd=None):
        """upload the given path to the target

        "Single" is an indication by the caller of whether or not this
        is the only item in a list to upload. The RsyncUploader uses
        that information to decide how many levels it should replicate
        remotely.
        """
        if target is None:
            target = self.target
        command = list(self.base_rsync_command)
        if self.follow_symlinks:
            command.append("--copy-links")  # -L
        # XXX: begin nasty rsync commandline logic

        # rsync is weird. it behaves differently when its arguments
        # have trailling slashes or not. this specifically affects
        # directory (but technically, if you pass a file with a
        # trailing slash, it will fail, obviously)
        #
        # the behavior is documented in the manpage, as such:

        # A trailing slash on the source changes this behavior to
        # avoid creating an additional directory level at the
        # destination. You can think of a trailing / on a source as
        # meaning "copy the contents of this directory" as opposed to
        # "copy the directory by name", but in both cases the
        # attributes of the containing directory are transferred to
        # the containing directory on the destination. In other words,
        # each of the following commands copies the files in the same
        # way, including their setting of the attributes of /dest/foo:
        #
        # rsync -av /src/foo /dest
        # rsync -av /src/foo/ /dest/foo

        # They ommitted, obviously, that this is also identical:
        #
        # rsync -av /src/foo/ /dest/foo/
        #
        # So we pick the latter form, IF WE UPLOAD A SINGLE DIRECTORY!
        # If we upload MULTIPLE FILES OR DIRECTORIES, we CANNOT use
        # the above form, as the last uploads would overwrite the
        # first ones. So if we have more than one file passed on the
        # commandline, we do, effectively, this:
        #
        # rsync -av /srv/foo /srv/bar /dest/foo/
        #
        # which, yes, is actually equivalent to:
        #
        # rsync -av /srv/foo /dest/foo/foo
        # rsync -av /srv/bar /dest/foo/bar

        # so here we go.

        # make sure we have a trailing slash at least to the
        # second argument, so we are *certain* we upload in a new
        # *directory*
        if not target.endswith("/"):
            target += "/"
        # for the source, special handling if it is a directory
        if os.path.isdir(path):
            if single:
                # single file to upload: upload at root which
                # means, for rsync, to have a trailing slash
                if not path.endswith("/"):
                    path += "/"
            else:
                # multiple files to upload: upload *within* the
                # root, so *remove* the trailing slash if present
                if path.endswith("/"):
                    path = path.rstrip("/")
        # XXX: end nasty rsync commandline logic
        command += (path, target)

        logging.debug("uploading with %r", shlex_join(command))
        if self.dryrun:
            return self.dryrun
        return subprocess.call(command, cwd=cwd) == 0

    def delete(self, target=None):
        """delete the given target, or the one from the constructor

        This is done by synchronizing it with an empty temporary
        directory, and by calling rsync with `--delete`. We also
        assert that the tmpdir is empty.
        """
        if target is None:
            target = self.target
        with tempfile.TemporaryDirectory() as empty_dir:
            assert not list(
                Path(empty_dir).iterdir()
            ), "tmpdir is not empty, delete would fail"
            command = list(self.base_rsync_command)
            command.append("--delete")
            command += (empty_dir + "/", target + "/")
            logging.debug("deleting with %r", shlex_join(command))
            if self.dryrun:
                return self.dryrun
            return subprocess.check_call(command) == 0


class History:
    TTL_PATH = ".publish.ttl"

    @dataclass
    class Entry:
        date: Optional[str] = None
        time: Optional[str] = None
        token: Optional[str] = None
        uri: Optional[str] = None

        @classmethod
        def _make(cls, line):
            items = line.strip().split(" ", 4)
            return History.Entry(*items)

        def __str__(self):
            return " ".join([self.date, self.time, self.token, self.uri])

    def __init__(self, path: str = None):
        if path is None:
            path = os.path.expanduser("~/.publish.history")
        self.path = path
        self.recorded = False

    def append(self, token, uri):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
        with open(self.path, "a") as fp:
            fp.write(" ".join((timestamp, token, uri)) + "\n")

    def append_once(self, token, uri):
        if not self.recorded:
            self.append(token, uri)
            self.recorded = True

    def remove(self, tokens=()):
        """remove the given tokens from history"""
        with open(self.path, "r") as old, open(self.path + ".new", "w") as new:
            for line in old.readlines():
                entry = History.Entry._make(line)
                if entry.token not in tokens:
                    new.write(line)
        os.rename(self.path + ".new", self.path)

    def __iter__(self):
        with open(self.path, "r") as fp:
            for line in fp.readlines():
                yield History.Entry._make(line)

    def last(self):
        """find last history token

        This is separate from the above generator to avoid messing
        with its state
        """
        # date, time, token, uri
        entry = None
        with open(self.path, "r") as fp:
            for line in fp.readlines():
                pass
        if line:
            entry = History.Entry._make(line)
            logging.debug("found last entry: %s", entry)
        return entry

    def purge(self, base_dir):
        logging.debug("purging from %s", base_dir)
        for path in [p for p in Path(base_dir).iterdir() if p.is_dir()]:
            token = path.name
            ttl_file = path / self.TTL_PATH
            if not ttl_file.exists():
                logging.info("no TTL file, token % never expires", token)
                continue
            with ttl_file.open("r") as fp:
                ttl_str = fp.read()
            try:
                ttl = int(ttl_str)
            except ValueError as e:
                logging.warning(
                    "invalid TTL found for token %s: %s in %s", token, e, ttl_file
                )
                continue
            now_utc = datetime.now(timezone.utc)
            local_tz = now_utc.astimezone().tzinfo
            last_modified = datetime.fromtimestamp(
                ttl_file.stat().st_mtime, tz=local_tz
            )
            diff = timedelta(days=ttl)
            logging.debug(
                "time delta, last: %s, diff: %s days, last + diff: %s, delta: %s, now: %s",
                last_modified,
                diff,
                last_modified + diff,
                now_utc - last_modified + diff,
                now_utc,
            )
            if last_modified + diff < now_utc:
                notify_user(
                    "token %s expired since %s, removing directory: %s"
                    % (token, -(diff - (now_utc - last_modified)), path)
                )
                shutil.rmtree(path)
            else:
                logging.info(
                    "TTL %s days not passed yet (%s left) for token %s",
                    ttl,
                    diff - (now_utc - last_modified),
                    token,
                )


def secret_token():
    """return a secret token made of multiple components, as a tuple"""
    return datetime.now().strftime("%Y-%m-%d"), secrets.token_urlsafe()


class AbstractClipboard:
    def __init__(self, selection: str):
        """configure the clipboard, based on whether the clipboard is PRIMARY
        or CLIPBOARD
        """
        raise NotImplementedError()

    def put_text(self, text: str):
        raise NotImplementedError()

    def put_image(self, path: bytes):
        raise NotImplementedError()

    def get(self) -> Tuple[Optional[bytes], Optional[str]]:
        raise NotImplementedError()


# NOTE: we use xclip and gi directly here as the alternative is
# pyperclip, which does exactly the same thing:
#
# https://pypi.org/project/pyperclip/
#
# also, pyperclip actually *fails* to use gi in my tests, in Debian
# bullseye, so really, it's a lot of code for nothing for us. Worse,
# it doesn't support copying images the way we do.
class GtkClipboard(AbstractClipboard):
    "Clipboard implementation with a GTK/GI backend"

    def __init__(self, selection):
        """initialize a clipboard based on CLIPBOARD or PRIMARY selection

        we use a string argument here to abstract away the GTK stuff"""
        assert selection in ("CLIPBOARD", "PRIMARY"), "invalid clipboard selection used"
        if selection == "CLIPBOARD":
            self._cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        elif selection == "PRIMARY":
            self._cb = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        logging.debug("created clipboard with %s selection", selection)

    def _gdk_event_handler(self, event, user_data=None):
        logging.debug("event: %r, user_data: %r", event, user_data)
        # pass the event to GTK so we actually send the paste back,
        # and do whatever it is GTK does with events
        # https://developer.gnome.org/pygtk/stable/gtk-functions.html#function-gtk--main-do-event
        Gtk.main_do_event(event)
        # this is xclip's behavior: when another process takes the
        # selection, it exits
        # https://developer.gnome.org/pygtk/stable/class-gdkevent.html#description-gdkevent
        if event.type == Gdk.EventType.SELECTION_CLEAR:
            logging.info("selection picked up by another process, exiting")
            Gtk.main_quit()

    def _wait_for_paste(self):
        # add an event handler to exit early when something is pasted
        # https://developer.gnome.org/gdk3/stable/gdk3-Events.html#gdk-event-handler-set
        Gdk.event_handler_set(self._gdk_event_handler)
        # Gtk won't process clipboard events unless we start
        # Gtk.main(). Believe me, I tried.
        Gtk.main()

    def put_text(self, text: str):
        """set the clipboard to the given text"""

        def callback():
            logging.debug("setting clipboard text to %r", text)
            # NOTE: yes, it's silly that set_text() asks for the data
            # length, this is python after all?
            self._cb.set_text(text, len(text))

        return self._put(callback)

    def put_image(self, path: bytes):
        """load the image from the given path name and put in the clipboard"""

        def callback():
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
            logging.debug("setting clipboard image to %r", pixbuf)
            self._cb.set_image(pixbuf)

        return self._put(callback)

    def _put(self, callback):
        """utility to do the actual paste, fork and wait for the paste to complete

        This will just call the given callback, which is assumed to
        have the data itself, either because it's a class method or
        (easier) an inline function."""
        pid = os.fork()
        if pid:  # parent
            logging.info(
                "forked child %d to hold onto clipboard data",
                pid,
            )
            # TODO: use IPC to confirm paste with child
            return True
        else:  # child
            callback()
            # TODO: this is where we would send success to parent
            self._wait_for_paste()
            # important, because we're in the child and otherwise we'd
            # duplicate the parent's control flow
            #
            # we use _exit() to avoid firing atexit() in double
            os._exit(0)

    def get(self):
        """get the clipboard content, possible as an image or, failing that, as text

        GTK clipboards also support "rich text" and "URI", but I'm not
        sure what to do with those. See:

        https://developer.gnome.org/gtk3/3.24/gtk3-Clipboards.html#gtk-clipboard-wait-for-rich-text
        https://developer.gnome.org/gtk3/3.24/gtk3-Clipboards.html#gtk-clipboard-wait-is-uris-available
        https://python-gtk-3-tutorial.readthedocs.io/en/latest/clipboard.html
        """
        if self._cb.wait_is_image_available():
            data = self._cb.wait_for_image()
            if data is None:
                logging.warning("no clipboard content")
                return None, None
            res, imgdata = data.save_to_bufferv("png", [], [])
            if not res:
                logging.warning(
                    "could not parse clipboard data (%d bytes) as image, ignoring",
                    len(data),
                )
                return None, None
            logging.debug("found %d bytes of image data in clipboard", len(imgdata))
            return imgdata, "png"
        elif self._cb.wait_is_text_available():
            # https://developer.gnome.org/gtk3/3.24/gtk3-Clipboards.html#gtk-clipboard-wait-for-text
            # https://stackoverflow.com/questions/13207897/how-to-get-clipboard-content-in-gtk3-gi-and-python-3-on-ubuntu
            data = self._cb.wait_for_text()
            if data is None:
                logging.warning("no clipboard content")
                return None, None
            logging.debug("found %d bytes of text data in clipboard", len(data))
            return data.encode("utf-8"), "txt"
        else:
            logging.warning("unsupported clipboard type")
            return None, None


# TODO: xsel support? might be hard because it relies on a clipboard
# manager (e.g. xclipboard(1)) to store the selection for us, which we
# can't rely on... The equivalent in GTK is the `store()` command,
# which didn't work in my environment (i3 minimal desktop).
class XclipClipboard(AbstractClipboard):
    def __init__(self, selection):
        assert selection in ("CLIPBOARD", "PRIMARY"), "invalid clipboard selection used"
        self.command = ("xclip", "-selection", selection.lower())

    def put_text(self, text: str):
        if not os.environ.get("DISPLAY"):
            logging.warning("could not copy to clipboard without a DISPLAY variable")
            return False
        p = subprocess.Popen(self.command, stdin=subprocess.PIPE)
        p.communicate(text.encode("utf-8"))
        if p.returncode == 0:
            return True
        else:
            logging.warning("could not copy to clipboard with: %r", self.command)
            return False

    def put_image(self, data: bytes):
        raise NotImplementedError("xclip does not support copying images")

    def get(self):
        command = list(self.command) + ["-o"]
        try:
            clipboard = subprocess.check_output(command)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            logging.error("could not find tool to paste clipboard: %s", e)
            return None, None
        return clipboard, "txt"


if gi:
    Clipboard: Type[AbstractClipboard] = GtkClipboard
else:
    Clipboard = XclipClipboard


def notify_user(message):
    logging.warning(message)
    if os.environ.get("DISPLAY") is None:
        return
    command = ("notify-send", message)
    # do not fail on notifications
    if subprocess.call(command) != 0:
        logging.warning("failed to run command %r", command)


def main():
    """
    This program does the following:

    1. dispatch history commands: purge, show-history or last-token
    2. prepare the token from history or generate one
    3. guess the URL of the resulting paste
    4. dispatch the various commands
    5. write the TTL file to eventually expire this paste
    6. upload resulting files
    7. add the guesed URL to the clipboard
    8. notify the user, probably with notify-send
    """
    logging.basicConfig(format="%(message)s", level="WARNING")
    args = PubpasteArgumentParser().parse_args()

    history = History()

    # 1. dispatch history commands like show-history or last-token
    if args.command == "show-history":
        for entry in history:
            print(entry)
        sys.exit(0)
    elif args.command == "last-token":
        last = history.last()
        if last:
            print(last.token)
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.command == "purge":
        history.purge(args.base_dir)
        sys.exit(0)

    # 2. prepare the token

    # ... from history (if --republish, which is implicity with --undo)
    if args.republish or args.command == "undo":
        last = history.last()
        # do not override provided token
        if last and not args.token:
            args.token = last.token

    # ... no token provided, generate a new one
    if args.token is None:
        args.token = "-".join(secret_token())

    logging.debug("using secret token %s", args.token)

    # 3. guess the URL of the resulting paste
    #
    # user has a public facing URL for publishing, generate the
    # resulting URL for this paste
    if args.url_prefix:
        assert args.url_prefix.endswith(
            "/"
        ), "args parsing should have ensured a trailing slash"
        uri_with_token = args.url_prefix + args.token + "/"
    else:
        uri_with_token = None

    # files that we are confident we can show the user on the
    # terminal. those are typically stdin and xselection but could
    # grow to include text files..
    dump_content = []

    # prepare our uploader object
    uploader = RsyncUploader(
        target=args.output + args.token, follow_symlinks=args.follow_symlinks
    )
    if logging.getLogger("").level >= 20:  # INFO or DEBUG
        uploader.base_rsync_command += ("--progress", "--verbose")
    if args.relative:
        uploader.base_rsync_command += ("--relative",)

    # list of cleanup functions to run after upload
    if not args.dryrun:
        tmp_dir = tempfile.TemporaryDirectory()
        atexit.register(tmp_dir.cleanup)

    # 4. dispatch the various commands
    #
    # main command dispatcher, a block may just exit here if it does
    # all its work, or it may change args.files to add more files to
    # the upload queue

    if args.command == "undo":
        if not uploader.delete():
            notify_user("failed to delete target %s" % args.token)
            sys.exit(1)
        history.remove(args.token)
        notify_user("deleted target %s" % args.token)
        sys.exit(0)

    elif args.command in ("xselection", "xclipboard"):
        logging.info("reading from xselection...")
        clipboard_primary = Clipboard(
            "PRIMARY" if args.command == "xselection" else "CLIPBOARD"
        )
        data, extension = clipboard_primary.get()
        if data is None:
            logging.error("no clipboard data found, aborting")
            sys.exit(1)
        assert extension is not None, "clipboard should have guess extension"
        # NOTE: could this be optimized? can we *stream* the
        # clipboard?
        clipboard_tmp_path = Path(tmp_dir.name) / ("clipboard." + extension)
        clipboard_tmp_path.write_bytes(data)
        logging.info(
            "written %d bytes from clipboard into %s", len(data), clipboard_tmp_path
        )
        args.files = [str(clipboard_tmp_path)]
        if extension == "txt":
            dump_content = [str(clipboard_tmp_path)]

    elif args.command == "screenshot":
        m = Maim(args, dryrun=args.dryrun, save_screenshots=args.save_screenshots)
        args.files = m.process([], tmp_dir.name)

    elif args.command == "gallery":
        logging.debug("processing files %s with Sigal", args.files)
        f = Sigal(args, dryrun=args.dryrun).process(args.files, tmp_dir.name)
        if f is not None:
            args.files = f
            logging.debug("modified files: %s", args.files)

    elif not args.files:
        # default to stdin
        args.files = ["-"]

    if not args.output:
        logging.error("no output provided, nothing to do, aborting")
        sys.exit(1)

    # this should never be reached, but just in case
    if not args.files:
        logging.error("no files provided, nothing to do, aborting")
        sys.exit(1)

    # 5. write the TTL file to eventually expire this paste
    #
    # we do this before the upload to make sure uploads are expired
    # even if they fail or are interrupted half-way through
    if args.ttl:
        # use a separate tmpdir to avoid uploading the ttl file twice
        with tempfile.TemporaryDirectory() as ttl_tmp_dir:
            ttl_file = ttl_tmp_dir + "/" + history.TTL_PATH
            if not args.dryrun:
                with open(ttl_file, "w") as fp:
                    fp.write(args.ttl + "\n")
            if not uploader.upload(history.TTL_PATH, cwd=ttl_tmp_dir):
                notify_user("failed to upload TTL file for %s" % args.token)

    # 6. upload resulting files
    #
    # main upload loop, files either from the commandline or previous
    # dispatchers
    for key, path in enumerate(args.files):
        # generate a new URI *specific to this file*
        uri = None
        if uri_with_token:
            uri = uri_with_token
            if not os.path.isdir(path):
                uri += quote(path)

        # process "-" specially
        cwd = None
        if path == "-":
            logging.info("reading from stdin...")
            stdin_tmp_path = tmp_dir.name + "/" + args.stdin_name
            cwd = tmp_dir.name
            path = args.stdin_name
            args.files[key] = path
            with open(stdin_tmp_path, "w+b") as tmp:
                shutil.copyfileobj(sys.stdin.buffer, tmp)
            dump_content = [stdin_tmp_path]
            if uri_with_token:
                uri = uri_with_token + quote(path)

        # dump file contents we know is terminal-safe
        if path in dump_content:
            with open(path) as fp:
                print("uploading content: %r" % fp.read())
        assert args.output.endswith("/")

        # record history
        history.append_once(args.token, uri_with_token or None)

        if uri:
            logging.info("uploading %s to %s", path, uri)
        else:
            logging.info("uploading %s", path)

        # actual upload
        if not uploader.upload(path, single=(len(args.files) == 1), cwd=cwd):
            notify_user("failed to upload %s as %s, aborting" % (path, args.token))
            sys.exit(1)

    # if we don't have a URI to announce, we're done
    if not uri_with_token:
        notify_user("uploaded %s" % shlex_join(args.files))
        sys.exit(0)

    uri = uri_with_token
    # if we've processed a single file, add it to the announced URL
    if len(args.files) == 1:
        path = Path(args.files[0])
        if not path.is_dir():
            uri += quote(os.path.basename(path))

    # 7. add the guesed URL to the clipboard
    selection_clipboard = Clipboard("CLIPBOARD")
    pasted = selection_clipboard.put_text(uri)

    # 8. notify the user, probably with notify-send
    message = "uploaded %s to '%s'" % (shlex_join(args.files), uri)
    if pasted:
        message += " copied to clipboard"
    if args.ttl:
        message += ", expiring in %s days" % args.ttl
    else:
        message += ", never expiring"
    notify_user(message)


if __name__ == "__main__":
    main()
