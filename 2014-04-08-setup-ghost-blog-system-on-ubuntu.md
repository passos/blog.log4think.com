---
title: Setup Ghost blog system on Ubuntu
date: '2014-04-08 17:54:27 +0800'
---
## Installation

Make sure you have install all required package

    sudo apt-get install npm nodejs

Goto https://ghost.org/download/ , download the latest zip file

    $ wget https://ghost.org/zip/ghost-0.4.2.zip
    $ unzip ../ghost-0.4.2.zip -d ghost
    $ cd ghost
    $ npm install --production
    ...
    $ npm start

    > ghost@0.4.2 start /home/simon/downloads/ghost
    > node index

    Ghost is running in development...
    Listening on 127.0.0.1:2368
    Url configured as: http://my-ghost-blog.com
    Ctrl+C to shut down

Now you can browse your own Ghost blog at http://127.0.0.1:2368

> It's very possible that you got the below error when you run 
```
npm install --production
```
    > sqlite3@2.2.0 install /home/simon/downloads/ghost/node_modules/sqlite3
    > node-pre-gyp install --fallback-to-build                                                                       

    /usr/bin/env: node: No such file or directory
    npm WARN This failure might be due to the use of legacy binary "node"
    npm WARN For further explanations, please read
    /usr/share/doc/nodejs/README.Debian                                                                              

    npm ERR! sqlite3@2.2.0 install: `node-pre-gyp install --fallback-to-build`
    npm ERR! `sh "-c" "node-pre-gyp install --fallback-to-build"` failed with 127
    npm ERR!
    npm ERR! Failed at the sqlite3@2.2.0 install script.
    npm ERR! This is most likely a problem with the sqlite3 package,
    npm ERR! not with npm itself.
    npm ERR! Tell the author that this fails on your system:
    npm ERR!     node-pre-gyp install --fallback-to-build
    npm ERR! You can get their info via:
    npm ERR!     npm owner ls sqlite3
    npm ERR! There is likely additional logging output above.

    npm ERR! System Linux 3.11.0-13-generic
    npm ERR! command "/usr/bin/nodejs" "/usr/bin/npm" "install" "--production"
    npm ERR! cwd /home/simon/downloads/ghost
    npm ERR! node -v v0.10.15
    npm ERR! npm -v 1.2.18
    npm ERR! code ELIFECYCLE
    npm ERR!
    npm ERR! Additional logging details can be found in:
    npm ERR!     /home/simon/downloads/ghost/npm-debug.log
    npm ERR! not ok code 0

This error is caused by the wrong 
```
node
```
 command symblic link in your system. To fix this, run the following command, then run 
```
npm install --production
```
 again.

    sudo update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10

It should work now.

## Configuration

After start the Ghost successfully, you need to go to administration page to configure your Blog or write a new post.

First, go to 
```
http://127.0.0.1:2368/ghost/
```
. It will redirect to sign up page. 

Then, type your inforamtion and 'Sign Up', you will be redirect to the administration page.

