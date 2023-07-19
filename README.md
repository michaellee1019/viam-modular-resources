# Development
## Packaging
```
docker run -it -v .:/module navikey/raspbian-bullseye bash

sudo apt-get update
sudo apt-get install -y python3-pip python3-venv


Custom API install:
1. curl -sSL https://install.python-poetry.org | python3.10 - 
2. make install
3. 

Testing on Pi:
python MCP23017_API/main.py

Deployment:
rm -rf MCP23017_API 

scp -r /Users/michaellee/show/MCP23017_Base/custom/src  lights@lightsmichael:/home/lights/MCP23017_API

pyinstaller --onefile --hidden-import="googleapiclient" ~/MCP23017_API/main.py && sudo rm /mcp_api && sudo cp dist/main /mcp_api && sudo systemctl restart viam-server && echo "done"


```# viam-modular-resources
