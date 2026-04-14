#	COUNTDOWN
#	I used this script to work out
#	the logic  to put a "cooldown" on certain
#	events in a program / sequence	
import time
def cooldown()
	start = time.time()
	action = 0
	nextaction = 4.7   #Initial setting to decide when first action occurs
	interval = 3	   #Determines time between actions becoming available again
	time_elapsed_old = 0 #just used to prevent excesssive prints
	while(True):
		time_elapsed = round((time.time() - start), 2)
		if(action):
			print("ACTION")
			nextaction = time_elapsed + interval 
			action = 0
		elif(time_elapsed >= nextaction):
			action = 1
		if(time_elapsed_old != time_elapsed):
			print(time_elapsed)
		time_elapsed_old = time_elapsed
		
cooldown()

