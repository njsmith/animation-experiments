from animhelpers import *

with make_anim("anim2-assets.svg", "anim2-2.svg"):
    hidden(
        "layer2",  # "Guides" layer -- can leave visible for debugging
        "hello",   # moving "hello" box
        "world",   # moving "world" box
        "receive-hello-arrow",  # -> next to first receive()
        "receive-world-arrow",  # -> next to second receive()
    )

    send_task_lines = LineSeq("task1")
    receive_task_lines = LineSeq("task2")

    def send_task_step(word, slide_dur):
        send_task_lines.next()
        sleep(0.5)
        with keep_time():
            animate(word, 1, "opacity", from_=0, to=1)
        slide(word, slide_dur, f"{word}-path-in")

    def receive_task_step(word):
        receive_task_lines.next()
        slide(word, 3, f"{word}-path-out")
        with keep_time():
            animate(f"receive-{word}-arrow", 0.5, "opacity", to=1)
        animate(f"{word}-box", 1, "opacity", to=0)
        sleep(0.5)

    sleep(0.5)
    send_task_step("hello", 3)
    send_task_step("world", 2.5)
    send_task_lines.finish()
    sleep(0.5)
    receive_task_step("hello")
    receive_task_step("world")
    receive_task_lines.finish()
