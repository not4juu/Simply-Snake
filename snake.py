'''
	Snake game created in python with extended cpp code (boost-python) and curses lib

	to run the program use enclosed Makfile or put simple comand:
		g++ -shared Food.cpp -fPIC -I/usr/include/python2.7 -lboost_python -o food.so
		python snake.py

	to control snake or choose any options use keyboard arrows and enter button

'''
import curses
import time
import food

window = curses.initscr()
dim = window.getmaxyx()
curses.noecho()
window.keypad(1)

'''
	Global properties :
		- snake length at the beginning (5,20>
		- how many pieces add to snake during eating food 
		- speed level (there are 3 options: Easy, Medium, Hard)
'''
snakeLength = 5
snakeGrowth = 1
snakeLevel = 0

'''
	initGame function - initialize menu content and user choice
'''
def initGame():
 window.clear()
 window.nodelay(0)
 select = -1
 option = 0
 optionsNumber = 3
 window.addstr(dim[0]/2 - 2, dim[1]/2 - 5, "Snake game")
 #window.addstr(0, 0, "Resolution: " + str(dim[0])+" "+str(dim[1]))
 while select < 0:
  css = [0]*optionsNumber
  css[option] = curses.A_REVERSE
  window.addstr(dim[0]/2 , dim[1]/2 - 5, "Start game", css[0])
  window.addstr(dim[0]/2 + 1,  dim[1]/2 - 4, "Options", css[1])
  window.addstr(dim[0]/2 + 2, dim[1]/2 - 2, "Quit", css[2])
  window.refresh()
  action = window.getch()

  if action == curses.KEY_UP:
   option = (option - 1) % optionsNumber
  elif action == curses.KEY_DOWN:
   option = (option + 1) % optionsNumber 

  elif action == ord('\n'):
   select = option
   if select == 0:
    game()
   elif select == 1:
    gameOptions()
   elif select == 2:
    curses.endwin()

'''
	game function - responsible for snake movement and user control
'''

def game():
 window.clear()
 window.nodelay(1)
 window.border()
 head = [dim[0]/2,dim[1]/2]
 body = [head[:]]*snakeLength
 direction = 1 # 0-up 1-right 2-down 3-left
 gameover = False
 deadcell = body[-1][:]
 foodmake = True
 foodGenerator = food.Food(dim[0] - 2, dim[1] - 2)
 timeSpeed = [0.1, 0.07, 0.04]
 while not gameover:

  while foodmake:
   y, x = list(foodGenerator.run())
   if window.inch(y,x) == ord(' '):
    window.addch(y,x,'o')
    foodmake = False
   
  step = window.getch()
  if step == curses.KEY_UP and direction != 2:
   direction = 0
  if step == curses.KEY_RIGHT and direction != 3:
   direction = 1
  if step == curses.KEY_DOWN and direction != 0:
   direction = 2
  if step == curses.KEY_LEFT and direction != 1:
   direction = 3

  window.addch(head[0],head[1],'#')

  if deadcell not in body:
   window.addch(deadcell[0], deadcell[1],' ')
  
  if direction == 0:
   head[0] -= 1
  if direction == 1:
   head[1] += 1
  if direction == 2:
   head[0] += 1
  if direction == 3:
   head[1] -= 1
 
  deadcell = body[-1][:]
  for i in range(len(body)-1,0,-1):
   body[i] = body[i-1][:]

  body[0] = head[:]

  if window.inch(head[0],head[1]) != ord(' '):
   if window.inch(head[0],head[1]) == ord('o'):
    for i in range(snakeGrowth):
     body.append(body[-1])
    foodmake = True
   else:
    gameover = True
  window.refresh()
  time.sleep(timeSpeed[snakeLevel])
 gameOver(len(body) - snakeLength)

'''
	gameOptions function  - enable user to change global properties
'''

def gameOptions():
 global snakeLength, snakeGrowth, snakeLevel
 window.clear() 
 window.nodelay(0)
 select = -1
 option = 0
 optionsNumber = 4
 while select < optionsNumber - 1:
  css = [0]*optionsNumber
  css[option] = curses.A_BOLD
  stringLevel = ['Easy', 'Medium', 'Hard']
  optionsString = ['Snake length : ' + str(snakeLength),
				 'Growth rate : ' + str(snakeGrowth ),
				 'Level : ' + stringLevel[snakeLevel],
				 'Save & Back']
  for i in range(len(optionsString)):
   window.addstr((dim[0] - len(optionsString))/2 + i, (dim[1] - len(optionsString[i]))/2, optionsString[i], css[i])
  window.refresh()
  action = window.getch()

  if action == curses.KEY_UP:
   option = (option - 1) % optionsNumber
  elif action == curses.KEY_DOWN:
   option = (option + 1) % optionsNumber
  elif action == ord('\n'):
   window.clear()
   select = option
   if select == 0:
    snakeLength = (snakeLength + 1) % 21
    if snakeLength == 0:
     snakeLength = 5
   elif select == 1:
    snakeGrowth =  (snakeGrowth + 1) % 6
    if snakeGrowth == 0:
     snakeGrowth = 1
   elif select == 2:
    snakeLevel = (snakeLevel + 1) % 3
   elif select == 3:
    initGame() 

'''
	gameOver function - display option when user lost out the game
'''
def gameOver(points):
 window.clear()
 window.nodelay(0)
 window.addstr(dim[0]/2 - 2, dim[1]/2 - 4, "GAME OVER")
 window.addstr(dim[0]/2 - 1,  dim[1]/2 - 9, "You scored " + str(points) + " points")
 select = -1
 option = 0
 optionsNumber = 2
 while select < 0:
  css = [0]*optionsNumber
  css[option] = curses.A_REVERSE
  window.addstr(dim[0]/2 + 1, dim[1]/2 - 5, "Play again", css[0])
  window.addstr(dim[0]/2 + 2, dim[1]/2 - 2, "Quit", css[1])
  window.refresh()
  action = window.getch()

  if action == curses.KEY_UP:
   option = (option - 1) % optionsNumber
  elif action == curses.KEY_DOWN:
   option = (option + 1) % optionsNumber 

  elif action == ord('\n'):
   select = option
   if select == 0:
    initGame()
   elif select == 1:
    curses.endwin()




'''
	__main__ 
'''

if __name__ == "__main__":
 if dim[0] < 10 or dim[1] < 20:
  raise Exception("Terminal resolution is to small min(10,20), actually - " + str(dim[0]) +" "+ str(dim[1]))
  curses.endwin()
 else:
  initGame()
  
