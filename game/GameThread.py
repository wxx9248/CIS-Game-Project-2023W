# -*- coding: utf-8 -*-
from core.SubsystemThread import SubsystemThread
from event.EventDispatcher import EventDispatcher


class GameThread(SubsystemThread):
    def __init__(self, global_event_dispatcher: EventDispatcher):
        super().__init__(global_event_dispatcher)

    def run(self):
        pass
