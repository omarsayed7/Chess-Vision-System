'''
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
#####################################################(PLEASE DON'T MAKE INVALID MOVE)#####################################################################
'''


import cv2 
import numpy as np 
import os
import time
from operator import itemgetter

#global final_old

final_old =[]

cap = cv2.VideoCapture(0)

x = 0 
crops_black = []
crops_white = []
thres_check = 0
h = w = 75
nums = [8,7,6,5,4,3,2,1]
while x == 0 :
	print("Starting..............")
	ret,frame = cap.read()
	cv2.imwrite('/home/omar/Desktop/hello.jpg',frame)
	x = 1
while x == 1 : 
	img = cv2.imread('/home/omar/Desktop/hello.jpg',1)
	new_corners = []
	img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	corners = cv2.goodFeaturesToTrack(img2gray, 100,0.1,10)

	corners = np.int0(corners)
	for corner in corners:
		x,y = corner.ravel()
		cv2.circle(img,(x,y),5,(255,0,255),-1)
	corners = corners.tolist()
	for x in range (0,len(corners)):
		new_corners.append(corners[x][0])

	sorty = sorted(new_corners, key = itemgetter(1))


	sortx = sort = sorted(new_corners, key = itemgetter(0))


	cr1 = sorty[0]
	cr2 = sortx[-1]
	cr3 = sortx[0]
	cr4 = sorty[-1]
	for i in range(81):
		if cr1[0] > 205:
			cr1 = sorty[0+i]
		if cr2[1] >60:
			cr2 = sortx[-1-i]
		if cr3[1] < 430:
			cr3 = sortx[0+i]
		if cr4[0] < 560 :
			cr4 = sorty[-1-i]

	cv2.circle(img,(cr1[0],cr1[1]),5,(0,0,255),-1)
	cv2.circle(img,(cr2[0],cr2[1]),5,(0,0,255),-1)
	cv2.circle(img,(cr3[0],cr3[1]),5,(0,0,255),-1)
	cv2.circle(img,(cr4[0],cr4[1]),5,(0,0,255),-1)


	cv2.imshow('image',img)
	k = cv2.waitKey(0)
	if k == 27:
		x = 2
		cv2.destroyAllWindows()

	
def genrate(result_, resultc_):
	
	for ii, yy in zip(range(8,0,-1),range(0,600,75)) :
		for j, xx in zip([chr(i) for i in range(ord('a'),ord('i'))],range(0,600,75)):
			if len(notations) < 64 :
				notations.append(j+str(ii))
			crop = edges[yy:yy+75, xx:xx+75]
			cropc = resultc_[yy:yy+75, xx:xx+75]
			crops.append(int(np.mean(crop)))
			if int(np.mean(cropc)) <= 230:
				item = 3
			elif int(np.mean(crop)) >= 18 :
				item = 1
			else:
				item = 0 
			lis.append(item)
	final_state = zip(notations,lis)
	return final_state

while x == 2 : 
	#intit
	#Notations 
	# 0:empty 
	# 1: White 
	# 3: Black
	tic = time.time()
	
	first=''
	second='' 
	notations = []
	
	lis = []
	crops=[]
	item = 0
	#image transform to BOARD
	ret,img = cap.read()
	pts1 = np.float32([[cr1[0],cr1[1]],[cr2[0],cr2[1]],[cr3[0],cr3[1]],[cr4[0],cr4[1]]])
	pts2 = np.float32([[0,0],[600,0],[0,600],[600,600]])
	matrix = cv2.getPerspectiveTransform(pts1,pts2)

	#output transform (600*600) RGB image contains only the chess_board 
	board_transform = cv2.warpPerspective(img,matrix,(600,600))
	kernel = np.ones((6,6),np.uint8)
	erosion = cv2.erode(board_transform,kernel,iterations = 2)
	edges = cv2.Canny(erosion,90,90)
	#Save the image 
	cv2.imwrite('/home/omar/Desktop/out.jpg',board_transform)
	
	#take copy of an image to generate the move 
	#board_normal = cv2.imread('/home/amr/Desktop/out.jpg',1)  #generate list of occuiped boxes (0,1)
	board_black = board_transform    #generate list of black pieces only (0,3)
	
	#convert to gray channel 
	gray = cv2.cvtColor(board_black , cv2.COLOR_BGR2GRAY)
	#detect the black pieces 
	a_, mask= cv2.threshold(gray, 17, 255,cv2.THRESH_BINARY)    #change anything else black to white (255,255,255)
	#apply threshhold on the frames 
	board_black[mask == 255] = [255, 255, 255]
	cv2.imwrite('/home/omar/Desktop/mask.jpg',board_black)
	cv2.imwrite('/home/omar/Desktop/edges.jpg',edges)
	#genrate the state of the board 
	final = genrate(edges,board_black)


	#genrate the move if exists 
	for ind in range (0,len(final)):
		if final_old == [] :
			continue
		if final[ind][1] == final_old[ind][1]:
			continue
		elif final[ind][1]-final_old[ind][1] == 3 or final[ind][1]-final_old[ind][1] == 1 or final[ind][1]-final_old[ind][1] == -2 or final[ind][1]-final_old[ind][1] == 2:
			second = str(final[ind][0])
			 
		elif final[ind][1]-final_old[ind][1] == -1 or final[ind][1]-final_old[ind][1] == -3 :
			first = str(final[ind][0])
	Move = first+second #example a2a4
	if len(Move) == 4:
		print 'The move is:',Move

	cv2.imshow('result',img)
	if cv2.waitKey(1) == 27:
		break

	toc = time.time()
	#save the current frame to be olddddddddddd (to be comapred to the new frame in the next iteration
	final_old = final

	#print('Operations Time :',(toc - tic) * 1000 )
	
	#wait for indecator button for the safty of human 
	v = raw_input("Waiting....................")

	#FLUSH THE BUFFER 
	for o in range (5):
		cap.read()
