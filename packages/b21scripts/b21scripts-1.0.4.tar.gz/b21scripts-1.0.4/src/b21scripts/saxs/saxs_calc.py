'''
Created on Sept 19, 2022

@author: nathan
'''

import glob
import logging
import os
import re
from subprocess import check_output, STDOUT
import sys
import matplotlib.pyplot as plt

class SaxsCalc():
    """Run crysol or Foxs and plot the results
    
    This function of this class is to be able to run crysol or FoXs on
    a pdb file, optionally with a pdb file and plot the result and extract
    chi^2 score as a variable
    """
    
    '''
    Constructor
    '''
    def __init__(self):
        ###start a log file
        self.logger = logging.getLogger('SaxsCalc')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(module)s: %(message)s',"[%Y-%m-%d %H:%M:%S]")
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        if len(self.logger.handlers) == 0:
            self.logger.addHandler(streamhandler)
        self.logger.info('Starting a new SaxsCalc job')        

        ####SET SOME PARAMETERS
        self.datdata = {'Q': [], 'DATA': [], 'FIT': []}
        self.datfile = None
        self.datfile_name = None
        self.pdbfile = None
        self.clean_files = True
        self.number_of_points = 51
        self.subtract_constant = False
        self.chi_score = None
        self.files_for_deletion = []
        
    def AddPdbFile(self, pdbfile):
        if os.path.isfile(pdbfile) and pdbfile[-4:] == '.pdb':
            self.logger.info(f'Added pdb file {pdbfile}')
            self.pdbfile = pdbfile
            return True
        else:
            self.logger.error('You did not enter a valid pdb file')
            return False

    def ReturnPdbFile(self):
        return self.pdbfile

    def ReturnDatFileName(self):
        return self.datfile_name
    
    def AddDatFile(self, datfile):
        if os.path.isfile(datfile) and datfile[-4:] == '.dat':
            self.logger.info(f'Added dat file {datfile}')
            self.datfile = datfile
            self.datfile_name = datfile
            return True
        else:
            self.logger.error('You did not enter a valid dat file')
            return False

    def AutoLimitDatFile(self):
        self.logger.info('cutting out dodgy points from low Q')
        first_good_point = 1
        #test autorg is on the path
        command = 'which autorg'
        output = check_output(command, shell=True).rstrip()
        if not os.path.isfile(output):
            sys.exit('autorg is not on your path, use the -a option to turn off points truncation')
        #parse the dat data
        dat_data = {'Q': [], 'I': [], 'E': []}
        if self.datfile:
            with open(self.datfile) as f:
                filedata = f.readlines()
            for line in filedata:
                line = line.rsplit()
                try:
                    dat_data['Q'].append(float(line[0]))
                    dat_data['I'].append(float(line[1]))
                    dat_data['E'].append(float(line[2]))
                except:
                    pass
            #find out where its good from
            command = f'autorg {self.datfile}'
            output = check_output(command, shell=True).decode('utf-8').split('\n')
            for line in output:
                if line[:6] == 'Points':
                    try:
                        first_good_point = int(line.split()[1]) - 1
                    except:
                        self.logger.error('could not determine good points from autorg')
            #write out the good data
            if first_good_point > 1:
                self.logger.info(f'will not include points below: {first_good_point}')
                outstring_array = []
                for index, q in enumerate(dat_data['Q']):
                    outstring_array.append('{0: <16.9f}{1: <16.9f}{2: <16.9f}'.format(
                                q,
                                dat_data['I'][index],
                                dat_data['E'][index]))
                outfile_name = 'saxscalc.dat'
                outfile = open(outfile_name, 'w')
                outfile.write('\n'.join(outstring_array[first_good_point:]))
                outfile.close()
                self.datfile = outfile_name
                self.files_for_deletion.append(outfile_name)
            
    def SetNumberOfPoints(self, number_of_points=51):
        if type(number_of_points) == type(1):
            self.logger.info(f'Number of points set to: {number_of_points}')
            self.number_of_points = number_of_points
            return True
        else:
            self.logger.error('SetNumberOfPoints needs an integer as an argument')
            return False

    def SetCleanFiles(self, clean_files=True):
        if type(clean_files) == type(True):
            if clean_files:
                self.logger.info('Will remove files after running')
            else:
                self.logger.info('Will not remove files after running')
            self.clean_files = clean_files
            return True
        else:
            self.logger.error('SetCleanFiles needs a boolean (True or False)')
            return False

    def SetSubtractConstant(self, subtract_constant=True):
        if type(subtract_constant) == type(True):
            if subtract_constant:
                self.logger.info('Will subtract a constant')
            else:
                self.logger.info('Will not subtract a constant')
            self.subtract_constant = subtract_constant
            return True
        else:
            self.logger.error('SetSubtractConstant needs a boolean (True or False)')
            return False

    def OutputChiScore(self):
        self.logger.info(f'Chi score is: {self.chi_score}')
        return self.chi_score

    def DeleteFiles(self):
        self.logger.info('Deleting output files')
        for file in self.files_for_deletion:
            os.remove(file)

    def PlotTheFit(self, outfile=False):
        self.logger.info('Plotting the data')
        fig = plt.figure()
        ax1 = fig.add_subplot(111, autoscale_on=True)
        ax1.plot(self.datdata['Q'], self.datdata['DATA'], marker='.', color='0.55', markersize = 4.0, linestyle='None')
        ax1.plot(self.datdata['Q'], self.datdata['FIT'], marker='None', color='0', linewidth=2.0, linestyle='-')
        ax1.set_xlabel('$Q (\AA^{-1}$)', fontsize=20, color='black')
        ax1.set_ylabel('$I(0)$', fontsize=20, color='black')
        ax1.set_yscale('log')
        ax1.set_xscale('log')
        ax1.autoscale(enable=True, axis='both', tight=None)
        if outfile:
            plt.savefig(outfile)
        plt.show()
        
    def RunFoxs(self):
        self.logger.info('Running FoXS')
        #test foxs is on the path
        command = 'which foxs'
        output = check_output(command, shell=True).rstrip()
        if not os.path.isfile(output):
            sys.exit('foxs is not on your path, try the -j crysol option')

        command = f'foxs -s {self.number_of_points} '

        if self.subtract_constant:
            command = f'{command} -o '

        if not self.pdbfile:
            self.logger.error('Cannot execute run foxs without a pdb file')
            return False
        else:
            command = f'{command} {self.pdbfile}'

        if self.datfile:
            command = f'{command} {self.datfile}'

        filelist_before = os.listdir(os.getcwd())
        output = check_output(command, shell=True, stderr=STDOUT).decode('utf-8')
        filelist_after = os.listdir(os.getcwd())
        self.files_for_deletion = self.files_for_deletion + list(set(filelist_after) - set(filelist_before))

        output = output.split('\n')
        pattern = re.compile('.* Chi\^2 = .*')
        for line in output:
            if re.match(pattern, line):
                line = line.split()
                try:
                    self.chi_score = "%.3f" % (float(line[line.index('=')+1]))
                except:
                    self.logger.error('Could not find chi in the foxs output')
                    self.chi_score = "****"
        if self.datfile:
            #PARSE THE FIT FILE
            fitfile = self.pdbfile[:-4]+'_'+self.datfile
            with open(fitfile) as f:
                filedata = f.readlines()
            for line in filedata:
                line = line.rsplit()
                try:
                    self.datdata['Q'].append(float(line[0]))
                    self.datdata['DATA'].append(float(line[1]))
                    self.datdata['FIT'].append(float(line[2]))
                except:
                    pass
                
            #TEST THE OUTPUT
            if len(self.datdata['Q']) > 0:
                return True
            else:
                return False


        
    def RunCrysol(self):
        self.logger.info('Running Crysol')
        #test crysol is on the path
        command = 'which crysol'
        output = check_output(command, shell=True).rstrip()
        if not os.path.isfile(output):
            sys.exit('crysol is not on your path, try the -j foxs option')

        command = f'crysol -ns {self.number_of_points} '
        
        if self.subtract_constant:
            command = f'{command} -cst '

        if not self.pdbfile:
            self.logger.error('Cannot execute runCrysol without a pdb file')
            return False
        else:
            command = f'{command} {self.pdbfile}'

        if self.datfile:
            command = f'{command} {self.datfile}'
        
        filelist_before = os.listdir(os.getcwd())
        output = check_output(command, shell=True).decode('utf-8')
        filelist_after = os.listdir(os.getcwd())
        self.files_for_deletion = self.files_for_deletion + list(set(filelist_after) - set(filelist_before))

        if self.datfile:
            #PARSE THE CRYSOL OUTPUT
            output = output.split('\n')
            try:
                index = [i for i, item in enumerate(output) if re.search('.*Chi.*', item)][-1]
                self.chi_score = "%.3f" % (float(output[index].split(':')[-1]))
            except:
                self.logger.error('Could not find chi in the crysol output')
                self.chi_score = "****"
    
            #PARSE THE FIT FILE
            fitfile = [ m for m in self.files_for_deletion if m[-4:] == '.fit'][0]
            with open(fitfile) as f:
                filedata = f.readlines()
            for line in filedata:
                line = line.rsplit()
                try:
                    self.datdata['Q'].append(float(line[0]))
                    self.datdata['DATA'].append(float(line[1]))
                    self.datdata['FIT'].append(float(line[3]))
                except:
                    pass
    
            #REMOVE EXTRAPOLATED POINTS AT START OF FIT
            while self.datdata['DATA'][0] == self.datdata['DATA'][1]:
                del self.datdata['Q'][0]
                del self.datdata['DATA'][0]
                del self.datdata['FIT'][0]
            del self.datdata['Q'][0]
            del self.datdata['DATA'][0]
            del self.datdata['FIT'][0]
                
            #TEST THE OUTPUT
            if len(self.datdata['Q']) > 0:
                return True
            else:
                return False


