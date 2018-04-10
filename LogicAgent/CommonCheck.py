


# add all parameters from KB and alpha into symbols list
def TT_Entail(KB, alpha):
    # KB:   the knowledge base
    # alpha:  the query
    global symbols
    return(TT_Check_All(KB, alpha, symbols, {}))




#   TT check for PROBLEM 2
def TT_Check_All(KB, alpha, symbols, model):
    if Empty(symbols):
        if PL_True_P2(KB, model):
            return PL_True_P2(alpha, model)
        else:
            # when KB is false, always return true
            return True
    else:
        P = symbols[0]
        rest = symbols[1:]
        model_f = model
        model[P] = True
        result_t = TT_Check_All(KB, alpha, rest, model)
        model[P] = False
        result_f = TT_Check_All(KB, alpha, rest, model)
        return(result_t & result_f)

# TT check for PROBLEM 1
def TT_Check_P1(KB, alpha, symbols, model):
    if Empty(symbols):
        if PL_True_P1(KB, model):
            return PL_True_P1(alpha, model)
        else:
            # when KB is false, always return true
            return True
    else:
        P = symbols[0]
        rest = symbols[1:]
        model[P] = True
        result_t = TT_Check_P1(KB, alpha, rest, model)
        model[P] = False
        result_f = TT_Check_P1(KB, alpha, rest, model)
        return(result_t & result_f)


# TT check for PROBLEM 3
def TT_Check_P3(KB, alpha, symbols, model):
    if Empty(symbols):
        if PL_True_P3(KB, model, alpha):
            return PL_True_P3(alpha, model, alpha)
        else:
            # when KB is false, always return true
            return True
    else:
        P = symbols[0]
        rest = symbols[1:]
        model[P] = True
        result_t = TT_Check_P3(KB, alpha, rest, model)
        model[P] = False
        result_f = TT_Check_P3(KB, alpha, rest, model)
        return(result_t & result_f)

# TT check for PROBLEM 4 82-12
def TT_Check_P4_1(KB, alpha, symbols, model):
    if Empty(symbols):
        if PL_True_P4_1(KB, model, alpha):
            return PL_True_P4_1(alpha, model, alpha)
        else:
            # when KB is false, always return true
            return True
    else:
        P = symbols[0]
        rest = symbols[1:]
        model[P] = True
        result_t = TT_Check_P4_1(KB, alpha, rest, model)
        model[P] = False
        result_f = TT_Check_P4_1(KB, alpha, rest, model)
        return(result_t & result_f)


# TT check for PROBLEM 4 83-11
def TT_Check_P4_2(KB, alpha, symbols, model):
    if Empty(symbols):
        if PL_True_P4_2(KB, model, alpha):
            return PL_True_P4_2(alpha, model, alpha)
        else:
            # when KB is false, always return true
            return True
    else:
        P = symbols[0]
        rest = symbols[1:]
        model[P] = True
        result_t = TT_Check_P4_2(KB, alpha, rest, model)
        model[P] = False
        result_f = TT_Check_P4_2(KB, alpha, rest, model)
        return (result_t & result_f)


# check if the sumbols list is empty
def Empty(symbols):
    # check if the symbols is empty
    if len(symbols) == 0:
        return True
    else:
        return False

# check if p1 implied p2
def Implied(P1, P2):
    if (P1, P2) == (True, False):
        return False
    else:
        return True





# check if sentence is true by model for PROBLEM 1
def PL_True_P1(sentence, model):
    # set a initial result of True
    PL_check = True
    for Ri in sentence:
        if Ri == 'Q':
            return model[Ri]
        elif Ri == 'R1':
            # P
            PL_check = PL_check & (model['P'])
        elif Ri == 'R2':
            # P => Q

            if (model['P'],model['Q']) == (True, False):
                result = False
            else:
                result = True
            PL_check = PL_check & result
    return PL_check



# check if sentence is true by model for PROBLEM 2
def PL_True_P2(sentence, model):
    # set a initial result of True
    PL_check = True
    for Ri in sentence:
        if Ri == 'P1_2':
            return model[Ri]
        elif Ri == 'R1':
            # not P1_1
            PL_check = PL_check & (not model['P1_1'])
        elif Ri == 'R2':
            # B1_1 <=> (P1_2 or P2_1)
            if model['B1_1'] == (model['P1_2'] | model['P2_1']):
                PL_check = PL_check & True
            else:
                return False
        elif Ri == 'R3':
            # B2_1 <=> (P1_1 or P2_2 or P3_1)
            if model['B2_1'] == (model['P1_1'] | model['P2_2'] | model['P3_1']):
                PL_check = PL_check & True
            else:
                return False
        elif Ri == 'R4':
            #
            PL_check = PL_check & (not model['B1_1'])
        elif Ri == 'R5':
            PL_check = PL_check & model['B2_1']
    return PL_check

# check if sentence is true by model for PROBLEM 3
def PL_True_P3(sentence, model, alpha):
    PL_check = True
    for Ri in sentence:
        if Ri == alpha[0]:
            return model[Ri]
        elif Ri == 'R1':
            PL_check = PL_check & Implied(model['P1'], model['P2'])
        elif Ri == 'R2':
            P1 = not model['P1']
            P2 = not model['P2']
            P3 = model['P3']
            P2 = P2 & P3
            PL_check = PL_check & Implied(P1, P2)
        elif Ri == 'R3':
            PL_check = PL_check & Implied((model['P2'] | model['P3']), model['P4'])
        elif Ri == 'R4':
            PL_check = PL_check & Implied(model['P4'], model['P5'])
    return PL_check


# check if sentence is true by model for PROBLEM 4 (a)
def PL_True_P4_1(sentence, model, alpha):
    PL_check = True
    A = model['A']
    B = model['B']
    C = model['C']
    for Ri in sentence:
        if Ri == alpha[0]:
            return model[Ri]
        elif Ri == 'R1':
            PL_check = PL_check & Implied(A, C & A)
        elif Ri == 'R2':
            PL_check = PL_check & Implied(B, not C)
        elif Ri == 'R3':
            PL_check = PL_check & Implied(C, B or not A)
        elif Ri == 'R4':
            P = not (C & A)
            PL_check = PL_check & Implied(not A, P)
        elif Ri == 'R5':
            PL_check = PL_check & Implied(not B, C)
        elif Ri == 'R6':
            P = (not B) & A
            PL_check = PL_check & Implied(not C, P)
    return PL_check


# check if sentence is true by model for PROBLEM 4 (b)
def PL_True_P4_2(sentence, model, alpha):
    PL_check = True
    A = model['A']
    B = model['B']
    C = model['C']
    for Ri in sentence:
        if Ri == alpha[0]:
            return model[Ri]
        elif Ri == 'R1':
            PL_check = PL_check & Implied(A, not C)
        elif Ri == 'R2':
            PL_check = PL_check & Implied(B, A & C)
        elif Ri == 'R3':
            PL_check = PL_check & Implied(C, B)
        elif Ri == 'R4':
            PL_check = PL_check & Implied(not A, C)
        elif Ri == 'R5':
            P = not (A & C)
            PL_check = PL_check & Implied(not B, P)
        elif Ri == 'R6':
            PL_check = PL_check & Implied(not C, not B)
    return PL_check


''' Problem 1. Modus Ponens '''
def ModusPonens_Test():
    symbols = ['P', 'Q']
    alpha = ['Q']
    KB = ['R1', 'R2']
    print(TT_Check_P1(KB, alpha, symbols, {}))


# ModusPonens_Test()

''' Problem 2. Wumpus World (Simple) '''
def WumpusWorld_Test():
    symbols = ['P1_1', 'P1_2', 'P3_1', 'P2_1', 'B1_1', 'B2_1', 'P2_2']
    alpha = ['P1_2']
    KB = ['R1', 'R2', 'R3', 'R4', 'R5']
    print(TT_Check_All(KB, alpha, symbols, {}))


# WumpusWorld_Test()


''' Problem 3. Horn Clauses '''
def HornClauses_Test(alpha):
    '''
    mythical: P1
    immortal: P2
    mammal:   P3
    horned:   P4
    magical:  P5
    '''
    symbols = ['P1', 'P2', 'P3', 'P4', 'P5']
    # a) P1; b) P5; c) P4;
    alpha
    KB = ['R1', 'R2', 'R3', 'R4']
    print(TT_Check_P3(KB, alpha, symbols, {}))

# HornClauses_Test('P1')  # is mythical?
# HornClauses_Test('P5')  # is magical?
# HornClauses_Test(['P4'])    # is horned?



''' Problem 4. Liar and Truth-tellers OSSMB 82-12'''
def LiarTruthTeller_8212_Test(person):
    '''
    Amy:    A
    Bob:    B
    Cal:    C
    '''
    symbols = ['A', 'B', 'C']
    person
    KB = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
    print(TT_Check_P4_1(KB, person, symbols, {}))
# LiarTruthTeller_8212_Test(['C'])

''' Problem 4. OSSMB 83-11'''
def LiarTruthTeller_8311_Test(person):
    '''
    Amy:    A
    Bob:    B
    Cal:    C
    '''
    symbols = ['A', 'B', 'C']
    person
    KB = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
    print(TT_Check_P4_2(KB, person, symbols, {}))
# LiarTruthTeller_8311_Test(['A'])

while True:
    question = int(input('Please enter the number of question you want to check(1,2,3,4 | 0 for quit):'))
    if question==1:
        ModusPonens_Test()
    elif question==2:
        WumpusWorld_Test()
    elif question==3:
        index = int(input('Please enter the index for clause(0 for Mythical; 1 for Magical; 2 for Horned): '))
        clause = ['P1', 'P5', 'P4']
        HornClauses_Test(clause[index])
    elif question==4:
        index = input('Please enter the index for sub question(a or b)')
        person = ['A', 'B', 'C']
        person_ind = int(input('Please enter the short name of person(0 for Amy, 1 for Bob, 2 for Cal): '))
        if index=='a':
            LiarTruthTeller_8212_Test(person[person_ind])
        elif index=='b':
            LiarTruthTeller_8311_Test(person[person_ind])
    elif question==0:
        break





