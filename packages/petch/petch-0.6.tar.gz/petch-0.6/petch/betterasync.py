import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, TypeVar
import nest_asyncio
from petch.betterlist import BetterList

nest_asyncio.apply()
T = TypeVar("T")


def run_concurrent_tasks(async_func: Callable[[T], Any], args_list: list[T]):
    """
    This function is shortcut for the situation where you want to run function
    over a list concurrently.

    You need to have:

    1. list of inputs
        Ex.
        num_list = [1,2,3,4]

    2. async function that takes single input from the args list
        Ex.
        async def print_num(num:int):
            await asyncio.sleep(1)
            print(num)
            return num

    Usage
        Ex.
        results = run_concurrent_tasks(print_num,num_list)
        print(results)
    """

    async def main():
        tasks = BetterList([asyncio.create_task(async_func(arg)) for arg in args_list])
        results = await asyncio.gather(*tasks)
        return results

    return asyncio.run(main())


@dataclass
class Message:
    ok: bool
    time: datetime
    sender: str
    category: str
    message: Any


class Producer:
    """
    The producer of messages.
    Modify at async run function
    Use
    - self.send_msg to send normal message
    - self.send_err to send error message

    Ex.

    class MyProducer(Producer):
        async def run(self):
            while True:
                await asyncio.sleep(1)
                await self.send_msg("NormalMSG", "This is message!")


    producer_1 = MyProducer(name="1")
    """

    def __init__(self, name=""):
        self.notify_corr: Callable[[Message], Any]
        self.name = name

    async def send_msg(self, category: str, message: Any):
        msg = Message(
            ok=True,
            time=datetime.now(),
            sender=self.name,
            category=category,
            message=message,
        )
        await self.notify_corr(msg)

    async def send_err(self, category: str, message: Any):
        err = Message(
            ok=False,
            time=datetime.now(),
            sender=self.name,
            category=category,
            message=message,
        )
        await self.notify_corr(err)

    async def run(self):
        raise NotImplementedError


class Consumer:
    """
    The consumer of messages.
    Modify at async on_msg function

    Ex.
    class MyConsumer(Consumer):
        async def on_msg(msg):
            if msg.category != "MyCategory":
                return
            elif not msg.ok:
                print(f"Error! {msg}")
                return
            print(f"I got my message! {msg}")
    """

    def __init__(self, name=""):
        self.name = name

    async def on_msg(self, msg: Message):
        raise NotImplementedError


class MessageChannel:
    """
    The communication channel.
    There can only be one message channel at a time in an application.
    There're 4 classes working together.

                             Channel
    Producer#1  ---Message---> | |  ---Message--->  Every Consumer
                               | |
    Producer#2  ---Message---> | |  ---Message--->  Every Consumer
    Producer#1  ---Message---> | |  ---Message--->  Every Consumer
                               | |

    Ex.
    Channel = MessageChannel()
    Channel .register_producer(producer_1)
            .register_producer(producer_2)
            .register_consumer(consumer_1)
            .register_consumer(consumer_2)
            .run()
    """

    def __init__(self):
        self.producers: list[Producer] = []
        self.consumers: list[Consumer] = []

    async def notify_corr(self, msg: Message):
        tasks = BetterList(
            [asyncio.create_task(con.on_msg(msg)) for con in self.consumers]
        )
        return await asyncio.gather(*tasks)

    def register_producer(self, producer: Producer):
        producer.notify_corr = self.notify_corr
        self.producers.append(producer)
        return self

    def register_consumer(self, consumer: Consumer):
        self.consumers.append(consumer)
        return self

    def run(self):
        async def main():
            tasks = BetterList(
                [asyncio.create_task(producer.run()) for producer in self.producers]
            )
            return await asyncio.gather(*tasks)

        return asyncio.run(main())
