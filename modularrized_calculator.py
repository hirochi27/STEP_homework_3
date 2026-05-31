#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_aster(line, index):
    token = {'type': 'ASTER'}
    return token, index + 1


def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1


def read_left_paren(line, index):
    token = {"type": "LEFT_PAREN"}
    return token, index + 1


def read_right_paren(line, index):
    token = {"type": "RIGHT_PAREN"}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_aster(line, index)
        elif line[index] == "/":
            (token, index) = read_division(line, index)
        elif line[index] == "(":
            (token, index) = read_left_paren(line, index)
        elif line[index] == ")":
            (token, index) = read_right_paren(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    #print(tokens)
    return tokens


# def evaluate_paren(tokens):
#     index = 1

#     while index < len(tokens):
#         if tokens[index]["type"] == "LEFT_PAREN":
#             stack = []
#             stack.append(index)
#             index += 1
#         elif tokens[index]["type"] == "left_PAREN":
#             left_paren = stack.pop()
#             ebvaluate_paren = tokens[left_paren : index]
#             paren_answer = 
#             tokens.insert(left_paren, )
#             tokens.pop(left_paren+1 : index + 1)
#             index += 1

            # left_paren_index = index
            # stack = []
            # while tokens[index]["type"] == "RIGHT_PAREN":
            #     stack.append(tokens[index])
            #     index += 1
            # right_paren_index = index
            # stack.appned(tokens[index])#一番内側の右括弧を入れる


def evaluate_aster_division(tokens):
    index = 1   

    while index < len(tokens):
        if tokens[index]["type"] == "ASTER":
            tokens[index -1] = str(tokens[index - 1]["number"] * tokens[index + 1]["number"])
            tokens[index - 1] = tokenize(tokens[index-1])[0]
            tokens.pop(index)
            tokens.pop(index)
        elif tokens[index]["type"] == "DIVISION":
            tokens[index -1] = str(tokens[index - 1]["number"] / tokens[index + 1]["number"])
            tokens[index - 1] = tokenize(tokens[index-1])[0]
            tokens.pop(index)
            tokens.pop(index)
        else:
            index += 1
    return tokens


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1

    while index < len(tokens):

        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            # elif tokens[index - 1]['type'] == 'ASTER':
            #     answer *= tokens[index]['number']
            # elif tokens[index -1]['type'] == 'DIVISION':
            #     answer /= tokens[index]['number']
            # elif tokens[index -1]["type"] == "LRFT_PAREN":
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    # paren_answer = evaluate_paren(tokens) #括弧内を計算
    aster_division_anser = evaluate_aster_division(tokens) #掛け算割り算を計算
    actual_answer = evaluate(aster_division_anser)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1+3*2+4")
    test("1+3/2+4")
    test("0.4+1.2-12.0")
    test("1+3*1.5+4")
    test("1+3/1.5+4")
    test("1+3*2-4/2")
    test("1+2*3/2-1") #掛け算割り算の連続
    test("1/3*4*2/10/100")
    test("0.5*0.1/0.3")

    test("1000000000+10000000000")
    test("1000000000/10000000000*100000000000")
    
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)


#line = input
