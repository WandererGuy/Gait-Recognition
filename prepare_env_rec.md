- spec: gpu support highest CUDA 11.3
- for my GPU CUDA support highest 11.3, go on previous torch local
```
conda create -p /home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/env python==3.9
```
# for linux:
```
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
conda install -y conda-forge::tqdm anaconda::pyyaml conda-forge::tensorboard opencv conda-forge::kornia conda-forge::einops conda-forge::imageio conda-forge::matplotlib anaconda::scikit-learn conda-forge::loguru 
pip install fastapi uvicorn pydantic python-multipart opencv-python
```
# for WINDOW:
```
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
pip install tqdm pyyaml tensorboard opencv-python kornia einops imageio matplotlib scikit-learn loguru
pip install fastapi uvicorn pydantic python-multipart
```
