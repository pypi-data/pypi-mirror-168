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
        self.prefix = None

        self.client = client
        self.lock = lock
        self.handlers = set()

    def topic_for(self, absolute=False, **kwargs):
        """ Generate the topic path for this topic with the placeholders filled in.
        The behavior is the same as url_for, use absolute=True to generate the path including
        the prefix

        :param absolute: Include the prefix in the result
        :param kwargs: variables to put in the placeholders
        :return: topic path
        :rtype: str
        """
        part = self.name.strip('/').split('/')
        prefix_parts = 0
        if self.prefix and len(self.prefix) > 0:
            prefix_parts = len(self.prefix.split('/'))

        for var in self.variables:
            part[var[0] + prefix_parts] = str(kwargs[var[2]])

        if absolute:
            return '/'.join(part)
        else:
            return '/'.join(part[prefix_parts:])

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
