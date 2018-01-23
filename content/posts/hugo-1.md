---
title: "Publish a blog using markdown, Github and Hugo"
date: 2018-01-23
draft: false
menu: main
---

I wanted to start a blog about programming, keeping things very minimal, writing just markdown. I tried Hugo + Github pages, let's go through the steps to get your markdown powered blog online.

<!--more-->

Note that I don't know if Hugo + Github pages is better than any alternative. But I thought it was better to get something done instead of hesitating forever about the "best" solution.

# Create your github repositories

One thing that was not super clear to me at first was whether the sources (markdown...) should live in the same repo as the generated pages (html...).
Actually, not only there is no need mix sources and generated pages, but it's much simpler and cleaner to fully separate those. So let's have 2 repositories:

**create a repo named _username_/github.io**

- You have to respect this name pattern
- This will contain the generated pages
- For me the repo is https://github.com/galdebert/galdebert.github.io
- Clone it in a local _username_/github.io folder (for me: galdebert.github.io)
- Look at https://pages.github.com/ for more details

**create a repo named blog**

- You can use any other name you like
- This will contains the sources (markdown...) of your blog
- For me the repo is https://github.com/galdebert/blog
- Clone it in a local blog folder


# Install Hugo

The [install page](https://gohugo.io/getting-started/installing/) has everything you need. Here is a quick 2 steps install summary for windows:

## 1. Install chocolatey

I'm mostly on windows these days, and installing hugo was the occasion to install chocolatey, (one of) the package manager for Windows. I have little experience with chocolatey, but this looks very good. From now on, I'll try using chocolatey as often as possible.

You should read https://chocolatey.org/install, one option that worked for me was to run the following command from a powershell (ran as administrator):
```
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

## 2. Install hugo with chocolatey

In your terminal (ran as administrator):
```
choco install hugo -confirm
```

The hugo [install page](https://gohugo.io/getting-started/installing/) tells you to install Pygments, but the [hugo syntax highlighting page](https://gohugo.io/content-management/syntax-highlighting/) says there is a built-in default syntax hightlighter named Chroma. Ok, good, let's not install Pygments then.


# Creating your blog content

More details here: http://gohugo.io/getting-started/quick-start/

## 1. Create the basic directory structure

In your blog directory:
```
hugo new site . --force
```
`--force` allows to write in the directory even if it's not empty (it already has the usual .git, README, LICENSE).

## 2. Download and use a theme

In your blog directory:
```
git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
```
and add the following line to `config.toml`
```
theme = "ananke"
```
There are tons of other themes here: https://themes.gohugo.io/

## 3. Add some markdown

In your blog directory:
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
called "front matter". This sets parameters to your markdown file that hugo and the current theme can read to generate html.

## 4. Generate the html and serve it locally

In your blog directory:
```
hugo server -D
```
`-D` means: include content marked as draft

View the locally generated html in your browser at `http://localhost:1313/`

Now the html is automatically generated everytime the content is changed. So you can see your changes in realtime, everytime the markdown files are saved to disk.

A couple of interesting notes about `hugo server`:

- It writes generated pages in memory, so you won't find any generated pages on your disk
- It injects JavaScript into the generated pages that allow the LiveReload thing

## 5. Modify Themes

The hugo doc tells you that you should customize a theme by creating files in your blog folder. So `blog/themes/hyde/static/css/hyde.css` is overriden by your manually created `blog/static/css/hyde.css` file. The idea is that you don't modify the original theme and instead you only apply minimal changes.

But this seems a bit awkward to me:

- How does the overriding mechanism work? Is the granularity per file? If yes, this sounds "not very minimal to me. If no, this sounds quite complicated.
- At least in these first discovery days, I want to be able to tweak theme1, tweak theme2, and change between those with one flag: `hugo server -D -t theme2`. Using theme specific files in the root folder make this impossible (or very very awkward).
- To track changes, and merge stuff, we have git, let's use it.

Let's use the hyde theme:

- fork https://github.com/spf13/hyde
- clone your fork: `git submodule add https://github.com/galdebert/hyde themes/galdebert-hyde`
- in your `config.toml` set `theme = "galdebert-hyde"`
- Make your changes in `themes/galdebert-hyde`, commit/push them


# Publish on github pages

First change `draft: true` to `draft: false` at the top of your markdown file.

There are different options on [this hugo doc page](http://gohugo.io/hosting-and-deployment/hosting-on-github/) (using /docs, gh-pages, master). But [this github help page](https://help.github.com/articles/configuring-a-publishing-source-for-github-pages/) says: "repository named <username>.github.io are only published from the master branch". So let's do that.

In the config.toml, write the correct address of the online site, for me it's :<br>
`baseURL = "https://galdebert.github.io/"`<br>
Be careful, the trailing / is mandatory. Without it, everything was fine locally, but the site was broken online.

Here are the steps to publish:

1. call plain `hugo` (not `hugo server`)
  - with the destination folder explicitely `-d ../galdebert.github.io` (in my case)
  - with `--cleanDestinationDir` that clears the destination folder first (this keeps the .git subfolder)
2. `git add`, `git commit`, `git push`


Here is a bash/cmd script that publishes, provided that `galdebert.github.io` and `blog` share the same parent dir:
```
hugo --cleanDestinationDir -d ../galdebert.github.io
cd ../galdebert.github.io
git add -A
git commit -m "new generated pages"
git push
cd ../blog
```

To also commit+push the `blog` repo and its `themes/galdebert-hyde` submodule:
```
cd themes/galdebert-hyde
git add -A
git commit -m "new template sources"
git push

cd ../..
git add -A
git commit -m "new blog sources"
git push

hugo --cleanDestinationDir -d ../galdebert.github.io
cd ../galdebert.github.io
git add -A
git commit -m "new generated pages"
git push

cd ../blog
```

# A few tips

- Hugo extracts summaries from your posts, by brutally taking their first N words. To limit the extracted summaries, add `<!--more-->` where your post introduction finishes.
- Browser cache can be super annoying, [this](https://superuser.com/questions/173210/how-can-i-clear-a-single-site-from-the-cache-in-firefox) was a life saver (read the 2 best answers).
- You should keep an eye on the terminal where you started the `hug server`, Hugo errors are logged there and can be very useful when you mess up.
