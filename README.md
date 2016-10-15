gitlab-artifact-cleanup
=======================

Currently (as of GitLab 8.12) there are no admin tools for cleaning up
build artifacts (see issue [#18351]). This script erases build artifacts
using the GitLab API.

## Requirements
- Python 3 only
- [`python-gitlab`] - As of at least [d4a24a5c4d], which is currently unreleased.

## Usage
This script leverages the [`python-gitlab` config file][python-gitlab-config].
Just like the `gitlab` CLI tool, you can specify a non-default Gitlab server
with the `-g`/`--gitlab` option.

You can specify any number of projects with the `-p`/`--project` option:

    $ gitlab-artifact-cleanup --project jreinhart/artifact-test --project jreinhart/python-gitlab

Or, you can cleanup all projects visible to you:

    $ gitlab-artifact-cleanup --all-projects

Builds for tags are never removed.


[#18351]: https://gitlab.com/gitlab-org/gitlab-ce/issues/18351
[`python-gitlab`]: https://github.com/gpocentek/python-gitlab
[d4a24a5c4d]: https://github.com/gpocentek/python-gitlab/commit/d4a24a5c4dc54ac03b917723347047e3995afcc9
[python-gitlab-config]: http://python-gitlab.readthedocs.io/en/stable/cli.html#configuration
