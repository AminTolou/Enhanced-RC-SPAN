# RPC-SPAN
 RPC-SPAN -Residual Parallel Channel  Splitting Attention Network for Single Image Super resolution 



Abstract
This paper presents a novel approach to image super-resolution that incorporates the Parallel Channel Attention (PCA) mechanism within the Residual Channel Split Attention Network (RC-SPAN). The aim is to enhance the network's ability to prioritize key features while effectively balancing the contributions from different channels, thereby improving image quality and detail retention. The RC-SPAN architecture is thoughtfully constructed, including a shallow feature extraction module, multiple residual groups, an attention mechanism, an upscaling module, and a reconstruction component. We integrate Parallel Channel Attention into the attention mechanism, which combines global average pooling with a texture function. This method evaluates channel importance by using the contrast of each channel alongside the average, with the expectation that channels rich in texture will exhibit higher contrast, leading to a more accurate assessment of channel significance and better detail preservation in the reconstructed images.
Significantly, our proposed method, RPC-SPAN, demonstrates enhanced performance in PSNR, SSIM, PI, and other metrics, along with improved visual quality. Our results indicate that RPC-SPAN consistently surpasses traditional methods and current state-of-the-art models across various benchmark datasets and scaling factors. These findings highlight the effectiveness of our approach in advancing image super-resolution capabilities, striking a solid balance between performance and computational efficiency for practical applications. 
Keywords: Single Image Super Resolution, , Channel Splitting Attention, Parrall Channel Attention, Low Complexity.


This Code are based RCAN and EDSR . thanks for share it.
The code is based on the EDSR (Enhanced Deep Super-Resolution) and RCAN (Residual Channel Attention Network) methods. https://github.com/sanghyun-son/EDSR-PyTorch https://github.com/yulunzhang/RCAN This implementation takes the foundations of those previous models and builds upon them.

![image](https://github.com/user-attachments/assets/b32200c4-5023-47e5-a360-7dc8cee82eba)

![image](https://github.com/user-attachments/assets/f001e9f7-8b43-4c03-b13e-068de81ccde5)

![image](https://github.com/user-attachments/assets/09f11089-3e8a-40d6-9efc-54cf0c05e6a0)

![image](https://github.com/user-attachments/assets/79ad6552-7b3f-449b-87f9-9c07f4cdb5c6)

![image](https://github.com/user-attachments/assets/b7201ebe-4392-4fd4-9d61-dea8175b47dd)

5 Conclusion, Potential Applications, and Future Work

In conclusion, the RPC-SPAN method has demonstrated superior performance compared to existing techniques such as  RC-SPAN in the realm of super-resolution image processing. Through quantitative evaluation, it has been shown to consistently achieve higher PSNR, SSIM, and PI values, highlighting its effectiveness in producing high-quality super-resolution results. The visual representation further emphasizes the enhancement provided by RPC-SPAN over RC-SPAN, showcasing its potential for advancing image enhancement technologies.

          The RPC-SPAN method holds significant potential for various applications in the field of image processing and computer vision. Some potential applications include medical imaging for enhancing diagnostic accuracy, surveillance systems for improving image clarity, satellite imaging for enhancing spatial resolution, and digital photography for enhancing image quality. Additionally, the superior performance of RPC-SPAN in generating high-quality super-resolution results opens up opportunities for applications in video processing, content creation, and virtual reality.

           Moving forward, future work on the RPC-SPAN method could focus on further optimizing the algorithm to enhance computational efficiency and reduce processing time. Additionally, exploring the application of RPC-SPAN in real-time image processing scenarios and integrating it with deep learning frameworks could further enhance its capabilities. Further research could also investigate the adaptability of RPC-SPAN to different types of images and explore its potential for multi-modal image enhancement. Overall, continued research and development on the RPC-SPAN method could lead to advancements in super-resolution image processing and open up new possibilities for image enhancement technologies.

####################################################################################################################################
1- Prepare training data Download DIV2K training data https://data.vision.ee.ethz.ch/cvl/DIV2K/

2- Specify '--dir_data' based on the HR and LR images path. In option.py, '--ext' is set as 'sep_reset', which first convert .png to .npy. If all the training images (.png) are converted to .npy files, then set '--ext sep' to skip converting files.

3- download bench mark data base that were used for Test https://drive.google.com/file/d/1WTcGH3IPsqbPmPQh79GoQCT3x3rSG46O/view?usp=drive_link

4- Unpack the tar file to any place you want. Then, change the dir_data argument in src/option.py to the place where DIV2K images are located.

5-We recommend you to pre-process the images before training. This step will decode all png files and save them as binaries. Use --ext sep_reset argument on your first run. You can skip the decoding part and use saved binaries with --ext sep argument.

You can train code by yourself. All scripts are provided in the src/demo.sh.

cd src
sh demo.sh
