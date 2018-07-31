import random
import sys

class Solver_8_queens(object):

    def __init__(self, pop_size=100, cross_prob=0.5, mut_prob=0.25):
        rows = 8
        cols = 2
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.best_fit = 0
        self.epoch_num = 0
        self.visualization=""
        self.pop = [[[self.randomize(ROWS,COLS) for COLS in range(cols)] for ROWS in range(rows)]for POP_SIZE in range(pop_size)]

    def randomize(self,rows,cols):
        if cols == 0:
            result = rows
        else:
            result = random.randint(0,7)
        return (result)

    def fitness(self,a):
        result = 1
        r0 = 0
        while r0 < 8:
            r1 = 0
            while r1 < 8:
                if a[r0][0] == a[r1][0] and r0 != r1:
                    result = result - 0.06
                if a[r0][1] == a[r1][1] and r0 != r1:
                    result = result - 0.06
                if a[r0][0] - a[r0][1] == a[r1][0] - a[r1][1] and r0 != r1:
                    result = result - 0.06
                r1 = r1 + 1
            r0 = r0 + 1
        if result < 0:
            result = 0.01
        return (result)

    def crossover(self,parent1,parent2):
        i = 0
        while i < 8:
            temp1 = str(bin(parent1[i][1]))[2:]
            if len(temp1) == 1:
                temp1 = "00" + temp1
            if len(temp1) == 2:
                temp1 = "0" + temp1
            temp2 = str(bin(parent2[i][1]))[2:]
            if len(temp2) == 1:
                temp2 = "00" + temp2
            if len(temp2) == 2:
                temp2 = "0" + temp2
            cut = random.randint(1, 2)
            temp1left = temp1[:cut]
            temp1right = temp1[cut:]
            temp2left = temp2[:cut]
            temp2right = temp2[cut:]
            temp1 = temp1left + temp2right
            temp2 = temp2left + temp1right
            temp1 = int("0b" + temp1, 2)
            temp2 = int("0b" + temp2, 2)
            parent1[i][1] = temp1
            parent2[i][1] = temp2
            i = i + 1
        return (parent1,parent2)

    def mutation(self,a):
        i = random.randint(0, 7)
        temp = str(bin(a[i][1]))[2:]
        if len(temp) == 1:
            temp = "00" + temp
        if len(temp) == 2:
            temp = "0" + temp
        invert = random.randint(0, 2)
        if temp[invert] == "0":
            temp = temp[:invert-1] + "1" + temp[:invert+1]
        else:
            temp = temp[:invert-1] + "0" + temp[:invert+1]
        temp = int("0b" + temp, 2)
        a[i][1] = temp
        return (a)

    def draw(self,a):
        rows = 8
        cols = 8
        n = 8
        ROWS = 0
        result = ""
        symbol = ""
        while ROWS < rows:
            COLS = 0
            while COLS < cols:
                nn = 0
                while nn < n:
                    if a[nn][0] == ROWS and a[nn][1] == COLS:
                        symbol = "Q"
                        break
                    else:
                        symbol = "+"
                    nn = nn + 1
                result = result + symbol
                COLS = COLS + 1
            result = result + "\n"
            ROWS = ROWS + 1
        return (result)
    
    def solve(self, min_fitness=0.9, max_epochs=100):
        best_fitness = 0
        rembr = 0
        epochs = 0
        while epochs < max_epochs:
            num = 0
            fit_list = [0 for num in range(self.pop_size)]
            R_divider = 0
            while num < self.pop_size:
                fit_list[num] = self.fitness(self.pop[num])
                if fit_list[num] > best_fitness:
                    best_fitness = fit_list[num]
                    rembr = num
                R_divider = R_divider + fit_list[num]
                num = num + 1
            snum = 0
            select = [0 for snum in range(self.pop_size)]
            while snum < self.pop_size:
                select[snum] = fit_list[snum]/R_divider
                snum = snum + 1
            if best_fitness <= min_fitness:
                if random.random() <= self.cross_prob:
                    i = 0
                    while i < self.pop_size:
                        if random.random() <= select[i]:
                            j = 0
                            while j < self.pop_size:
                                if random.random() <= select[j] and i != j:
                                    self.pop[i], self.pop[j] = self.crossover(self.pop[i], self.pop[j])
                                j = j + 1
                        i = i + 1
                if random.random() <= self.mut_prob:
                    i = random.randint(0, self.pop_size - 1)
                    self.pop[i] = self.mutation(self.pop[i])
            else:
                break
            num = 0
            best_fitness = 0
            fit_list = [0 for num in range(self.pop_size)]
            while num < self.pop_size:
                fit_list[num] = self.fitness(self.pop[num])
                if fit_list[num] > best_fitness:
                    best_fitness = fit_list[num]
                    rembr = num
                num = num + 1
            epochs = epochs + 1
        self.visualization=self.draw(self.pop[rembr])
        self.best_fit = best_fitness
        self.epoch_num = epochs
        return (self.best_fit, self.epoch_num, self.visualization)

solver=Solver_8_queens()
best_fit, epoch_num, visualization=solver.solve()

print("Best solution:")
print("Fitness:",best_fit)
print("Iterations:",epoch_num)
print(visualization)