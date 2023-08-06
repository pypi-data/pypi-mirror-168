"""file that stores the main bot runner code"""

import urllib.parse
import logging
from .client import Client
from .links import links
from .html_default_templates import (original_html,
                                     param_bio,
                                     html_list,
                                     blockquote)
from typing import (Callable as Function,
                    Any,
                    Dict,
                    Tuple,
                    get_type_hints,
                    List)
from flask import Flask, render_template, request
from waitress import serve
from threading import Thread
from time import sleep
from .param import Param
from .exceptions import NamesMustBeAlphanumeric
from .utils._uuid import random_characters

app = Flask(__name__)
_started_buttons = {}

@app.route('/<command>/<user>/<choice>/<rand_chars>')
def _parse_button_commands(command, user, choice, rand_chars):
    global _started_buttons
    if (command in _started_buttons and user in _started_buttons[command]
        and rand_chars in _started_buttons[command][user]):
        _started_buttons[command][user][rand_chars] = choice
        return render_template("index.html", html="<h1>your request has been processed, you can close this tab</h1>")
    else:
        return render_template("index.html", html="<h1>you cannot do this right now</h1>")

class Button:
    def __init__(self, user: str, command: str):
        self.choice = None
        self.user = user
        self.command = command

    def __getattr__(self, key: str):
        global _started_buttons
        if (self.command not in _started_buttons): _started_buttons[self.command] = {}
        rand_chars = random_characters(15)
        _started_buttons[self.command].update({
            self.user: {
                rand_chars: None
            }
        })
        parsed = f"{self.command}/{self.user}/{urllib.parse.quote(key)}/{rand_chars}"

        return f"[{key}]({links.docs}/{parsed})"

    def get_choice(self):
        current = list(_started_buttons[self.command][self.user].values())[0]
        while (current is None):
            current = list(_started_buttons[self.command][self.user].values())[0]
        return current

class Bot(Client):
    """main bot object"""
    def __init__(self, token: str = None, username: str = None, password: str = None, prefix: str = "/", bio: str = "") -> None:
        if (token is not None or (username is not None and password is not None)):
            super()
            super().__init__(token, username, password)
            self.init_ = True
        else:
            self.init_ = False

        def help_function(ctx, command):
            if (command == "None"):
                ctx.reply(f"See the docs there {links.docs}")
            else:
                ctx.reply(f"description of command: {self.commands[command]['desc']}")
        
        self.commands = {
            "help": {
                "call": help_function,
                "desc": "See commands",
                "name": "help",
                "thread": False,
                "params": {"command": Param(required=False, default="None")}
            }
        }
        self.token = token
        self.logging = logging
        self.bio = bio
        self.prefix = prefix
        self.alias = {}
        self.listeners = {}
        self.threads_ = []
        self._call_when_followed = lambda ctx, person_who_followed: print("person followed", person_who_followed)

    def command(self, name: str, thread: bool = False, desc: str = None, alias: List[str] = []):
        """takes in args"""
        name = name.lower()
        if (not name.replace('-', '').isalnum()):
            raise NamesMustBeAlphanumeric("Name must be alphanumeric")
        def wrapper(func: Function[..., Any]) -> Function[..., Any]:
            """adds to command list"""
            self.commands[name] = {
                "call": func,
                "desc": desc,
                "name": name,
                "params": get_type_hints(func),
                "thread": thread
            }
            for i in alias:
                self.alias[i] = name
        return wrapper

    def listener(self, name: str, thread: bool = False, desc: str = None):
        name = name.lower()
        if (not name.replace('-', '').isalnum()):
            raise NamesMustBeAlphanumeric("Name must be alphanumeric")
        def wrapper(func: Function[..., Any]) -> Function[..., Any]:
            if (name not in self.listeners): self.listeners[name] = []
            self.listeners[name].append({
                "call": func,
                "desc": desc,
                "name": name,
                "params": get_type_hints(func),
                "thread": thread
            })
        return wrapper
    
    def follower(self, func):
        self._call_when_followed = func
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """parses command

        `@Example-Bot /say message:hi!`
        ->
        ```
        {
            "options": {
                "message": "hi!"
            },
            "ping statement": "@Example-Bot",
            "command": "hello"
        }
        ```
        
        """
        splited = command.split(' ')
        if (len(splited) < 2):
            return {}
            
        output = {
            "options": {},
            "ping statement": splited[0],
            "command": splited[1].lstrip(self.prefix),
        }
        _current_command = None
        current = ""
        for i in splited[2:]:
            if (':' in i and _current_command is not None):
                output['options'][_current_command] = current.rstrip()
                _current_command, current = i.split(':')
            elif (':' in i and _current_command is None):
                _current_command, current = i.split(':')
            else:
                current += i + ' '
        if (_current_command is not None):
            output['options'][_current_command] = current
        return output

    def valid_command(self, resp: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """validates command. Returns true if is valid `(True, parsed_json)` or false if not `(False, {'None': None})"""
        if (resp == {} or resp["comment"] == None):
            return (False, {"None": None})
        parsed = self.parse_command(resp["comment"]["body"])
        if (parsed != {} or
            parsed["ping statement"] != self.user.username):
                return (False, {"None": None})
        return (True, parsed)

    def get_kwargs(self, resp: Dict[str, Any], given_params: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """get arguements based on type hints of function"""
        params = resp["params"]
        output = {}
        for i in params:
            if (i in given_params):
                output[i] = given_params[i]
            elif (not params[i].required):
                output[i] = params[i].default
            else:
                return (False, {"None": None})
            if (params[i].type_cast is not None):
                output[i] = params[i].type_cast(output[i])
        return (True, output)

    def create_docs(self) -> None:        
        html = original_html.format(self.user.username,
                                    self.prefix,
                                    blockquote.format(self.bio) if self.bio else "")
        for i in self.commands:
            data = self.commands[i]
            if (not len(data['params'])):
                bio_ = "this command has no parameters"
            else:
                if (data["desc"]):
                    bio_ = blockquote.format(data['desc'])
                else:
                    bio_ = ""
            
            html += param_bio.format(self.prefix,
                                     data['name'],
                                     bio_)
            current_json = {}
            for j in data["params"]:
                _param = data['params'][j]
                current_json[j] = (_param.default
                                   if not _param.required
                                   else None)
                html += html_list.format(j,
                                         _param.desc,
                                         _param.required,
                                         _param.default)

        for i in self.listeners:
            if (len(self.listeners[i]) == 0): continue
            if (not len(data['params'])):
                bio_ = "this command has no parameters"
            else:
                if (data["desc"]):
                    bio_ = blockquote.format(data['desc'])
                else:
                    bio_ = ""
            data = self.listeners[i][0]
            html += param_bio.format(self.prefix,
                                     data['name'],
                                     bio_)
            current_json = {}
            for j in data["params"]:
                _param = data['params'][j]
                current_json[j] = (_param.default
                                   if not _param.required
                                   else None)
                html += html_list.format(j,
                                         _param.desc,
                                         _param.required,
                                         _param.default)
            
        @app.route('/')
        def _() -> None:
            return render_template("index.html", html=html)
    
    def _delete_threads(self) -> None:
        while True:
            for i in self.threads_:
                i.join()
            sleep(5)
    
    def run(self, token: str = None, username: str = None, password: str = None) -> None:
        """mainest runner code"""
        if (token is not None and not self.init_):
            super()
            super().__init__(token, username, password)
            self.init_ = True
        self.once("ready", lambda client: print(f"Botting {client.user.username}"))
        self.create_docs()
        Thread(target=self._delete_threads).start()

        def _run(notif) -> None:
            """main runner code"""
            if (getattr(notif, "comment", False)):
                notif.comment.author = notif.comment.user
                notif.comment.author.mention = "@" + notif.comment.author.username
                notif.comment.Image = lambda url, caption="": f"![{caption}]({url})"
                notif.comment.Link = lambda text, url: f"[{text}]({url})"
                parsed_json = self.parse_command(notif.comment.body)
                if ("command" in parsed_json and
                    (parsed_json["command"] in self.commands or
                     parsed_json["command"] in self.alias)):
                    c = parsed_json["command"]
                    if (parsed_json["command"] in self.alias):
                        c = self.alias[c]
                    valid, kwargs = self.get_kwargs(self.commands[c], parsed_json['options'])
                    if (valid):
                        notif.comment.button = Button(notif.comment.user.username, c)
                        
                        print("logging command")
                        if (self.commands[c]["thread"]):
                            t = Thread(target=self.commands[c]["call"],
                                       args=(notif.comment,),
                                       kwargs=kwargs)
                            t.start()
                            self.threads_.append(t)
                        else:
                            self.commands[c]["call"](notif.comment, **kwargs)
                    else:
                        print("logging command")
                        notif.comment.reply(f"please include all required params. You can check the bot docs here {links.docs}")
                elif ("command" in parsed_json and
                      (parsed_json["command"] in self.listeners)):
                    c = parsed_json["command"]
                    valid, kwargs = self.get_kwargs(self.commands[c], parsed_json["options"])
                    if (valid):
                        notif.comment.button = Button(notif.comment.user.username, c)
                        print("logging command")
                        for command in self.listeners[c]:
                            if (command[c]["thread"]):
                                t = Thread(target=command[c]["call"],
                                           args=(notif.comment,),
                                           kwargs=kwargs)
                                t.start()
                                self.threads_.append(t)
                            else:
                                command[c]["call"](notif.comment, **kwargs)
                    else:
                        print("logging command")
                        notif.comment.reply(f"please include all required params. You can check the bot docs here {links.docs}")
                elif ("command" in parsed_json):
                    print("logging command")
                    notif.comment.reply(f"That is not a valid command. You can see the bot docs here {links.docs}")
            else:
                self._call_when_followed(notif.command)
        
        self.on("notification", _run)
        self.user.notifications.startEvents()
        serve(app, host="0.0.0.0", port=8080)