# MaterialEyes_Framework

!!!look at the .sh files in each folder, important!!!!

> change the input/output paths and put the weight files in the correct position

Three parts:
1. figure separator
> change --image to --image_dir if the input is a folder of images
```bash
python test.py --detect_thresh 0.5 --ckpt checkpoints/snapshot200.ckpt --image  ./data/complex_1.png --result_dir /home/weixin/Documents/MyProjects/PhDResearch/ArgonneProjects/MaterialEyes_Framework/data/subfigures/ --image_extend png --save_bbox --save_image --bbox_expand 0.1
```
> weight position:
```bash
/path_to_MaterialEyesFramework/image_separator/checkpoints
or
/path_to_MaterialEyesFramework/image_separator/checkpoints_2000
```

2. annotation separator
```bash
python test.py --dataroot /home/weixin/Documents/MyProjects/PhDResearch/ArgonneProjects/MaterialEyes_Framework/data/subfigures --name pix2pix_res9block_3layer --model pix2pix --netG resnet_9blocks --direction AtoB --num_test 100  --results_dir /home/weixin/Documents/MyProjects/PhDResearch/ArgonneProjects/MaterialEyes_Framework/data/annotation_maps --preprocess none  --epoch 300
```
> weight position (two weights: net_G and net_D):
```bash
/path_to_MaterialEyesFramework/annotation_separator/checkpoints/pix2pix_res9block_3layer/
```

3. subfigure label/scaling bar detection
> change --image_dir to --image if the input is a single image
```bash
python test.py --detect_thresh 0.5 --ckpt checkpoints/snapshot500.ckpt --image_dir  /home/weixin/Documents/MyProjects/PhDResearch/ArgonneProjects/MaterialEyes_Framework/data/subfigures/ --result_dir /home/weixin/Documents/MyProjects/PhDResearch/ArgonneProjects/MaterialEyes_Framework/data/subfigurelabels/ --image_extend png
```

> weight position:
```bash
/path_to_MaterialEyesFramework/annotation_recognition/checkpoints
```


** How to put weights file?

Download the weights.zip file from "All Files/LDRD_MaterialEyes/Datasets/material_framework_weights/", unzip it.

```bash
git clone git@github.com:WeixinGithubJiang/MaterialEyes_Framework.git
cd MaterialEyes_Framework
cd image_separator
mkdir checkpoints
cd checkpoints
cp /path-to-weights_image_separator/snapshot200.ckpt ./
cd ..
cd ..
cd annotation_separator
mkdir checkpoints
cd checkpoints
cp -r /path-to-weights_annotation_separator/pix2pix_res9block_3layer ./
cd ..
cd ..
cd annotation_recognition
mkdir checkpoints
cd checkpoints
cp /path-to-weights_annotation_recognition/snapshot500.ckpt ./
```