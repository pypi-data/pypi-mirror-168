# Flask-MultiMQTT

This is a piece of Flask middleware inspired by Flask-MQTT. It adds thread handling code so MQTT can safely
be used inside a multithreading uwsgi container. The MQTT connection is limited to running in the first
thread that calls `connect()` and other threads can still publish messages.

This extension also supports setting a global topic prefix that abstracts away a common prefix when using a
shared mosquitto server. To make dealing with permissions easier there is also helper functions for the
dynsec plugin that's included in Mosquitto 2.0

## Example

Connection configuration is done exactly in the way you'd expect from Flask:

```python
from flask import Flask
from flask_multimqtt import MultiMQTT

app = Flask(__name__)
# Specify the connection with an URI
app.config['MQTT_URI'] = 'mqtt://username:password@127.0.0.1/myprefix'

# or with the equivalent seperate fields
app.config['MQTT_HOST'] = '127.0.0.1'
app.config['MQTT_USERNAME'] = 'username'
app.config['MQTT_PASSWORD'] = 'password'
app.config['MQTT_PREFIX'] = 'myprefix'

mqtt = MultiMQTT(app)
```

TLS is supported when specifying an `mqtts://` uri.

Subscribing to topics can be done in multiple ways. This extension will keep track of all the requested
subscriptions and will delay executing them until the connection is complete so it's safe to register them
early

```python
# Subscribe to a topic and link some functions to it
topic = mqtt.register_topic('home/sensor/#', qos=0)
topic.on_message(this_function_receives_messages)
topic.on_message(this_function_is_also_called)


# Use the decorator
@mqtt.topic('my_topic/#')
def my_topic(client, message):
    # The topic decorator is equivalent to running mqtt.register_topic and hooking up the function
    print('my_topic', message.topic, message.payload)


@mqtt.topic('number/<int:number>')
def number_topic(client, message, number):
    # topic routes support the int, float, str, path and uuid placeholders
    print(f"The number is {number}")
```

Publishing messages can be done with the `MultiMQTT.publish()` method. This can be done from any thread.

```python
# Publishing a message works from any thread
mqtt.publish('my-thread', thread.name)

# If the payload is a list or dict it will automatically be jsonified
mqtt.publish('example', {
    'hello': 'world'
})

# Messages can be sent to a topic without the global prefix, for system topics
mqtt.publish('$CONTROL/something', {'example': True}, no_prefix=True)
```

To get a topic path for a subscribed topic there is the `topic_for(name, absolute=False, **kwargs)` function.

```python
@mqtt.topic('number/<int:number>')
def number_topic(client, message, number):
    # topic routes support the int, float, str, path and uuid placeholders
    print(f"The number is {number}")

    
@app.route('/demo')
def demo():
    # This returns number/42
    return mqtt.topic_for('number_topic', number=42)
```

With `absolute=True` the returned topic includes the global topic prefix, this can be used for sending topics
to external services that connect to the MQTT server.