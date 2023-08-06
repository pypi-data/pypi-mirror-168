# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 17:12:28 2022

replace tqdm without additional package install.

@author: Donggeun Kwon (donggeun.kwon at gmail.com)
"""

class progress_bar(object):
    '''
    you can replace tqdm without additional package install.
     
    '''
    def __init__(self, title='', **kwarg):
        '''
        progress bar with callback
        
        Parameters
        ----------
        title : str, optional
            It will display in front of the bar. The default is ''.
        scale : int
            scale of bar, the default is terminal's window size.
        verbose : int (> 1, 100 >=)
            freq of printing the progress bar. When it is 1, then always.
            If more than, only print when current percent is a multiple 
            of verbose. The default is 1.

        Returns
        -------
        None.

        '''
        assert type(title)==str, "title must be string"
        self.title = title
        
        if list(kwarg)==[]:
            scale = None
            verbose = 1
        else:
            kw = list(kwarg)
            for k in kw:
                assert k in ['scale', 'verbose'], "can input only 'scale', 'verbose'."
        
            try: scale = kwarg['scale']
            except: pass
            try: verbose = kwarg['verbose']
            except: pass
    
        if scale is not None:
            self.scale = scale
        else:    
            try:
                try:
                    import os
                    terminal_width = os.get_terminal_size()[1]
                except:
                    import shutil
                    terminal_width = shutil.get_terminal_size()[1]
            except:
                self.scale = 10
            else:
                self.scale = terminal_width - 6
                
        assert type(verbose)==int, "verbose must be a int type."
        if verbose > 100:
            verbose = 100
        elif verbose < 1:
            verbose = 1
        self.verbose = verbose
    
    def __call__(self, current, total):
        '''
        dont call me
        '''
        current_percent = int((current / total) * 100)
        
        if (current_percent != 0) and (current_percent % self.verbose):
            return None
        
        print("\r"+self.title+" {0:3d}%|".format(current_percent), end='')
        
        scal_c = int((current_percent/100) * self.scale)
        scal_l = self.scale - scal_c
        
        # done
        for i in range(scal_c):
            print("█", end='')
        
        # not 
        for i in range(scal_l):
            print(" ", end='')
        
        print("|", end="")
        
        if total==current:
            print("")

        return None

'''
# test
if __name__ == '__main__':
    def time_sleep(t, clb=None):
        # import time
        for i in range(t):
            # time.sleep(0.001)
            if clb is not None:
                clb(i+1, t)                
        return None
    
    clb = progress_bar(title="hello world")
    time_sleep(100, clb)
'''
