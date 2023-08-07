import asyncio
import os
import sys
# sys.path.append("..")

from viam import logging
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.generic import Generic

# these must be set, you can get them from your robot's 'CODE SAMPLE' tab
robot_secret = os.getenv('ROBOT_SECRET') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

async def connect():
    creds = Credentials(type="robot-location-secret", payload=robot_secret)
    opts = RobotClient.Options(refresh_interval=0, dial_options=DialOptions(credentials=creds), log_level=logging.DEBUG)
    return await RobotClient.at_address(robot_address, opts)


async def main():
    robot = await connect()

    print("Resources:")
    print(robot.resource_names)

    mcp = Generic.from_robot(robot, name="mcp")

    response = await mcp.do_command({"flash_word": {"word":"ASDF"}})
    print(f"LED Should have Flashed 'HELLO'")
    print(response)

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())