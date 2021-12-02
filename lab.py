#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main(su_name):
    
    assert isinstance(su_name,str), 'Give me the correct str'
    
    import os

    assert os.path.isfile(su_name), 'No such file!'

    import numpy as np
    import json
    
    #i = iB = 1
    ch=1
    #kB=kB1=kB2=0
    sB=np.array([])
    
    s_inp = np.array(json.load(open(su_name,'r')))
    
    assert s_inp.shape == (9,9), 'Invlid sudoku'
    
    print(s_inp)
    s_inp = np.expand_dims(s_inp, axis=0)
    for i in range(9):
        s_inp = (np.append(s_inp,np.full((1,9,9), 1, dtype=bool),axis=0))
    #print(s_inp)
    
    for i1 in range(9):
        for i2 in range(9):
            s_inp[1:,i1,i2][s_inp[0,i1,i2]!=0]=0
            s_inp[1:,i1,i2][s_inp[0,i1,i2]-1] =1
    
    print('++++ SO HERE IS NUMBER OF POSSIBLE VARIANTS FOR EACH CELL ++++')
    for i1 in range(9):
        for i2 in range(9):
            print(np.where(s_inp[1:,:,:][:,i1,i2]==1)[0].shape[0],end=' ')
        print()
    print('-----------------')
    
            
    def in_cell(n1,n2):
        cell_num = int(n1/3)*3 + int(n2/3)
        return cell_num
    
    def without_pr(num,r_n,c_n,k,i1,i2):
        #in_cell(r_n, c_n) == in_cell(i1, i2)
        if (num ==k and (r_n == i1 or c_n == i2 or in_cell(r_n, c_n) == in_cell(i1, i2))):
            return 0
        else:
            return 1
        
    def check_an_cell(num,r_n,c_n):
        res = np.zeros(9)
        for i1 in range(9):
            for i2 in range(9):
                if(i2 == c_n and i1 == r_n):
                    continue 
                for k in range(1,10):
                    res[k-1] = np.logical_and(s_inp[k,i1,i2], without_pr(num,r_n,c_n,k,i1,i2))
                if not np.any(res):
                    return False
        return True
        
    def solve():   
        for i1 in range(9):
            for i2 in range(9):
                for k in range(1,10):
                    s_inp[k,i1,i2] = s_inp[k,i1,i2] & check_an_cell(k,i1,i2)
        #print( s_inp)
    #BACKUP FOR SELF-CONTROL
    
    sB = s_inp.copy()
    while(ch>0):
        
        s_inp_b = s_inp.copy()
        solve()
        # print('++++ after solve ++++')
        # print('-----------------')
        # for i1 in range(9):
        #     for i2 in range(9):
        #         print(np.where(s_inp[1:,:,:][:,i1,i2]==1)[0][0]+1, end=' ')
        #     print()
        # print('-----------------')
        
        
        while(not np.array_equal(s_inp,s_inp_b)):
            s_inp_b = s_inp.copy()
            solve()
            # for i1 in range(9):
            #     for i2 in range(9):
            #         print(np.where(s_inp[1:,:,:][:,i1,i2]==1)[0][0]+1, end=' ')
            #     print()
            # print('-----------------')
            
        #min for self-control > 1#
        m_n = [20,0,0]
        print('++++ SO HERE IS NUMBER OF POSSIBLE VARIANTS FOR EACH CELL AFTER solve() ++++')
        for i1 in range(9):
            for i2 in range(9):
                cur_n_v = np.where(s_inp[1:,:,:][:,i1,i2]==1)[0].shape[0]
                if cur_n_v < m_n[0] and cur_n_v > 1: 
                    m_n[0] = cur_n_v 
                    m_n[1] = i1
                    m_n[2] = i2
                print(cur_n_v,end=' ')
            print()
        print('-----------------')
        if m_n[0] == 20:
            for i1 in range(9):
                for i2 in range(9): 
                    if (np.array_equal(s_inp[1:,:,:][:,i1,i2], np.zeros(9)) and ch==0):
                        print('no poly')
                        return
                    elif (np.array_equal(s_inp[1:,:,:][:,i1,i2], np.zeros(9)) and ch==1):
                        print('no sol')
                        return
            print('win')
            for i1 in range(9):
                for i2 in range(9):
                    print(np.where(s_inp[1:,:,:][:,i1,i2]==1)[0][0]+1, end=' ')
                print()
            print('-----------------')
            return
        print('possible variant for {}: {}'.format((m_n[1],m_n[2]), np.where(s_inp[1:,:,:][:,m_n[1],m_n[2]]==1)[0] +1))
        ch = m_n[0]
        ch -= 1
        s_inp[(np.where(s_inp[1:,:,:][:,m_n[1],m_n[2]]==1)[0]+1)[0],m_n[1],m_n[2]] =0
        print('minus chance')
                
    print('++++ SO HERE IS NUMBER OF POSSIBLE VARIANTS FOR EACH CELL ++++')
    for i1 in range(9):
        for i2 in range(9):
            cur_n_v = np.where(s_inp[1:,:,:][:,i1,i2]==1)[0].shape[0]
            if cur_n_v < m_n[0] and cur_n_v > 1: 
                m_n[0] = cur_n_v 
                m_n[1] = i1
                m_n[2] = i2
            print(cur_n_v,end=' ')
        print()
    print('-----------------')
                
    print('++++ after solve ++++')
    print('-----------------')
    for i1 in range(9):
        for i2 in range(9):
            print(np.where(s_inp[1:,:,:][:,i1,i2]==1)[0][0]+1, end=' ')
        print()
    print('-----------------')  
           
    
if __name__ == "__main__":
    for x in range(1,8):
        for i in ['sudoku_0{}.json'.format(x)]:
            print(i)
            main(i)
