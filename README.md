# viam-modular-resources
This repository contains a monolith of [Viam Robotics Modular Resources](https://docs.viam.com/extend/modular-resources/) that I have needed support for in my hobby projects.

## Models included
### michaellee1019:mcp23017:eightsegment
This model utilizes an MCP23017 chip to control an Eight Segment LED. Currently alpha-numeric characters are supported, but some characters are not printed and are ignored when they cannot be displayed.

Example Config:
```
{
      "model": "michaellee1019:mcp23017:eightsegment",
      "name": "my-model",
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
{"play":{"sound":"name_of_sound"}}
```

By default the sound will play out of the audio output jack on the board. The module does not currently allow configuration of sound settings, and need to be done manually. On most boards audio is enabled by default. Optionally you can update a Raspberry Pi to stream the output instead to GPIO pins, using this command:

```
sudo dtoverlay audremap pins_18_19
```
Then connect the an amplifier, such as a [PAM8403](https://www.amazon.com//dp/B00M0F1LJW/) to GPIO pins 18 and 19.
### michaellee1019:grove:4_channel_spdt_relay
This model implements support for the [Grove 4 Channel SPDT Relay](https://www.seeedstudio.com/Grove-4-Channel-SPDT-Relay-p-3119.html).

Example Config:
```
{
  "attributes": {},
  "depends_on": [],
  "model": "michaellee1019:grove:4_channel_spdt_relay",
  "name": "my-model",
  "type": "generic"
}
```

```
{"pulse_one":{"address":"0x11", "bit":"0x2", "pulse_seconds": "1"}}
```

### michaellee1019:ht16k33
The ht16k33 family of components is a Viam wrapper around the [Adafruit_CircuitPython_HT16K33](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33/) library. The model has also been tested and works with the vk16k33 family of components which functionality is similar to the ht16k33.

#### seg_14_x_4
This component supports 14-segment LED devices that have a four character display in each device. Depending on the device you can chain multiple displays together on the same channel, usually by soldering contacts that change the i2c address. Put each device address into the address array when wanting to string together the characters in each display, in the order that they are physically positioned from left to right.

This model implements the [adafruit_ht16k33.segments.Seg14x4 API](https://docs.circuitpython.org/projects/ht16k33/en/latest/api.html#adafruit_ht16k33.segments.Seg14x4)

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

Example Do Commands:

Marquee text across the display once. Repeating marquee is currently not supported.
```
{"marquee":{"text":"MICHAELLEE1019"}}
```

Marquee text with a custom time between scrolls, in seconds
{"marquee":{"text":"MICHAELLEE1019","delay":0.1}}

Print text onto the display. This method does not clear existing characters so it is recommended to pad the text with space chacters.
```
{"print":{"value":"ELLO POPPET"}}
```

Print number. Optionally, provide `decimal` to round the number to a specific number of points.
```
{"print":{"value":3.14159265,"decimal":2}}
```

Not working:
{"scroll":{"count":2}}

Not working:
{"set_digit_raw":{"index":1,"bitmask":24}}


### michaellee1019:tm1637

#### 4_digit
Viam wrapper of [Raspberry Pi Python 3 TM1637](https://github.com/depklyon/raspberrypi-tm1637) library that provides ability to control 4 digit displays that use a TM1637.

### michaellee1019:prusa_connect:camera_snapshot
This component provides a bridge a webcamera and PrusaConnect. Use this to easily setup one or more webcams connected to a Raspberry Pi, or other types of boards, and feed snapshots to PrusaConnect.

First, add each camera as a [webcam](https://docs.viam.com/components/camera/webcam/) using Viam. You can also add a [Camera Serial Interface (CSI) camera](https://docs.viam.com/modular-resources/examples/csi/) that is integrated into the Raspberry Pi. I highly recommend using the builder to auto detect your connected cameras and generate the correct configuration.

After adding each camera, add this component to your config. The full example of the relationship between cameras and this component is shown below:

You need to populate two attributes for each camera. First go to the Cameras tab on connect.prusa.com. Click "Add new other camera" and copy the Token value provided into your Viam config as the `token`. Next is the `fingerprint` attribute. This can be any value you'd like between but it has to have at least 16 and maximum of 64 characters. I usually use the associated camera's video path.

Note that names must match throughout the config! The camera components name must match the attributes in camera_snapshot, and camera_snapshot must have each camera in its `depends_on` field.

Example Config
```
{
      "attributes": {
        "video_path": "usb-046d_HD_Pro_Webcam_C920_79AA2B6F-video-index0"
      },
      "depends_on": [],
      "model": "webcam",
      "name": "prusaxl2",
      "namespace": "rdk",
      "type": "camera"
    },
    {
      "attributes": {
        "video_path": "usb-046d_C922_Pro_Stream_Webcam_F684FE8F-video-index0"
      },
      "depends_on": [],
      "model": "webcam",
      "name": "prusaxl1",
      "namespace": "rdk",
      "type": "camera"
    },
    {
      "attributes": {
        "cameras_config": {
          "prusaxl1": {
            "fingerprint": "usb-046d_C922_Pro_Stream_Webcam_F684FE8F-video-index0",
            "token": "<secret from connect.prusa.com>"
          },
          "prusaxl2": {
            "fingerprint": "usb-046d_HD_Pro_Webcam_C920_79AA2B6F-video-index0",
            "token": "<secret from connect.prusa.com>"
          }
        }
      },
      "depends_on": [
        "prusaxl1",
        "prusaxl2"
      ],
      "model": "michaellee1019:prusa_connect:camera_snapshot",
      "name": "prusa_connect",
      "type": "generic"
    }
```

## Development
Read this section if developing within this repository.

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

## Development Workflow
For a faster development cycle, follow the steps below, except run python directly instead of pyinstaller. This will do some runtime evaluation and return errors. If you get to the point where it warns of missing socket arguments, you have to deploy as a module and follow the full steps below.

```
make development-workflow  target=username@hostname.local
```

### Testing Workflow
Test changes to models by running an unpackaged version of the module on a single robot. This command will copy code onto your robot and make the module ready to start by Viam. This is the fastest option provided to iterate with your code using a real robot to test hardware.

```
make test-workflow target=username@hostname.local
```

The following configuration needs to be added to your Viam robot. It points to the [test.sh](test.sh) file which installs the required dependencies, and then starts the module program. Note that `test-workflow` restarts `viam-server` each time it is ran, which is required to reload any code that has changed in the module.

```
"modules": [
    {
      "executable_path": "/home/username/test.sh",
      "type": "local",
      "name": "test"
    }
  ]
```

### Packaging workflow
The package workflow is used to generate a bundle of your module. It utilizes [pyinstaller](https://pyinstaller.org/en/stable/) to produce a single file containing all dependencies as well as the python runtime. Packaging the module means it can be deployed to any board with a compatible platform without installing any dependencies.

**Note:** Run the Development Workflow at least once, as the process will install all dependencies onto the pi that will be used for packaging.

```
make package-workflow target=username@hostname.local
```

The workflow will copy the bundle into the root directory for you to try running on your robot. Do this to make sure the packaged module works before sharing with others.
```
"modules": [
    {
      "executable_path": "/viam-module",
      "type": "local",
      "name": "packaged"
    }
  ]
``` 

### Upload to Viam
You can upload the packaged moduled to Viam to use on multiple robots within your organization, or can make it public to share with others.
1. Install the Viam CLI 
1. Upload to registry using the CLI
```
viam module upload --version <version> --platform linux/arm64 archive.tar.gz
```