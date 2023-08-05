import os
import functions as fc
missing_operator = []
current_nb = []

cont = "1"
while(cont == "1"):
    os.system('cls')
    input_str = str(input("Enter the 4 enigma's digits : "))
    while(fc.decompose(input_str,0) == []):
        input_str = str(input("Enter the 4 enigma's digits : "))

    tmp_digits = input_str
    current_nb = fc.decompose(input_str,0)

    input_str = str(input("Enter the banned operators (Press Enter if there's none) : "))
    while(fc.decompose(input_str,1) == []):
        input_str = str(input("Enter the banned operators (Press Enter if there's none) : "))

    tmp_banop = input_str
    missing_operator = fc.decompose(input_str,1)

    operator_list = ["+","-","*","/"]

    if missing_operator != ["none"]:
        for i in missing_operator:
            operator_list.remove(i)

    for k in range(len(current_nb)):
        current_nb[k] = int(current_nb[k])
    pattern = {"par_ou1" : 0, "num1" : -1, "op1" : 0, "par_ou2" : 0, "num2" : -1, "par_fe1" : 0, "op2" : 0, "par_ou3" : 0, "num3"  : -1, "par_fe2" : 0, "op3" : 0, "num4" : -1, "par_fe3" : 0}

    solution = fc.research(pattern,current_nb,operator_list)
    os.system('cls')
    print("Digits : " + tmp_digits)
    if(missing_operator == ["none"]):
        print("Banned operators : none")
    else:
        print("Banned operators : " + tmp_banop)
    if(solution == []):
        print("No solution found. You enter wrong values or there is no solution.")
    else:
        print("We found [ " + str(len(solution)) + " ] solutions !")
        if(len(solution) == 1):
            print("Here it is :")
            print("")
            print(solution[0])
        else:
            print("Here is one : ")
            print("")
            print(solution[0])
            print("")
            print("Would you like to see all the answers ?")

            display_all = str(input("(Press Enter to skip, 0 to display all possible solutions) : "))
            while(display_all != "" and display_all != "0"):
                display_all = str(input("(Press Enter to skip, 0 to display all possible solutions) : "))

            print("")
            if(display_all == "0"):
                for k in range(len(solution)):
                    print("Solution n°"+str(k+1)+" : "+solution[k])

    print("")
    print("")
    print("")
            
    cont = str(input("Would you like to continue ? (1 for YES, 0 for NO) : "))
    while(cont not in ["1","0"]):
        print("Please enter either 0 or 1.")
        cont = str(input("Would you like to continue ? (1 for YES, 0 for NO) : "))
