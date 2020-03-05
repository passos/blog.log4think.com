---
title: Accessing Facebook by LWP
date: '2013-10-30 11:09:51 +0800'
---
Usually, we can get the content of a url by the following code in Perl

    perl -MLWP::Simple -e 'getprint "http://www.google.com"';

But if you try to use it to access Facebook, like this

    perl -MLWP::Simple -e 'getprint "http://www.facebook.com"';

you will get a page "Upadte your browser" instead of the real one. That's because Facebook doesn't like the default UserAgent of LWP or WWW::Curl.

The simplest way to solve it is to change the default LWP user agent string to your own string.

    perl -e 'use LWP::Simple qw($ua get); $ua->agent("My agent/1.0"); print get "http://www.facebook.com";'

