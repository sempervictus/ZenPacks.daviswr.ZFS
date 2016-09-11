# ZenPacks.daviswr.ZFS

ZenPack to model & monitor ZFS pools and datasets

## Requirements

* Solaris or Illumos-based OS, or Linux with [ZFS-on-Linux (ZoL)](http://zfsonlinux.org/)
  * Only tested with Debian 7 with ZoL 0.6.5 so far...
* An account on the ZFS-capable host, which can
  * Log in via SSH with a key
  * Run the `zdb`, `zpool`, and `zfs` commands with certain parameters without password via `sudo`

Example entries in `/etc/sudoers`

```
Cmnd_Alias ZDB = /sbin/zdb -L
Cmnd_Alias ZPOOL = /sbin/zpool get -pH all, /sbin/zpool iostat -y 1 1, /sbin/zpool status -v
Cmnd_Alias ZFS = /sbin/zfs get -pH all
zenoss ALL=(ALL) NOPASSWD: ZDB, ZPOOL, ZFS
```
## Illumos notes
Being a ZoL user, I don't have an Illumos system handy to develop against, so everything uses `sudo` rather than `pfexec` and paths to things are `/sbin` rather than `/usr/sbin`.

That said, this ZenPack's still a work in progress; all of the `zdb`, `zpool`, and `zfs` parameters should work on an Illumos system, at least. Some [patient](https://github.com/Crosse) SmartOS-using [friends](https://github.com/baileytj3) have helped me with that.

## Usage

I'm not going to make any assumptions about your device class organization, so it's up to you to configure the `daviswr.cmd.ZPool` and `daviswr.cmd.ZFS` modelers on the appropriate class or device. The ZPool modeler must be higher in the list of modelers than the ZFS one.
