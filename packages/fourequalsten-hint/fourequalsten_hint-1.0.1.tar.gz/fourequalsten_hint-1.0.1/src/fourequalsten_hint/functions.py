def decompose(input,x):
    number_list = ["0","1","2","3","4","5","6","7","8","9"]
    operator_list = ["+","-","*","/"]
    allowed_char = number_list + operator_list
    res = []

    if(type(input) != str):
        print("ERROR : Wrong type ! You need to enter a string.")
    else:
        if(x == 0):
            if(len(input) != 4):
                print("ERROR : You need to enter 4 numbers.")
            else:
                inc = 1
                valid = 1
                for i in input:
                    if(i not in number_list):
                        valid = 0
                        print("ERROR : The character n°"+str(inc)+" is invalid.")
                    inc += 1
                if(valid == 1):
                    res = [input[0],input[1],input[2],input[3]]
        elif(x == 1):
            if(len(input)>len(operator_list)-1):
                print("ERROR : You banned too many operators !")
            else:
                inc = 1
                valid = 1
                for i in input:
                    if(i not in operator_list):
                        valid = 0
                        print("ERROR : The character n°"+str(inc)+" is invalid.")
                    inc += 1
                if(valid == 1):
                    if(len(input) == 0):
                        res = ["none"]
                    else:
                        for i in input:
                            res.append(i)
        else:
            print("ERROR : The input is neither 4 numbers or the list of banned operators.")
    
    return res

def research(pattern,current_nb,operator_list):
    nb_chiffre = {}

    for i in current_nb:
        nb_chiffre[i] = current_nb.count(i)

    if(len(nb_chiffre) == 4):
        nb_db = 24
    elif(len(nb_chiffre) == 3):
        nb_db = [3,1,0,0]
    elif(len(nb_chiffre) == 2):
        if(nb_chiffre[current_nb[0]] == 2):
            nb_db = [0,2,0,0]
        else:
            nb_db = [1,0,1,0]
    elif(len(nb_chiffre) == 1):
        nb_db = [0,0,0,1]

    nb_par = 0
    nb_signe = 0
    nb_chiffre = 0
    no_swap = 0
    solution = []

    operator_equ = {}

    for k in range(len(operator_list)):
        operator_equ[k] = operator_list[k]

    while(nb_par <= 5):
        nb_chiffre = 0
        while(nb_chiffre < 24):
            no_swap = 0
            nb_signe = 0
            if(nb_par == 0 and nb_signe == 0 and nb_chiffre == 0):
                pattern["num1"] = current_nb[0]
                pattern["num2"] = current_nb[1]
                pattern["num3"] = current_nb[2]
                pattern["num4"] = current_nb[3]
            else:
                if(nb_chiffre%6 == 0):
                    if(pattern["num1"] != pattern["num" + str((nb_chiffre//6)+1)] or nb_chiffre == 0):
                        pattern["num1"], pattern["num" + str((nb_chiffre//6)+1)] = pattern["num" + str((nb_chiffre//6)+1)], pattern["num1"]
                    else:
                        no_swap = 1
                else:
                    if(nb_chiffre%2 == 1):
                        if(pattern["num3"] != pattern["num4"]):
                            pattern["num3"], pattern["num4"] = pattern["num4"], pattern["num3"]
                        else:
                            no_swap = 1
                    else:
                        if(pattern["num2"] != pattern["num4"]):
                            pattern["num2"], pattern["num4"] = pattern["num4"], pattern["num2"]
                        else:
                            no_swap = 1

            while(nb_signe < len(operator_list)**3):
                pattern["op1"] = operator_equ[nb_signe//len(operator_list)**2]
                pattern["op2"] = operator_equ[(nb_signe//len(operator_list))%len(operator_list)]
                pattern["op3"] = operator_equ[nb_signe%len(operator_list)]
                if(no_swap == 0):
                    res = calcul(pattern)
                    if(res != "unsolved" and res != "invalid"):
                        solution.append(res)
                nb_signe += 1
            nb_chiffre += 1
        nb_par += 1
        pattern = par_pattern(nb_par,pattern)

    return solution

def valid_pattern(pattern):
    if(pattern["op1"] == 0 or pattern["op2"] == 0 or pattern["op3"] == 0):
        res = False
    else:
        res = True

    return res

def add_par(x,y,pattern):
    if(x in [0,1,2,3]):
        if(x == 1):
            pattern["par_ou1"] = 1
            pattern["par_ou2"] = 0
            pattern["par_ou3"] = 0

            if(y == 1):
                pattern["par_fe1"] = 1
                pattern["par_fe2"] = 0
                pattern["par_fe3"] = 0
            elif(y == 2):
                pattern["par_fe1"] = 0
                pattern["par_fe2"] = 1
                pattern["par_fe3"] = 0
        elif(x == 2):
            pattern["par_ou1"] = 0
            pattern["par_ou2"] = 1
            pattern["par_ou3"] = 0

            if(y == 1):
                pattern["par_fe1"] = 0
                pattern["par_fe2"] = 1
                pattern["par_fe3"] = 0
            elif(y == 2):
                pattern["par_fe1"] = 0
                pattern["par_fe2"] = 0
                pattern["par_fe3"] = 1
        elif(x == 3):
            pattern["par_ou1"] = 0
            pattern["par_ou2"] = 0
            pattern["par_ou3"] = 1

            pattern["par_fe1"] = 0
            pattern["par_fe2"] = 0
            pattern["par_fe3"] = 1
        else:
            pattern["par_ou1"] = 0
            pattern["par_ou2"] = 0
            pattern["par_ou3"] = 0

            pattern["par_fe1"] = 0
            pattern["par_fe2"] = 0
            pattern["par_fe3"] = 0

    return pattern

def str_calcul(pattern):
    str_calcul = str(pattern["num1"]) + str(pattern["op1"]) + str(pattern["num2"]) + str(pattern["op2"]) + str(pattern["num3"]) + str(pattern["op3"]) + str(pattern["num4"])
    if(pattern["par_ou1"] == 1):
        str_calcul = "(" + str_calcul
        if(pattern["par_fe1"] == 1):
            str_calcul = str_calcul[:4] + ")" + str_calcul[4:]
        else:
            str_calcul = str_calcul[:6] + ")" + str_calcul[6:]
    elif(pattern["par_ou2"] == 1):
        str_calcul = str_calcul[:2] + "(" + str_calcul[2:]
        if(pattern["par_fe2"] == 1):
            str_calcul = str_calcul[:6] + ")" + str_calcul[6:]
        else:
            str_calcul = str_calcul + ")"
    elif(pattern["par_ou3"] == 1):
        str_calcul = str_calcul[:4] + "(" + str_calcul[4:] + ")"
    
    return str_calcul

def calcul(pattern):
    if(valid_pattern):
        calcul_res = 0
        tmp = 0

        if(pattern["par_ou1"] == 1):
            if(pattern["par_fe1"] == 1):
                calcul_res = calcul_op(pattern["num1"],pattern["num2"],pattern["op1"])
                if(prior_op(pattern["op2"],pattern["op3"]) == 1):
                    calcul_res = calcul_op(calcul_res,pattern["num3"],pattern["op2"])
                    calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                else:
                    tmp = calcul_op(pattern["num3"],pattern["num4"],pattern["op3"])
                    calcul_res = calcul_op(calcul_res,tmp,pattern["op2"])
            else:
                if(prior_op(pattern["op1"],pattern["op2"]) == 1):
                    calcul_res = calcul_op(pattern["num1"],pattern["num2"],pattern["op1"])
                    calcul_res = calcul_op(calcul_res,pattern["num3"],pattern["op2"])
                    calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                else:
                    calcul_res = calcul_op(pattern["num2"],pattern["num3"],pattern["op2"])
                    calcul_res = calcul_op(calcul_res,pattern["num1"],pattern["op1"])
                    calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
        elif(pattern["par_ou2"] == 1):
            if(pattern["par_fe2"] == 1):
                calcul_res = calcul_op(pattern["num2"],pattern["num3"],pattern["op2"])
                if(prior_op(pattern["op1"],pattern["op3"]) == 1):
                    calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])
                    calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                else:
                    calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                    calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])
            else:
                if(prior_op(pattern["op2"],pattern["op3"]) == 1):
                    calcul_res = calcul_op(pattern["num2"],pattern["num3"],pattern["op2"])
                    calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                    calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])
                else:
                    calcul_res = calcul_op(pattern["num3"],pattern["num4"],pattern["op3"])
                    calcul_res = calcul_op(pattern["num2"],calcul_res,pattern["op2"])
                    calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])
                
        elif(pattern["par_ou3"] == 1):
            calcul_res = calcul_op(pattern["num3"],pattern["num4"],pattern["op3"])
            if(prior_op(pattern["op1"],pattern["op2"]) == 1):
                tmp = calcul_op(pattern["num1"],pattern["num2"],pattern["op1"])
                calcul_res = calcul_op(tmp,calcul_res,pattern["op2"])
            else:
                calcul_res = calcul_op(pattern["num2"],calcul_res,pattern["op2"])
                calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])
        else:
            if(prior_op(pattern["op1"],pattern["op2"]) == 1):
                if(prior_op(pattern["op1"],pattern["op3"]) == 1):
                    calcul_res = calcul_op(pattern["num1"],pattern["num2"],pattern["op1"])
                    if(prior_op(pattern["op2"],pattern["op3"]) == 1):
                        calcul_res = calcul_op(calcul_res,pattern["num3"],pattern["op2"])
                        calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                    else:
                        tmp = calcul_op(pattern["num3"],pattern["num4"],pattern["op3"])
                        calcul_res = calcul_op(calcul_res,tmp,pattern["op2"])
            elif(prior_op(pattern["op2"],pattern["op1"]) == 1):
                if(prior_op(pattern["op2"],pattern["op3"]) == 1):
                    calcul_res = calcul_op(pattern["num2"],pattern["num3"],pattern["op2"])
                    if(prior_op(pattern["op1"],pattern["op3"]) == 1):
                        calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])
                        calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                    else:
                        calcul_res = calcul_op(calcul_res,pattern["num4"],pattern["op3"])
                        calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])
            else:
                if(prior_op(pattern["op1"],pattern["op2"]) == 1):
                    tmp = calcul_op(pattern["num1"],pattern["num2"],pattern["op1"])
                    calcul_res = calcul_op(tmp,calcul_res,pattern["op2"])
                else:
                    calcul_res = calcul_op(pattern["num2"],calcul_res,pattern["op2"])
                    calcul_res = calcul_op(pattern["num1"],calcul_res,pattern["op1"])

        if(calcul_res == 10):
            res = str_calcul(pattern)
        else:
            res = "unsolved"

    else:
        res = "invalid"

    return res

def calcul_op(x,y,op):
    if(op == "+"):
        return x+y
    elif(op == "-"):
        return x-y
    elif(op == "*"):
        return x*y
    elif(op == "/"):
        if(y != 0):
            return x/y
        else:
            return 9999
    else:
        print("ERROR : Invalid operator !")
        return False

def prior_op(op1,op2):
    def_prior = ["*","/","-","+"]
    if(op1 in def_prior and op2 in def_prior):
        id_op1 = def_prior.index(op1)
        id_op2 = def_prior.index(op2)

        if(id_op1 <= id_op2):
            return 1
        else:
            return 2
    else:
        print("ERROR : One of the two operators given are invalid !")
        return False

def par_pattern(x,pattern):
    if(x == 1):
        pattern = add_par(1,1,pattern)   
    elif(x == 2):
        pattern = add_par(1,2,pattern)
    elif(x == 3):
        pattern = add_par(2,1,pattern) 
    elif(x == 4):
        pattern = add_par(2,2,pattern) 
    elif(x == 5):
        pattern = add_par(3,1,pattern) 

    return pattern
