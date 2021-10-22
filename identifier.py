#여기서 의미하는 value란 getvalue()를 의미
def returnthing(value,num):
    thing=[]
    for x in range(len(value)):
        thing.append(value[x][num])
    return thing