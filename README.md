# viam-modular-resources
This repository contains a monolith of [Viam Robotics Modular Resources](https://docs.viam.com/extend/modular-resources/) that I have needed support for in my hobby projects.

## Models included
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