import yaml
import re

from yaml import Loader

from ..hooks import HookTrigger, MessageHook, ReactionHook
from ..utils import find_item_in_array

from .base import Tag, on_render, TagConfig, Optional, Union, EmptyEntry, InvalidEntry


class ConfigTag(Tag):

    _config = TagConfig(name="config")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = {}

    @on_render()
    async def render(self, args):
        self.config = yaml.load(self.content, Loader=Loader)
        self.root.config = self.config


class ForTag(Tag):

    _config = TagConfig(
        name="for",
        args={
            "in":     list,
            "var":    Optional(str, "item"),
            "start":  Optional(int, None),
            "end":    Optional(int, None),
            "inline": Optional(bool, False)
        }
    )

    @on_render()
    async def render(self, args):
        out = []
        items = args['in'] or []
        
        for index, item in enumerate(items[args.start:args.end]):
            self.update_state({
                args.var: item,
                'index': index + 1
            })
            if to_add := await self.render_content():
                out.append(to_add)

        return (' ' if args.inline else '').join(out)


class IfTag(Tag):

    _config = TagConfig(
        name="if",
        args={
            "exp": bool
        }
    )

    @on_render()
    async def render(self, args):
        if args.exp and (content := await self.render_content()):
            return content
            
        return ""


# might be best to create an action for this
class CheckTag(Tag):

    _config = TagConfig(name="check", singleton=True)

    @on_render()
    async def render(self, args):
        async def event(*_):
            if entry := self.root.empty_entry:
                raise EmptyEntry(entry.get_arg('name'))

        self.ui.queue_event(event)


class EntryTag(Tag):

    _config = TagConfig(
        name="entry",
        args={
            "name":    str,
            "var":     Optional(str),
            "require": Optional(bool, False),
            "value":   Optional(str),
            "type":    Optional(str),
            "options": Optional(str),
            "match":   Optional(str),
            "show":    Optional(bool, True),
            "repeat":  Optional(bool, True),
            "move":    Optional(bool, True)
        }
    )

    MATCHES = {
        'tag': r"\<@!?([0-9]+?)\>",
        'role': r"<@&([0-9]+?)>",
        'channel': r"<#([0-9]+?)>",
    }

    def parse_data(cls, new_data, old_data, args):

        if exp := cls.MATCHES.get(args.match):
            if not (data := re.findall(exp, new_data)):
                raise InvalidEntry(f"Input of type \"**{args.match}**\" required.") 
        else:
            data = [new_data]
            
        if any(opts := re.split(r", ?", args.options or "")):
            opt_checked_data = [] 

            for index, item in enumerate(data):

                if checked_item := find_item_in_array(item, opts, threshold=0.05):

                    opt_checked_data.append(checked_item)

            if opt_checked_data:
                data = opt_checked_data
            else:
                raise InvalidEntry(f"Invalid option \"**{new_data}**\"")

        if args.type == 'list':

            if not args.repeat:

                non_repeat_data = old_data or []

                for item in data:
                    if item not in non_repeat_data:
                        non_repeat_data.append(item)

                data = non_repeat_data

            else:
                data = (old_data or []) + data
        
        else:
            data = data[0] if data else ''

        return data

    # method for setting entry data; triggered by message hook ([^\-].+)
    async def set_data(self, trigger, args):
        
        old_data = self.root.get_state(args.name) or []
        parsed_data = self.parse_data(trigger.data, old_data, args)

        self.root.update_state({args.name: parsed_data})
        self.update_state({"length": len(parsed_data)})

        if args.move and parsed_data and (old_data != parsed_data):
            self.root.next_entry()

        trigger.resolve({"delete_input": True})

    # method for deleting entry data; triggered by message hook (-d)
    async def delete_data(self, trigger, args):
        self.root.update_state({args.name: ''})
        self.update_state({"length": 0})

        trigger.resolve({"delete_input": True})

    # method for deleting the last item in an array entry field;
    # triggered by message hook (-)
    #
    # ASSUMES THE ENTRY DATA IS A LIST!!
    async def delete_last(self, trigger, args):
        data = self.root.get_state(args.name)

        self.root.update_state({args.name: data[:-1]})

        self.update_state({"length": len(data) - 1})

    # method for quick navigation between entries; 
    # triggered by message hook using a letter from the entry name
    async def navigate_to(self, trigger, index):
        self.root.entry_index = index

        trigger.resolve()
        # why return true?
        return True

    def message_hook(self, exp, func, *args):
        self.ui.register_hook(
            MessageHook(exp, checks=[
                lambda t: t.user.id == self.ui.renderer.author.id
            ]),
            func=lambda trigger: func(trigger, *args)
        )

    def register_nav_char(self, name):

        name_chars = list(name)
        index   = 0
        discrim = 0

        while name_chars and (ch := name_chars.pop(0)):

            if (l_ch := ch.lower()) not in self.root.used_entry_chars:

                self.update_state({
                    'dname': f"{name[:index]}__{ch}__{name[index+1:]}"
                })
                self.root.used_entry_chars.append(l_ch)
                break

            if not name_chars:
                name_chars.append(str(discrim := discrim + 1))

            index += 1

        # register quick navigation hook
        self.message_hook(
            f"({ch.lower()}|{ch.upper()})", self.navigate_to, self.root.entry_count
        )

    def register_set_data_event(self, args):
        async def wrapper():
            self.message_hook(r"([^\-].*)", self.set_data, args)

        return wrapper

    # checks whether the given entry is required,
    # if so it's set as an emtpy_entry on the root
    # NOT TESTED
    def check_required(self, data, args):
        # to prevent a situation where an actual entry is skipped because the empty_entry
        # slot is being hogged by a non-empty entry, every entry attempts to set itself as THE empty_entry;
        # this results in empty entry errors resolving up backwards
        if args.required and not data:
            self.root.empty_entry = self

        elif data and self.root.empty_entry == self:
            self.root.empty_entry = None

    @on_render()
    async def render(self, args):

        entry_data = self.root.get_state(args.name)

        self.check_required(entry_data, args)

        self.update_state({
            # this lets the placeholder value to be used as possible argument
            # in other tags, leading to undesired behaviour
            args.var or 'value': entry_data or args.value,
            'name':   args.name,
            'dname':  args.name,
            'active': 0
        })

        self.register_nav_char(args.name)

        # check whether this entry is active
        if self.root.entry_index == self.root.entry_count:

            self.update_state({
                'dname':  f"[ {self.get_state('dname')} ]",
                'active': 1
            })
            # register quick nav hook
            self.message_hook(r"([^\-].+)", self.set_data, args)

            # register hook to delete entry data
            self.message_hook(r"(-d)", self.delete_data, args)

        self.root.entry_count += 1

        # only shows the entry if it's active or 'show' is true
        if args.show or self.get_state('active'):
            return await self.render_content()


# sets/changes a root state variable
class SetTag(Tag):

    _config = TagConfig(
        name="set",
        args={
            "var": str,
            "value": Union(str, int, list)
        },
        singleton=True
    )

    @on_render()
    async def render(self, args):
        self.root.update_state(
            {args.var: args.value}
        )
        # page flipping needs this to work but 
        # when outside conditional it causes infinte loop
        # self.root.double_render()


class GetTag(Tag):

    _config = TagConfig(
        name="get",
        args={
            "var":     str,
            "source":  list,
            "key":     str,
            "default": Optional(int, 0)
        },
        singleton=True
    )

    @on_render()
    async def render(self, args):
        for item in args.source:
            if item[0] == args.key:
                var = item[1:]
                break
        else:
            var = args.default

        self.root.update_state({args.var: var})


class DecorTag(Tag):

    _config = TagConfig(
        name="decor",
        args={
            "exp": Optional(bool, False),
            "op":  str,
            "ed":  str
        }
    )

    @on_render()
    async def render(self, args):
        out = await self.render_content()

        if args.exp:
            out = args.op + out + (args.cl or args.op[::-1])
        
        return out
