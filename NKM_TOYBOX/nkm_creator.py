#Landscape Generator
import os
from landscape import *
from RandomGenerator import set_seed
import cPickle, sys
# READ INFLUENCE MATRIX DATA
def read_inf_files(root_path):
    from glob import glob
    files = glob("%s/*.txt" % (root_path,))
    return files
#
def create_landscape(file_name,root_path):
    num_of_lands = 100
    inf = construct_influence_matrix_from_file(file_name,'x')
    lands = develop_landsacpes_from_influence_matrix(inf,num_of_lands) #multiprocessing
    class_of_land = file_name.replace(root_path,'').replace('.txt','')
    os.mkdir(class_of_land)
    for k, land in enumerate(lands):
        set_seed(k)
        fname_out = "%s/nk_%s_tn%03d_s%03d.nkland" % (class_of_land,class_of_land,num_of_lands,k,)
        fout = open(fname_out,'wb')
        cPickle.dump(land,fout)
        fout.close()
if __name__ == "__main__":
    root_path = sys.argv[1]
    print "Start"
    file_names = read_inf_files(root_path)
    for fn in file_names:
        print "...%s in progress" % (fn,)
        create_landscape(fn,root_path)
        print "......done"
    print "\nThank you."