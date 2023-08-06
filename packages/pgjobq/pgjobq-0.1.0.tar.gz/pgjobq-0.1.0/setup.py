# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgjobq', 'pgjobq.sql']

package_data = \
{'': ['*'], 'pgjobq.sql': ['migrations/*']}

install_requires = \
['anyio>=3.6.1,<3.7.0', 'asyncpg>=0.26.0,<0.27.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.3.0,<5.0.0']}

setup_kwargs = {
    'name': 'pgjobq',
    'version': '0.1.0',
    'description': 'PostgreSQL backed job queues',
    'long_description': '# pgjobq\n\nA job queue built on top of Postgres.\n\n## Features\n\n* Best effort at most once delivery (jobs are only delivered to one worker at a time)\n* Automatic redelivery of failed jobs\n* Low latency delivery (near realtime, uses PostgreSQL\'s `NOTIFY` feature)\n* Completion tracking (using `NOTIFY`)\n* Fully typed async Python client (using [asyncpg])\n* Optional FIFO queuing\n* Persistent scheduled jobs (scheduled in the database, not the client application)\n\nPossible features:\n\n* Bulk sending\n* Exponential backoffs\n* Maybe more efficient continuous polling?\n\nUnplanned features:\n\n* Sending back response data (currently it needs to be sent out of band)\n* Supporting "subscriptions" (this is a simple queue, not a message broker)\n\n## Examples\n\n```python\nfrom contextlib import AsyncExitStack\n\nimport anyio\nimport asyncpg  # type: ignore\nfrom pgjobq import create_queue, connect_to_queue, migrate_to_latest_version\n\n\nasync def main() -> None:\n\n    async with AsyncExitStack() as stack:\n        pool: asyncpg.Pool = await stack.enter_async_context(\n            asyncpg.create_pool(  # type: ignore\n                "postgres://postgres:postgres@localhost/postgres"\n            )\n        )\n        await migrate_to_latest_version(pool)\n        await create_queue("myq", pool)\n        (send, rcv) = await stack.enter_async_context(\n            connect_to_queue("myq", pool)\n        )\n        async with anyio.create_task_group() as tg:\n\n            async def worker() -> None:\n                async for msg_handle in rcv.poll():\n                    async with msg_handle:\n                        print("received")\n                        # do some work\n                        await anyio.sleep(1)\n                        print("done processing")\n                    print("acked")\n\n            tg.start_soon(worker)\n            tg.start_soon(worker)\n\n            async with send.send(b\'{"foo":"bar"}\') as completion_handle:\n                print("sent")\n                await completion_handle()\n                print("completed")\n                tg.cancel_scope.cancel()\n\n\nif __name__ == "__main__":\n    anyio.run(main)\n    # prints:\n    # "sent"\n    # "received"\n    # "done processing"\n    # "acked"\n    # "completed"\n```\n\n## Development\n\n1. Clone the repo\n2. Start a disposable PostgreSQL instance (e.g `docker run -it -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres`)\n3. Run `make test`\n\n[asyncpg]: https://github.com/MagicStack/asyncpg\n\nSee this release on GitHub: [v0.1.0](https://github.com/adriangb/pgjobq/releases/tag/0.1.0)\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'dev@adriangb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adriangb/pgjobq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
