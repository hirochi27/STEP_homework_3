#! /usr/bin/python3

#################トークン化######################

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

#和算
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

#減算
def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

#乗算
def read_aster(line, index):
    token = {'type': 'ASTER'}
    return token, index + 1

#除算
def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1

#括弧：左
def read_left_paren(line, index):
    token = {"type": "LEFT_PAREN"}
    return token, index + 1

#括弧：右
def read_right_paren(line, index):
    token = {"type": "RIGHT_PAREN"}
    return token, index + 1

#abs
def read_abs(line, index):
    token = {"type": "ABS"}
    return token, index + 3


#入力された文字列をトークン化
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
        elif line[index] == "a":
            (token, index) = read_abs(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    #print(tokens)
    return tokens


#####################括弧の処理#######################

#括弧内を切り出す
def paren(tokens, index):
    stack = []
    while index < len(tokens):

        #左の括弧を見つけたらスタックに入れる
        if tokens[index]["type"] == "LEFT_PAREN":
            stack.append(index)
            index += 1  

        #閉じ括弧を見つけたら一番新しい左括弧を取り出し、かっこ内を抜き出す
        elif tokens[index]["type"] == "RIGHT_PAREN":
            left_paren = stack.pop()
            inner_tokens = {
                "type": "PAREN",
                "left_index": left_paren, 
                "right_index": index, 
                "inner_tokens": tokens[left_paren + 1 : index]
                }  
            index += 1
            return inner_tokens
        else:
            index += 1
    return None

#括弧内を計算した値と入れ替え
def evaluate_paren(tokens, inner_tokens):

    #括弧内を計算
    inner_answer_tokens = manegement_aster_division(inner_tokens["inner_tokens"])
    inner_answer = evaluate(inner_answer_tokens)

    left_index = inner_tokens["left_index"]
    right_index = inner_tokens["right_index"]
    
    #括弧内の結果をトークン化
    tokens[left_index : right_index + 1] = [{'type': 'NUMBER', 'number': inner_answer}]
    #print(tokens)
    return tokens


#abs絶対値の計算
def evaluate_abs(tokens, inner_tokens):
    #括弧内を計算
    inner_answer_tokens = manegement_aster_division(inner_tokens["inner_tokens"])
    inner_answer = evaluate(inner_answer_tokens)

    #括弧内の結果が負の数の場合、正の数に変換
    if inner_answer < 0:
        inner_answer = (-1) * inner_answer

    left_index = inner_tokens["left_index"]
    right_index = inner_tokens["right_index"]
    
    #結果をトークン化
    tokens[left_index - 1 : right_index + 1] = [{'type': 'NUMBER', 'number': inner_answer}]
    return tokens


#括弧の管理
def manegement_paren(tokens):
    index = 0
    while index < len(tokens):
        #print(f"indexの中身{tokens[index]}")
        #左括弧を見つけたら、この処理を始める
        if tokens[index]["type"] == "LEFT_PAREN":
            inner_tokens = paren(tokens, index)

            #括弧の種類ごとに処理
            if tokens[inner_tokens["left_index"] - 1]["type"] == "ABS":
                tokens = evaluate_abs(tokens, inner_tokens)
            elif inner_tokens["type"] == "PAREN":
                tokens = evaluate_paren(tokens, inner_tokens)            
            else:
                index += 1
        else:
            index += 1
    return tokens 


#####################乗算除算#######################
#乗算
def evaluate_aster(tokens, index):
    tokens[index -1] = str(tokens[index - 1]["number"] * tokens[index + 1]["number"])
    tokens[index - 1] = tokenize(tokens[index-1])[0]
    tokens.pop(index)
    tokens.pop(index)
    return tokens 


#除算
def evaluate_division(tokens, index):
    #print(tokens)
    #print(index)
    tokens[index -1] = str(tokens[index - 1]["number"] / tokens[index + 1]["number"])
    tokens[index - 1] = tokenize(tokens[index-1])[0]
    tokens.pop(index)
    tokens.pop(index)
    return tokens

   
#乗算除算の管理
def manegement_aster_division(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "ASTER":
            tokens = evaluate_aster(tokens, index)
        elif tokens[index]["type"] == "DIVISION":
            tokens = evaluate_division(tokens, index)
        else:
            index += 1
    return tokens



###################和算減算########################

#普通の足し算引き算
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
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer



#テスト
def test(line):
    tokens = tokenize(line)
    print("tokenize OK")
    tokens = manegement_paren(tokens)
    print("paren OK")
    tokens = manegement_aster_division(tokens)
    print(tokens)   
    actual_answer = evaluate(tokens)
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

    # test("1000000000+10000000000")
    # test("1000000000/10000000000*100000000000")

    test("(1+2)")
    test("1+(1+2)")
    test("(1+2)+3")
    test("1*(3+2)")
    test("1+(2*3)")
    test("1+2*3/4*(5+6/7)")
    test("2+3*1/(8*(2+9/2))")
    test("5+(1+2)-(4-1)")
    test("((1+2)+(3+4))")
    test("((1*2)/(3+4))")
    test("(2+6)*0.5+1-(5*3-1/(7-0.8))")
    #負の数は考えない？　test("1+(2+6)*5-(5*3-1/(7-8))")
    #マイナス×マイナスの計算ができない
  
    test("abs(1-3)")


    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)


#line = input
