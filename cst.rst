Copious Spare Time
==================

I do two things well: Play music, and write code. This is what I do when I'm
all out of music.

Paid
----

Stuff in this category will eventually be finished simply because I'm getting
paid for it, which guarantees that a large, fixed amount of my time is
dedicated to it.

 * Pydra. Listed here for completeness and boss appeasement, since Pydra
   progress is tracked on the official bug tracker at
   http://pydra-project.osuosl.org/.

Unpaid
------

Stuff here is almost completely boredom-motivated. If you want to see
something move up on my list of priorities, you should click on my nonexistent
Paypal button.

 * Gallium.

   * Galahad. Just about every assert in driver code should be moved up to the
     Galahad layer and shared between all drivers.
   * Docs. Gallium's docs aren't API-complete or feature-complete.

     * Consider adapting the current C header comments into the documentation,
       to avoid having to rewrite the original comments in ReST.
     * In addition to a technical overview and API, document some examples or
       other forms of developer braindump in order to provide more useful
       documentation to newbies.

   * Pylladium. Listed here because it relies on Gallium. Needs to be
     finished.

 * PyFluidSynth. Already far ahead of the other Python-FluidSynth bindings,
   but at some point it should get API-complete.

   * For that matter, Salsa needs to be completed, since that was the original
     reason for developing PyFluidSynth.

 * DarkLight. Possibly the most important thing on the unpaid list.

   * Finish the GUI. It's really not that hard of a task.
   * Convince people to deploy it, and start stress-testing it with real data.
   * Anything else in the README; there's plenty of things to go after.

 * Linux. A variety of projects await.

   * The LeapFrog Didj and Explorer have open-source kernel patches floating
     out there. A good, Linux-style set of platform drivers and platform
     support should be written at some point. Currently stalled on getting my
     Didj back in working order, or obtaining an Explorer.

   * KMS.

     * ATI Rage 128. Can be done inside the current radeon kernel module.
       Would require userspace updates. Currently stalled on getting my r128
       to actually boot.
     * Voodoo Banshee. Would require userspace updates, but be so gratifying.
       James Simmons has already started on this. Currently stalled on getting
       my older AGP board, the only one that fits the Banshee, booting again.
     * XGI Volari. Supposedly a Direct3D 9-class chipset, meaning that Gallium
       drivers could be written once the kernel backend is in place. This is
       definitely a non-trivial task since the documentation for the chipset
       is sparse and almost entirely in C.

Maintenance
-----------

I wrote this stuff, but I'm not touching it at the moment either because I'm
not **that** bored or because it doesn't need updates.

 * Hackabot. I didn't write this, and I don't need to write anything else for
   it. Mike's maintaining it and doing just fine.
 * Gallium r300 and r600 drivers. Marek's maintaining r300g *de facto*, and
   Jerome's r600g ended up getting merged instead of mine. 
 * Kong. Nothing more to write, I think.
 * Tiger. Ditto.
 * Dioxide. Porting the last of it to CSound right now, and once that's done,
   further development probably won't affect the old codebase.
 * alsa-patch-bay. I have no contact from original upstream, no contact from
   distros that don't have it, etc. Might change at some point.
 * utripper. It's just sitting there, really.
 * magicpoint. Ditto.
 * ttk. Meh.
