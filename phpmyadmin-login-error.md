---
title: phpMyAdmin login error to remote server
date: '2013-11-11 16:20:07 +0800'
---

# 2013-11-11  phpMyAdmin login error to remote server

I have a fresh install of Ubuntu 13.10 and phpMyAdmin version 4:4.0.6-1 . I add a remote server in config.inc.php for multiple server management. But phpMyAdmin failed to login to remote server.

there are following error logs in `/var/log/apache2/error.log`

```text
PHP Fatal error:  Call to a member function getPresence() on a non-object in /usr/share/phpmyadmin/libraries/navigation/NavigationTree.class.php on line 1046
```

The code of `NavigationTree.class.php` at 1046 are

```text
1039         } else if (($node->type == Node::CONTAINER
1040             && (   $node->real_name == 'tables'
1041                 || $node->real_name == 'views'
1042                 || $node->real_name == 'functions'
1043                 || $node->real_name == 'procedures'
1044                 || $node->real_name == 'events')
1045             )
1046             && $node->realParent()->getPresence($node->real_name) >= (int)$GLOBALS['cfg']    ['NavigationTreeDisplayItemFilterMinimum']
1047         ) {
```

I am not sure the root cause of this issue. But I can fix this error by adding a check for if statment

```text
1039         } else if (($node->type == Node::CONTAINER
1040             && (   $node->realParent )
1041             && (   $node->real_name == 'tables'
1042                 || $node->real_name == 'views'
1043                 || $node->real_name == 'functions'
1044                 || $node->real_name == 'procedures'
1045                 || $node->real_name == 'events')
1046             )
1047             && $node->realParent()->getPresence($node->real_name) >= (int)$GLOBALS['cfg']['NavigationTreeDisplayItemFilterMinimum']
1048         ) {
```

That's it.

