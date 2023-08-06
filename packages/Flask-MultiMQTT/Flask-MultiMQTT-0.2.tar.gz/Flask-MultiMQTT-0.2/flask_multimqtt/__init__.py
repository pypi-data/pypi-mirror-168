import json
import ssl
import threading
import logging
from urllib.parse import urlparse

import paho.mqtt.client as mqtt

# Global state for the Flask multithreading
from flask_multimqtt.topic import Topic

_client = None
_main = None
_client_lock = threading.Lock()

_logger = logging.getLogger('MultiMQTT')


class MultiMQTT:
    def __init__(self, app=None, client_id=None):
        self.main_thread = False
        self.client_id = client_id

        self.host = None
        self.port = None
        self.tls = None
        self.username = None
        self.password = None
        self.prefix = ''

        self.connected = False
        self.topics = {}
        self.route_name = {}

        self._handle_connect = set()
        self._handle_disconnect = set()
        self._handle_message = set()

        if app is not None:
            self.init_app(app, client_id=client_id)

    def init_app(self, app, client_id=None):
        self.client_id = client_id

        _client_lock.acquire()
        global _client
        global _main
        if _client is None:
            self.main_thread = True
            _main = self

            uri = app.config.get("MQTT_URI", "mqtt://127.0.0.1")
            component = urlparse(uri, scheme='mqtt')
            self.host = component.hostname
            self.username = component.username
            self.password = component.password
            self.port = component.port
            self.prefix = component.path[1:] if len(component.path) > 0 else ''
            self.tls = component.scheme == 'mqtts'

            self.host = app.config.get("MQTT_HOST", self.host)
            self.username = app.config.get("MQTT_USERNAME", self.username)
            self.password = app.config.get("MQTT_PASSWORD", self.password)
            self.prefix = app.config.get("MQTT_PREFIX", self.prefix)

            _client = mqtt.Client(client_id=client_id)

            _client._transport = app.config.get("MQTT_TRANSPORT", "tcp").lower()
            _client._protocol = app.config.get("MQTT_PROTOCOL_VERSION", mqtt.MQTTv311)
            _client.on_connect = self._on_connect
            _client.on_disconnect = self._on_disconnect
            _client.on_message = self._on_message
        _client_lock.release()

    def connect(self):
        _client_lock.acquire()
        if _main.username:
            _client.username_pw_set(_main.username, _main.password)
        default_port = 1883
        if _main.tls:
            context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
            _client.tls_set_context(context)
            default_port = 8883
        _client.connect(_main.host, port=int(_main.port) if _main.port is not None else default_port)
        _client.loop_start()
        _client_lock.release()

    def on_connect(self, handler, remove=False):
        if remove:
            self._handle_connect.remove(handler)
        else:
            self._handle_connect.add(handler)

    def on_disconnect(self, handler, remove=False):
        if remove:
            self._handle_disconnect.remove(handler)
        else:
            self._handle_disconnect.add(handler)

    def publish(self, topic, payload, qos=0, retain=False, no_prefix=False):
        if no_prefix is False:
            topic = self._join_topic(self.prefix, topic)

        if isinstance(payload, list) or isinstance(payload, dict):
            payload = json.dumps(payload)

        _client_lock.acquire()
        _client.publish(topic, payload, qos=qos, retain=retain)
        _client_lock.release()

    def register_topic(self, name, qos=0, nolocal=False, route_name=None):
        """ Subscribe to a topic on the server and create a Topic object to register message handlers.
        The subscriptions are deduplicated

        :param name: Topic to subscribe to
        :param qos: QoS setting
        :returns Topic
        """
        parts = []
        variables = []
        for i, part in enumerate(name.split('/')):
            if part.startswith('<') and part.endswith('>'):
                if ':' in part:
                    dtype, varname = part[1:-1].split(':', maxsplit=1)
                else:
                    dtype = 'str'
                    varname = part[1:-1]
                variables.append((i, dtype, varname))
                part = '#' if dtype == 'path' else '+'
            parts.append(part)
        name = '/'.join(parts)

        name = self._join_topic(self.prefix, name)

        _client_lock.acquire()
        if name in _main.topics:
            topic = _main.topics[name]
        else:
            topic = Topic(name, _client, _client_lock)
            topic.qos = qos
            topic.variables = variables
            topic.nolocal = nolocal
            topic.prefix = self.prefix
            if _main.connected:
                try:
                    if nolocal and _client._protocol != mqtt.MQTTv5:
                        _logger.error(f"requested nolocal for {name} but protocol is not set to MQTTv5")
                        options = mqtt.SubscribeOptions(qos=topic.qos)
                    elif nolocal:
                        options = mqtt.SubscribeOptions(qos=topic.qos, noLocal=topic.nolocal)
                    else:
                        options = mqtt.SubscribeOptions(qos=topic.qos)
                    res, mid = _client.subscribe(topic.name, options=options)
                    if res == mqtt.MQTT_ERR_SUCCESS:
                        _logger.debug(f'subscribed to topic "{topic.name}" qos {topic.qos}')
                        topic.subscribed = True
                    else:
                        _logger.error(f'failed to subscribe to "{topic.name}" qos {topic.qos}')
                    _main.topics[name] = topic
                except:
                    pass
            else:
                _main.topics[name] = topic
                if route_name is not None:
                    _main.route_name[route_name] = topic
        _client_lock.release()
        return topic

    def topic(self, topic, nolocal=False, name=None):
        """ A decorator to register the on_message callback on a specific topic. Adding the decorator automatically
        subscribes to the topic. The usual mqtt wildcards are supported. Example::

           @mqtt.topic("home/sensor/#")
           def sensor_data(client, message):
               print(message.payload)

        :param topic: Topic to subscribe to
        :param nolocal: Don't receive messages sent by yourself, requires protocol V5
        :param name: Alternate name for this handler, for use with topic_for()
        """

        def decorator(f):
            if name is None:
                rname = f.__name__
            else:
                rname = name
            t = self.register_topic(topic, nolocal=nolocal, route_name=rname)
            t.on_message(f)
            return f

        return decorator

    def topic_for(self, name, absolute=False, **kwargs):
        """ Generate the topic path for this topic with the placeholders filled in.
        The behavior is the same as url_for, use absolute=True to generate the path including
        the prefix

        :param name: Route name
        :param absolute: Include the prefix in the result
        :param kwargs: variables to put in the placeholders
        :return: topic path
        :rtype: str
        """

        return _main.route_name[name].topic_for(absolute=absolute, **kwargs)

    def _dynsec(self, command):
        self.publish('$CONTROL/dynamic-security/v1', {
            "commands": [command]
        }, no_prefix=True)

    def dynsec_add_client(self, username, password, clientid=None, roles=None):
        _logger.debug(f'add dynsec client: {username}')
        command = {
            'command': 'createClient',
            'username': username,
            'password': password,
        }
        if clientid is not None:
            command['clientid'] = clientid
        self._dynsec(command)

        if roles is not None:
            for role in roles:
                command = {
                    'command': 'addClientRole',
                    'username': username,
                }
                if isinstance(role, str):
                    command['rolename'] = role
                else:
                    command['rolename'] = role[0]
                    command['priority'] = role[1]
                self._dynsec(command)

    def dynsec_delete_client(self, username):
        _logger.debug(f'delete dynsec client: {username}')
        self._dynsec({
            'command': 'deleteClient',
            'username': username
        })

    def dynsec_create_role(self, role):
        _logger.debug(f'add dynsec role: {role}')
        self._dynsec({
            'command': 'createRole',
            'rolename': role
        })

    def dynsec_delete_role(self, role):
        _logger.debug(f'delete dynsec role: {role}')
        self._dynsec({
            'command': 'deleteRole',
            'rolename': role
        })

    def dynsec_add_role_acl(self, role, acltype, topic, allow, priority=None):
        _logger.debug(f'add dynsec acl: {role} {acltype} {topic} {allow}')
        topic = self._join_topic(self.prefix, topic)
        command = {
            'command': 'addRoleACL',
            'rolename': role,
            'acltype': acltype,
            'topic': topic,
            'allow': allow,
        }
        if priority is not None:
            command['priority'] = priority
        self._dynsec(command)

    def dynsec_remove_role_acl(self, role, acltype, topic):
        _logger.debug(f'remove dynsec acl: {role} {acltype} {topic}')
        topic = self._join_topic(self.prefix, topic)
        self._dynsec({
            'command': 'removeRoleACL',
            'rolename': role,
            'acltype': acltype,
            'topic': topic
        })

    def _on_message(self, client, userdata, message):
        topic = message.topic
        prefix = self.prefix.rstrip('/')
        message.topic = topic[len(prefix):].lstrip('/').encode('utf-8')
        for n in self.topics:
            if self.topics[n].re.match(topic):
                self.topics[n]._on_message(client, message)

        for handler in self._handle_message:
            handler(client, message)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == mqtt.MQTT_ERR_SUCCESS:
            self.connected = True
            _logger.debug(f"connected to {self.host}")
            for name in self.topics:
                topic = self.topics[name]
                if not topic.subscribed:
                    try:
                        if topic.nolocal and _client._protocol != mqtt.MQTTv5:
                            _logger.error(f"requested nolocal for {name} but protocol is not set to MQTTv5")
                            options = mqtt.SubscribeOptions(qos=topic.qos)
                        elif topic.nolocal:
                            options = mqtt.SubscribeOptions(qos=topic.qos, noLocal=topic.nolocal)
                        else:
                            options = mqtt.SubscribeOptions(qos=topic.qos)
                        res, mid = _client.subscribe(topic.name, options=options)

                        if res == mqtt.MQTT_ERR_SUCCESS:
                            _logger.debug(f'subscribed to topic "{topic.name}" qos {topic.qos}')
                            topic.subscribed = True
                        else:
                            _logger.error(f'failed to subscribe to "{topic.name}" qos {topic.qos}')
                        _main.topics[name] = topic
                    except Exception as e:
                        _logger.error(e)

        else:
            _rc = {
                0: 'success',
                1: 'requested MQTT protocol is not supported',
                2: 'client-id refused',
                3: 'server unavailable',
                4: 'username or password incorrect',
                5: 'not authorized',
            }
            _logger.error(f"failed to connect to {self.host}: {_rc[rc]} ({rc})")

        for handler in self._handle_connect:
            handler()

    def _on_disconnect(self, client, userdata, rc):
        _logger.warning('disconnected from the mqtt server')
        self.connected = False
        for handler in self._handle_disconnect:
            handler()

    def _join_topic(self, *args):
        slash = '/' if args[0].startswith('/') else ''
        parts = []
        for p in args:
            parts.append(p.strip('/'))
        return slash + '/'.join(parts).strip('/')
