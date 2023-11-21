
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

# install cmake
```
download from https://cmake.org/download/
cd /usr
sudo tar --strip-components=1 -xzf /home/jetson/Downloads/cmake-3.27.8-linux-aarch64.tar.gz
cmake --version
```

# install gcc-9
```
sudo apt install gcc-9 g++-9
sudo update-alternatives --config gcc

or sudo apt install gcc-9 g++-9 gcc-10 g++-10 gcc-11 g++-11 g++-12 gcc-12 g++-13 gcc-13
```

# install clang
```
sudo apt install clang

```

# install qt dependencies
```
sudo apt install -y \
  build-essential \
  curl \
  git \
  libfontconfig-dev \
  libfreetype-dev \
  libglib2.0-dev \
  libgl-dev \
  libgl1-mesa-dev \
  libice-dev \
  libsm-dev \
  libssl-dev \
  libx11-dev \
  libx11-xcb-dev \
  libxcb1-dev \
  libxcb-glx0-dev \
  libxcb-icccm4-dev \
  libxcb-image0-dev \
  libxcb-xinput-dev \
  libxcb-keysyms1-dev \
  libxcb-randr0-dev \
  libxcb-render-util0-dev \
  libxcb-render0-dev \
  libxcb-shape0-dev \
  libxcb-shm0-dev \
  libxcb-sync-dev \
  libxcb-util-dev \
  libxcb-xfixes0-dev \
  libxcb-xinerama0-dev \
  libxcb-xinput-dev \
  libxcb-xkb-dev \
  libxext-dev \
  libxfixes-dev \
  libxi-dev \
  libxkbcommon-dev \
  libxkbcommon-x11-dev \
  libxrender-dev \
  ninja-build
```

# download qt
```
https://download.qt.io/archive/qt/6.4/6.4.3/single/
tar -xf qt-everywhere-src-6.4.3.tar.xz

cd qt-everywhere-src-6.4.3
mkdir build
cd build
../configure
cmake --build . --parallel 2
sudo cmake --install .

rememeber to use set gcc and g++ version to 9
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```

# install pyinstaller
```
first need to install pyinstaller
git clone https://github.com/pyinstaller/pyinstaller
cd pyinstaller, then cd bootloader
python3 ./waf distclean all
pip install . 

at last you need to copy strip
cd /usr/local/bin
sudo cp /usr/bin/strip .

```

# install pyside-setup
```
have to install pyinstaller first.
https://download.qt.io/official_releases/QtForPython/shiboken6/PySide6-6.4.3-src/

https://github.com/qtproject/pyside-pyside-setup.git
git clone https://code.qt.io/pyside/pyside-setup
cd pyside-setup
git checkout 6.4

change requirements.txt: pyinstaller==3.6 => pyinstaller>=3.6
python -m pip install -r requirements.txt
python setup.py build --qtpaths=/usr/local/Qt-6.4.3/bin/qtpaths --ignore-git --parallel 4 --standalone

python setup.py build --qtpaths=/usr/local/Qt-6.6.0/bin/qtpaths --ignore-git --parallel 4 --standalone

python create_wheels.py
cd dist_new
pip install ./*whl


```

# fix error:  "/usr/lib/llvm-10/lib/libclangBasic.a"

```
when in configuration qt met this issue


sudo apt install clang libclang-dev



```
