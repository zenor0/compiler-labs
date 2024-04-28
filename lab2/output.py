 
# SLR分析开始
def SLR(Action, Goto, source, production_list):
    source.append([0, "$", "结束符"])
    statusstack = [0]
    sentence_stack = ["$"]
    print(source)
    while 1:
        print("*****************************************")
       
        terminal = source.pop(0)
 
        
        print("句型栈", sentence_stack)
        # 移进
        if Action[statusstack[len(statusstack) - 1]][terminal[0]].do == "S":
            print("动作： 移入操作，从缓冲区中读取",terminal[1],"元素进行移入，并根据Action压入",Action[statusstack[len(statusstack) - 1]][terminal[0]].which,"状态")
            statusstack.append(Action[statusstack[len(statusstack) - 1]][terminal[0]].which)
            sentence_stack.append(terminal[1])
        elif Action[statusstack[len(statusstack) - 1]][terminal[0]].do == "R":
            # 归约
            # 记录归约产生式
            r_production = 0
            for production in production_list:
                if production.number == Action[statusstack[len(statusstack) - 1]][terminal[0]].which:
                    r_production = production
            for i in range(len(r_production.right)):
                statusstack.pop()
                sentence_stack.pop()
            statusstack.append(Goto[statusstack[len(statusstack) - 1]][getCol(r_production.left[0])])
            print("动作： 归约操作，根据Action表利用第",r_production.number,"个产生式归约")
            sentence_stack.append(r_production.left[0])
            source.insert(0, terminal)
 
        elif Action[statusstack[len(statusstack) - 1]][terminal[0]].do == "acc":
 
            print("！！！！！！！！！！语义分析完成！！！！！！！！！！！！！！")
            break;
        else:
            print("error 462!");