
REM git submodule foreach --recursive git add -A
REM git submodule foreach --recursive git add -A
REM git commit -m "new generated pages"

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
