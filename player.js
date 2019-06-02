svg = document.rootElement;
svg.pauseAnimations();
svg.setCurrentTime(0);
function init() {
    play_overlay = document.getElementById("play-overlay");
    replay_overlay = document.getElementById("replay-overlay");
    at_end = false;

    svg.addEventListener("click", function() {
        if (at_end) {
            at_end = false;
            replay_overlay.style.opacity = "0";
            // this cancels the transition on replay_overlay
            replay_overlay.style.display = "none";
            svg.setCurrentTime(0);
            svg.unpauseAnimations();
        } else {
            if (svg.animationsPaused()) {
                play_overlay.style.display = "none";
                svg.unpauseAnimations();
            } else {
                play_overlay.style.display = "inline";
                svg.pauseAnimations();
            }
        }
    })
    play_overlay.style.display = "inline";

    animations = Array.from(document.querySelectorAll("animate, animateMotion, animateColor, animateTransform, set"));
    // Hack: assume that the last tag in document order corresponds to the
    // animation that finishes last in the timeline.
    last_anim = animations[animations.length - 1];
    // This is what I used to do, to try to calculate this directly, but I
    // couldn't figure out how to make it work on Chrome. In general browsers
    // are really fiddly about when they'll let you call
    // getStartTime()/getSimpleDuration().
    // finish_times = animations.map(a => { console.log(a); a.getStartTime() + a.getSimpleDuration() });
    // last_finish_time = Math.max(...finish_times);
    // last_i = finish_times.indexOf(last_finish_time);
    // last_anim = animations[last_i];
    last_anim.addEventListener("endEvent", function() {
        console.log("the end is here");
        at_end = true;
        play_overlay.style.display = "none"; // just in case
        replay_overlay.style.display = "inline";
        // this has to be delayed a bit from the display change so the
        // transition fires, plus a short delay looks nice
        window.setTimeout(
            function() { replay_overlay.style.opacity = 1; },
            500
        );
    })
}
