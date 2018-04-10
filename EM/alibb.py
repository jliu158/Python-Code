def HR(N):
    stu = []
    if N > 1:
        for i in range(N+1):
            for j in range(N+1):
                if [i,j]==[0,0]:
                    continue
                l_stu = len(stu)
                if l_stu==0:
                    stu.append([i,j])
                icon = 0    # icon for check
                for pre_stu in stu:
                    if check_stu([i,j],pre_stu) == 1:
                        icon = 1
                        break
                if icon == 0:
                    stu.append([i,j])
    return len(stu)



def check_stu(a, b):
    if b[0] == 0:
        if a[0] == 0:
            return 1
        else:
            return 0
    elif b[1] == 0:
        if a[1] == 0:
            return 1
        else:
            return 0
    elif a[0]/float(b[0]) == a[1]/float(b[1]):
        return 1
    else:
        return 0


print HR(6)