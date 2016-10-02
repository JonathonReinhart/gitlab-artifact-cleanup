gitlab-artifact-cleanup
=======================

Currently (as of GitLab 8.12) there are no admin tools for cleaning up
build artifacts (see issue [#18351]). This script erases build artifacts
using the GitLab API.

## Requirements
- [`python-gitlab`] - My fork must be used until [PR 159] is accepted.

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
[`python-gitlab`]: https://github.com/JonathonReinhart/python-gitlab
[PR 159]: https://github.com/gpocentek/python-gitlab/pull/159
[python-gitlab-config]: http://python-gitlab.readthedocs.io/en/stable/cli.html#configuration
