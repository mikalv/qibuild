# Copyright (c) 2012-2018 SoftBank Robotics. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the COPYING file.

"""Run the same command on each buildable project.

Use -- to separate qibuild arguments from the arguments of the command.
For instance
  qibuild --ignore-errors -- ls -l
"""

import qisys.actions
import qibuild.parsers


def configure_parser(parser):
    """Configure parser for this action """
    qisys.parsers.worktree_parser(parser)
    qibuild.parsers.project_parser(parser, positional=False)
    parser.add_argument("command", metavar="COMMAND", nargs="+")
    parser.add_argument("--continue", "--ignore-errors", dest="ignore_errors",
                        action="store_true", help="continue on error")


def do(args):
    """Main entry point"""
    build_worktree = qibuild.parsers.get_build_worktree(args)
    projects = qibuild.parsers.get_build_projects(build_worktree, args,
                                                  default_all=True)
    qisys.actions.foreach(projects, args.command,
                          ignore_errors=args.ignore_errors)
