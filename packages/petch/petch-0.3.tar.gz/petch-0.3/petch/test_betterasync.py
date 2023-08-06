from unittest import IsolatedAsyncioTestCase
from betterasync import MessageChannel, Producer, Consumer, run_concurrent_tasks


class TestBetterAsync(IsolatedAsyncioTestCase):
    async def test_system(self):
        class MyProducer(Producer):
            async def run(self):
                for i in range(3):
                    await self.send_msg("Normal", i)
                await self.send_err("End", "")
                return i

        class MyConsumer(Consumer):
            def __init__(self, name=""):
                super().__init__(name)
                self.x = 0

            async def on_msg(self, msg):
                if not msg.ok:
                    self.x += 10
                else:
                    self.x += 1

        channel = MessageChannel()
        producer_1 = MyProducer("Producer#1")
        producer_2 = MyProducer("Producer#2")
        consumer_1 = MyConsumer("Consumer#1")
        results = (
            channel.register_producer(producer_1)
            .register_producer(producer_2)
            .register_consumer(consumer_1)
            .run()
        )
        self.assertEqual(consumer_1.x, 26)
        self.assertEqual(results, [2, 2])

    def test_run_concurrent_tasks(self):
        async def my_task(a):
            return a**2

        results = run_concurrent_tasks(my_task, [1, 2, 3])
        self.assertEqual(results, [1, 4, 9])
