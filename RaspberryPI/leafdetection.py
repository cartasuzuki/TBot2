import importlib_metadata
from pandas.core.series import Series
import tensorflow as tf
import numpy as np
import PIL.Image, PIL.ImageDraw
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from cv2 import *
from objectdetection import ObjectDetection




def predict(model_filename, image_filename):
    od_model = ObjectDetection(model_filename)

    image = PIL.Image.open(image_filename)
    return od_model.predict_image(image)


def ShowImageWithBestPrediction(imagefilename, predictions):
    
    print("Show Image With Best Prediction")
    image = PIL.Image.open(imagefilename)
    draw = PIL.ImageDraw.Draw(image)
    w, h = image.size

    pred = predictions[0]   
    

    x_min, y_min, x_max, y_max  = pred[0]

    x_min = x_min * w
    y_min = y_min * h
    x_max = x_max * w
    y_max = y_max * h

    draw.rectangle([(x_min,y_min ), (x_max, y_max)], fill=None, width=3, outline ="red")

    image.show()
    
def ShowImageWithBoundingBoxes(imagefilename, predictions):
    
    print("Show Image With Bounding Boxes")
    image = PIL.Image.open(imagefilename)
    draw = PIL.ImageDraw.Draw(image)
    w, h = image.size

    

    for pred in zip(*predictions):
        
        if(pred[1]>0.3):
            x_min, y_min, x_max, y_max  = pred[0]

            x_min = x_min * w
            y_min = y_min * h
            x_max = x_max * w
            y_max = y_max * h
            draw.rectangle([(x_min,y_min ), (x_max, y_max)], fill=None, width=3, outline ="red")

    image.show()


def PrintPredictions(predictions, labels_filename):
    with open(labels_filename) as f:
        labels = [l.strip() for l in f.readlines()]

    for pred in zip(*predictions):
        print(f"Class: {labels[pred[2]]}, Probability: {pred[1]}, Bounding box: {pred[0]}")

def CreatePredictionDataFrame(predictions, imagefilename):
    predictionsDF = pd.DataFrame(columns = ["x", "y", "X", "Y"])
    image = PIL.Image.open(imagefilename)
    w, h = image.size
    for pred in zip(*predictions):
        if(pred[1]>0.3):
            predSeries = pd.Series(pred[0], index=predictionsDF.columns)
            predSeries['x'] = predSeries['x'] * w
            predSeries['X'] = predSeries['X'] * w
            predSeries['y'] = predSeries['y'] * h
            predSeries['Y'] = predSeries['Y'] * h
            print("PredSERIES")
            print(predSeries)
            predictionsDF = predictionsDF.append(predSeries,ignore_index=True)
    return predictionsDF



