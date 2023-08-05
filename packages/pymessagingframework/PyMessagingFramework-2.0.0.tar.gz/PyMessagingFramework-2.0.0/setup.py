# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymessagingframework']

package_data = \
{'': ['*']}

install_requires = \
['pika==1.3.0']

setup_kwargs = {
    'name': 'pymessagingframework',
    'version': '2.0.0',
    'description': 'Messaging infrastructure for communication between microservices in Python',
    'long_description': '# PyMessagingFramework\n\nThis is a messaging framework to manage commands and events of RabbitMQ in a microservice architecture.\n\nIn a microservice architecture, currently commands and events are published as json data or via pickled objects. However, in a language independent system where RabbitMQ is the message broker, passing messages between the systems is feasible mainly via json objects.\n\nIf the data is passed as json, and if the message format changes, we have to find all json calls in the service and update them. This creates a problem as the same json data for a message can exist in multiple places.\n\nThis library creates a messaging framework which decouples the Broker from application and manages the messages passed between producer-consumer and publisher-subscriber.\n\n\n## Producer passing a command to a consumer\n\nIn order to manage this centrally, each service can create commands as classes in separate command directory.\n\nExample: Let Service A be a microservice with the following directory structure:\n\n \n    - Base    \n    |    \n    -- Command    \n    |    \n    ----CommandA.py    \n    |\n    ----CommandB.py\n    |\n    -- CommandHandlers\n    |\n    ----HandlerA.py\n    |\n    ----HandlerB.py\n    --main.py\n    \n   \nHere, ServiceA contains the command classes in a directory and the handlers for the commands in a separate directory.\n  \nFile: CommandA.py\n  \n```\nfrom PyMessagingFramework.main import BaseCommand\nclass CommandA(BaseCommand):\n    def __init__(self, param1:str, param2:str):\n        self.param1 = param1\n`       self.param2 = param2\n```\n\nThis command class inherits the BaseCommand class and contains the parameters which the handler is expected to receive.\n\nThe handler for the command is as follows:\n\nFile: HandlerA.py\n\n```\nfrom PyMessagingFramework.main import BaseCommandHandler\nfrom Base.Command.CommandA import CommandA\n\nclass HandlerA(BaseCommandHandler):\n    def handle(self, command:CommandA):\n        # Perform task after receiving the message\n        pass\n``` \n\nWhen the application starts we can configure the MessagingFramework so that it connects with RabbitMQ, creates the required exchanges and queue for the service.\nThen we can hook up the command and handler so that if MQ sends a message to the service, it decodes the message and calls the appropriate handler of the message.\n\nFilename: main.py\n\n```\nfrom PyMessagingFramework.main import MessagingFramework\nfrom Base.Command.CommandA import CommandA\nfrom Base.CommandHandlers.HandlerA import HandlerA\n\n# Creates the framework objects, connects to MQ and creates the required exchanges and queues.\n\nframework = MessagingFramework(\nbroker_url="localhost",\nbroker_port=5672,\nbroker_username="username",\nbroker_password="password",\nqueue_name="queue_name"\n)\n\n# Hook up the command and handler\nframework.register_commands_as_consumer(CommandA, HandlerA)\n\n# Start the framework to listen for requests\nframework.start()\n```\n\nNow, whenever the application will receive a message matching CommandA, \'handle\' method of HandlerA will be executed.\n\nIn order to send a command to ServiceA, let us create a new service ServiceB. We can package the \'Command\' directory os serviceA and install it in serviceB. In that way the commands of ServiceA can be managed in one place and upgrading the package in ServiceB will automatically update the commands of ServiceA.\n\nSimilar to ServiceA, we can create a MessagingFramework object, connect it to RabbitMQ and send a command to ServiceA as follows:\n\nFilename: producer.py\n\n```\nfrom PyMessagingFramework.main import MessagingFramework\nfrom ServiceA.commands.CommandA import CommandA\n\n# Creates the framework objects, connects to MQ and creates the required exchanges and queues.\n\nframework = MessagingFramework(\nbroker_url="localhost",\nbroker_port=5672,\nbroker_username="username",\nbroker_password="password",\nqueue_name="service_b_queue"\n)\n\n# Hook up the command with the queue of ServiceA. The routing key used in serviceA is \'queue_name\'\n\nframework.register_commands_as_producer(command=CommandA, routing_key="queue_name", exchange_name=\'\')\n\n# Send a command to SerciceA\nframework.publish_message(CommandA(param1="Hello", param2="World!"))\n```\n\nThe MessagingFramework will convert the command object to json data and route it to the queue of ServiceA. The MessagingFramework of ServiceA will receive the json data, parse it to the command object and call the associated handler to execute the task. \n\n## Publisher publishing an event for one or more subscribers\n\nPublisher and subscriber can interact with events similar to consumers and producers. Some example services are provided in the \'example\' directory.\n\nThe following type of events can currently be created:\n\n1. Direct\n\n2. Fanout\n\n3. Topic\n\n## Future updates\n\n1. Currently this library supports creating only blocking connections for the subscribers and consumers. Non-blocking connection will be implemented soon.\n\n2. Currently the library supports only RabbitMQ as the message broker. We have a plan to add support for other message brokers like Redis, etc.\n\n3. There is a plan to provide the functionality to implement Sagas for the services.\n\nIn order to contribute to the project or provide feedback please contact zuhairmhtb@gmail.com. We would love to hear from you.',
    'author': 'zuhairmhtb',
    'author_email': 'zuhairmhtb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
