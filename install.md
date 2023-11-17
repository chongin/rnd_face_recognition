
# install gpart
sudo apt-get install gparted

# ssh key gen
```
ssh-keygen -t rsa
vi ~/.ssh/id_rsa.pub

copy it to your github
```

# download vscode
```
sudo apt install ./code_1.84.2-1699527205_arm64.deb
```

# install multible screen terminal
```
sudo apt install terminator
```

# upgrade in jetson-nano 20.04
```
sudo apt-get upgrade
sudo apt --fix-broken install (no need use to this command)
```


# check version
```
gcc --version # 8.4.0
python3 --version #  3.8.10
pip --version # 20.0.2
python3 -c "import numpy; print(numpy.__version__)"   # 1.18.5
python3 -c "import cv2; print(cv2.__version__)" # 4.8.0
python3 -c "import torch; print(torch.__version__)" # 1.13.0a0+git7c98e70
python3 -c "import torchvision; print(torchvision.__version__)" # 0.14.0a0+5ce4506
python3 -c "import tensorflow; print(tensorflow.__version__)" # 2.4.1
```

# install jtop
```
sudo pip3 install -U jetson-stats
jtop
```

# install venv
```
sudo apt install python3.8-venv
# pip install virtualenv (in this OS, no need)
cd ~/rnd_face_recognition
pip install --system-site-packages package_name

python3 -m venv --system-site-packages venv2
python3 -m venv env
source env/bin/activate
```

# install Yolo V8
```
pip install ultralytics
```

# install recognition
```
ref link: https://medium.com/@ageitgey/build-a-hardware-based-face-recognition-system-for-150-with-the-nvidia-jetson-nano-and-python-a25cb8c891fd

sudo apt-get updatesudo apt-get install python3-pip cmake libopenblas-dev liblapack-dev libjpeg-dev
git clone https://github.com/JetsonHacksNano/installSwapfile./installSwapfile/installSwapfile.sh
./installSwapfile/installSwapfile.sh




```


# fix error: Cv2: Cannot allocate memory in static TLS block
```
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

```

# fix error: AttributeError: module 'numpy' has no attribute 'typeDict'
```
numpy already is the latest one: 1.24.4, but it still raise this error
should update: pip install --upgrade h5py

```