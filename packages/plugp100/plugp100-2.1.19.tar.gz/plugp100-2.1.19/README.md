# Plug P100
This is a fork of original work of [@K4CZP3R](https://github.com/K4CZP3R/tapo-p100-python)

The purpose of this fork is to provide the library as PyPi package. 

# How to install
```pip install plugp100```

# Code example

```python
import asyncio

from plugp100 import TapoApiClient, TapoApiClientConfig, LightEffect


async def main():
    # create generic tapo api
    config = TapoApiClientConfig("<ip>", "<email>", "<passwd>")
    sw = TapoApiClient.from_config(config)
    await sw.login()
    await sw.on()
    await sw.set_brightness(100)
    state = await sw.get_state()
    print(state.get_unmapped_state())

    # light effect example
    await sw.set_light_effect(LightEffect.rainbow())
    state = await sw.get_state()
    print(state.get_unmapped_state())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(0.1))
loop.close()

if __name__ == "__main__":
    main()

```

