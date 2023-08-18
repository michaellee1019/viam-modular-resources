# viam-modular-resources

## Models included
### michaellee1019:mcp23017:eightsegment
This model utilizes an MCP23017 chip to control an Eight Segment LED. Currently alpha-numeric characters are supported. Some characters are not printed and are ignored when they cannot be displayed.

Example Config:
```
{
      "model": "michaellee1019:mcp23017:eightsegment",
      "name": "mcp",
      "type": "generic",
      "attributes": {
        "device": "B" // not used yet, for the future
      },
      "depends_on": []
    }
```

Example Do Command:
```
{"flash_word": {"word":"ASDF"}}
```

Example Client Code:
This can be ran on the robot or on any computer with python installed. Must install viam-sdk first.
```
ROBOT_SECRET="<secret>" ROBOT_ADDRESS="<address>" python3 src/client.py
```
### michaellee1019:audio_output:play_file
This model is an audio output component that plays files stored on the robot itself. The implementation is a wrapper on [pygame](http://www.pygame.org/docs/ref/music.html) which supports various file types.

Example Config:
```
{
  "files": {
    "name_of_sound": "/path/to/sound.mp3"
  }
}
```

This config sets a mapping of sound names to the filepath destination on the robot, allowing control code of the robot through SDK to not care about the file structure on a robot.

Example Do Command:
```
{"play":{"filename":"name_of_sound"}}
```

By default the sound will play out of the audio output jack on the board. The module does not currently allow configuration of sound settings, and need to be done manually. On most boards audio is enabled by default. Optionally you can update a RaspberryPi to stream the output instead to GPIO pins, using this command:

```
sudo dtoverlay audremap pins_18_19
```

### michaellee1019:grove:4_channel_spdt_relay
```
{"pulse_one":{"address":"0x11", "bit":"0x2", "pulse_seconds": "1"}}
```

### michaellee1019:ht16k33
The ht16k33 family of components is a Viam wrapper around the [Adafruit_CircuitPython_HT16K33](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33/) library.

#### seg_14_x_4
This component supports 14-segment LED devices that have a four character display in each device. Depending on the device you can chain multiple displays together on the same channel, usually by soldering contacts that change the i2c address. Put each device address into the address array when wanting to string together the characters in each display.

Example Config
```
{
      "model": "michaellee1019:ht16k33:seg_14_x_4",
      "name": "segments",
      "type": "generic",
      "attributes": {
        "address": ["0x70","0x71"]
      },
      "depends_on": []
}
```

Example Do Command
```
{"marquee":{"text":"MICHAELLEE1019"}}
```

```
{"print":{"value":3.14159265,"decimal":2}}
```

```
{"print":{"value":"ELLO POPPET"}}
```

## Development and Packaging
### Copy SSH Key
Save yourself some hassle and time. The first time connecting to a robot, run the following to copy the SSH key to your computer. Afterwards you never have to enter the password again.
```
make ssh-keygen target=username@hostname.local
```

### Robot Config
```
"modules": [
    {
      "executable_path": "/viam-modular-resources-build",
      "type": "local",
      "name": "build"
    },
    {
      "executable_path": "/home/username/test.sh",
      "type": "local",
      "name": "test"
    }
  ]
```

### Testing Workflow
If you are developing in this package, you can test changes to models by running an unpackaged version of the module. This will also immediately start your program, giving you feedback about any runtime errors your program has.

```
make robot-runtime-test-workflow target=username@hostname.local
```

If you receive the exception "Need socket path as command line argument", then there are no runtime errors detected and next should look at the robot logs and check for issues there. Finally, test your robot using the control tab.

### Packaging workflow

1. Run the Testing Workflow at least once, as the process will install all dependencies onto the pi that will be used for packaging.
1. Run the following to package the program into a python binary using pyinstaller.

```
make robot-deploy-workflow target=username@hostname.local
```

TODO

1. Upload to registry
```
viam module upload --version <version> --platform linux/arm64 archive.tar.gz
```

## Development
For a faster development cycle, follow the steps below, except run python directly instead of pyinstaller. This will do some runtime evaluation and return errors. If you get to the point where it warns of missing socket arguments, you have to deploy as a module and follow the full steps below.

```python ~/viam_modular_resources/src/main.py```