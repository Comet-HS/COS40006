# Open-Source Framework for AI agents
# group i39 - COS40006

In this project we aim to create a system with 2 main functions including a reminder system and text based emotion detection.

# Installation

### 1. Clone the repository

```
git clone https://github.com/Comet-HS/COS40006.git
```

### 2. Set up your virtual environment

Navigate to the project repository

```
cd (path)/cos40006
```

Set up virtual environment
```
python -m venv venv         # first time only
./venv/scripts/activate     # Windows
source venv/bin/activate    # macOS/Linux
```

### 3. Install dependencies

```
pip install -e .
```

# Usage

Environment initialization:
Enable virtual environment in every terminal as shown above

In root folder, run this command.
```
aiko_registrar
```
if you want to monitor your processes, also run this command in a second terminal.
```
aiko_dashboard
```


Current deployment:
currently only tested using bash terminal

currently utilises gemini LLM. This requires user to have an API key to host. 
One can be acquired from https://aistudio.google.com/app/apikey
Requires a google account. Save your API key.

In a new terminal, navigate to the path:
../cos40006/src/cos40006/user_interface
FIRST, define your API key with the following command. This needs to be repeated each time it is run.
```
export API_KEY="your api key"   # BASH
```

# EXPERIMENTAL #
```
set API_KEY="your api key'      # POWERSHELL temp
setx API_KEY="your api key"     # POWERSHELL permanent
```

Once you have defined your api key
run the application
```
python app.py
```
Once loaded, the localhost server address will be displayed.
Navigate to the address in a browser


output data will be displayed in terminal

tbc

# Authors

* Henry Sutton: 103072963@student.swin.edu.au
* Rafsun Al Mujib: 103840186@student.swin.edu.au 
* Raitha Mehjabeen: 103804629@student.swin.edu.au
* Kazi Talha: 103805790@student.swin.edu.au
* Ankur Saha: 103486797@student.swin.edu.au
* MD Riaz Uddin: 103802843@student.swin.edu.au
