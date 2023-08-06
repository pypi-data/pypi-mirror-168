# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynumaflow',
 'pynumaflow.function',
 'pynumaflow.function.generated',
 'pynumaflow.sink',
 'pynumaflow.tests',
 'pynumaflow.tests.function',
 'pynumaflow.tests.sink']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'grpcio-tools>=1.48.1,<2.0.0',
 'grpcio>=1.48.1,<2.0.0',
 'msgpack>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'pynumaflow',
    'version': '0.2.0',
    'description': 'Provides the interfaces of writing Python User Defined Functions and Sinks for NumaFlow.',
    'long_description': '# Python SDK for Numaflow\n\nThis SDK provides the interface for writing [UDFs](https://numaproj.github.io/numaflow/user-defined-functions/) \nand [UDSinks](https://numaproj.github.io/numaflow/sinks/user-defined-sinks/) in Python.\n\n## Implement a User Defined Function (UDF)\n\n```python\n\nfrom pynumaflow.function import Messages, Message, Datum\nfrom pynumaflow.function.server import UserDefinedFunctionServicer\n\n\ndef map_handler(key: str, datum: Datum) -> Messages:\n    val = datum.value\n    _ = datum.event_time\n    _ = datum.watermark\n    messages = Messages()\n    messages.append(Message.to_vtx(key, val))\n    return messages\n\n\nif __name__ == "__main__":\n    grpc_server = UserDefinedFunctionServicer(map_handler)\n    grpc_server.start()\n```\n\n### Sample Image (TODO)\n\n## Implement a User Defined Sink (UDSink)\n\n```python\nfrom typing import List\nfrom pynumaflow.sink import Message, Responses, Response, HTTPSinkHandler\n\n\ndef udsink_handler(messages: List[Message], __) -> Responses:\n    responses = Responses()\n    for msg in messages:\n        responses.append(Response.as_success(msg.id))\n    return responses\n\n\nif __name__ == "__main__":\n    handler = HTTPSinkHandler(udsink_handler)\n    handler.start()\n```\n\n### Sample Image\n\nA sample UDSink [Dockerfile](examples/sink/simplesink/Dockerfile) is provided \nunder [examples](examples/sink/simplesink).\n',
    'author': 'NumaFlow Developers',
    'author_email': 'None',
    'maintainer': 'Avik Basu',
    'maintainer_email': 'avikbasu93@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
