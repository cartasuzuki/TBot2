import numpy as np
import pandas as pd
import os
import leafdetection

print("TBot2 Start")



def main():
     path = os.getcwd()

     print(path)
     predictions = leafdetection.predict("model.pb","image.jpg")

if __name__ == '__main__':
    main()