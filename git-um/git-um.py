#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# git-um - Git Upstream Manager.
# Copyright (C) 2011  Pavel Shilovsky <piastry@etersoft.ru>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from gitupstream import *
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description='Git Upstream Manager')
	subparsers = parser.add_subparsers(dest='command_name')
	pull_p = subparsers.add_parser('pull')
	gr = pull_p.add_mutually_exclusive_group()
	gr.add_argument('--continue', action='store_true', help='continue a pull process')
	gr.add_argument('--skip', action='store_true', help='skip the current patch in rebase and continue a pull process')
	gr.add_argument('--abort', action='store_true', help='abort a pull process')
	update_p = subparsers.add_parser('update')
	update_p.add_argument('since', help='commit id or branch name to start with (excluded)')
	update_p.add_argument('to', help='commit id or branch name that specifies the last entry')
	create_parser = subparsers.add_parser('create')
	create_parser.add_argument('--remote', metavar='server/branch', help='remote branch to track with')
	create_parser.add_argument('--current', metavar='branch', help='current development branch')
	create_parser.add_argument('--upstream', metavar='branch', help='copy of tracked upstream branch')
	create_parser.add_argument('--rebased', metavar='branch', help='branch with our patches on top')
	args = vars(parser.parse_args(sys.argv[1:]))

	if args['command_name'] == 'pull':
		if args['continue']:
			GitUpstream().continue_pull('--continue')
		elif args['skip']:
			GitUpstream().continue_pull('--skip')
		elif args['abort']:
			GitUpstream().abort()
		else:
			GitUpstream().pull()
	elif args['command_name'] == 'update':
		GitUpstream().update_rebased(args['since'], args['to'])
	elif args['command_name'] == 'create':
		# default branch names
		upstream_branch = 'upstream'
		rebased_branch = 'rebased'
		current_branch = 'current'
		remote_branch = 'origin/master'

		if args['remote']:
			remote_branch = args['remote']
		if args['current']:
			current_branch = args['current']
		if args['upstream']:
			upstream_branch = args['upstream']
		if args['rebased']:
			rebased_branch = args['rebased']
		GitUpstream().create(remote_branch, current_branch, upstream_branch, rebased_branch)

if __name__ == "__main__":
	main()
