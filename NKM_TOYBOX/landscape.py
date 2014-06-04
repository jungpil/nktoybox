'''
landscape.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''
import numpy as NP #Numpy
import RandomGenerator
import copy
import sys
import itertools
#cython modules
#import inf_util

class InfluenceMatrix:
    """
|  ** ABOUT DEPENDENCE MATRIX **
|  A valid input matrix must be a square matrix with 0's and 1's. The
|  diagonal entries must be all 1's. The number of 1's in each row should be
|  the same.
|
|  ** EXAMPLE **
|  If the input matrix is a valid influence matrix, then extract the value
|  of N and K, and also store the dependent elements for each element
|  explicitly. N is the number of elements, K is the number of dependent
|  elements that one element can have.
|
|  E.g., input matrix T is
|                *0 *1 *2
|  element #0 ->[[1, 1, 0]
|  element #1 -> [1, 1, 0]
|  element #2 -> [0, 1, 1]],
|
|  then N = 3, K = 1,
|  dependent element of element #0 is *1, dependent element of element #1 is *0,
|  dependent element of element #2 is *1.
|
|  Therefore, the dependent matrix should be:
|  [[1, 0, 0]
|   [0, 0, 0]
|   [1, 0, 0]]
|  (In this case, K == 1)
|
|  E.g., input matrix R is
|                *0 *1 *2 *3
|  element #0 ->[[1, 0, 1, 1]
|  element #1 -> [1, 1, 1, 0]
|  element #2 -> [0, 1, 1, 1]
|  element #3 -> [1, 1, 0, 1]],
|
|  then N = 4, K = 2,
|  dependent elements of element #0 is *2 and *3,
|  dependent elements of element #1 is *0 and *1, dependent elements of element #2 is *1 and 3,
|  dependent elements of element #3 is *0 and *1.
|
|  The dependent matrix is:
|
|  [[2, 3, 0, 0]
|   [0, 1, 0, 0]
|   [1, 3, 0, 0]
|   [0, 1, 0, 0]]
|  (K == 2)
|
|  ** NUMPY **
|  To learn more about Numpy, http://docs.scipy.org/doc/numpy/user
    """
    def __init__(self,influence_matrix = None,matrix_input = None):
        # CONSTRUCTOR
        if influence_matrix != None and matrix_input == None: # If only an influence matrix is given,
            self.my_N = influence_matrix.my_N # copy N
            self.my_K = influence_matrix.my_K # copy K
            self.my_raw_matrix = influence_matrix.my_raw_matrix # reference raw matrix
            self.my_dependence_matrix = influence_matrix.my_dependence_matrix.copy() #numpy array, just copy
        elif matrix_input != None and influence_matrix == None: # If a Numpy matrix is given,
            self.my_N = matrix_input.shape[0]
            self.my_K = 0
            # ASSERTION - IF NOT MET, TERMINATE PROGRAM IMMEDIATELY.
            assert self.chk_matrix_shape(matrix_input), "Invalid length of influence matrix in row!"
            assert self.chk_valid_entry(matrix_input), "Invalid entry value of influence matrix in position!"
            assert self.chk_diagonal_elements(matrix_input), "Invalid self-dependence in row!"
            self.my_K = matrix_input[0].sum() - 1 # traces must not be included! s.t. -1
            assert self.chk_consistent_K(matrix_input), "Inconsistent K between rows!"
            if self.my_K == 0: # even landscape, no need to think about dependent matrix
                self.my_raw_matrix = None
                self.my_dependence_matrix = None
            else: # major part
                self.my_raw_matrix = matrix_input
                self.my_dependence_matrix = NP.zeros(self.my_N**2,dtype=NP.int).reshape((self.my_N,self.my_N,)) # zero matrix, the same size
                temp_matrix = matrix_input.copy() #copy of the input
                temp_matrix = temp_matrix - NP.diag(NP.diag(temp_matrix)) #change diagonal elements as zeros
                temp_matrix = (temp_matrix == 1) #mark places of 1 in the matrix (1=True, o.w=False)
                for _,row in enumerate(temp_matrix): #for each row
                    idx = NP.where(row == True)[0] #get an index of element
                    self.my_dependence_matrix[_,:len(idx)] = idx #store index values in sequence (queuing)
                del temp_matrix #delete memory reference instantly
    def chk_matrix_shape(self,matrix_input):
        # ASSERTION
        dimensions = matrix_input.shape
        if dimensions[0] != dimensions[1]:
            return False # not rectangle
        if dimensions[0] == 0:
            return False # not even one element
        return True
    def chk_valid_entry(self,matrix_input):
        # ASSERTION
        judge = ((matrix_input == 0) + (matrix_input == 1)).all() #should be zero or one
        return judge
    def chk_diagonal_elements(self,matrix_input):
        # ASSERTION
        diagonal_array = matrix_input.diagonal()
        judge = (diagonal_array == 1).all()
        return judge
    def chk_consistent_K(self,matrix_input):
        # ASSERTION
        result_comparison_by_column = (NP.sum(matrix_input,1) - 1)[1:] - self.my_K
        judge = (result_comparison_by_column == 0).all()
        return judge
    def get_dependent_elements_of(self,row_idx):
        # ASSERTION
        #return inf_util.get_dependent_element_of(self.my_dependence_matrix,row_idx,self.my_K)
        a = self.my_dependence_matrix[row_idx][:self.my_K]
        return a.copy()
    def __str__(self):
        info = "N = %05d, K = %05d\n" % (self.my_N,self.my_K,)
        line = "--------------------\n"
        matrix_str = self.my_raw_matrix.__str__().replace("\n",";") #matrix -> [[0,1,2];[3,4,5];[6,7,8]]
        return "%s%s%s" % (info,line,matrix_str)
class FitnessContributionTable:
    """
|  ** INTRODUCTION **
|  Internally create a 3-dimensional table, by N by 2 by 2^K, where N and K
|  are from the influence matrix. Dimension 1 represents N elements.
|  Dimension 2 represents the 2 choices (i.e. 0 or 1) for one element.
|  Dimension 3 represents all the possible combination of one element's
|  dependent elements.
|
|  ** HOW TO GENERATE CONTRIBUTION VALUE **
|  The value is a randomly generated fitness contribution value between 0 to 1.
|
|  ** EXAMPLE **
|  Let's suppose that we have N = 3 and K = 1.
|  The fitness contribution table should be:
|  [
|  [[0<-0.001,1<-0.343]
|   [0<-0.334,1<-0.998]]
|  [[0<-0.991,1<-0.134]
|  ...
|  ]
|  (index in binary code<-value)
|
|  E.g., when N = 6 and K = 5, the value in [0][1][5] gives the fitness
|  contribution value when "the 0th element" is "1" given
|  "its 5 dependent elements are 0,0,1,0,1 respectively".
|
|  E.g., when N = 4 and K = 2, the value in [1][0][1] gives the fitness
|  contribution value when "the 1st element" is "0" given
|  "its 2 dependent elements are 0,1 respectively".

    """
    def __init__(self,influence_matrix):
        # CONSTRUCTOR
        self.influence_matrix = influence_matrix
        self.dim_1 = self.influence_matrix.my_N
        self.dim_2 = 2
        self.dim_3 = 1 << self.influence_matrix.my_K # i.e., power of 2 by K
        self.my_table = RandomGenerator.random_generator.rand(self.dim_1,self.dim_2,self.dim_3) #Mersenne Twister Random Generator
            # random generate of three dimensional table
    def get_value_of(self, index_1, index_2, index_3):
        #return inf_util.get_value_of(self.my_table,index_1,index_2,index_3)
        return self.my_table[index_1][index_2][index_3]
    def __str__(self):
        # REPRESENTATION
        print_limit = 1000 # limit of size
        str_table = self.my_table.__str__().replace("\n",";")
        str_info = "Fitness Contribution Table\n--------------------------\nN = %d\nChoice = %d\nCombination = %d\n" % (self.dim_1,self.dim_2,self.dim_3,)
        if len(str_table) > print_limit:
            str_table = str_table[:print_limit]
        result = "%s%s\n" % (str_info,str_table,)
        return result
class Landscape:
    def __init__(self,influence_matrix = None,fitness_contribution_matrix = None):
        self.influence_matrix = influence_matrix
        self.locations_list = []
        self.fitness_value = NP.array([])
        self.standardized_fitness_value = None
        if influence_matrix != None and fitness_contribution_matrix == None:
            self.influence_matrix = influence_matrix
            self.fitness_contribution_table = FitnessContributionTable(self.influence_matrix) # KEY!
        elif influence_matrix == None and fitness_contribution_matrix != None:
            self.fitness_contribution_table = fitness_contribution_matrix
            self.influence_matrix = fitness_contribution_matrix.influence_matrix
    def get_influence_matrix_N(self):
        return self.influence_matrix.my_N
    def get_influence_matrix_K(self):
        return self.influence_matrix.my_K
    def get_score_of_location_by_id(self,location_id): # KEY!
        """
|  Return the fitness value of the given location id. If the performance
|  value was cached, return the cached value. Otherwise, compute and cache
|  the performance value, then return.
        """
        return self.fitness_value[location_id]
    def get_noised_score_of_location_by_id(self,location_id, func=None, **kargs): # KEY!
        c_i = self.fitness_value[location_id]
        e_i = func(c_i=c_i, **kargs)
        return e_i
    def compute_all_locations_id(self, fix_plan=None):
        """
|  Brutely compute all before we do something
        """
        map_size = 1 << self.get_influence_matrix_N()
        self.locations_list = []
        add_locs = self.locations_list.append
        self.fix_plan = fix_plan
        for i in xrange(map_size):
            add_locs(self.location_id_to_location(i))
        '''
        Calculate all fitness_value
        '''
        if fix_plan == None:
            self.fitness_value = NP.array(map(self.compute_score_for_location_id,xrange(map_size)))
        else:
            result_temp = []
            result_temp_add = result_temp.append
            for l_id in xrange(map_size):
                result_temp_add(self.compute_score_for_location_id(l_id,fix_plan = fix_plan))
            self.fitness_value = NP.array(result_temp)
        '''
        Statistics
        '''
        self.fitness_value = NP.around(self.fitness_value,4)
    def compute_score_for_location_id(self,location_id,fix_plan=None,reduced=True):
        """
|  Compute and return the fitness value of the given location id.
|  fix_plan indicates cognitive representation for low dimensionality (see Gavetti 2000)
        """
        assert len(self.locations_list) > 0, "You should specify location ids first."
        locations = self.locations_list[location_id] # first, we need location, ndarray(int)
        result = 0.0 #float
        c_is = []
        if fix_plan == None or fix_plan == range(self.get_influence_matrix_N()):
            coverage = range(self.get_influence_matrix_N())
            for i in coverage:
                idx1 = i # in sequence
                idx2 = locations[i] # case determined by location id
                idx3 = 0
                if self.get_influence_matrix_K() > 0:
                    dependence = self.influence_matrix.get_dependent_elements_of(i) # given row
                    locations.dtype = NP.int
                    dependence.dtype = NP.int
                    #idx3 = inf_util.compute_idx3(self.get_influence_matrix_K(),locations,dependence)
                    x = locations[dependence]
                    a = NP.ones(self.get_influence_matrix_K(),dtype=NP.int) * 2
                    b = NP.arange(self.get_influence_matrix_K(),dtype=NP.int)
                    y = a ** b[::-1] #inverse
                    idx3 = NP.dot(x,y) # step by 2, (0,1), (0,1,2,3), (0,1,2,3,4,5,6,7), (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15) <- spanning vector space (for e.g.)
                    #idx3_n = 2^n*a_0 + 2^(n-1)*a_1 +...+2^1*a_(n-1)+a_n
                score = self.fitness_contribution_table.get_value_of(idx1, idx2, idx3)
                result += score
                if not reduced:
                    c_is.append(score)
            rv = result / float(len(coverage))
        else:
            assert len(fix_plan) > 0, "You should suggest at least one decision element."
            N = self.get_influence_matrix_N()
            N1 = len(fix_plan)
            N2 = N - N1
            unknown_effect = self.create_dimension_external_element(locations,fix_plan)
            rv = unknown_effect
            if not reduced:
                c_is.extend([unknown_effect for _ in range(N2)])
        if reduced:
            return rv
        else:
            return (rv,NP.array(c_is))
    def location_id_to_location(self,location_id):
        """
|  Return an integer array that "looks" like the binary form of the given
|  location id. E.g., when N = 4, location id = 13, then the array is
|  [1,1,0,1]
        """
        N = self.get_influence_matrix_N()
        #return inf_util.location_id_to_location(N,location_id) #cython extension
        idx = NP.arange(N)
        locations = ((location_id/(2**(N - 1 - idx))) % 2).astype(NP.int)
        return locations
    def location_to_location_id(self,locations):
        locid = 0
        for i in locations:
            locid <<=1
            locid += i
        return locid
    def toggle_element_in_location_id(self,location_id, element_id):
        """
|  Return a location id whose binary form is one bit different from the
|  given location id, and the position of the different bit is determined by
|  the given element index.
|
|  E.g., when N = 4, location id = 13, element index = 1, then the binary
|  form is [1,1,0,1]. The new binary form is [1,0,0,1] and the new location
|  id is 9.
        """
        shift_amount = self.get_influence_matrix_N() - 1 - element_id
        if ((location_id >> shift_amount) % 2) == 0:
            par = 1
        else:
            par = -1
        comp_line_1 = location_id + (1 << shift_amount) * par
        return comp_line_1 #new location_id
    def get_neighbors_inclusive(self,location_id, elements, processing_power):
        """
|  ** INTRODUCTION **
|  Define the distance between two configurations/locations to be the number
|  of different element values.
|
|  ** EXAMPLE **
|  E.g., distance between configurations 1,0,0,0 and 1,0,0,1 is 1, distance
|  between configurations 1,0,0,0 and 0,1,1,0 is 3.
|
|  ** DISTANCE AND ELEMENT CONFIGURATION **
|  Define the distance between two configurations/locations w.r.t. a set of
|  element indices to be the number of different element values in and ONLY
|  in the given set of element indices.
|
|  E.g., the set of all configurations whose distances to configuration
|  1,0,0,0 are 1 w.r.t. element indices {0,1,2} is {[0,0,0,0], [1,1,0,0],
|  [1,0,1,0]}
|
|  E.g., the set of all configurations whose distances to configuration
|  1,0,0,0 are 2 w.r.t. element indices {0,1,2} is {[1,1,1,0], [0,1,0,0],
|  [0,0,1,0]}

|  This method returns the set of all location ids whose distances to the
|  given location id w.r.t. the given elements are smaller or equal to the
|  given processing power.
        """
        result = set()
        if processing_power == 0 or len(elements) == 0:
            #TEST
            try:
                result.add(location_id)
            except:
                print "ERROR"
                sys.exit()
            return result
        reduced_element = copy.deepcopy(elements) #deep copy
        itr = iter(reduced_element) #get iterator
        next_element = itr.next()
        toggle_location_id = self.toggle_element_in_location_id(location_id, next_element)
        reduced_element.remove(next_element)
        result = self.get_neighbors_inclusive(toggle_location_id, reduced_element, processing_power - 1)
        result = result.union(self.get_neighbors_inclusive(location_id, reduced_element, processing_power))
        return result # Be careful, the input location_id is included in the result. You should clear it before using....
    def who_are_neighbors(self,location_id, elements, processing_power,include_myself=True):
        """
        delegated method of get_neighbors_inclusive
        """
        ls = list(self.get_neighbors_inclusive(location_id, elements, processing_power))
        if not include_myself:
            ls.remove(location_id)
        return set(ls)
    def change_element(self, loc_id,loc_id_mask,changable_elements):
        locations = self.location_id_to_location(loc_id)
        location_masks = self.location_id_to_location(loc_id_mask)
        for i in changable_elements:
            locations[i] = location_masks[i]
        return self.location_to_location_id(list(locations))
    def create_dimension_external_element(self,locations,bounded_elements):
        N = len(locations) - len(bounded_elements)
        seq_rep = [list(s) for s in itertools.product("01",repeat=N)]
        seq_rep = NP.array(seq_rep,dtype=NP.int)
        locations_new = []
        if seq_rep.size > 0:
            for sr in seq_rep:
                blank = locations.copy()
                new_mask = list(set(NP.arange(locations.size)) - set(bounded_elements))
                blank[new_mask] = sr
                locations_new.append(blank)
        else:
            locations_new.append(locations)
        original_ids = []
        for lnew in locations_new:
            original_ids.append(self.location_to_location_id(lnew))
        #unbounded_element = list(set(range(self.get_influence_matrix_N())) - set(bounded_elements))
        unbounded_element = range(self.get_influence_matrix_N())
        results = []
        for original_id in original_ids:
            locations_orign = self.locations_list[original_id]
            result = 0.0 #float
            coverage = unbounded_element
            for i in coverage:
                idx1 = i # in sequence
                idx2 = locations_orign[i] # case determined by location id
                idx3 = 0
                if self.get_influence_matrix_K() > 0:
                    dependence = self.influence_matrix.get_dependent_elements_of(i) # given row
                    x = locations_orign[dependence]
                    a = NP.ones(self.get_influence_matrix_K(),dtype=NP.int) * 2
                    b = NP.arange(self.get_influence_matrix_K(),dtype=NP.int)
                    y = a ** b[::-1] #inverse
                    idx3 = NP.dot(x,y)
                score = self.fitness_contribution_table.get_value_of(idx1, idx2, idx3)
                result += score
            results.append(result/float(len(coverage)))
        results = NP.array(results)
        average_effect_from_unknown = float(results.mean())
        return average_effect_from_unknown
    def standardize(self):
        assert len(self.fitness_value) > 0, "No fitness values are assigned."
        self.fitness_max = NP.max(self.fitness_value)
        self.fitness_min = NP.min(self.fitness_value)
        self.fitness_mean = NP.mean(self.fitness_value)
        self.standardized_fitness_value = self.fitness_value / self.fitness_max
    def get_standardized_value(self,fitness_value):
        if self.standardized_fitness_value == None:
            self.standardize()
        return fitness_value / float(self.fitness_max)
# =====================================
class LandscapeAdaptive(Landscape):
    def __init__(self,influence_matrix = None,fitness_contribution_matrix = None):
        Landscape.__init__(self,influence_matrix=influence_matrix,fitness_contribution_matrix=fitness_contribution_matrix)
        self.fitness_value_dict = {} # main data set
        self.fitness_correction_item = {} #c_i for algorithm
        self.fix_plan = None
        self.standardized_fitness_value_dict = None
    def compute_all_locations_id(self, fix_plan=None):
        """
|  Brutely compute all before we do something
        """
        map_size = 1 << self.get_influence_matrix_N()
        self.locations_list = []
        add_locs = self.locations_list.append
        self.fix_plan = fix_plan
        for i in xrange(map_size):
            add_locs(self.location_id_to_location(i))
    def shocked(self,shock_func,**kargs):
        """
Dynamism represents the notion that requirements may change over time, which can
be modeled a the landscape undergoing correlated shocks at some point in time during the RE process.
Intuitively, one might think of this as searching across a landscape beset by earthquakes.
Once a landscape is created, every delta periods, each contribution value c_i
        """
        self.fitness_contribution_table.my_table = shock_func(contribution_table=self.fitness_contribution_table.my_table,**kargs)
        # replace to new contribution values
        # CORRECTION
        for key in self.fitness_value_dict.keys():
            self.fitness_value_dict[key],self.fitness_correction_item[key] = self.compute_score_for_location_id(location_id,fix_plan=self.fix_plan,reduced=False)
    def get_score_of_location_by_id(self,location_id): # KEY!
        try:
            return self.fitness_value_dict[location_id]
        except KeyError:
            self.fitness_value_dict[location_id],self.fitness_correction_item[location_id] = self.compute_score_for_location_id(location_id,fix_plan=self.fix_plan,reduced=False)
            return self.fitness_value_dict[location_id]
    def get_noised_score_of_location_by_id(self,location_id, func = None, **kargs): # KEY!
        try:
            check = self.fitness_value_dict[location_id]
            c_i = self.fitness_correction_item[location_id]
        except:
            self.fitness_value_dict[location_id],c_i = self.compute_score_for_location_id(location_id,fix_plan=self.fix_plan,reduced=False)
            self.fitness_correction_item[location_id] = c_i
            #if there is no true fitness value is not defined, update it.
        e_i = func(c_i=c_i, **kargs)
        return e_i
    def standardize(self):
        assert len(self.fitness_value_dict) > 0, "No fitness values are assigned."
        fitness_value = NP.array(self.fitness_value_dict.values())
        self.fitness_max = NP.max(fitness_value)
        self.fitness_min = NP.min(fitness_value)
        self.fitness_mean = NP.mean(fitness_value)
        standardized_fitness = fitness_value / self.fitness_max
        self.standardized_fitness_value_dict = dict(zip(self.fitness_value_dict.keys(),standardized_fitness))
    def get_standardized_value(self,fitness_value):
        if self.standardized_fitness_value_dict == None:
            self.standardize()
        return fitness_value / float(self.fitness_max)
class Probe:
    def __init__(self):
        self.location_id = -1
        self.performance = 0.0
        self.moved = False
def count_local_peak(landscape,plan=None):
    N = landscape.get_influence_matrix_N()
    total_scope = 2**N
    if plan == None:
        full_plan = range(N)
    else:
        full_plan = plan
    probes = []
    for current_id in xrange(total_scope):
        probe = Probe()
        probe.location_id = current_id
        probe.performance = landscape.get_score_of_location_by_id(probe.location_id)
        probes.append(probe)
        while 1:
            neighbors = landscape.who_are_neighbors(probe.location_id,full_plan,1,True)
            scores = []
            max_score = -1
            max_id = -1
            for n in neighbors:
                nei_score = landscape.get_score_of_location_by_id(n)
                if nei_score > max_score:
                    max_id = n
                    max_score = nei_score
                elif nei_score == max_score and n > max_id:
                    max_id = n
            if max_score > probe.performance:
                probe.location_id = max_id
                probe.performance = max_score
                probe.moved = True
            elif max_score == probe.performance:
                if max_id > probe.location_id:
                    probe.location_id = max_id
                    probe.moved = True
                else:
                    break
            elif max_score < probe.performance and probe.moved == False:
                probe.moved = True
                break
            else:
                break
    all_peak = []
    for probe in probes:
        if probe.moved:
            all_peak.append(probe.location_id)
    all_peak = set(all_peak)
    return len(all_peak)
'''
Utilities
'''
def construct_influence_matrix_from_file(file_name, markchr='1'):
    """
|  You can construct an influence matrix from a text file.
|  Input should have a marking character to indicate an association (or relationship).
|  The default value is '1' (i.e., text 1); but you can use any character if you identify it properly.
|  E.g., you can use 'x': >>> construct_influence_matrix_from_file('input.txt','x')
|  In this case,
|
|      x,x,0
|      x,x,0
|      x,0,x
|
    """
    f = open(file_name)
    lines = f.readlines()
    f.close()
    try:
        n_size = len(lines[0].split(","))
    except:
        assert False, "Influence Matrix input file error!"
    mat1 = NP.zeros(n_size * n_size, dtype='i')
    ind = 0
    for line in lines:
        line = line.replace("\n","")
        items = line.split(",")
        for s in items:
            if s == markchr:
                mat1[ind] = 1
            else:
                mat1[ind] = 0
            ind += 1
    mat2 = mat1.reshape((n_size,n_size,))
    influence_matrix = InfluenceMatrix(matrix_input = mat2)
    return influence_matrix
def construct_influence_matrix_from_list(inf_list):
    """
|  You can construct an influence matrix from a list (Python object).
|  An association should be identified by 1. Otherwise, the entry should be 0.
    """
    assert type(inf_list) == list, "Input should be a list object."
    assert len(inf_list) > 0, "List should not be empty."
    mat1 = NP.array(inf_list).astype('i')
    assert mat1.ndim == 2, "The matrix should have two dimensions."
    assert mat1.shape[0] == mat1.shape[1], "The matrix should have the same lengths."
    influence_matrix = InfluenceMatrix(matrix_input = mat1)
    return influence_matrix
def multicore_inf(influence_matrx):
    fit = FitnessContributionTable(influence_matrx)
    land = Landscape(fitness_contribution_matrix = fit)
    #land.compute_all_locations_id_cython() #Cython implementation
    land.compute_all_locations_id() #Python implementation
    return land
def develop_landsacpes_from_influence_matrix (influence_matrix,num_land,processors=0):
    '''
    Create multiple landscapes using multiprocessors
    '''
    from multiprocessing import Pool,cpu_count
    if processors == 0:
        processors = cpu_count() / 2
    print "Please wait."
    pool = Pool(processors)
    pd = []
    for _ in range(num_land):
        pd.append(influence_matrix)
    lands = pool.map(multicore_inf,pd)
    print "\nNew landscapes are ready."
    pool.terminate()
    return lands
def save_landscapes(landscapes,file_name):
    import cPickle
    f = open(file_name,'wb')
    cPickle.dump(landscapes,f)
    f.close()
def load_landscapes(file_name):
    import cPickle
    f = open(file_name)
    obj = cPickle.load(f)
    return obj
# END OF PROGRAM #