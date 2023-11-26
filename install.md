
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
# install dlib
```
reference this link: https://medium.com/@ageitgey/build-a-hardware-based-face-recognition-system-for-150-with-the-nvidia-jetson-nano-and-python-a25cb8c891fd

test dlib support cuda or not

python
>>> import dlib
>>> dlib.DLIB_USE_CUDA

the output should be true if it support cuda.
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

# fix error: qt.qpa.plugin: Could not find the Qt platform plugin "xcb" in ""
```
fixed it by install pyside-setup 6.4.3,and it doesn't support 6.6.0

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



install gcc-6.3

reference url: https://askubuntu.com/questions/1229774/how-to-use-an-older-version-of-gcc

echo "deb http://old-releases.ubuntu.com/ubuntu zesty main" | sudo tee /etc/apt/sources.list.d/zesty.list
sudo apt-add-repository -r universe

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 1




-- Looking for cuDNN install...
-- Found cuDNN: /usr/lib/aarch64-linux-gnu/libcudnn.so
-- Enabling CUDA support for dlib.  DLIB WILL USE CUDA, compute capabilities: 50





it cannot support build for gcc-6.3, it should use gcc-7.5 to compile the dlib

after change to gcc-7.5

cd build
run cmake then 
make install

then cd .. go to the dlib root folder
sudo python3 setup.py install --set DLIB_USE_CUDA=1 --set USE_AVX_INSTRUCTIONS=1

then test:
import dlib
dlib.DLIB_USE_CUDA

it will show true
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

Debug Qt load error: qt.qpa.plugin: Could not find the Qt platform plugin "xcb" in ""
export QT_DEBUG_PLUGINS=1
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

pip3 install *.whl

```

# fix error:  "/usr/lib/llvm-10/lib/libclangBasic.a"

```
when in configuration qt met this issue


sudo apt install clang libclang-dev



```
