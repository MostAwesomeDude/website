title: Secrets
type: entry
category: entries
datetime: 2011-11-29 17:03:00
---

After accidentally hitting yet another window manager key combination this
morning, I finally was fed up, and went off to read ``chromeos-wm`` source
code to discover all of the key bindings. Here's the complete list:

 * Ctrl-F5: Take fullscreen screenshot
 * Ctrl-Shift-F5, Print Screen: Take region screenshot

 * Alt-Tab: Cycle windows forward
 * Alt-Shift-Tab: Cycle windows backwards
 * Alt-1 through Alt-8: Go to window 1 through 8, 1-indexed
 * Alt-9: Go to the last window

 * Ctrl-Alt-t: Create a new shell window
 * Ctrl-Shift-W: Kill the current window

These are only available in overlapping-window mode, which appears to be the
default on at least Samsung Series 5 Chromebooks:

 * F5: Toggle overlapping-window mode
 * Alt-Comma: Expand current window
 * Alt-Period: Shrink current window
