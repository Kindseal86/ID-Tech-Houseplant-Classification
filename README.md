# Houseplant Classification

This is my submission for the final project. How it works is you give it a picture of a common houseplant and it will give you the species name so you can learn how to better care for it.

![This is an example output image that shows the species and the confidence](https://github.com/Kindseal86/ID-Tech-Houseplant-Classification/blob/master/output.jpg)

## The Algorithm

My algorithm runs the image classification model that was trained with my dataset and shows the plant species. It also displays information on how often to water it. My algorithm was retrained from the resnet18 base image classification model to recognize 18 different common houseplant species.

## Running this project

1. Download the repository and the jetson-inference library
2. Change directory into the project folder
3. Run: `python3 Runner.py <input image> <output image>`
   
## Resources
[View a video explanation here](video link)
[Jetson-Inference Library](https://github.com/dusty-nv/jetson-inference)
[Dataset](https://github.com/dusty-nv/jetson-inference)
