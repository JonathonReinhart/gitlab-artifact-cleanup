#!/usr/bin/env python
from __future__ import print_function
import argparse
from datetime import datetime, timedelta
from gitlab import Gitlab
from gitlab.exceptions import *

__version__ = '0.1.0'

class GitlabArtifactCleanup(object):
    def __init__(self, dry_run=False, min_age=None):
        self.dry_run = dry_run
        self.min_age = timedelta() if min_age is None else min_age

        self.total_deleted = 0


    def cleanup_project(self, proj):
        print('Cleaning up', proj.name_with_namespace)

        total_size = 0
        now = datetime.utcnow()

        for build in proj.builds.list(all=True):

            # Skip builds without artifacts
            if not hasattr(build, 'artifacts_file'): continue

            # Skip builds run for tagged commits
            if build.tag:
                print('  Build {}: Skipping for tag'.format(build.id))
                continue

            # Skip builds that are too recent
            ts = datetime.strptime(build.created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            age = now - ts
            if age < self.min_age:
                print('  Build {}: Skipping, too recent'.format(build.id))
                continue

            af = build.artifacts_file
            total_size += af['size']
            print('  Build {id}: {action} {filename} ({size} bytes)'.format(
                id = build.id,
                action = 'Would delete' if self.dry_run else 'Deleting',
                filename = af['filename'],
                size = af['size']))

            if not self.dry_run:
                build.erase()

        self.total_deleted += total_size
        return total_size


def parse_timedelta(s):
    parts = s.split()
    n = int(parts[0])

    if len(parts) == 1:
        return timedelta(seconds=n)

    if len(parts) == 2:
        unit = parts[1].lower()

        # Allow singular units to be given
        if unit[-1] != 's':
            unit += 's'

        # Support units not supported by timedelta constructor
        if unit == 'years':
            unit = 'days'
            n *= 365
        elif unit == 'months':
            unit = 'days'
            n *= 30

        # Leverage timedelta kwargs for handling most units
        return timedelta(**{unit: n})

    raise ValueError

def parse_args():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('-g', '--gitlab',
            help='GitLab server defined in config file .python-gitlab')
    ap.add_argument('--all-projects', action='store_true',
            help='Cleanup artifacts for all accessible projects')
    ap.add_argument('-m', '--min-age', type=parse_timedelta, default=timedelta(),
            help='Minimum age for artifacts to be deleted;\n'
                 'e.g. "172800"\n'
                 '  == "172800 seconds"\n'
                 '  == "2880 minutes"\n'
                 '  == "48 hours"\n'
                 '  == "2 days"')
    ap.add_argument('-n', '--dry-run', action='store_true',
            help="Don't actually delete anything")
    ap.add_argument('-p', '--project', dest='projects', action='append',
            help='Project for which to cleanup artifacts -- can be given multiple times')
    ap.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)

    args = ap.parse_args()

    if not (args.all_projects or args.projects):
        ap.error('-p or --all-projects must be specified')
    if (args.all_projects and args.projects):
        ap.error('-p and --all-projects are mutually exclusive')

    return args

def main():
    args = parse_args()
    print('Deleting artifacts older than {}'.format(args.min_age))

    gl = Gitlab.from_config(gitlab_id=args.gitlab)

    cleanup = GitlabArtifactCleanup(
            dry_run = args.dry_run,
            min_age = args.min_age,
            )

    if args.all_projects:
        for proj in gl.projects.all(all=True):
            cleanup.cleanup_project(proj)
    else:
        for pname in args.projects:
            try:
                proj = gl.projects.get(pname)
            except GitlabGetError as e:
                print("Error getting project", pname, e)
                continue
            deleted = cleanup.cleanup_project(proj)
            print('  {action} {size} bytes of artifacts'.format(
                action = 'Would delete' if args.dry_run else 'Deleted',
                size = deleted))

    print('{action} {size} bytes of artifacts total'.format(
        action = 'Would delete' if args.dry_run else 'Deleted',
        size = cleanup.total_deleted))

if __name__ == '__main__':
    main()
