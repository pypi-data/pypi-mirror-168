from threading import Thread
from typing import Dict, Any, List, Tuple, Callable as Function
import logging

class BasicEventEmitter:
    def __init__(self):
        self._events = {}
        Thread(target = self._resolve).start()

    def on(self, name: str, func: Function[..., Any]) -> None:
        if (name not in self._events): self._events[name] = {}
        self._events[name].update({
            "func": func,
            "input_args": [],
            "input_kwargs": [],
            "resolved": 0,
            "once": False
        })

    def once(self, name: str, func: Function[..., Any]) -> None:
        if (name not in self._events): self._events[name] = {}
        self._events[name].update({
            "func": func,
            "input_args": [],
            "input_kwargs": [],
            "resolved": 0,
            "once": True
        })
    
    def emit(self, name: str, *args, **kwargs) -> None:
        if (name not in self._events): self._events[name] = {
            "input_args": [],
            "input_kwargs": [],
            "resolved": 0,
        }
            
        self._events[name]["resolved"] += 1
        self._events[name]["input_args"].append(args)
        self._events[name]["input_kwargs"].append(kwargs)

    def _resolve(self):
        while True:
            once = []
            try:
                for i in self._events:
                    if (self._events[i]["resolved"] and "func" in self._events[i] and len(self._events[i]["input_args"]) > 0 and len(self._events[i]["input_kwargs"]) > 0):
                        if (self._events[i]['once']):
                            once.append(i)
                        self._events[i]["func"](*self._events[i]["input_args"].pop(), **self._events[i]["input_kwargs"].pop())
                        self._events[i]["resolved"] -= 1
                        print("resolved", i)
 
                    elif (len(self._events[i]["input_args"]) == 0 or len(self._events[i]["input_kwargs"]) == 0):
                        self._events[i]["resolved"] = 0
                for i in once:
                    del self._events[i]
            except (IndexError, RuntimeError) as e:
                print("runtime/index error", e)
                for i in self._events:
                    self._events[i]["resolved"] = True