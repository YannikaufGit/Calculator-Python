import re

class CalculatorEngine():
    
    def __init__(self, expression, result):
        self.startpoint = expression
        self.expression = expression
        self.result= result
        self.error = False
        self.zero = "0"

    def press(self, key):
        if key == "=":
            self.tokenizer()
        elif (key == "DELETE" and len(self.expression)>0) or (key == "d" and len(self.expression)>0):
            self.expression = self.expression[:-1:]
            print(self.expression)
        elif key=="c"and len(self.expression)>0:
            self.expression = ""
            self.error = False
            print(self.expression)
        else:
            self.expression += key
            print(self.expression)
    
    def tokenizer(self):
        components = re.split(r"([-+*:/()\-\]])", self.expression)
        components = [x for x in components if x!=""] # sort out ""
        
        # First dealing with the minus components. If they are identified as a sign "-" then the two components of the list will be added to one and the list will be sliced.

        minus_count = 0
        if components[0] == "-":
            self.result = float(components[0]+components[1])
            components = [components[0]+components[1]] + components[2:] 
        elif components[0] == "(" and components[1] == "-":
            components = [components[0]]+[components[1]+components[2]] + components[3:]
        while minus_count < len(components):
            if components[minus_count] == "-" and components[minus_count-1] in {"+","-","*","/"}:
                if minus_count+2 < len(components):
                    components = components[:minus_count]+[components[minus_count]+components[minus_count+1]] + components[minus_count+2:]
                else:
                    components = components[:minus_count]+[components[minus_count]+components[minus_count+1]]
            minus_count+=1
        
        
        # Treatment of the brackets as an Last-In-First-Out principle with a stack:

        stack = []
        pairs = []
        for i, token in enumerate(components):
            if token == "(":
                stack.append(i)

            elif token == ")":
                if not stack:
                    self.error = True
                    print("Too many closing brackets! Please correct!")
                    return None
                start_index = stack.pop()
                pairs.append([start_index, i])
        if stack:
            self.error = True
            print("Too many opening brackets! Please correct!")
            return None
        
        for i in range(len(pairs)):
            res_bracket = self._evaluate(components[pairs[i][0]+1:pairs[i][1]])
            components = components[:pairs[i][0]] + res_bracket + components[pairs[i][1]+1:]
            print(components)
            for j in range(i+1,len(pairs)):
                if pairs[j][0] > pairs[i][0]:
                    pairs[j][0] -= len(components[pairs[i][0]+1:pairs[i][1]])+1
                if pairs[j][1] > pairs[i][0]:
                    pairs[j][1] -= len(components[pairs[i][0]+1:pairs[i][1]])+1

        # Deadling with possible wrong user input:

        if components[0] in {"+", "-", "/", "*"}:
            print("Error: operator at the beginning! Please correct!")
            self.error = True
            return None
        elif components[-1] in {"+", "-", "/", "*"}:
            print("Error: operator at the end! Please correct!")
            self.error = True
            return None
        error_count = 0
        while error_count < len(components):
            if components[error_count] in {"+","-","*","/"} and components[error_count+1] in {"+","-","*","/"}:
                print("Error: two operators successively! Please correct!")
                self.error = True
                return None
            error_count +=1
        
        # Depiction of the result as float or int and if needed rounded

        self.result = float(self._evaluate(components)[0])
        components_result = re.split("([.])", self._evaluate(components)[0])
        if components_result[2] == "0":
            self.result = int(self.result)    
        if len(components_result[0]) > 12:
            print("rounded!")
            self.result = round(self.result, 12)
        elif len(components_result[2]) > 12:
            print("rounded!")
            self.result = round(self.result, 12)
        self.expression = str(self.result)
        print(self.result)
        
    def _evaluate(self, components):
        
        # First multiplication and division is being dealt 

        point_counter = 0
        while point_counter < len(components):
            if components[point_counter] == "*":
                res_mul = str(float(components[point_counter-1])*float(components[point_counter+1]))
                if point_counter + 2 <= len(components):
                    components = components[:point_counter-1] + [res_mul] + components[point_counter+2:]
                else:
                    components = components[:point_counter-1] + [res_mul]
                continue
            elif components[point_counter] == "/":
                res_div = str(float(components[point_counter-1])/float(components[point_counter+1]))
                if point_counter + 2 <= len(components):
                    components = components[:point_counter-1] + [res_div] + components[point_counter+2:]
                else:
                    components = components[:point_counter-1] + [res_div]
                continue
            else:
                point_counter+=1

        # Now dealing with addition and subtraction -> return of components which is now sliced down to one element which is the result of the calculation
        
        line_counter = 0
        while line_counter < len(components):
            if components[line_counter] == "+":
                if line_counter+2 <= len(components):
                    res_add = str(float(components[line_counter-1]) + float(components[line_counter+1]))
                    components = components[:line_counter-1] + [res_add] + components[line_counter+2:]
                else:
                    components = components[:line_counter-1] + [res_add]
                continue
            elif components[line_counter] == "-":
                if line_counter+2 <= len(components):
                    res_sub = str(float(components[line_counter-1]) - float(components[line_counter+1]))
                    components = components[:line_counter-1] + [res_sub] + components[line_counter+2:]
                else:
                    components = components[:line_counter-1] + [res_sub]
                continue
            line_counter+=1
        return components