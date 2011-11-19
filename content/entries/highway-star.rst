title: Highway Star
type: entry
category: entries
datetime: 2011-08-09 02:03:29
---

I have a Chromebook_. Specifically, a Samsung Series 5, courtesy of Google_.
It's pretty snazzy, but what's really great is that the "Chrome OS" which it
comes with is actually a modified `Gentoo Linux`_. Cool, right?
Unfortunately, the Chromebook is a bit too hobbled for generic Gentoo usage,
but I will outline the steps I have taken towards getting mine to a point
where I'm happy with it.

When modding hardware, especially hardware over which one has limited control,
it's good to set a goal, so I'll outline my goal in terms of what I usually do
on traveling laptops: Games and music. Since there's usually a pretty heavy
limit on disk space, but plenty of bandwidth, I want to be able to access some
kind of music stream, and as far as games, I'll go with a selection of small
puzzles as well as classic emulators. In particular, I want to have Pianobar_
(media-sound/pianobar), `Simon Tatham's Puzzles`_ (games-puzzle/sgt-puzzles),
and either VBA-M_ (games-emulation/vbam) or ZSNES_ (games-emulation/zsnes).

First things first: Let's get access to the shell. Two keyboard commands to
know (which have no mouse equivalents!) are the classic Alt+Tab, for switching
between windows, as well as Alt+Shift+Tab for going through the window list
backwards, and also the common Ctrl+Alt+T, which spawns a shell. On a
Chromebook, the shell provided by default is "crosh", a remarkably useless
shell mostly provided for diagnostics. Crosh has a secret command, "shell",
which spawns a real shell, bash! However, we can't get to it until `Developer
Mode`_ has been enabled. After Developer Mode is enabled, crosh will now
permit us to get a real shell, and the real fun can begin.

As a user on the filesystem, we are always under the login "chronos". We can
sudo freely and without limit; invocations like ``sudo -i`` to gain root shell
access work as expected. Let's take a look at what's in the filesystem at the
moment.

(Aside: If you just want to know how I got stuff working on my Chromebook,
skip the next few paragraphs; I'm going to talk about my though processes and
the current state of what I know about the machine. Interesting stuff,
perhaps, but not really directly relevant to getting up and running.)

::

    chronos@localhost ~ $ mount
    rootfs on / type rootfs (rw)
    /dev/root on / type ext2 (ro,relatime)
    devtmpfs on /dev type devtmpfs (rw,size=970408k,nr_inodes=242602,mode=755)
    none on /proc type proc (rw,nosuid,nodev,noexec,relatime)
    none on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
    /tmp on /tmp type tmpfs (rw,nosuid,nodev,noexec,relatime)
    udev on /dev type tmpfs (rw,nosuid,noexec,relatime,mode=755)
    shmfs on /dev/shm type tmpfs (rw,nosuid,nodev,noexec,relatime)
    devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620)
    /dev/sda1 on /mnt/stateful_partition type ext3
    (rw,nosuid,nodev,noexec,relatime,errors=continue,commit=600,data=ordered)
    /dev/sda1 on /var type ext3
    (rw,nosuid,nodev,noexec,relatime,errors=continue,commit=600,data=ordered)
    /dev/sda1 on /home type ext3
    (rw,nosuid,nodev,noexec,relatime,errors=continue,commit=600,data=ordered)
    varrun on /var/run type tmpfs (rw,nosuid,nodev,noexec,relatime,mode=755)
    varlock on /var/lock type tmpfs (rw,nosuid,nodev,noexec,relatime)
    /media on /media type tmpfs (rw,nosuid,nodev,noexec,relatime)
    debugfs on /sys/kernel/debug type debugfs (rw,relatime)
    cgroup on /tmp/cgroup/cpu type cgroup (rw,relatime,cpu)
    /home/.shadow/d72e888592600e3025a778270172192458d0a039/vault on
    /home/chronos/user type ecryptfs
    (rw,nosuid,nodev,relatime,ecryptfs_sig=6c1fcef0779bc58d,ecryptfs_fnek_sig=997328e527b573bc,ecryptfs_cipher=aes,ecryptfs_key_bytes=16,ecryptfs_unlink_sigs)
    chronos@localhost ~ $ df -h
    Filesystem            Size  Used Avail Use% Mounted on
    rootfs                837M  548M  290M  66% /
    /dev/root             837M  548M  290M  66% /
    devtmpfs              948M  472K  948M   1% /dev
    /tmp                  948M   24M  925M   3% /tmp
    udev                  948M  472K  948M   1% /dev
    shmfs                 948M  256K  948M   1% /dev/shm
    /dev/sda1              11G  3.4G  6.7G  34% /mnt/stateful_partition
    /dev/sda1              11G  3.4G  6.7G  34% /var
    /dev/sda1              11G  3.4G  6.7G  34% /home
    varrun                948M   68K  948M   1% /var/run
    varlock               948M     0  948M   0% /var/lock
    /media                948M     0  948M   0% /media
    /home/.shadow/d72e888592600e3025a778270172192458d0a039/vault
                           11G  3.4G  6.7G  34% /home/chronos/user

What a list of mounts! I'll try to explain. The rootfs and kernel each live on
partitions not mounted during normal operation, and are generally reasonably
protected. Modifying them is beyond what I will discuss today, but rest
assured that they are there and modifiable if developer-mode BIOS is enabled.
(All the gory details are on the Chromium OS wiki, linked above.) If we want
to avoid making changes which can be easily wiped out, then we will have to
consider an alternative approach to modifying the rootfs. There is apparently
a way to cook an entirely-new Chromium OS image, but I'm going to avoid that
for a pair of reasons:

 * The build process takes a fair amount of space and time
 * The image has to be respun for every update

These two things wouldn't be that big of a deal, if I knew exactly what I
wanted ahead of time and didn't plan to update more than every three months or
so. However, knowing the speed of Gentoo, this isn't going to be reasonable.
Moreover, there are a few things missing from the Chrome OS rootfs: Portage
and a compiler, to say nothing of Python. There aren't even the tools for
bootstrapping a stage3. Also, look at how much space is allocated to the
default rootfs: 840MiB, nowhere near enough to get anywhere when it's already
two-thirds full. An alternate approach sounds better.

Can't we just wipe the entire SSD and put a standard Gentoo install on it?
Well, no. There's a couple obstacles. First, how does one get into a live
Gentoo environment? We can't boot from USB or MMC/SD into a non-Chrome OS
environment, thanks to a verified bootloader. We can't access the deepest
bootloaders easily; while an EFI loader is shipped onboard, it appears to be
unused, and documentation points to a signed kernel loader being used instead.
This is frustrating, because it means that we have to use the same kind of
partitioning as the current system, and we have to sign our kernels. While the
tools are all there in the Chromium OS repositories, I didn't feel like going
through the ardour of figuring out how to put it all together and flashing my
device multiple times to get it all going. (I'm lazy like that; if some
enterprising developer wants to do it, please, go ahead!) So, we'll stick to
userspace modifications.

The next thing I noticed: chroot is available in the rootfs! This could get us
into a Gentoo environment! But what would we do in there? We can't install
things directly onto the rootfs or stateful partition, and we can't change the
partition table. Either one would wreck the Chrome OS boot pretty thoroughly.
But, we could always go the brutish, lazy route, and simply have a chroot
*in our home directory*. Getting at our Portage and compiler would be
as easy as invoking chroot, and we could still have the rest of the system
(Chrome, WiFi manager, battery monitor, terminal emulator, window manager) at
our disposal. Excellent.

How much disk space would this take? It sounds wasteful. As you may have
noticed from the above filesystem readout, though, it only adds about 2.8GiB
for an entire chroot with everything I like to have in my minimal Gentoo
systems. I'm a bit of a pig, but even so, it's possible to have a very
slimmed-down chroot.

So, let's get started. First, create your chroot directory in your home,
calling it "chroot" or something like that. You can go ahead and be root for
this. In fact, get comfortable being root; you will always be root in your
chroot. I mean, seriously, why not? There's all the traditional reasons to not
be root, but the Chrome OS is a brand-new world, a world where people can be
root inside a chroot inside a cryptfs inside a single-user system inside
**the cloud**.

.. _Gentoo Handbook's Chroot Guide: http://www.gentoo.org/proj/en/base/x86/chroot.xml

You should have the `Gentoo Handbook's Chroot Guide`_ open while you do this,
as what we are doing is quite similar. The one catch is that you *must* be
root in order to create all the device nodes. Once your chroot is in place,
the following script will enter the chroot: https://gist.github.com/1128864
Just put it in your home directory, ``chmod +x`` it, and we're almost ready to
go!

Oops, wait, what's with this cryptic "bad interpreter" error? For security
reasons, most filesystems are mounted noexec. Sadly, there's no good place to
put a shell script to turn it off, so I instead encourage you to memorize
``mount -i -o remount,exec ~``. It rolls right off the tongue! You only have
to do this once, at boot, but you can't put it in the rootfs without alerting
Chrome OS to our shenanigans. If Chrome OS gets ticked enough at our meddling,
it will destroy the entire stateful partition, including the chroot. (If you
want to keep your chroot on a USB drive or SD card, I would totally
understand!)

There are a few more things required to get all of the things in the chroot
working. Presumably you will eventually want to run applications which talk to
the local X11 server; for that, you will need to add a single line to your
.bashrc inside the chroot::

    export XAUTHORITY="/root/.Xauthority"

So, now that we're inside our chroot, and have everything wired up, it's time
to start experimenting. I've gone ahead and selected the following USE flags::

    USE="X alsa ao mmx opengl sse sse2 sse3 -cups -xscreensaver"

And here's the package list in my world file (/var/lib/portage/world)::

    app-admin/localepurge
    app-editors/vim
    app-misc/screen
    app-portage/eix
    app-portage/genlop
    app-portage/gentoolkit
    app-portage/ufed
    games-emulation/vbam
    games-emulation/zsnes
    games-puzzle/sgt-puzzles
    media-sound/pianobar
    net-im/pidgin
    x11-apps/mesa-progs
    x11-apps/xauth
    x11-apps/xdpyinfo
    x11-apps/xhost

You may notice that I emerged things I don't technically need. This is because
I am a creature of habit, and several things nearly always make their way into
my list, like vim, eix, genlop, gentoolkit, and ufed. I emerged all of the X
and GL programs to help debug X issues; they are not necessary at all for you
as long as you have set up .Xauthority as I have.

You may also notice that I grabbed localepurge. I highly recommend trimming
the fat from your chroot with localepurge; that and trimming the categories
from your Portage tree (do you really need ``sci-*``?) are going to save
around 500MiB if done zealously.

With the current setup, pianobar Just Works. sgt-puzzles installs its binaries
as games, so you will have to make sure that, when chrooted, your user has the
games group set. This is the purpose of that mystical ``--groups=35`` on the
chroot invocation -- 35 is the GID of the games group! This is definitely the
cleanest solution. With that added, sgt-puzzles works. Two of four.

.. _Chromebook: http://en.wikipedia.org/wiki/Chromebook
.. _Google: http://google.com/
.. _Gentoo Linux: http://www.gentoo.org/
.. _Pianobar: https://github.com/PromyLOPh/pianobar
.. _Simon Tatham's Puzzles: http://www.chiark.greenend.org.uk/~sgtatham/puzzles/
.. _VBA-M: http://vba-m.com/
.. _ZSNES: http://zsnes.com/
.. _Developer Mode: http://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices/samsung-series-5-chromebook
