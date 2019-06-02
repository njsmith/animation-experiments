# What is this

This is a sweet and hacky little framework for generating vector
animations, especially diagrams for the Trio docs.

The basic flow is:

- Make a template SVG file. I recommend Inkscape (one of my favorite
  programs of all time).
- Give some of the objects in your template SVG file unique ids.
- Write a Python script describing what you want those objects to do
  and when, using the framework in `animhelpers.py`
- Run the script, which will read in the template, mangle it
  appropriately, and write it out to a new animated SVG file.
  
SVG is just XML, so this isn't actually that complicated. For the
animation part we use
[SMIL](https://en.wikipedia.org/wiki/Synchronized_Multimedia_Integration_Language)
tags, which are well-supported in all popular browsers *except*
Internet Explorer. Sorry. Maybe we can polyfill or something? Or
somehow record the animations to GIFs as a fallback? I haven't figured
that out. Hopefully most IE users at least have Firefox or something
available too as an option?


# Requirements

To run the scripts you need:

- Inkscape on your path (used to automatically convert text to paths)
- Fonts (where Inkscape can find them):
  - Montserrat
  - DejaVu Sans Mono
- `pip install lxml tinycss2 svgpathtools scour`


# Making animations

## General info

Look at some existing .py files and template .svgs to get a sense of
how things fit together.

The wacky animation logic guts are all in `animhelpers.py`.

It might also help to be generally familiar with how SMIL works. [This
is a good
overview](https://css-tricks.com/guide-svg-animations-smil/), and
here's the [MDN entry
point](https://developer.mozilla.org/en-US/docs/Web/SVG/SVG_animation_with_SMIL).

After generating an animation, there's a `whatever.svg.tmp` file left
behind, which is the un-minimized version. It might be a bit easier to
read if you need to look at it. It's not particularly mysterious.

The final output is pretty readable too honestly. We use `scour` for
SVG minimization. (This runs automatically as part of your script, you
don't have to do anything special.) In my tests it produces files that
are ~5% bigger than fancier alternatives, but the fancier alternatives
I tried were all so fancy that they mangled the animation tags and
broke everything. Plus `scour` is on PyPI, which is convenient.


## The timeline

The Python helpers use globals and stuff everywhere. Everything is
stateful.

Part of that state is the "current time". When you add an animation by
calling `animate` or `slide`, then the animation's start point is
automatically set to the current time, and then the current time is
updated to point to the end point of that animation. (This is usually
`dur` seconds after the start, but if you get fancy with repeats or
something it might not be.)

If you don't want the time to change, use `with keep_time(): ...`.

You can also change the current time explicitly to an absolute time
with `set_time`, or a relative time using `wait`. If you're into
time-travel, you can pass negative seconds to `wait` (since it's
really moving around on the animation timeline, not real time).

There's also some clever machinery where `animate` and `slide` return
an object that represents the start/end time of the animation, and you
can use it to access related times:

```python
anim1 = animate(...)
set_time(anim1.start + 3)
# This will start 3 seconds after anim1 started
animate(...)
```

I'm not sure if this is actually useful though.


## Animation controls

One thing `animhelpers.py` does is inject JS-based controls to play,
pause, replay the animation. These are in `player.js`,
`play-overlay.svg`, `replay-overlay.svg`.

There's a gross hack that you might need to be aware of. It's
surprisingly hard to figure out when a sequence of SMIL animations
have finished. So the JS code currently assumes that whichever
animation appears last *in the .svg source code*, is also the one that
finishes last in the animation timeline. (Which in turn will be
whichever call to `animate` or `slide` appears last in your Python
script.) This is almost always going to be true just because it would
be weird to do it otherwise, but watch out in case you're doing
something weird.


## `LineSeq`

The `LineSeq` helper is convenient for managing the background
highlights on source code.

It's pretty simple-minded. To use:

- In Inkscape, draw all the backgrounds as you like.
- Give them ids like `COMMONPREFIX-0`, `COMMONPREFIX-1`, ...
- In your `.py` file, do `lines = LineSeq("COMMONPREFIX")`.
- That will make sure that only `COMMONPREFIX-0` is visible at the
  start, and each time you call `lines.next()` it will animate a
  transition to the next object.


## Misc tips and tricks

In Inkscape, you can see or edit an object's `id` by using the "Object
Properties" pane. The "XML editor" pane is also useful sometimes to
see what's going on. (Internally, Inkscape is basically a very very
very specialized text editor: it keeps the SVG internally and that
*is* its internal source-of-truth about things. You can make arbitrary
edits through the XML editor and Inkscape's display will update live!)

You can also edit the template .svg directly in your text editor, but
Inkscape won't automatically reload if the file is changed on disk, so
if you do this then make sure to exit Inkscape first, or use File ->
Revert.

When you use `slide` it applies a *relative* motion to the object. So
it doesn't matter where you drew the path in inkscape. It's convenient
to attach it to some reference point of the object, but you don't have
to. If you want several objects to move in parallel while keeping
their relative position, you can draw one path and them have them all
follow it (possibly at different times).


# Rejected alternatives

There are a few different ways to show animations on the web.

You can use CSS animation. This is what the standards bodies are
gradually moving towards. But at least at the time of writing, [there
isn't any portable way to move an object along a
path](https://caniuse.com/#feat=css-motion-paths), which is pretty
crucial for us. So this is out for now.

You can make your animations in Adobe After Effects, and then export
them to "Bodymovin JSON", and play them with
[Lottie](http://airbnb.io/lottie/). AFAICT this is currently the
industry standard for high-end animations. But:

- Adobe After Effects is expensive and has a steep learning curve
- You have to do everything with clicking and dragging; you can't
  describe an animation using a 'for' loop. (Or maybe you can somehow,
  if you get far enough up that learning curve, but probably anyone
  writing Trio docs already knows Python.)

You can use the open-source [Synfig Studio](https://www.synfig.org/).
This is pretty cool actually. But its vector editing tools are way
clunkier than Inkscape's, so you'd still need to use Inkscape to build
most of the diagram, and then add motion in Synfig Studio. And it's
not scriptable. And it only outputs raster-based animation format.
(Though there's a [GSoC project to add Lottie/Bodymovin as an export
format](https://forums.synfig.org/t/gsoc-2019-export-animation-for-web/9507/45).)

You can build something with some kind of JS animation library. But
all the ones I looked at would need some significant extra stuff
hacked in to do what we want, and I barely know JS.

So that's why for now we're using SMIL, even if it doesn't work in IE
and CSS animations are the future.

Hopefully if we have to eventually convert to another format like CSS
animations or JS, we can do that by just rewriting the `animate`,
`slide`, etc. helpers.
