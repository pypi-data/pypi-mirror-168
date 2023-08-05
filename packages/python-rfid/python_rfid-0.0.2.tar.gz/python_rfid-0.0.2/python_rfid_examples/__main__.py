#!/usr/bin/env python3

import plac
import python_rfid_examples.dump_version as dump_version
import python_rfid_examples.read_new_card as read_new_card
import python_rfid_examples.send_read_fifo as send_read_fifo

TASKS = {
    "dump_version": dump_version.run,
    "read_new_card": read_new_card.run,
    "send_read_fifo": send_read_fifo.run,
}

@plac.pos("task", help="What to do...")
def main(
        task="dump_version"
):
    fn = TASKS[task]
    fn()

if __name__=="__main__":
    plac.call(main)
