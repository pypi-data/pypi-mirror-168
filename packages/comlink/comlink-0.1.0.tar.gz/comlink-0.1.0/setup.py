# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comlink']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=2.4,<3.0']

setup_kwargs = {
    'name': 'comlink',
    'version': '0.1.0',
    'description': 'Send and receive messages by using SQS queues.',
    'long_description': '![Comlink logo](https://raw.githubusercontent.com/art1415926535/comlink/main/assets/logo.svg)\n\nSend and receive messages by using SQS queues.\n\n\n## Docs\n### Example\n\n```python\nimport asyncio\nimport datetime\nfrom comlink import SqsConsumer, SqsQueue\n\n\nasync def example(sqs_client, queue_url):\n    # Create a queue object\n    sqs_queue = SqsQueue(url=queue_url, client=sqs_client)\n\n    # Event for stopping the consumer\n    stop_event = asyncio.Event()\n    # Create a consumer with a handler that just prints the message\n    consumer = SqsConsumer(queue=sqs_queue, handler=print)\n    # Start the consumer\n    consumer_task = await consumer.start(stop_event=stop_event)\n\n    # Send a message to the queue\n    await sqs_queue.put(f"{datetime.datetime.now()} Hello, world!")\n    # Wait for 1 second for the message to be processed\n    await asyncio.sleep(1)\n\n    # Stop the consumer\n    stop_event.set()\n    # Wait for the consumer to stop\n    await consumer_task\n```\n\n## Development\n\n### Setup\n\n1. Install [Poetry](https://python-poetry.org/).\n1. Install dependencies with `poetry install`.\n1. Install [Docker](https://www.docker.com/).\n1. Run `docker compose -f docker-compose.dev.yml up -d` to start \nthe development environment (localstack). Tests will fail until the environment is up and running.\n\n\n### Testing\n\nRun `poetry run pytest` to run the tests.\n\n\n### Formatting\n\nRun `poetry run black .` to format the code.\n\nRun `poetry run isort .` to sort the imports.',
    'author': 'Artem Fedotov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/art1415926535/comlink',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
