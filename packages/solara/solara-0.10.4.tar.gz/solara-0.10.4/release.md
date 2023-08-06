
# Fully automated

    $ ./release.sh patch


## Making an alpha release


    $ ./release.sh patch --new-version 0.10.4a1


# semi automated
To make a new release
```
# update react-ipywidgets/_version.py
$ git add -u && git commit -m 'Release v0.10.4' && git tag v0.10.4 && git push upstream master v0.10.4
```


If a problem happens, and you want to keep the history clean
```
# do fix
$ git rebase -i HEAD~3
$ git tag v0.10.4 -f &&  git push upstream master v0.10.4 -f
```
