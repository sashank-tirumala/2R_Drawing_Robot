import pandas as pd
import networkx as nx
name = 'square'
df = pd.read_csv('used_by_program/'+name+'.csv')
# print(df)
node_dic={}
i=0
node1=[]
node2=[]
weight=[]
for index, rows in df.iterrows():
    tup1 = (rows['x1'],rows['y1'])
    tup2 =(rows['x2'],rows['y2'])
    # print(tup1)
    weight.append(round(rows['weight'],3))
    if tup1 in node_dic:
        # print("is present")
        node1.append(node_dic[tup1])
    else:
        # print("created node: ",i)
        node_dic[tup1]=i
        node1.append(node_dic[tup1])
        i=i+1
    if tup2 in node_dic:
        # print("is present")
        node2.append(node_dic[tup2])

    else:
        # print("created node: ",i)
        node_dic[tup2]=i
        node2.append(node_dic[tup2])
        i=i+1



current_df = pd.DataFrame({'node1':node1,'node2':node2,'weight':weight})
current_df.to_csv(sep=",",index=False, path_or_buf='ans2.csv')
G = nx.Graph()
print("creating graph")
for index, rows in current_df.iterrows():
    G.add_node(rows['node1'])
    G.add_node(rows['node2'])
    G.add_edge(rows['node1'],rows['node2'],weight=rows['weight'])
inv_node_dic = {v: k for k, v in node_dic.items()}
print("completed inverting the node, starting to write string")
u = 0
adj_str = ""
req_str = ""
# while(u<len(node_dic)):
#     adj_str = adj_str + ','
#     req_str = req_str + ','
#     adj_str = adj_str+str(u)
#     req_str =req_str+ "1"
#     u = u+1
# adj_str = adj_str +"\n"
# req_str =req_str+ "\n"
u=0
while(u<len(node_dic)):
    v=0
    # adj_str = adj_str+str(u)
    # req_str=req_str+"1"
    while(v<len(node_dic)):
        if(v == 0):
            nothing =1
        else:
            adj_str = adj_str + ','
            req_str = req_str + ','
        x1 = inv_node_dic[u][0]
        x2 = inv_node_dic[v][0]
        y1 = inv_node_dic[u][1]
        y2 = inv_node_dic[v][1]
        if(u == v):
            dist = -1
        else:
            dist =int(((x2-x1)**2 +(y2-y1)**2)**0.5)
        adj_str = adj_str + str(dist)
        if((u,v) in G.edges):
            req_str = req_str+"1"
        else:
            req_str = req_str+"0"
        v=v+1
    adj_str=adj_str+"\n"
    req_str=req_str+"\n"
    u=u+1

final_adj  = open('used_by_program/'+name+'_mc'+'.csv','w')
final_req  = open('used_by_program/'+name+'_mc_required'+'.csv','w')
final_adj.write(adj_str)
final_req.write(req_str)
