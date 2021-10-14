# Dynamic-Stylus-Snake-Game
************************
Stylus Snake Game is the advanced version of old nokia snake game. In the old version we use to detect the direction of snake by "up", "down","left" and "right" key. But in the advance game we had obtain the direction of snake by the stylus or the object which will be capture by camera and by performing some operation it will decide the direction.

## steps to make dynamic stylus snake game
### 1. Making dynamic stylus

      * This part of code will find the HSV values of object detected in specific area by averaging the pixels.
    
### 2. With the help of stylus we find the direction which snakes will follow.

     * Here I have drawn rectangle on the frame if you cross the boundaries of rectangle the snake will move in specific direction.
<img src="https://user-images.githubusercontent.com/83348619/137355021-a730abd0-aeef-4ed7-82b6-a177bbb0d8c2.gif" width="60%" hight="80%">

### 3. With the help of pygame I built the snake and food.

     * If snake move over the food then the length of snake will increases and score function will increase its score by +1.
     * There are three hurdels/obstacles which will be called randomely when the game begins.
     * The game will be close if:
         * snake collide with the hurdels/obstacles.
         * snake collide with the boundries of the display bord.
         * snake collide with its body.
<img src="https://user-images.githubusercontent.com/83348619/137362670-459d479d-6084-49ef-808d-36451b6a3afd.gif" width="60%" hight="80%">


# DEMO VIDEO
[click here](https://drive.google.com/file/d/1HiQ00NWvJxJatx9AM5Z49U-Oj8ZnUV_8/view?usp=sharing)
