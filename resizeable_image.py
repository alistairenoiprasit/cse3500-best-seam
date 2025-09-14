import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        #English description

        # Table size m*n of i columns, j rows
        seamDistTable = [[0 for _ in range(self.height)] for _ in range(self.width)]
        # We're initialising with zero, however, since we fill out the first
        # row, the algorithm will not be impacted by initialising all values to 0
        # since we work from top to bottom.

        # i is colum
        # j is row

        # Base case
        # We know that the energy consumed vertical seem from (i,0) to (i,0)
        # is energy(i,0)
        for i in range(self.width): #O(m)
            seamDistTable[i][0] = self.energy(i, 0)

        # Let dp[i, j] be the solution to subproblem (i, j).
        # Then, for a vertical seam, dp[i, j] =
        # min(dp[i− 1, j− 1],
        #     dp[i, j− 1],
        #     dp[i + 1, j− 1]) + energy(i, j)
        for j in range(1, self.height):
            for i in range(self.width): #O(mn)
                if i.__eq__(0): #bc its at the very left
                    seamDistTable[i][j] = self.energy(i,j) + min(seamDistTable[i][j-1], seamDistTable[i+1][j-1])
                elif i.__eq__(self.width-1): # bc its at the very right
                    seamDistTable[i][j] = self.energy(i,j) + min(seamDistTable[i-1][j-1], seamDistTable[i][j-1])
                else:
                    seamDistTable[i][j] = self.energy(i,j) + min(seamDistTable[i-1][j-1], seamDistTable[i][j-1], seamDistTable[i+1][j-1])

        # Traceback
        # We start from the bottom row because, we know based of the above
        # formula, that the lowest column in the bottom row will have the lowest
        # total energy consumed for seam removal.
        # Since we know the end point, and lowest value,
        # starting from the bottom we can work our way back up using the rules above
        # to find the appropriate path.

        shortest_path = []

        # Find lowest bottom row

        min_val = seamDistTable[0][self.height-1]
        coord = [0, self.height-1]
        i_coord = 0;
        for i in range(self.width):
            if seamDistTable[i][self.height-1] < min_val:
                min_val = seamDistTable[i][self.height-1]
                coord = [i, self.height-1]
                i_coord = i

        shortest_path.append(coord)

        '''for j in range(self.height-2, -1, -1):
            local_i_coord = i_coord
            min_val = seamDistTable[i_coord][j]

            if i_coord > 0 and seamDistTable[i_coord - 1][j] < min_val:
                min_val = seamDistTable[i_coord - 1][j]
                local_i_coord = i_coord - 1
            if i_coord < self.width - 1 and seamDistTable[i_coord + 1][j] < min_val:
                min_val = seamDistTable[i_coord + 1][j]
                local_i_coord = i_coord + 1
            i_coord = local_i_coord
            coord = [local_i_coord, j]
            shortest_path.append(coord) '''
        # AI helped me understand this section
        # I asked ClaudeAI what I was looking for in traceback
        # as I tried the above code and it just kept failing
        # They said that I should be looking for the target value
        # instead of trying to find the minimum since we've already calculated
        # the minimum, the end goal is actually to find the path used to make our minimum (its about finding the path
        # to sum to the final minimum)

        # What is target value?
        # The above minimum value should match the current
        for j in range(self.height-2, -1, -1):
            target_value = seamDistTable[i_coord][j+1] - self.energy(i_coord, j+1)

            if i_coord > 0:
                if seamDistTable[i_coord - 1][j] == target_value:
                    i_coord = i_coord - 1
            if i_coord < self.width - 1:
                if seamDistTable[i_coord + 1][j] == target_value:
                    i_coord = i_coord + 1
            coord = [i_coord, j]
            shortest_path.append(coord)
            # i-1,i,i+1
        print(shortest_path)

        shortest_path.reverse()
        return shortest_path




