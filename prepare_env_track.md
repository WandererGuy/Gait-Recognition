- spec: gpu support highest CUDA 11.3 (SERVER MACHINE)
- For my GPU CUDA support highest 11.3, go on previous torch local
# LINUX or wsl linux 
```
conda create -p /home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/env_track python==3.9
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
conda install -y opencv conda-forge::cython conda-forge::filelock conda-forge::filterpy conda-forge::h5py conda-forge::kornia conda-forge::lap conda-forge::loguru conda-forge::motmetrics conda-forge::tqdm conda-forge::tensorboard conda-forge::tabulate conda-forge::ninja anaconda::scikit-image conda-forge::prettytable anaconda::wcwidth conda-forge::fastapi anaconda::requests conda-forge::configparser
```

- option 1 : (i have exclude installed library from requirement of byte track)
```
python3 -m pip install thop visualdl yolox cython-bbox 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
pip install fastapi uvicorn pydantic
```

- option 2: (recommended since bytetrack is the core)
 u follow bytetrack demo for installation like this 
```
git clone https://github.com/ifzhang/ByteTrack.git
cd ByteTrack
pip3 install -r requirements.txt
python3 setup.py develop
pip3 install cython; pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
pip3 install cython_bbox
pip install fastapi uvicorn pydantic
python3 -m pip install thop
```
- last step:
 put check point like in  prepare_ckpt.md


# Window: (Updated: FAIL , DO NOT TRY)
- ALL FAIL TO SET BYTETRACK ENV, LINUX IS THE BEST 
```
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
pip install opencv-python cython filelock filterpy h5py kornia loguru motmetrics tqdm tensorboard tabulate ninja scikit-image prettytable wcwidth fastapi requests configparser 
pip install lap
python3 -m pip install thop visualdl yolox cython-bbox 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
```

- build yolox from source : (build yolox from source on github guide then delete yolox folder)
```
git clone git@github.com:Megvii-BaseDetection/YOLOX.git
cd YOLOX
pip3 install -v -e .  # or  python3 setup.py develop
```
- bug installing:
  - cython-bbox
  - 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

- for window dev , bug :       
    ```
    building 'cython_bbox' extension
      error: Microsoft Visual C++ 14.0 or greater is required. 
      Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]
    ```





