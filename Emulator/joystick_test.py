import pygame
pygame.init()

BUTTON_DOWN = 1
DOWN = [0 , 1]
UP = [0, -1]
LEFT = [-1, 0]
RIGHT = [1, 0]
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

player_count = pygame.joystick.get_count()

for i in range(player_count):
	pygame.joystick.Joystick(i).init()
# -------- Main Program Loop -----------
while done==False:

	# EVENT PROCESSING STEP
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop

		for i in range(player_count):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()		
			
			# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
			if event.type == pygame.JOYBUTTONDOWN:
				player = {}
				for j in range(joystick.get_numbuttons()):
					button = joystick.get_button(j)
					if button == BUTTON_DOWN:
						print("Number: ", j)
			if event.type == pygame.JOYAXISMOTION:
				player = {}
				player[i] = []
				for j in range(joystick.get_numaxes()):
					axis = joystick.get_axis(j)
					player[i].append(int(round(axis)))
					if player[i] == DOWN:
						print("Player",i," DOWN")
					if player[i] == UP:
						print("Player",i," UP")
					if player[i] == LEFT:
						print("Player",i," LEFT")
					if player[i] == RIGHT:
						print("Player",i," RIGHT")


	pygame.display.flip()
	clock.tick(20)

pygame.quit ()