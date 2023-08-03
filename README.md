# viam-modular-resources

## Models included:
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
```
ROBOT_SECRET="<secret>" ROBOT_ADDRESS="<address>" python3 src/mcp23017/client.py
```

## Packaging
```
1. Cleanup previous work: 
```rm -rf ~/*```

1. Sync files to pi
```scp -r /Users/michaellee/show/MCP23017_Base/custom/src  lights@lightsmichael:/home/lights/MCP23017_API```

1. Package into binary, and test on Viam RDK, restarting RDK between builds (otherwise new binaries do not get picked up)
```
pyinstaller --onefile --hidden-import="googleapiclient" ~/MCP23017_API/main.py && sudo rm /mcp_api && sudo cp dist/main /mcp_api && sudo systemctl restart viam-server && echo "done"
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

```python ~/MCP23017_API/main.py```