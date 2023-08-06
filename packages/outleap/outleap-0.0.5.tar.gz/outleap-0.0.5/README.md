# outleap

A Python library using asyncio to control a Second Life viewer over the LEAP protocol.

See <https://bitbucket.org/lindenlab/leap/src/main/> for more details on LEAP.

## Installing

`pip install outleap`, or `pip install -e .` to install from source.

## Usage

Look in the [examples](examples) directory.

```python
import asyncio
import sys

from outleap import (
    LEAPClient,
    LEAPProtocol,
    LLViewerControlWrapper,
    connect_stdin_stdout,
)


async def amain():
    # Create a client speaking LEAP over stdin/stdout and connect it
    reader, writer = await connect_stdin_stdout()
    async with LEAPClient(LEAPProtocol(reader, writer)) as client:
        # Use our typed wrapper around the LLViewerControl LEAP API
        viewer_control_api = LLViewerControlWrapper(client)
        # Ask for a config value and print it in the viewer logs
        print(await viewer_control_api.get("Global", "StatsPilotFile"), file=sys.stderr)


def main():
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(amain())

main()
```

## Credits

The project scaffolding is based on code from https://github.com/MatthieuDartiailh/bytecode
