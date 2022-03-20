import numpy as np
import cv2
import glob



def CalibrateCameraPerspective():

    writeValues=True

    #load camera calibration
    savedir="/home/carlo/Documents/Visual Studio Code/TBotCamera/CameraData/"
    cam_mtx=np.load(savedir+'cam_mtx.npy')
    dist=np.load(savedir+'dist.npy')
    newcam_mtx=np.load(savedir+'newcam_mtx.npy')
    roi=np.load(savedir+'roi.npy')

    #load center points from New Camera matrix
    cx=newcam_mtx[0,2]
    cy=newcam_mtx[1,2]
    fx=newcam_mtx[0,0]
    print("cx: "+str(cx)+",cy "+str(cy)+",fx "+str(fx))

    #MANUALLY INPUT YOUR MEASURED POINTS HERE
    #ENTER (X,Y,d*)
    #d* is the distance from your point to the camera lens. (d* = Z for the camera center)
    #we will calculate Z in the next steps after extracting the new_cam matrix


    #world center + 9 world points

    total_points_used=10

    X_center=17.5
    Y_center=13.5
    Z_center=37
    

    worldPoints=np.array([[X_center,Y_center,Z_center],
                       [5.5,3.5,40.0],
                       [14.5,3.5,38.0],
                       [23.5,3.5,40.0],
                       [5.5,10.5,38.5],
                       [14.5,10.5,37.5],
                       [23.5,10.5,37.5],
                       [5.5,17.5,40],
                       [14.5,17.5,37.5],
                       [23.5,17.5,37.5]], dtype=np.float32)

    #MANUALLY INPUT THE DETECTED IMAGE COORDINATES HERE

    #[u,v] center + 9 Image points
    imagePoints=np.array([[cx,cy],
                       [85,70],
                       [270,70],
                       [430,70],
                       [85,200],
                       [270,200],
                       [430,200],
                       [85,328],
                       [270,328],
                       [430,328]], dtype=np.float32)



    #FOR REAL WORLD POINTS, CALCULATE Z from d*

    for i in range(1,total_points_used):
        #start from 1, given for center Z=d*
        #to center of camera
        wX=worldPoints[i,0]-X_center
        wY=worldPoints[i,1]-Y_center
        wd=worldPoints[i,2]

        d1=np.sqrt(np.square(wX)+np.square(wY))
        wZ=np.sqrt(np.square(wd)-np.square(d1))
        worldPoints[i,2]=wZ
    print("Real World Points")
    print(worldPoints)                  

    #print(ret)
    print("Camera Matrix")
    print(cam_mtx)
    print("Distortion Coeff")
    print(dist)

    print("Region of Interest")
    print(roi)
    print("New Camera Matrix")
    print(newcam_mtx)
    inverse_newcam_mtx = np.linalg.inv(newcam_mtx)
    print("Inverse New Camera Matrix")

    print("solvePNP")
    ret, rvec1, tvec1=cv2.solvePnP(worldPoints,imagePoints,newcam_mtx,dist)
    print("solvePNP")
    ret, rvec1, tvec1=cv2.solvePnP(worldPoints,imagePoints,newcam_mtx,dist)

    print("pnp rvec1 - Rotation")
    print(rvec1)
    if writeValues==True: np.save(savedir+'rvec1.npy', rvec1)

    print("pnp tvec1 - Translation")
    print(tvec1)
    if writeValues==True: np.save(savedir+'tvec1.npy', tvec1)

    print("R - rodrigues vecs")
    R_mtx, jac=cv2.Rodrigues(rvec1)
    print(R_mtx)
    if writeValues==True: np.save(savedir+'R_mtx.npy', R_mtx)

    print("R|t - Extrinsic Matrix")
    Rt=np.column_stack((R_mtx,tvec1))
    print(Rt)
    if writeValues==True: np.save(savedir+'Rt.npy', Rt)

    print("newCamMtx*R|t - Projection Matrix")
    P_mtx=newcam_mtx.dot(Rt)
    print(P_mtx)
    if writeValues==True: np.save(savedir+'P_mtx.npy', P_mtx)

    s_arr=np.array([0], dtype=np.float32)
    s_describe=np.array([0,0,0,0,0,0,0,0,0,0],dtype=np.float32)

    for i in range(0,total_points_used):
        print("=======POINT # " + str(i) +" =========================")
        
        print("Forward: From World Points, Find Image Pixel")
        XYZ1=np.array([[worldPoints[i,0],worldPoints[i,1],worldPoints[i,2],1]], dtype=np.float32)
        XYZ1=XYZ1.T
        print("{{-- XYZ1")
        print(XYZ1)
        suv1=P_mtx.dot(XYZ1)
        print("//-- suv1")
        print(suv1)
        s=suv1[2,0]    
        uv1=suv1/s
        print(">==> uv1 - Image Points")
        print(uv1)
        print(">==> s - Scaling Factor")
        print(s)
        s_arr=np.array([s/total_points_used+s_arr[0]], dtype=np.float32)
        s_describe[i]=s
        if writeValues==True: np.save(savedir+'s_arr.npy', s_arr)

CalibrateCameraPerspective()