import asyncio, asyncssh
from pathlib import Path

HOST = "localhost"
USER = "tparment"
HOST = "faraday.inria.fr"
USER = "root"
KEY = Path.home() / ".ssh" / "id_rsa"

#async def run_client(host, username):
#    async with asyncssh.connect(host, username=username) as conn:
#        result = await conn.run("hostname")  # check=True
#        print(result.stdout, end="")


async def run_client_key(host, username, keypath):
    async with asyncssh.connect(
            host, username=username, client_keys=[keypath],
            # 2022 mar 20
            # without config=None here, I'm unable to connect to faraday.inria.fr
            # as my ssh config comes into play and messes stuff up totally
            config=None) as conn:
        result = await conn.run("hostname")  # check=True
        print(result.stdout, end="")


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
loop.set_debug(True)

try:
    #loop.run_until_complete(run_client(HOST, USER))
    loop.run_until_complete(run_client_key(HOST, USER, KEY))
except (OSError, asyncssh.Error) as exc:
    print(f"SSH connection failed: {type(exc)} {exc=}")
    exit(1)
