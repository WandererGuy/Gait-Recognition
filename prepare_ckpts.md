follow these steps to download checkpoints
- step 1:
```
cd OpenGait
mkdir demo/checkpoints
cd demo/checkpoints
mkdir bytetrack_model
cd bytetrack_model
python -m pip install --upgrade --no-cache-dir gdown
gdown https://drive.google.com/uc?id=1P4mY0Yyd3PPTybgZkjMYhFri88nTmJX5
```
- step 2: <br>
put the script ByteTrack/exps/example/mot/yolox_x_mix_det.py into OpenGait/demo/checkpoints/bytetrack_model
- step 3: 
```
cd ..
mkdir seg_model
cd seg_model/
wget https://paddleseg.bj.bcebos.com/dygraph/pp_humanseg_v2/human_pp_humansegv2_mobile_192x192_inference_model_with_softmax.zip
unzip human_pp_humansegv2_mobile_192x192_inference_model_with_softmax.zip
cd ..
mkdir gait_model
cd gait_model/
wget https://github.com/ShiqiYu/OpenGait/releases/download/v2.0/pretrain_gait3d_gaitbase.zip
unzip -j pretrained_gait3d_gaitbase.zip
```
