# Awesome Messages Generic PubSub

Generic Message Listeners and Publishers.

This module provides interfaces to work with any kind of message
publisher and consumer.

This module also provides currently the following implementations:

- RabbitMQ Message Listener
- RabbbitMQ Message Publisher


![Project logo](assets/logo.png)

Currently only rabbitmq support is implemented but in a future other
infrastructure pieces could be supported too.

The infrastructure of this package rely on abstractions so it is highly
decoupled. Apps code should depend only in `MessageHandler`,
`MessagePublisher` and `MessageListener`.


## Installation

`pip install awesome_messages`


## Create a MessageHandler to handle the received messages

```python
from awesome_messages.domain.handler import MessageHandler


class PrintRequestHandler(MessageHandler):
    def on_msg(self, message: dict):
        print(message)

```

## Configure a listener

I'm using here the RabbitMQ listener implementation.

You can write your custom listener using `MessageListener` interface.
if you write your own listener please make a pull request so that the
rest of the community can use it too.

```python
# Import infrastructure specific listener
from awesome_messages.infra.rabbitmq.listener import RabbitMessageListener


connection_string = "amqps://user:password@host/.."
queue = "my_awesome_queue"

# Declare our listener with our previously defined MessageHandler
msg_listener = RabbitMessageListener(
    connection_string, queue, PrintRequestHandler()
)

# Currently RabbitMQ listener is blocking
try:
    msg_listener.start_listening()
finally:
    msg_listener.stop_listening()
```

## Configure a publisher

I'm using here the RabbitMQ publisher implementation.

You can write your custom publisher using `MessagePublisher` interface.
if you write your own publisher please make a pull request so that the
rest of the community can use it too.

```python
# Import infrastructure specific publisher
from awesome_messages.infra.rabbitmq.publisher import RabbitMessagePublisher


msg_publisher = RabbitMessagePublisher(connection_string, queue)
try:
    # Publish a message
    msg_publisher.publish({"my msg": "my msg data"})
finally:
    msg_publisher.stop_publishing()

```

## Author notes
The way this module is structured allows anyone to easily replace one
implementation by another without changing the rest of the application
code.

This module invites the developer to use dependency injection to build
their app. Relying on defined interfaces rather than implementations
allows changes in dependencies be possible without changing the code.

### Best practices in big projects

You can use a dependency injection library for configure your message
handler, listener and publisher like the following one.

- https://python-dependency-injector.ets-labs.org/

## Support my work

If this module has been useful to you, it would mean a lot to me if you could support my work.
This way you help to keep this and other projects alive.

- https://ko-fi.com/elchicodepython

## Contributors

- Samuel López Saura - [Linkedin Contact](https://es.linkedin.com/in/sam-sec)
