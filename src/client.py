import asyncio
import os

from viam import logging
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.generic import Generic


def _getenv(key: str) -> str:
    out = os.getenv(key)
    if not out:
        raise Exception(f"Env var {key} not found. See your robot's 'Code sample' tab")
    return out


async def get_client() -> RobotClient:
    address = _getenv('ROBOT_ADDRESS')

    secret = _getenv('ROBOT_SECRET')
    creds = Credentials(type="robot-location-secret",
                        payload=secret)

    refresh_interval = 0
    log_level = logging.DEBUG

    dial_options = DialOptions(credentials=creds)
    opts = RobotClient.Options(refresh_interval=refresh_interval,
                               dial_options=dial_options,
                               log_level=log_level)
    return await RobotClient.at_address(address, opts)


async def main():
    robot = await get_client()

    print("Resources:")
    print(robot.resource_names)

    mcp = Generic.from_robot(robot, name="mcp")

    response = await mcp.do_command({"flash_word": {"word": "ASDF"}})
    print(f"LED Should have Flashed 'HELLO'")
    print(response)

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
