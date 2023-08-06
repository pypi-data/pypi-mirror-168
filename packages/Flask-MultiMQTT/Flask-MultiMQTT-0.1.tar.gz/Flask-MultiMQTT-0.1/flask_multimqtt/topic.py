import re
import uuid


class Topic:
    def __init__(self, name, client, lock):
        self.name = name
        self.re = self._topic_to_regex(name)
        self.qos = None
        self.nolocal = False
        self.subscribed = False
        self.variables = None

        self.client = client
        self.lock = lock
        self.handlers = set()

    def on_message(self, handler, remove=False):
        if remove:
            self.handlers.remove(handler)
        else:
            self.handlers.add(handler)

    def _on_message(self, client, message):
        kwargs = {}
        if len(self.variables) > 0:
            part = message.topic.strip('/').split('/')
            for var in self.variables:
                value = part[var[0]]
                if var[1] == 'int':
                    value = int(value)
                elif var[1] == 'float':
                    value = float(value)
                elif var[1] == 'uuid':
                    value = uuid.UUID(value)
                kwargs[var[2]] = value

        for handler in self.handlers:
            handler(client, message, **kwargs)

    def _topic_to_regex(self, topic):
        regex = []
        for part in topic.split('/'):
            if part.startswith('<') and part.endswith('>'):
                if ':' in part:
                    dtype, name = part[1:-1].split(':', maxsplit=1)
                else:
                    dtype = 'str'

                part = '#' if dtype == 'path' else '+'
            if part == '+':
                regex.append(r'[^/]+')
            elif part == '#':
                regex.append(r'.+')
            else:
                regex.append(part)
        regex = '^' + '/'.join(regex) + '$'
        return re.compile(regex)
