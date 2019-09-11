import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

p_2 = pd.read_json("2.json")
p_6 = pd.read_json("6.json")
p_10 = pd.read_json("10.json")
p_15 = pd.read_json("15.json")
p_30 = pd.read_json("30.json")

datasets = [p_2, p_6, p_10, p_15, p_30]
labels = ['2 Clients', '6 Clients', '10 Clients', '15 Clients', '30 Clients']
result = []
index = [2, 6, 10, 15, 30]

for i, dataset in enumerate(datasets):
    grouped = dataset.groupby('method').size()
    total = grouped[0] + grouped[1]
    peer = grouped[0]
    server = grouped[1]
    minimum = total/index[i]
    result.append([total, peer, server, minimum])
test = pd.DataFrame(result, index=index, columns=['Total', 'Peer', 'Server', 'Min #Server Requests']) 
test.plot()
plt.savefig('clients_line_chart.pdf')

for i, data in enumerate(result):
    minimal = data[-1]
    dataset = datasets[i]
    serverResponses = dataset.loc[dataset['method'] == 'serverResponse']
    mask = serverResponses['loadTime'] > 3000
    timeOuts = serverResponses[mask]['loadTime'].count()
    df = pd.DataFrame({labels[i]: [data[1], timeOuts, max(data[2]-minimal-timeOuts, 0), minimal]}, index=['Peer', 'Server Responses due to timeout', 'Server (additional)', 'Server (required)'])
    plot = df.plot.pie(y=labels[i], figsize=(5, 5), autopct='%1.0f%%', explode=[0.05, 0.05, 0.05, 0.05])
    plt.savefig('pie_'+labels[i]+'.pdf')
