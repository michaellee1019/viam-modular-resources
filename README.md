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
This model is an audio output component that plays files stored on the robot itself.

```
{"play":{"filename":"chaching"}}
```

## Development and Packaging
### Install Prerequisites
The following needs to be ran on the robot used for packaging, it does not need to be ran on every robot the module is deployed to:
```
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv
pip install pyinstaller
pip install -U viam-sdk
pip install smbus
pip install google-api-python-client

pip install google-api-core
```

### Configuration steps
enable 12c on every robot first using `sudo raspi-config`.

Note: Reopen your terminal after running pyinstaller.

### Packaging workflow
1. Sync files to pi
```scp -r /Users/michaellee/show/MCP23017_Base/custom/src  lights@lightsmichael:/home/lights/MCP23017_API```

1. Package into binary, and test on Viam RDK, restarting RDK between builds (otherwise new binaries do not get picked up)
```
 rm -rf ~/dist ; rm -rf ~/build ; rm main.spec ;
 pyinstaller --onefile --hidden-import="googleapiclient" ~/viam-modular-resources/src/main.py && sudo rm /main ; sudo cp dist/main /main && sudo systemctl restart viam-server && echo "done"
```

1. Sync binary back
```
scp lights@lightsmichael:/home/lights/dist/main main 
```

1. Compress and archive into tar.gz
```
tar -czvf archive.tar.gz main
```

1. Upload to registry
```
viam module upload --version <version> --platform linux/arm64 archive.tar.gz
```

## Development
For a faster development cycle, follow the steps below, except run python directly instead of pyinstaller. This will do some runtime evaluation and return errors. If you get to the point where it warns of missing socket arguments, you have to deploy as a module and follow the full steps below.

```python ~/viam_modular_resources/src/main.py```