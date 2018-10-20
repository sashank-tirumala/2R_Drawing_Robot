txt_file = open('sol.txt','r')
parse = txt_file.read()
parse = parse.split(' -> ')
parse_int=[]
for x in parse:
    parse_int.append(int(x))

i=0
parse_int.append(-1)
parsed = []
for x in parse_int:
    if(i+1<len(parse_int)-1):
        tup1 = (x,parse_int[i+1])
        parsed.append(tup1)
        i = i+1
str1=""
for x in parsed:
    str1 = str1+str(x[0])+","+str(x[1])+"\n"

txt_file = open('parsed_sol.txt','w')
txt_file.write(str1)
