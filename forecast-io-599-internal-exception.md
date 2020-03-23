---
title: 'Forecast::IO 599 Internal Exception'
date: '2014-03-25 16:42:30 +0800'
---

# 2014-03-25  Forecast::IO 599 Internal Exception

Forecast.io provide great public weather data service API. They also provide SDK for many languages which is very friendly to developers.

However if you are using their Perl module Forecast::IO, maybe you will have this error when you try to install it

```text
Running make test
PERL_DL_NONLAZY=1 /usr/bin/perl "-MExtUtils::Command::MM" "-e" "test_harness(0, 'blib/lib', 'blib/arch')" t/*.t
t/forecast.t .. # Please enter your Forecast.io API key:
xxxxxxxxxxxxxxxxxxxx
Request to 'https://api.forecast.io/forecast/xxxxxxxxxxxxxxxxxxxx/43.6667,-79.4167,1373241600?units=auto' failed: 599 Internal Exception
# Looks like your test exited with 255 before it could output anything.
t/forecast.t .. Dubious, test returned 255 (wstat 65280, 0xff00)
Failed 6/6 subtests
```

The root cause of this error is Forecast::IO use HTTP::Tiny for HTTP request. And HTTP::Tiny need Net::SSLeay module to access HTTPS url. If the module was not installed HTTP::Tiny would only say 599 error and you can't know the real reason unless you look into the code and try it like below.

```text
$ perl -e "use HTTP::Tiny; use Data::Dumper; print Dumper(HTTP::Tiny->new>get('https://api.forecast.io/forecast/xxxxxxxxxxxxxxxxxxxx/43.6667,-79.4167,1373241600?units=auto'));"
$VAR1 = {
          'success' => '',
          'headers' => {
                         'content-type' => 'text/plain',
                         'content-length' => 53
                   },
          'status' => 599,
          'content' => 'Net::SSLeay 1.49 must be installed for https support',
          'reason' => 'Internal Exception',
          'url' => 'https://api.forecast.io/forecast/xxxxxxxxxxxxxxxxxxxx/43.6667,-79.4167,1373241600?units=auto'
        };
```

This is really a confused way to report this error.

Anyway, to fix this issue you only need to install the module Net::SSLeay

```text
sudo perl -MCPAN -e 'install Net::SSLeay'
```

