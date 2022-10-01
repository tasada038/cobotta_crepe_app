# cobotta_crepe_app
This repository is application for

**Two COBOTTA units used for performing the multiple processes for crepe cooking**

<br>

## Environment
*  cobotta
    * OS: **Standard OS**, not COBOTTA driver for Linux
    * Version: 2.7.x ~
    * IP: 192.168.0.1 , 192.168.0.2

* Laptop Computer
    * OS: Cross-platform (Windows/Linux/macOS)
    * IP: 192.168.0.xxx

<br>

## Installation

### usage on webserver
```
pip3 install flask
pip3 install flask_sqlalchemy
pip3 install paypayopa
```

Open one shell, run the webserver program.

```
cd ./app
python3 server.py
```

Running on http://localhost:5073 (Press CTRL+C to quit)

<br>

If you use **Paypay API**, please change the following in "views.py" line 25.

```
API_KEY = "xxxxxxxxxx" #"YOUR_API_KEY"
API_SECRET = "xxxxxxxxxx" #"YOUR_API_SECRET"
MERCHANT_ID = "xxxxxxxxxx" #"YOUR_SHOP_ID"
```

<br>

### usage on Electron APP
Prepare material for icon and save "server.py" in the same directory with the following name

- crepe_icon.ico
- crepe_icon.png

<br>

Install nodejs & npm
```
sudo apt install -y nodejs npm
sudo npm install n -g
sudo n stable
sudo apt purge -y nodejs npm
exec $SHELL -l
node -v
```

create node_modules
```
cd ./app
npm i -D electron-packager
```

<br>

- Windows

```
npx electron-packager . app --platform=win32 --arch=x64 --icon=crepe_icon.ico
```

- Raspbian

```
npx electron-packager . app --platform=linux --arch=armv7l --overwrite --icon=crepe_icon.png
```

<br>

Then, platform=linux
```
cd ./COBOTTA_Crepe_Cooking-linux-arm64/
chmod +x COBOTTA_Crepe_Cooking
```

<br>

## Usage
### First
Enter your ID and password to log in.(No ID or PW required)

- ID: 
- PW: 

### Second
Perform COBOTTA CALSET.

Press the "Auto CALSET" button to execute CALSET for each COBOTTA.

### Third
Move each COBOTTA to the initial position for crepe making

### Latest
Select the menu and click the order button(Order with the above contents) to cook the crepes automatically.


<br>

## License
This repository is licensed under the MIT license, see LICENSE
