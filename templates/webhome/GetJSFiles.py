__author__ = 'madhurima'

ptr = open("ModifiedHeader.html", 'r')
end = 0
start = 0
temp = ptr.readline()
cnt = 1
while temp:
    if temp.find("{% block") != -1:
        start = ptr.tell()
        name = temp[8:-1]
        line = ptr.readline()
        cnt += 1
        newline = "{% endblock" + name
        while line.find(newline) == -1:
            line = ptr.readline()
            cnt += 1
        end = ptr.tell()
        ptr.seek(start, 0)
        while True:
            temp = ptr.readline()
            if ptr.tell() >= end:
                break
            if temp.find("{% else") != -1:
                start2 = ptr.tell()
                while temp.find("{% endif ") == -1:
                    temp = ptr.readline()
                end2 = ptr.tell()-len(temp)
                ptr.seek(start2,0)
                print "----------------------------------"
                while ptr.tell() < end2 :
                    temp = ptr.readline()
                    # print("temp = ", temp)
                    if temp:
                        sfname = temp.find("}}") + 2
                        efname = temp.find('">')
                        fname = temp[sfname: efname]
                        if fname != '' :
                            print fname
                    else :
                        break
                # print("count = ", cnt)
                break
        ptr.seek(end,0)
    temp = ptr.readline()
    cnt += 1



