#!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import sys
import argparse

from jetson_inference import imageNet
from jetson_utils import videoSource, videoOutput, cudaFont, Log

# parse the command line
parser = argparse.ArgumentParser(description="Classify a live camera stream using an image recognition DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=imageNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)


# load the recognition network

# note: to hard-code the paths to load a model, the following API can be used:
#
net = imageNet(model="resnet18.onnx", labels="labels.txt", 
                 input_blob="input_0", output_blob="output_0")

# create video sources & outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)
font = cudaFont()

# process frames until EOS or the user exits
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  

    classID, confidence = net.Classify(img)

    # draw predicted class labels
    classLabel = net.GetClassLabel(classID)
    confidence *= 100.0

    print(f"imagenet:  {confidence:05.2f}% class #{classID} ({classLabel})")

    font.OverlayText(img, text=f"{confidence:05.2f}% {classLabel}", 
                         x=5, y=5,
                         color=font.White, background=font.Gray40)
    if classLabel == "Aloe Vera":
        print("Water this plant every three weeks")
    if classLabel == "Asparagus Fern":
        print("Water this plant every seven to ten days")
    if classLabel == "Bird of Paradise":
        print("Water this plant every seven to ten days")
    if classLabel == "Chinese Money Plant":
        print("Water this plant every seven to ten days in summer and ten to fourteen in winter")
    if classLabel == "Daffodils":
        print("Water this plant every week")  
    if classLabel == "Dracaena":
        print("Water this plant every one to two weeks")
    if classLabel == "Dumb Cane":
        print("Water this plant every week")
    if classLabel == "Elephant Ear":
        print("Water this plant one to three times a week") 
    if classLabel == "Hyacinth":
        print("Water this plant every one to two weeks")   
    if classLabel == "Money Tree":
        print("Water this plant every one to three weeks") 
    if classLabel == "Monstera Deliciosa":
        print("Water this plant every one to two weeks") 
    if classLabel == "Orchid":
        print("Water this plant every seven to ten days")
    if classLabel == "Parlor Palm":
        print("Water this plant every one to two weeks") 
    if classLabel == "Polka Dot Plant":
        print("Water this plant every three to seven days") 
    if classLabel == "Prayer Plant":
        print("Water this plant every five to ten days")
    if classLabel == "Rubber Plant":
        print("Water this plant every one to two weeks")
    if classLabel == "Sago Palm":
        print("Water this plant every one to two weeks")
    if classLabel == "Tulip":
        print("Water this plant every two to three days")           
    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
