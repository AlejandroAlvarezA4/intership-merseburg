#!/usr/bin/python
# -*- coding: utf-8 -*-
# move a servo from a Tk slider - scruss 2012-10-28
# read about change env
# https://code.visualstudio.com/docs/python/environments

import pyfirmata
import components.timing as timing

MIN_STEP = 0
MAX_STEP = 0
# this means that 35% started fast and 40% MAX_SPEED and 35% finish slow

# TODO: REVIEW THE % AND CHANGE FOR ABSOULUTE FOR A BIG NUMBERS
porcentageToPerfom = 35
MIN_SPEED = 4000
MAX_SPEED = 1000

class Arduino():
    def __init__(self, port):
        self.port = port
        self.board = pyfirmata.Arduino(port)
        self.iter8 = pyfirmata.util.Iterator(self.board)
        self.iter8.start()
        self.stepPinX = 2 
        self.dirPinX = 5
        self.stepPinX = 2
        self.dirPinX = 5
        self.stepPinY= 3
        self.dirPinY = 6
        self.stepPinZ = 4
        self.dirPinZ = 7

    def _map(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def calculateProportion(self, value, porcentage):
        return value * (porcentage/100)

    def getSpeed(self, currentStep, totalStep):
        currentSpeed = 0
        MIN_STEP = self.calculateProportion(totalStep, porcentageToPerfom)
        if( currentStep <= MIN_STEP ):
            currentSpeed = self._map(currentStep, 0, MIN_STEP, MIN_SPEED, MAX_SPEED)
            return currentSpeed

        MAX_STEP = totalStep - MIN_STEP
        if (currentStep >= MAX_STEP):
            currentSpeed = self._map(currentStep, MAX_STEP,totalStep , MAX_SPEED, MIN_SPEED)
            return currentSpeed
        return MAX_SPEED

    def moveNumberSteps(self, stepsNumberToDo, stepPin, directionPin):
        if (stepsNumberToDo > 0):
            self.board.digital[directionPin].write(0)
        else:
            self.board.digital[directionPin].write(1)

        for x in range(abs(stepsNumberToDo)):
            currentStepDelay = self.getSpeed(x, abs(stepsNumberToDo))
            self.board.digital[stepPin].write(1)
            timing.delayMicroseconds(currentStepDelay)
            self.board.digital[stepPin].write(0)

    def movePosition(self, axis, steps):
        if(axis == "X"):
            self.moveNumberSteps(steps, self.stepPinX, self.dirPinX)
        if(axis == "Y"):
            self.moveNumberSteps(steps, self.stepPinY, self.dirPinY)
        if(axis == "Z"):
            self.moveNumberSteps(steps, self.stepPinZ, self.dirPinZ)
    
    def getAxis(self, axis):
        if(axis == "X"):
            return (self.dirPinX, self.stepPinX)
        if(axis == "Y"):
            return (self.dirPinY, self.stepPinY)
        if(axis == "Z"):
            return (self.dirPinZ, self.stepPinZ)

    def constansMove(self, axis, direction):
        directionPin, stepPin = self.getAxis(axis)
        if (direction > 0):
            self.board.digital[directionPin].write(0)
        else:
            self.board.digital[directionPin].write(1)

        currentStepDelay = 1400
        for x in range(abs(4)):
            self.board.digital[stepPin].write(1)
            timing.delayMicroseconds(currentStepDelay)
            self.board.digital[stepPin].write(0)

    def isClose(self):
        self.board.exit()

if __name__ == '__main__':
    arduino = Arduino("COM4")
    arduino.movePosition("X", 200)
    arduino.movePosition("Y", 200)
