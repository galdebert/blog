---
title: "How to write a blog in markdown, using Hugo and Github"
date: 2018-01-18T16:56:13+01:00
draft: false
menu: main
---

I wanted to start a blog about programming, keeping things very minimal, writing just markdown. I tried Hugo, a static page generators along with github pages that host your generated pages. Let's go through the steps for you to get your blog online.

# Create your github repositories

One thing that is was not super clear to me at first was whether the sources (markdown...) should live in the same repo as the generated pages (html...).
Actually, not only there is no need mix sources and generated pages, but it's much simpler and cleaner to fully separate those. So let's have 2 repositories:

- **create a repo named _username_/github.io**
  - You have to respect this name pattern
  - This will contain the generated pages
  - For me the repo is https://github.com/galdebert/galdebert.github.io
  - Clone it in a local _username_/github.io folder (for me: galdebert.github.io)
  - Look at https://pages.github.com/ for more details
- **create a repo named blog**
  - You can use any other name you like
  - This will contains the sources (markdown...) of your blog
  - For me the repo is https://github.com/galdebert/blog
  - Clone it in a local blog folder

# Install Hugo

The [install page](https://gohugo.io/getting-started/installing/) has everything you need. Here is a quick 2 steps install summary for windows:

## 1. Install chocolatey

I'm mostly on windows these days, and installing hugo was the occasion to install chocolatey, (one of) the package manager for Windows. I have little experience with chocolatey, but this looks very good. From now on, I'll try using chocolatey as often as possible.

You should read: https://chocolatey.org/install, one option that worked for me was to run the following command from a powershell (ran as administrator):
```
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

## 2. Install hugo with chocolatey

From a cmd prompt (ran as administrator):
```
choco install hugo -confirm
```

The hugo [install page](https://gohugo.io/getting-started/installing/) tells you to install Pygments, but the hugo syntax [highlighting page](https://gohugo.io/content-management/syntax-highlighting/) says there is a built-in default syntax hightlighter named Chroma. Ok, good, let's not install Pygments then.


# Creating your blog content

More details here: http://gohugo.io/getting-started/quick-start/

## 1. Create the basic directory structure

In your blog directory:
```
hugo new site . --force
```
`--force` allows to write in the directory even if it's not empty (it already has the usual .git, README, LICENSE).

## 2. Download and use a theme
```
git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
```
and add the following line to `config.toml`
```
theme = "ananke"
```
There are tons of other themes here: https://themes.gohugo.io/

## 3. Add some content

```
hugo new posts/my-first-post.md
```
This creates the file: `./content/posts/my-first-post.md`<br>
You can also create the file manually, but `hugo new` adds a few lines at the start of the md file:
```
---
title: "My First Post"
date: 2018-01-19T12:58:17+01:00
draft: true
---
```
called "front matter". Among other things, this allows hugo to organize your posts (links, sort by date...) in the generated html.

## 4. Generate the html and serve it locally

```
hugo server -D
```
-D means: include content marked as draft

View the locally generated html in your browser at `http://localhost:1313/`

Now the html is automatically generated everytime the content is changed. So you can see your changes in realtime, everytime the markdown files are saved to disk.


## 5. Modify Themes

The hugo doc tells you that you should customize a theme by creating files in your blog folder. So `blog/themes/hyde/static/css/hyde.css` is overriden by your manually created in `blog/static/css/hyde.css`. The idea is that this way you don't modify the original theme and instead yu only applies minimal changes.

But this seems a bit awkward to me:

- How does the overriding mechanism mechanism work? Is the granularity per file? If yes, this sounds "not very minimal to me. If no, this sounds quite complicated.
- At least in these first discovery days, I want to be able to tweak theme1, tweak theme2, and change between those with one flag: `hugo server -D -t theme2`. Using theme specific files in the root folder make this impossible (or very very awkward).
- Copying files and making changes is not a proper way to track changes, we have git for that, let's use it.

Let's use the hyde theme:

- fork https://github.com/spf13/hyde in https://github.com/username/hyde
- clone your fork: `git submodule add https://github.com/galdebert/hyde themes/galdebert-hyde`
- in your `config.toml` set `theme = "galdebert-hyde"`
- Make your changes in `themes/galdebert-hyde`, commit/push them


# Publish on github pages

There are different options on the [hosting-on-github](http://gohugo.io/hosting-and-deployment/hosting-on-github/) hugo page (using /docs, gh-pages, master). But the [configuring-a-publishing-source-for-github-pages](https://help.github.com/articles/configuring-a-publishing-source-for-github-pages/) github page says: "repository named <username>.github.io are only published from the master branch". So let's do that.

In the config.toml, write the correct address of the site, for me it's :<br>
`baseURL = "https://galdebert.github.io"`<br>

We could change the publishDir to our github page local repository, ie in `config.toml`:<br>
`publishDir = "../galdebert.github.io"`<br>

But we won't do that because we want to distinguish iterate-locally-with-LiveReload from publish actions:

- **iterate-locally-with-LiveReload**
  - relies on `hugo server`
  - injects JavaScript into the generated pages that allow the LiveReload thing
  - writes generated pages in memory

- **publish**
  - writes into galdebert.github.io
  - needs to remove the content in `galdebert.github.io`, because hugo does not remove any previously generated files
  - calls plain `hugo` (not `hugo server`) with the destination folder explicitely `hugo -s path/to/galdebert.github.io`
  - you probably want to `git add`, `git commit`, `git push` after the hugo call


## python script to automate the publish step



Now write some markdown in the md file below the "front matter". Let's add aldo some python code to verify that the syntax coloring works fine:


{{<highlight python>}}
#!/usr/bin/env python3
import os
from pathlib import Path
import glob

def norm_path(path: str) -> str:
    return Path(os.path.normpath(os.path.expanduser(os.path.expandvars(path)))).as_posix()

def glob_rel(glob_expr: str, base_absdir: str) -> str:
    base_absdir = norm_path(base_absdir)
    for p in glob.iglob(glob_expr, recursive='**' in glob_expr):
        yield relpath(p, base_absdir)
{{</highlight>}}
`hugo server -wDs ~/Code/hugo/docs -d dev`
When the content is ready for publishing, use the default public/ dir:

`hugo -s ~/Code/hugo/docs`
This prevents draft content from accidentally becoming available.

