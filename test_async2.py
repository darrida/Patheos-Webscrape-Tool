import asyncio
import pprint, traceback, functools
import datetime

def exceptionCatcherForAsyncDecorator():
    def deco(func):
        @functools.wraps(func)
        async def wrapped(*args):
            print('wrap function invoked')
            try:
                return await func(*args)
            except Exception as E:
                print(f'Exception occured at: {datetime.datetime.now()}\n {pprint.pformat(traceback.format_exc())}')
                raise #re-raise exception to allow process in calling function
        return wrapped
    return deco

########## Main program starts here ##############
import random
#@exceptionCatcherForAsyncDecorator() -- decorator commented out for demo
async def doProcessing(m,n):
    await asyncio.sleep(1)
    print(f'{m};{n};{m/n}')
    return m/n

async def callProcessing():
    while True:
        myNumerator=random.randint(1,100)
        myDenominator=random.randint(0,2)
        result=await doProcessing(myNumerator,myDenominator)
        print(f'result = {result}')


async def main():
    # spawn task to create events
    evtCreator_task = asyncio.create_task(callProcessing())
    # Sleep for and terminate.
    sleepTime=30
    print(f'Time now: {datetime.datetime.now()} - Sleeping for {sleepTime} seconds..')
    await asyncio.sleep(sleepTime)
    print (f'Time now: {datetime.datetime.now()}')
    print('..Terminated!')

asyncio.run(main())