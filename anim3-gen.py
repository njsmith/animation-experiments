from animhelpers import *

with make_anim("anim3-assets.svg", "anim3.svg"):
    # The moving letters
    all_letters = [
        *[f"hello-l{i}" for i in range(5)],
        *[f"world-l{i}" for i in range(5)],
    ]
    hidden(
        # "Guides" layer -- can leave visible for debugging
        "layer2",
        *all_letters,
        # Arrows next to receive()
        *[f"receive-arrow-{i}" for i in range(3)],
        # Results
        *[f"receive-result-{i}" for i in range(3)],
    )

    send_task_lines = LineSeq("task1")
    receive_task_lines = LineSeq("task2")

    def send_task_step(word):
        send_task_lines.next()
        sleep(0.5)
        for i in range(5):
            with keep_time():
                sleep(i * 0.2)
                animate(f"{word}-l{i}", 1, "opacity", from_=0, to=1)
        sleep(0.4)
        for i in range(5):
            with keep_time():
                sleep(i * 0.2)
                slide(f"{word}-l{i}", 2.5, f"{word}-l{i}-in")
        sleep(3)

    received = set()
    def receive_task_step(step, letters):
        received.update(letters)
        receive_task_lines.next()
        sleep(0.5)
        for i, letter in enumerate(letters):
            with keep_time():
                sleep(i * 0.2)
                slide(letter, 2.5, f"{letter}-out")
        # unreceived letters, in order
        for i, letter in enumerate(l for l in all_letters if l not in received):
            with keep_time():
                sleep(1 + i * 0.1)
                slide(letter, 1, f"receive-catchup-{step}")
        sleep(2.5 + len(letters) * 0.2)
        with keep_time():
            animate(f"receive-arrow-{step}", 0.5, "opacity", to=1)
        for letter in letters:
            with keep_time():
                animate(letter, 1, "opacity", to=0)
        animate(f"receive-result-{step}", 1, "opacity", to=1)
        sleep(0.5)

    sleep(1)
    send_task_step("hello")
    send_task_step("world")
    send_task_lines.finish()
    sleep(0.5)
    receive_task_step(0, ["hello-l0", "hello-l1", "hello-l2"])
    receive_task_step(1, ["hello-l3", "hello-l4", "world-l0", "world-l1"])
    receive_task_step(2, ["world-l2", "world-l3", "world-l4"])
    receive_task_lines.finish()
