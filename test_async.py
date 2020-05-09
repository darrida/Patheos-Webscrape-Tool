import asyncio
import time, sys


async def count(run_name: str, number: int, time: int, timer=True):
    count = 0
    if timer:
        while count < number:
            print(run_name, count)
            await asyncio.sleep(time)
            count += 1
    else:
        print_clear = 0
        while count < number:
            if print_clear == 40000:
                print(run_name, count)
                print_clear = 0
            await asyncio.sleep(0)
            count += 1
            print_clear += 1


async def io_related(name, number, time, timer=True):
    print(f'{name} started')
    await asyncio.sleep(1)
    await count(name.upper(), number, time, timer),
    print(f'{name} finished')


async def main():
    await asyncio.gather(
        io_related('first', 10000000, 1, timer=False),
        io_related('second', 10000000, 1, timer=False),
    )  # 1s + 1s = over 1s


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


