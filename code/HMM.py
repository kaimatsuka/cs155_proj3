########################################
# CS/CNS/EE 155 2018
# Problem Set 6
#
# Author:       Andrew Kang
# Description:  Set 6 skeleton code
########################################

# You can use this (optional) skeleton code to complete the HMM
# implementation of set 5. Once each part is implemented, you can simply
# execute the related problem scripts (e.g. run 'python 2G.py') to quickly
# see the results from your code.
#
# Some pointers to get you started:
#
#     - Choose your notation carefully and consistently! Readable
#       notation will make all the difference in the time it takes you
#       to implement this class, as well as how difficult it is to debug.
#
#     - Read the documentation in this file! Make sure you know what
#       is expected from each function and what each variable is.
#
#     - Any reference to "the (i, j)^th" element of a matrix T means that
#       you should use T[i][j].
#
#     - Note that in our solution code, no NumPy was used. That is, there
#       are no fancy tricks here, just basic coding. If you understand HMMs
#       to a thorough extent, the rest of this implementation should come
#       naturally. However, if you'd like to use NumPy, feel free to.
#
#     - Take one step at a time! Move onto the next algorithm to implement
#       only if you're absolutely sure that all previous algorithms are
#       correct. We are providing you waypoints for this reason.
#
# To get started, just fill in code where indicated. Best of luck!

import random

class HiddenMarkovModel:
    '''
    Class implementation of Hidden Markov Models.
    '''

    def __init__(self, A, O):
        '''
        Initializes an HMM. Assumes the following:
            - States and observations are integers starting from 0. 
            - There is a start state (see notes on A_start below). There
              is no integer associated with the start state, only
              probabilities in the vector A_start.
            - There is no end state.

        Arguments:
            A:          Transition matrix with dimensions L x L.
                        The (i, j)^th element is the probability of
                        transitioning from state i to state j. Note that
                        this does not include the starting probabilities.

            O:          Observation matrix with dimensions L x D.
                        The (i, j)^th element is the probability of
                        emitting observation j given state i.

        Parameters:
            L:          Number of states.
            
            D:          Number of observations.
            
            A:          The transition matrix.
            
            O:          The observation matrix.
            
            A_start:    Starting transition probabilities. The i^th element
                        is the probability of transitioning from the start
                        state to state i. For simplicity, we assume that
                        this distribution is uniform.
        '''

        self.L = len(A)
        self.D = len(O[0])
        self.A = A
        self.O = O
        self.A_start = [1. / self.L for _ in range(self.L)]
        

    def viterbi(self, x):
        '''
        Uses the Viterbi algorithm to find the max probability state 
        sequence corresponding to a given input sequence.

        Arguments:
            x:          Input sequence in the form of a list of length M,
                        consisting of integers ranging from 0 to D - 1.

        Returns:
            max_seq:    State sequence corresponding to x with the highest
                        probability.
        '''

        M = len(x)      # Length of sequence.

        # The (i, j)^th elements of probs and seqs are the max probability
        # of the prefix of length i ending in state j and the prefix
        # that gives this probability, respectively.
        #
        # For instance, probs[1][0] is the probability of the prefix of
        # length 1 ending in state 0.
        probs = [[0. for _ in range(self.L)] for _ in range(M + 1)]
        seqs  = [['' for _ in range(self.L)] for _ in range(M + 1)]

        # for each input
        for i, xthis in enumerate(x):
            
            # special operation for the first element
            if i == 0:
                
                # for each state
                for j in range(self.L):
                    probs[i][j] = self.O[j][xthis]*self.A_start[j]
                
                continue # skip the rest for initial iteration
            
            # after the first input, for each state
            for j in range(self.L):
                
                # compute max probability
                prob_candidate = [None]*self.L
                
                for k in  range(self.L):
                    prob_candidate[k] = probs[i-1][k]*self.A[k][j]*self.O[j][xthis]
                
                # find max value and index
                probs[i][j] = max(prob_candidate)
                seqs[i][j] = prob_candidate.index(probs[i][j])

        # compute the final probability
        probMax = max(probs[M-1])
        idx = probs[M-1].index(probMax)
        
        # trace sequence backwards
        max_seq = str(idx)
        for i in range(M,0,-1):
            idx = seqs[i-1][idx]
            max_seq = str(idx)+ max_seq # append at the beginning
        
        return max_seq


    def forward(self, x, normalize=False):
        '''
        Uses the forward algorithm to calculate the alpha probability
        vectors corresponding to a given input sequence.

        Arguments:
            x:          Input sequence in the form of a list of length M,
                        consisting of integers ranging from 0 to D - 1.

            normalize:  Whether to normalize each set of alpha_j(i) vectors
                        at each i. This is useful to avoid underflow in
                        unsupervised learning.

        Returns:
            alphas:     Vector of alphas.

                        The (i, j)^th element of alphas is alpha_j(i),
                        i.e. the probability of observing prefix x^1:i
                        and state y^i = j.

                        e.g. alphas[1][0] corresponds to the probability
                        of observing x^1:1, i.e. the first observation,
                        given that y^1 = 0, i.e. the first state is 0.
        '''

        M = len(x)      # Length of sequence.
        alphas = [[0. for _ in range(self.L)] for _ in range(M + 1)]

        ###
        ###
        ### 
        ### TODO: Insert Your Code Here (2Bi)
        ###
        ###
        ###
                
        # for each input
        for i in range(M):
            
            xthis = self.observations.index(x[i])
            
            if i == 0:
                
                # for each state
                for j in range(self.L):
                    alphas[1][j] = self.O[j][xthis]*self.A_start[j]
            else:
                
                # after the first input, for each state
                for j in range(self.L):
                    
                    # compute max probability
                    temp = 0
                    for k in  range(self.L):
                        temp += alphas[i][k]*self.A[k][j]
                        
                    
                    alphas[i+1][j] = self.O[j][xthis]*temp
                    
            if normalize == True:
                self.__rescale(alphas[i+1])
                
        # compute the final probability
        return alphas

    def __rescale(self, prob):

        scale = sum(prob)
        for i in range(len(prob)):
            prob[i] /= scale
                        
    def backward(self, x, normalize=False):
        '''
        Uses the backward algorithm to calculate the beta probability
        vectors corresponding to a given input sequence.

        Arguments:
            x:          Input sequence in the form of a list of length M,
                        consisting of integers ranging from 0 to D - 1.

            normalize:  Whether to normalize each set of alpha_j(i) vectors
                        at each i. This is useful to avoid underflow in
                        unsupervised learning.

        Returns:
            betas:      Vector of betas.

                        The (i, j)^th element of betas is beta_j(i), i.e.
                        the probability of observing prefix x^(i+1):M and
                        state y^i = j.

                        e.g. betas[M][0] corresponds to the probability
                        of observing x^M+1:M, i.e. no observations,
                        given that y^M = 0, i.e. the last state is 0.
        '''

        M = len(x)      # Length of sequence.
        betas = [[0. for _ in range(self.L)] for _ in range(M + 1)]

        ###
        ###
        ### 
        ### TODO: Insert Your Code Here (2Bii)
        ###
        ###
        ###

        # for each state
        for j in range(self.L):
            betas[M][j] = 1
            
        if normalize == True:
            self.__rescale(betas[M])
        
        # for each input
        for i in range(M-1,0,-1):
            
            xthis = self.observations.index(x[i])
            
            # after the first input, for each state
            for z in range(self.L):
                
                # compute max probability
                temp = 0
                for j in  range(self.L):
                    temp += betas[i+1][j]*self.A[z][j]*self.O[j][xthis]
                    
                betas[i][z] = temp
            self.__rescale(betas[i])

        return betas

    def supervised_learning(self, X, Y):
        '''
        Trains the HMM using the Maximum Likelihood closed form solutions
        for the transition and observation matrices on a labeled
        datset (X, Y). Note that this method does not return anything, but
        instead updates the attributes of the HMM object.

        Arguments:
            X:          A dataset consisting of input sequences in the form
                        of lists of variable length, consisting of integers 
                        ranging from 0 to D - 1. In other words, a list of
                        lists.

            Y:          A dataset consisting of state sequences in the form
                        of lists of variable length, consisting of integers 
                        ranging from 0 to L - 1. In other words, a list of
                        lists.

                        Note that the elements in X line up with those in Y.
        '''

        # Calculate each element of A using the M-step formulas.

        ###
        ###
        ### 
        ### TODO: Insert Your Code Here (2C)
        ###
        ###
        ###
        
        N = len(X) # number of sentences
        A_num = []
        for i in range(self.L):
           A_num.append([0.]*self.L) 
           
        A_den = [0.]*self.L
        
        for j in range(N):
            
            Mj = len(X[j])
            
            for i in range(Mj-1):
                a = Y[j][i]
                b = Y[j][i+1]
                A_num[a][b] += 1
                A_den[a] += 1
        
        for a in range(self.L):
            for b in range(self.L):
                self.A[a][b] = A_num[a][b]/A_den[a]
                
        # Calculate each element of O using the M-step formulas.
        O_num = []
        for i in range(self.L):
            O_num.append([0.]*self.D)
            
        O_den = [0.]*self.L
        
        for j in range(N):
            Mj = len(X[j])
            for i in range(Mj):
                w = X[j][i]
                z = Y[j][i]
                O_num[z][w] += 1
                O_den[z] += 1
                
        for z in range(self.L):
            for w in range(self.D):
                self.O[z][w] = O_num[z][w]/O_den[z]

        pass


    def unsupervised_learning(self, X, N_iters):
        '''
        Trains the HMM using the Baum-Welch algorithm on an unlabeled
        datset X. Note that this method does not return anything, but
        instead updates the attributes of the HMM object.

        Arguments:
            X:          A dataset consisting of input sequences in the form
                        of lists of length M, consisting of integers ranging
                        from 0 to D - 1. In other words, a list of lists.

            N_iters:    The number of iterations to train on.
        '''

        
        # make observation list
        observations = set()
        for x in X:
            observations |= set(x)
      
        # make an ordered list
        self.observations = list(observations)
        
        # N_iters = 1
        for i in range(N_iters):
            
            # this helper function implements the A, O update
            self.__usl_updateAO(X)
        
        pass


    def __usl_updateAO(self,X):
        '''
        A custom helper function that Kai created to simplify the code.
        This implements a single iteration of the unsupervised learning (usl)
        '''        
        
        # pre-allocate space for new A and O
        A_num = []
        O_num = []
        for i in range(self.L):
            A_num.append([0.]*self.L)
            O_num.append([0.]*self.D)
                    
        A_den = [0.]*self.L
        O_den = [0.]*self.L
        
        N = len(X)
        for j in range(N):
            
            # for each line of input, create marginals
            Mj = len(X[j])
            
            # for each line of input, create marginals
            alphas = self.forward(X[j],  normalize=True)
            betas  = self.backward(X[j], normalize=True)
        
            # given single line of data, compute its marginal 
            # probabilities as a list of list with size Mj x L
            marginal = self.__compute_marginal(Mj,alphas,betas)
                
           
            # for each observation 
            for i in range(Mj-1):
                xnext = self.observations.index(X[j][i+1])
                
                # prepare product of marginal
                prob_num = []
                for a in range(self.L):
                    prob_num.append([0.]*self.L)
                    
                for a in range(self.L):
                    for b in range(self.L):
                        prob_num[a][b] = alphas[i+1][a]*self.A[a][b]*self.O[b][xnext]*betas[i+2][b]
                        
                scalar = 0
                for a in range(self.L):
                    scalar += sum(prob_num[a])
                
                        
                # for each pair of transition
                for a in range(self.L):
                    A_den[a] += marginal[i][a]
                    for b in range(self.L):
                        A_num[a][b] += prob_num[a][b]/scalar
                        
            # incremenet O
                 
            # for each observation 
            for i in range(Mj):
                
                w = self.observations.index(X[j][i])
                
                # for each pair of transition
                for z in range(self.L):
                    O_num[z][w] += marginal[i][z]
                    O_den[z] += marginal[i][z]
            
        # after all N data, update A and O
        for a in range(self.L):
            for b in range(self.L):
                self.A[a][b] = A_num[a][b]/A_den[a]
                
        for z in range(self.L):
            for w in range(self.D):                
                self.O[z][w] = O_num[z][w]/O_den[z]
                
        pass # this function does not return anything
    
    def __compute_marginal(self,Mj, alphas, betas):
        ''' 
        This function computes the marginal 
        Returns:
            marginal matrix of Mj x L 
        '''
        
        # marginal is a list of list with size Mj x L
        marginal = []
        for i in range(Mj):
            
            prod = []
            for j in range(self.L):
                 prod.append(alphas[i+1][j]*betas[i+1][j])
            denom = sum(prod)
            
            # normalize for marginal
            for j in range(self.L):
                prod[j] /= denom
            
            # prod is a list of length L
            marginal.append(prod)
        
            
        return marginal

                
    def generate_emission(self, M):
        '''
        Generates an emission of length M, assuming that the starting state
        is chosen uniformly at random. 

        Arguments:
            M:          Length of the emission to generate.

        Returns:
            emission:   The randomly generated emission as a list.

            states:     The randomly generated states as a list.
        '''

        emission = []
        states = []

        ###
        ###
        ### 
        ### TODO: Insert Your Code Here (2F)
        ###
        ###
        ###
        
        # sample input
        y = self.__sample_prob(self.A_start)
        x = self.__sample_prob(self.O[y])
        
        emission.append(self.observations[x])
        states.append(y)
        
        for i in range(M-1):
            y = self.__sample_prob(self.A[y])            
            x = self.__sample_prob(self.O[y])
            
            emission.append(self.observations[x])
            states.append(y)
            
        return emission, states

    def generate_emission_with_seed(self, M, seed):
        '''
        Generates an emission of length M, with a specified see emission

        Arguments:
            M:          Length of the emission to generate.
            seed:       Integer representation of the seed observation

        Returns:
            emission:   The randomly generated emission as a list.

            states:     The randomly generated states as a list.
        '''

        # compute probability of y_i given seeds
        prob_y_given_seed = []
        for state in range(self.L):
            prob_y_given_seed.append(self.O[state][seed]*self.A_start[state])
        den = sum(prob_y_given_seed)
        for i in range(len(prob_y_given_seed)):
            prob_y_given_seed[i] /= den
        
        # Sample next state.
        state = self.__sample_prob(prob_y_given_seed)
        
        # add first word, and first state
        emission = [seed]
        states   = [state]
        
        
        for t in range(M-1):
            
            # Sample next state.
            next_state = self.__sample_prob(self.A[state])
            state = next_state
            
            # Sample next observation.
            next_obs = self.__sample_prob(self.O[state])
            
            # Append 
            states.append(state)
            emission.append(next_obs)

        return emission, states


    def __sample_prob(self, dist):
        '''
        Input: 
            dist  discrete distribution of size S such that sum is 1
        '''
        
        S = len(dist)
        
        # sample initial state
        r = random.random()
        cum_prob = 0
        for i in range(S):
            cum_prob += dist[i]
            if cum_prob > r:
                return i
            
        
    def probability_alphas(self, x):
        '''
        Finds the maximum probability of a given input sequence using
        the forward algorithm.

        Arguments:
            x:          Input sequence in the form of a list of length M,
                        consisting of integers ranging from 0 to D - 1.

        Returns:
            prob:       Total probability that x can occur.
        '''

        # Calculate alpha vectors.
        alphas = self.forward(x)

        # alpha_j(M) gives the probability that the state sequence ends
        # in j. Summing this value over all possible states j gives the
        # total probability of x paired with any state sequence, i.e.
        # the probability of x.
        prob = sum(alphas[-1])
        return prob


    def probability_betas(self, x):
        '''
        Finds the maximum probability of a given input sequence using
        the backward algorithm.

        Arguments:
            x:          Input sequence in the form of a list of length M,
                        consisting of integers ranging from 0 to D - 1.

        Returns:
            prob:       Total probability that x can occur.
        '''

        betas = self.backward(x)
        
        # beta_j(1) gives the probability that the state sequence starts
        # with j. Summing this, multiplied by the starting transition
        # probability and the observation probability, over all states
        # gives the total probability of x paired with any state
        # sequence, i.e. the probability of x.
        prob = sum([betas[1][j] * self.A_start[j] * self.O[j][x[0]] \
                    for j in range(self.L)])

        return prob


def supervised_HMM(X, Y):
    '''
    Helper function to train a supervised HMM. The function determines the
    number of unique states and observations in the given data, initializes
    the transition and observation matrices, creates the HMM, and then runs
    the training function for supervised learning.

    Arguments:
        X:          A dataset consisting of input sequences in the form
                    of lists of variable length, consisting of integers 
                    ranging from 0 to D - 1. In other words, a list of lists.

        Y:          A dataset consisting of state sequences in the form
                    of lists of variable length, consisting of integers 
                    ranging from 0 to L - 1. In other words, a list of lists.
                    Note that the elements in X line up with those in Y.
    '''
    # Make a set of observations.
    observations = set()
    for x in X:
        observations |= set(x)

    # Make a set of states.
    states = set()
    for y in Y:
        states |= set(y)
    
    # Compute L and D.
    L = len(states)
    D = len(observations)

    # Randomly initialize and normalize matrix A.
    A = [[random.random() for i in range(L)] for j in range(L)]

    for i in range(len(A)):
        norm = sum(A[i])
        for j in range(len(A[i])):
            A[i][j] /= norm
    
    # Randomly initialize and normalize matrix O.
    O = [[random.random() for i in range(D)] for j in range(L)]

    for i in range(len(O)):
        norm = sum(O[i])
        for j in range(len(O[i])):
            O[i][j] /= norm

    # Train an HMM with labeled data.
    HMM = HiddenMarkovModel(A, O)
    HMM.supervised_learning(X, Y)

    return HMM

def unsupervised_HMM(X, n_states, N_iters,observations=[]):
    '''
    Helper function to train an unsupervised HMM. The function determines the
    number of unique observations in the given data, initializes
    the transition and observation matrices, creates the HMM, and then runs
    the training function for unsupervised learing.

    Arguments:
        X:          A dataset consisting of input sequences in the form
                    of lists of variable length, consisting of integers 
                    ranging from 0 to D - 1. In other words, a list of lists.

        n_states:   Number of hidden states to use in training.
        
        N_iters:    The number of iterations to train on.
    '''

    if len(observations) == 0:
            
        # Make a set of observations.
        observations = set()
        for x in X:
            observations |= set(x)
    
    # Compute L and D.
    L = n_states
    D = len(observations)
    
    # random.seed(2020)
    # Randomly initialize and normalize matrix A.
    A = [[random.random() for i in range(L)] for j in range(L)]

    for i in range(len(A)):
        norm = sum(A[i])
        for j in range(len(A[i])):
            A[i][j] /= norm
    
    # random.seed(155)
    # Randomly initialize and normalize matrix O.
    O = [[random.random() for i in range(D)] for j in range(L)]

    for i in range(len(O)):
        norm = sum(O[i])
        for j in range(len(O[i])):
            O[i][j] /= norm

    # Train an HMM with unlabeled data.
    HMM = HiddenMarkovModel(A, O)
    HMM.unsupervised_learning(X, N_iters)

    return HMM
