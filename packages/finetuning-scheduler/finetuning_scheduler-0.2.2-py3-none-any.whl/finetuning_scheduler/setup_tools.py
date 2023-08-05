#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import re
from pathlib import Path
from typing import List, Optional

_PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(__file__))).parent
_TH = os.path.join(_PROJECT_ROOT, "tests/helpers")


def _load_requirements(
    path_dir: str, file_name: str = "base.txt", comment_char: str = "#", pl_commit: Optional[str] = None
) -> List[str]:
    """Load requirements from a file.

    >>> _load_requirements(_TH, file_name="req.txt")  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    direct dependency req 'git+https://github.com/t/test.git@test' has been pruned from the provided requirements
    direct dependency req 'http://github.com/user/repo/tarball/master' has been pruned from the provided requirements
    ['ok']

    >>> _load_requirements(_TH, file_name="req.txt", pl_commit='ok')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    direct dependency req 'git+https://github.com/t/test.git@test' has been pruned from the provided requirements
    direct dependency req 'http://github.com/user/repo/tarball/master' has been pruned from the provided requirements
    attempting dev setup with specific pytorch lightning commit: ok
    ['ok', 'lightning @ git+https://github.com/Lightning-AI/lightning.git@ok#egg=lightning']
    """
    with open(os.path.join(path_dir, file_name)) as file:
        lines = [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        # filer all comments
        if comment_char in ln:
            ln = ln[: ln.index(comment_char)].strip()
        # skip directly installed dependencies
        if ln.startswith(("http", "git+")) or "@http" in ln:
            print(f"direct dependency req '{ln}' has been pruned from the provided requirements")
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)
    if pl_commit:
        print(f"attempting dev setup with specific pytorch lightning commit: {pl_commit}")
        pldev_base = "lightning @ git+https://github.com/Lightning-AI/lightning.git@"
        pldev_egg = "#egg=lightning"
        pldev_setup_req = pldev_base + pl_commit + pldev_egg
        reqs.append(pldev_setup_req)
    return reqs


def _load_readme_description(path_dir: str, homepage: str, version: str) -> str:
    """Load readme as description.

    >>> _load_readme_description(_PROJECT_ROOT, "", "")  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '<div align="center">...'
    """
    path_readme = os.path.join(path_dir, "README.md")
    version_prefix = "v"  # standard prefix used for tagging versions
    text = open(path_readme, encoding="utf-8").read()

    github_source_url = os.path.join(homepage, "raw", version_prefix + version)
    # replace relative repository path to absolute link to the release
    #  do not replace all "docs" as in the readme we reger some other sources with particular path to docs
    text = text.replace("docs/source/_static/", f"{os.path.join(github_source_url, 'docs/source/_static/')}")

    # readthedocs badge
    text = text.replace("badge/?version=stable", f"badge/?version={version}")
    text = text.replace(
        "finetuning-scheduler.readthedocs.io/en/latest/", f"finetuning-scheduler.readthedocs.io/en/{version}"
    )
    # codecov badge
    text = text.replace("/branch/main/graph/badge.svg", f"/release/{version}/graph/badge.svg")
    # replace github badges for release ones
    text = text.replace("badge.svg?branch=main&event=push", f"badge.svg?tag={version}")
    # Azure...
    text = text.replace("?branchName=main", f"?branchName=refs%2Ftags%2F{version}")
    text = re.sub(r"\?definitionId=\d+&branchName=main", f"?definitionId=2&branchName=refs%2Ftags%2F{version}", text)

    skip_begin = r"<!-- following section will be skipped from PyPI description -->"
    skip_end = r"<!-- end skipping PyPI description -->"
    text = re.sub(rf"{skip_begin}.+?{skip_end}", "<!--  -->", text, flags=re.IGNORECASE + re.DOTALL)
    return text
