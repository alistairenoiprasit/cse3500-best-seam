import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        # We are finding the best seam by calculating the total lowest energy to
        # reach a certain path (i,j) and storing its value in a table
        # Then using traceback, we select the minimum lowest energy from the lowest
        # row in the table, and find the path working our way back up.

        shortest_path = []

        if dp:
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

            # AI assisted me in the traceback algorithm logic as I initially was recalculating
            # the best path from bottom up using energy, however, it suggested that we actually
            # need to trace the path that adds up to the minimum, not searching for the minimum itself.

            # What is target value?
            # The above minimum value should match the current
            for j in range(self.height-2, -1, -1):
                target_value = seamDistTable[i_coord][j+1] - self.energy(i_coord, j+1)
                # Default is to let the direct cell above be the path

                # Otherwise if other cells exist (left, right)
                # we check to see if they also match the target value.
                if i_coord > 0:
                    if seamDistTable[i_coord - 1][j] == target_value:
                        i_coord = i_coord - 1
                if i_coord < self.width - 1:
                    if seamDistTable[i_coord + 1][j] == target_value:
                        i_coord = i_coord + 1
                coord = [i_coord, j]
                shortest_path.append(coord)

            shortest_path.reverse()
        else:
            # Naive approach
            # start at top and find every possible route down
            # to the bottom
            paths_from_top = [[(i, 0)] for i in range(self.width)]
            for j in range(1, self.height, 1):
                extended_path_from_top = []
                for path in paths_from_top:
                    i_coord = path[-1][0] # Get the last (3,j) i_coord from the above path

                    #left (if exist)
                    if i_coord > 0:
                        extend_left = path + [(i_coord -1, j)]
                        extended_path_from_top.append(extend_left)

                    #middle
                    extend_middle = path + [(i_coord, j)]
                    extended_path_from_top.append(extend_middle)

                    #right (if exist)
                    if i_coord < self.width - 1:
                        extend_right = path + [(i_coord + 1, j)]
                        extended_path_from_top.append(extend_right)
                # All paths extended, update paths from top
                paths_from_top = extended_path_from_top
            # Now... find energy of each path
            # and find the minimum!
            minimum = None
            for curr_path in paths_from_top:
                curr_sum = sum(self.energy(i, j) for i, j in curr_path)
                if minimum is None:
                    minimum = curr_sum
                    shortest_path = curr_path
                if curr_sum < minimum:
                    minimum = curr_sum
                    shortest_path = curr_path

        return shortest_path

