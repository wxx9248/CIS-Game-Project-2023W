#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import pygame

from audio.AudioThread import AudioThread
from config.ConfigMonitorThread import ConfigMonitorThread
from event.EventDispatcher import EventDispatcher
from event.EventDispatchThread import EventDispatchThread
from graphic.GraphicThread import GraphicThread
from input.InputHandlingThread import InputHandlingThread


def main():
    # Logger setup
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
    logger = logging.getLogger()

    # Pygame setup
    pygame.init()

    # Event dispatcher initialization
    event_dispatcher = EventDispatcher()

    # Start all subsystems
    threads = [
        EventDispatchThread(event_dispatcher),
        ConfigMonitorThread(event_dispatcher, "config.json"),
        GraphicThread(event_dispatcher),
        AudioThread(event_dispatcher),
        InputHandlingThread(event_dispatcher)
    ]

    for thread in threads:
        logger.info(f"Starting {thread}")
        thread.start()

    while len(threads):
        thread = threads.pop()
        thread.join()
        logger.info(f"{thread} quit")


if __name__ == '__main__':
    main()
