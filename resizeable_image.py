import imagematrix
import sys  #For exits, remove after removing those

class ResizeableImage(imagematrix.ImageMatrix):
    def naiveSeam(self, row, col, total, seam, dictionary):
        #First, add the current coordinates into the list
        #of coordinates in the seam
        coord = (col, row)
        seam.append(coord)

        #Base case when we have a full seam
        if len(seam) == self.height:
            #If there is a duplicate seam, we just replace the dictionary entry
            dictionary[total] = seam
            return

        #And add to the total energy
        total += self.energy(col, row)
        newRow = row + 1
        
        #Call recursively where applicable
        if newRow < self.height:
            if (col - 1) >= 0:
                #Call left
                self.naiveSeam(newRow, col - 1, total, seam.copy(), dictionary)
            if (col + 1) < self.width:
                #Call right
                self.naiveSeam(newRow, col + 1, total, seam.copy(), dictionary)
            #Call down
            self.naiveSeam(newRow, col, total, seam.copy(), dictionary)

    def dpSeam(self):
        #Initialize the 3D list to hold [cumulativeEnergy[moves]]
        #I opted to use this architecture because I did not want to have
        #to update keys in a dictionary, and I wanted to keep my memory 
        #usage pretty low. So instead of creating a dictionary for each level, 
        #I replace the old seam data with the new
        energyMoves = []
        for col in range(0, self.width):
            temp = []
            moves = []
            coord = (col, 0)
            temp.append(self.energy(col, 0))
            moves.append(coord)
            temp.append(moves)
            energyMoves.append(temp)

        #Energy is accessed with [targetCol][0]
        #Iterate through the rows of the image, choosing the lowest cost path 
        #from above for each new pixel
        for row in range(1, self.height):
            temp = energyMoves.copy()
            energyMoves.clear()
            for col in range(0, self.width):
                newList = []
                newMoves = []
                newCol = -1
                coord = (col, row)
                if (col == 0):
                    #Check up and right
                    if (temp[col][0] <= temp[col+1][0]):
                        newCol = col
                    else:
                        newCol = col+1
                elif (col == (self.width - 1)):
                    #Check up and left
                    if (temp[col][0] <= temp[col-1][0]):
                        newCol = col
                    else:
                        newCol = col-1
                else:
                    #Check all 3
                    if (temp[col][0] <= temp[col-1][0] and temp[col][0] <= temp[col+1][0]):
                        newCol = col
                    elif (temp[col-1][0] <= temp[col][0] and temp[col-1][0] <= temp[col+1][0]):
                        newCol = col-1
                    elif (temp[col+1][0] <= temp[col][0] and temp[col+1][0] <= temp[col+1][0]):
                        newCol = col+1
                #Updating the data
                newEnergy = self.energy(col, row) + temp[newCol][0]
                newList.append(newEnergy)
                newMoves = temp[newCol][1].copy()
                newMoves.append(coord)
                newList.append(newMoves)
                energyMoves.append(newList)
            temp.clear()
        
        return energyMoves
        


    def best_seam(self, dp=True):
        #dp=True means call the dynamic solution, false means naive
        if dp == False:
            seamEnergy = {}
            #Get a dictionary of unique energies and seams
            for i in range(0, self.width):
                total = 0
                seam = []
                dictionary = {}
                self.naiveSeam(0, i, total, seam, dictionary)
                seamEnergy.update(dictionary)
            #Find the lowest energy seam and return it
            minSeamKey = min(seamEnergy.keys())
            return seamEnergy[minSeamKey]
        else:
            energyMoves = self.dpSeam()
            small = 0
            for i in range(1, len(energyMoves)):
                if energyMoves[i][0] < energyMoves[small][0]:
                    small = i
            return energyMoves[small][1]

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())