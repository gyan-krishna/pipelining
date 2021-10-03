# -*- coding: utf-8 -*-
"""
----------Phenix Labs----------
Created on Sat Aug 28 19:10:12 2021
@author: Gyan Krishna

Topic: State table generator for unifunction pipeline!
"""
import numpy as np

class state_table:

    def __init__(self, res_table):
        self.res_table = np.array(res_table)
        self.n_stages  = self.res_table.shape[0]
        self.max_t     = self.res_table.shape[1]

    def display_resource_table(self):
        print("    ", end = "")
        for i in range(self.max_t):
            print(i, end = " ")
        print("")
        for i, state in enumerate(self.res_table):
            print( "S{}".format( (i+1) ), end = " ")
            print(state)
        print()

    def extract_forbidden_state(self):
        self.forbidden_states = set()

        for i, stage in enumerate(self.res_table):
            pos_arr = self.get_pos_ones(stage)
            for j, pos in enumerate(pos_arr):
                for k in range(j+1, len(pos_arr)):
                    self.forbidden_states.add(pos_arr[k] - pos)

        self.forbidden_states = list(self.forbidden_states)
        self.forbidden_states.sort()
        print("forbidden states = ", self.forbidden_states)

    def extract_collision_vector(self):
        self.collision_vector = int(0)
        for i in self.forbidden_states:
            self.collision_vector |= 1 << (i-1)

        print("collision vector = ", bin(self.collision_vector))

    def extract_state_table(self):

        self.state_start = [self.collision_vector]
        self.state_table = []
        self.state_set = set([self.collision_vector])

        #flag = False
        ptr = 0 # points to each row of the state table.
        while( ptr < len(self.state_start)):
            zeros = self.get_vector_zeros(self.state_start[ptr])
            row = [0]*(self.max_t-1)
            for pos in zeros:
                tmp = self.state_start[ptr]
                tmp = (tmp >> pos) | self.state_start[0]
                row[pos] = tmp

                ## check if tmp is there in state set or not
                if(tmp not in self.state_set):
                    self.state_set.add(tmp)
                    self.state_start.append(tmp)

            self.state_table.append(row)
            ptr += 1


    def display_state_table(self):
        print("state table :: \n")
        for i, start in enumerate(self.state_start):
            print(str(bin(start))[2:],  "||", end = " ")
            for st in self.state_table[i]:
                if(st == 0):
                    print(str(bin(st))[2:], "\t\t\t", end = "")
                else:
                    print(str(bin(st))[2:], "\t", end = "")
            print()

    def get_pos_ones(self, arr):
        occ = []
        for i, val in enumerate(arr):
            if val == 1:
                occ.append(i)
        return occ

    def get_vector_zeros(self, vector):
        pos = []
        vector = str(bin(vector))[2:]
        vector = vector[::-1]
        for i, val in enumerate(vector):
            if(val == '0'):
                pos.append(i+1)
        return pos


'''
res_table = [[1,0,0,0,0,0,0,0,1],
             [0,1,1,0,0,0,0,1,0],
             [0,0,0,1,0,0,0,0,0],
             [0,0,0,0,1,1,0,0,0],
             [0,0,0,0,0,0,1,1,0]]

res_table = [[1,0,0,0,0,0,0],
             [0,1,0,1,0,0,0],
             [0,0,1,0,1,0,0],
             [0,0,0,0,0,1,0],
             [0,0,0,0,0,0,1]]

res_table = [[0,0,0,0,1],
             [0,1,0,1,0],
             [1,0,1,0,0],]
'''

res_table = [[1,0,0,0,0,0,0,0,1],
             [0,1,1,0,0,0,0,1,0],
             [0,0,0,1,0,0,0,0,0],
             [0,0,0,1,1,0,0,0,0],
             [0,0,0,0,0,1,1,0,0]]



obj = state_table(res_table)
obj.display_resource_table()
obj.extract_forbidden_state()
obj.extract_collision_vector()
obj.extract_state_table()
obj.display_state_table()