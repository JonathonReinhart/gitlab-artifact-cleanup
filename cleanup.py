#!/usr/bin/env python
from __future__ import print_function
import argparse
from gitlab import Gitlab
from gitlab.exceptions import *

def cleanup_project(proj):
    print('Cleaning up', proj.name_with_namespace)

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-g', '--gitlab',
            help='GitLab server defined in config file .python-gitlab')
    ap.add_argument('--all-projects', action='store_true',
            help='Cleanup artifacts for all accessible projects')
    ap.add_argument('-p', '--project', dest='projects', action='append',
            help='Project for which to cleanup artifacts -- can be given multiple times')

    args = ap.parse_args()

    if not (args.all_projects or args.projects):
        ap.error('-p or --all-projects must be specified')
    if (args.all_projects and args.projects):
        ap.error('-p and --all-projects are mutually exclusive')

    return args

def main():
    args = parse_args()
    gl = Gitlab.from_config(gitlab_id=args.gitlab)

    if args.all_projects:
        for proj in gl.projects.all(all=True):
            cleanup_project(proj)
    else:
        for pname in args.projects:
            try:
                proj = gl.projects.get(pname)
            except GitlabGetError as e:
                print("Error getting project", pname, e)
                continue
            cleanup_project(proj)

if __name__ == '__main__':
    main()
