import sys
import os
import math

import pygame as pg
import pygame.midi


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )


if __name__ == '__main__':
    device_id=None
    pg.init()
    pg.fastevent.init()
    event_get = pg.fastevent.get
    event_post = pg.fastevent.post

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        print('couldnt find device')
        input_id = pygame.midi.get_default_input_id()
    else:
        print('found device')
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    pg.display.set_mode((1, 1))

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [pg.QUIT]:
                going = False
            if e.type in [pg.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                ### status byte
                # print(str(bin(e.status))[2:6]) # midi status
                # print(str(bin(e.status))[-4:]) # channel ??

                ### data 1 -- pressure?
                # print(str(bin(e.data1))[2:]) #pressure?
                # print(e.data1) 

                ### data 2 -- velocity?
                # print(str(bin(e.data2))[2:])
                # if e.data2 != 0: print(e.data2) 

                ### data 3 -- sliders
                # print(str(bin(e.data3))[2:]) 
                # if e.data3 != 0: print(e.data3)
                # print(e.data3) # that section

                # get note
                if(str(bin(e.status))[2:6] == '1001'):
                    # print('note', e.data1)
                    print('')
                elif(str(bin(e.status))[2:6] == '1110'):
                    # print('bend', e.data1)
                    hashes = round(e.data1/10)
                    x = 0
                    for x in range(0, hashes): print('#', end='')
                    print('')


        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()