import asyncio

from ..client import Client
from ..common import hexlify
from . import to_int


async def subscriber(host,
                     port,
                     client_id,
                     topic,
                     keep_alive_s,
                     session_expiry_interval):
    client = Client(host,
                    port,
                    client_id,
                    keep_alive_s=keep_alive_s,
                    session_expiry_interval=session_expiry_interval,
                    subscriptions=[topic],
                    topic_alias_maximum=10)

    while True:
        print(f"Connecting to '{host}:{port}'.")
        await client.start()
        print('Connected.')

        while True:
            topic, message = await client.messages.get()

            if topic is None:
                print('Broker connection lost!')
                break

            print(f'Topic:   {topic}')
            print(f'Message: {hexlify(message)}')

        await client.stop()


def _do_subscribe(args):
    asyncio.run(subscriber(args.host,
                           args.port,
                           args.client_id,
                           args.topic,
                           args.keep_alive,
                           args.session_expiry_interval))


def add_subparser(subparsers):
    subparser = subparsers.add_parser('subscribe',
                                      description='Subscribe for given topic.')
    subparser.add_argument('--host',
                           default='localhost',
                           help='Broker host (default: %(default)s).')
    subparser.add_argument('--port',
                           type=int,
                           default=1883,
                           help='Broker port (default: %(default)s).')
    subparser.add_argument('--client-id',
                           help='Client id (default: mqttools-<UUID[0..14]>).')
    subparser.add_argument('--keep-alive',
                           type=int,
                           default=0,
                           help=('Keep alive time in seconds (default: '
                                 '%(default)s). Give as 0 to disable keep '
                                 'alive.'))
    subparser.add_argument(
        '--session-expiry-interval',
        default=0,
        type=to_int,
        help='Session expiry interval in the range 0..0xffffffff (default: %(default)s).')
    subparser.add_argument('topic', help='Topic to subscribe for.')
    subparser.set_defaults(func=_do_subscribe)
