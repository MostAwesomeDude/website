title: Copious Spare Time
type: generic
slug: cst
datetime: 2011-11-18 00:00:00
---

Copious Spare Time
==================

I do two things well: Play music, and write code. This is what I do when I'm
all out of music.

Paid
----

Stuff in this category will eventually be finished simply because I'm getting
paid for it, which guarantees that a large, fixed amount of my time is
dedicated to it.

 * Ganeti Web Manager. http://code.osuosl.org/projects/ganeti-webmgr
 * Django Object Permissions.
   http://code.osuosl.org/projects/object-permissions
 * Twisted VNC Authentication Proxy.
   http://code.osuosl.org/projects/twisted-vncauthproxy
 * txWS. http://github.com/MostAwesomeDude/txWS

Unpaid
------

Stuff here is almost completely boredom-motivated. If you want to see
something move up on my list of priorities, you should click on my Paypal
button and tell me in the notes what you like to see me working on.

 * DCoN.
 * Lye. The Lybrary is slowly getting fleshed out, and it should be complete
   enough for useful things soon.
 * Gallium.

   * Galahad. Just about every assert in driver code should be moved up to the
     Galahad layer and shared between all drivers. This might already be done.
   * Docs. Gallium's docs aren't API-complete or feature-complete.

     * Consider adapting the current C header comments into the documentation,
       to avoid having to rewrite the original comments in ReST.
     * In addition to a technical overview and API, document some examples or
       other forms of developer brain dump in order to provide more useful
       documentation to newbies.

   * Pylladium. Listed here because it relies on Gallium. Needs to be
     finished, although it might not matter that much these days.

 * PyFluidSynth. Already far ahead of the other Python-FluidSynth bindings,
   but at some point it should get API-complete.

   * For that matter, Salsa needs to be completed, since that was the original
     reason for developing PyFluidSynth. Salsa's unfortunately on hiatus, but
     all the Salsa-related art and music is still on schedule.

 * Linux. A variety of projects await.

   * The LeapFrog Didj and Explorer have open-source kernel patches floating
     out there. A good, Linux-style set of platform drivers and platform
     support should be written at some point. Currently stalled on getting my
     Didj back in working order, or obtaining an Explorer.

     * The Didj and Explorer machine files need to have
       .video_start/.video_end filled out. This fixes the current problematic
       video setup, where VRAM isn't known to Linux but is instead reserved by
       limiting the total system memory. This should allow us to remove the
       entire configurable memory system and switch to standard RAM
       auto-detection.
     * The GPIO pins have a strange interrupt-sharing scheme. Other platforms
       use virtual interrupts and an interrupt demuxer; this is completely
       viable for Pollux as well.

   * KMS.

     * ATI Rage 128. Can be done inside the current radeon kernel module.
       Would require userspace updates. I have experimental patches for this
       that need to be solidified and sent upstream.
     * Voodoo Banshee. Would require userspace updates, but be so gratifying.
       James Simmons has already started on this. I now have multiple Voodoos,
       so nothing's really standing in the way.
     * XGI Volari. Supposedly a Direct3D 9-class chipset, meaning that Gallium
       drivers could be written once the kernel backend is in place. This is
       definitely a non-trivial task since the documentation for the chipset
       is sparse and almost entirely in C.
     * Matrox G450 and other G-series chipsets. There's a lot of code
       consolidation that could happen here. Anybody tackling this would get
       to experience the joyful adventure of making the Matrox DRI work again
       as well.
     * SiS USB adapters.

Maintenance
-----------

I wrote this stuff, but I'm not touching it at the moment either because I'm
not **that** bored or because it doesn't need updates.

 * Construct. Full-on maintenance mode.

Retired
-------

Never touching this again without good reason.

 * Hackabot. I didn't write this, and I don't need to write anything else for
   it. Mike's maintaining it and doing just fine.
 * Gallium r300 driver. Dave and Marek are maintaining r300g *de facto*.
 * Kong. Nothing more to write, I think. Additionally, I don't care about it
   anymore.
 * Tiger. Ditto.
 * alsa-patch-bay. I have no contact from original upstream, no contact from
   distros that don't have it, etc. The Fedora bug's started moving again.
 * utripper. It's just sitting there, really. Talk with the John guys
   indicates that there might not be much optimization possible, and more
   modern trippers seem to be doing GPU-based stuff.
 * ttk. Meh. There's no longer any point to this.
 * Pydra. http://pydra-project.osuosl.org/ and
   http://code.osuosl.org/projects/pydra
 * Bravo. I can't deal with Minecraft communities any longer. I won't work on
   it for free.
