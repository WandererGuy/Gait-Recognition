- guide https://github.com/PaddlePaddle/PaddleSeg/tree/release/2.9/contrib/PP-HumanSeg
- CUDA 11.2 https://www.paddlepaddle.org.cn/

# both window and linux :
```
conda create -p /home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/env_seg python==3.9
conda install paddlepaddle-gpu==2.6.1 cudatoolkit=11.2 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/ -c conda-forge 
conda install -y opencv anaconda::scikit-learn anaconda::pyyaml conda-forge::tqdm conda-forge::filelock conda-forge::prettytable
pip install visualdl opencv-contrib-python fastapi uvicorn pydantic python-multipart opencv-python
```

