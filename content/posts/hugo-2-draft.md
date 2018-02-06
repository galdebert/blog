---
title: "Blog Tutorial using markdown, Github and Hugo - Part 2"
date: 2018-01-18
draft: true
menu: main
---


# Add comments

TODO
use disqus

# Add google analytics

TODO

# add icons

TODO

# add emojis

enableEmoji = true

# customize the layout

hugo templating

# Syntax Highligthing

TODO

# inject an existing file (instead of copy-paste it in your markdown)

TODO

# remove old commits in your generated pages

TODO

# Learn by example

Get themes and look into their files

hugo server -v



# python file

Same thing using `publish.py`

{{< highlight python >}}
#!/usr/bin/env python3

import os
import subprocess
from distutils.dir_util import copy_tree
from contextlib import contextmanager

@contextmanager
def chg_cwd(path: str):
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)

# check=True will raise an exception if returncode != 0
# it's like subprocess.chek_output() but we still want to print output even if returncode != 0
def run(cmd, check: bool):
    print(' '.join(cmd))
    completed = subprocess.run(cmd, check=check, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(completed.stdout.decode("utf-8"))
    if check and completed.returncode != 0:
        raise subprocess.CalledProcessError

blog = os.path.dirname(os.path.abspath(__file__))
generated = os.path.normpath(os.path.join(blog, '../galdebert.github.io'))
to_copy = os.path.join(blog, 'to_copy')

run(['hugo', '--cleanDestinationDir', '-d', generated], check=True)
copy_tree('./to_copy', generated)

with chg_cwd(generated):
    run(['git', 'add', '-A'], check=True)
    # git commit returns 1 if there is nothing to commit
    run(['git', 'commit', '-m', 'new generated pages'], check=False)
    run(['git', 'push'], check=True)
{{< /highlight >}}



# hugo content management

https://gohugo.io/content-management/organization/

content
+ about
  + _index.md   // <- https://example.com/about/



    example/content/posts
=> generates => 
https://example.com/posts/index.html

section = posts"


# _index.md

_index.md has a special role in Hugo. It allows you to add front matter and content to your list templates. These templates include those for section templates, taxonomy templates, taxonomy terms templates, and your homepage template.

Tip: You can get a reference to the content and metadata in _index.md using the .Site.GetPage function.


# gravatar

in Hyde-X
[params]
    gravatarHash = "MD5 hash of your Gravatar email address"
    
    # Sidebar social links, these must be full URLs.
    github = ""
    bitbucket = ""
    stackOverflow = ""
    linkedin = ""
    googleplus = ""
    facebook = ""
    twitter = ""
    youtube = ""