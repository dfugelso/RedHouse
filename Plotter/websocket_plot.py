'''
Plot data from websocket throughput test.
'''
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

d = dict()

d[12] = [1577, 1317, 1602, 1010, 1006, 1061, 1547, 1006 ,1008,]
d[17] = [1066, 1062, 1011, 1066, 1042	, 1070	, 1022	, 1080	, 1281	, ]
d[27] = [1010, 1007, 1269, 1046	, 1039	, 1062	, 1108	, 1052	, 1009	, ]
d[47] = [2032, 2302, 1009, 1136	, 1619	, 1011	, 1008	, 1301	, ]
d[87] = [1200, 1006, 1010, 1008	, 1037	, 1010	, 1180	, 1202	, 1036	, ]
d[167] = [976, 1381, 1013, 1048	, 1208	, 1282	, 1017	, 1015	, 1016	, ]	
d[327] = [1087, 1135, 1056, 1436	, 1296	, 1026	, 1020	, 1050	, 19298	, ]
d[647] = [1040, 1149, 1065, 1591	, 1439	, 1471	, 1117	, 1064	, 1058	, ]
d[1287] = [1051, 1271, 1420, 1287	, 1226	, 1076	, 1283	, 1405	, 2628	, ]
d[2567] = [1649, 1139, 1121, 1117	, 1102	, 1233	, 1116	, 1104	, 1104	, ]
d[5127] = [1765, 1214, 1236, 1211	, 1223	, 1216	, 1615	, 1181	, 1217	, ]
d[10247] = [1499, 1394, 1448, 1578	, 1461	, 1409	, 1422	, 1441	, 1408	, ]
d[20487] = [1818, 1843, 1987, 1831	, 1966	, 1800	, 1835	, 3310	, 2926	, ]
d[40967] = [2652, 2707, 8958, 9099	, 7186	, 4356	, 5134	, 4305	, 4926	, ]	
d[81927] = [4620, 34747, 13913, 8315	, 8662	, 9268	, 8886	, 9196	, 9387	, ]
d[163847] = [78739, 17632, 18003, 17504, 18289, 18121, 17625, 18780, 18388, ]

payloads = d.keys()
payloads.sort()
print payloads
for a in payloads:
    d[a] = np.array(d[a])
	



matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

x = np.array(payloads)
s = np.array([np.std(d[payload])/1000. for payload in payloads] )
y = np.array([np.mean(d[payload])/1000. for payload in payloads] )
mn = np.array([np.min(d[payload])/1000. for payload in payloads] )
mx = np.array([np.max(d[payload])/1000. for payload in payloads] )
mn = mn
mx = mx
cv = s/y

# example error bar values that vary with x-position
error = mn
# error bar values w/ different -/+ errors
lower_error = y - mn
upper_error = mx - y
asymmetric_error = [lower_error, upper_error]
#asymmetric_error = zip(mn, mx)

# fig, ax0 = plt.subplots(nrows=1, sharex=True)
# ax0.errorbar(x, y, yerr=asymmetric_error, fmt='o')
# ax0.set_title('Websocket Transmission Times by Payload Size')
# ax0.set_xscale('log')
# ax0.set_yscale('log')
# ax0.set_ylim([0,100])
# ax0.set_xlabel('Payload Size (Bytes)')
# ax0.set_ylabel('Time Between Send/Receive (Seconds)')

# font = {'family' : 'serif',
        # 'color'  : 'darkred',
        # 'weight' : 'normal',
        # 'size'   : 16,
        # }
# y = cv
# fig, ax0 = plt.subplots(nrows=1, sharex=True)  
# plt.plot(x, y, 'k')
# plt.title('Websocket Transmission Coefficent of Variation', fontdict=font)

# plt.xlabel('Payload Size (Bytes)', fontdict=font)
# plt.ylabel('Coefficient of Variation', fontdict=font)

# ax0.set_xscale('log')
# ax0.set_yscale('log')
# ax0.set_ylim([0,100])

import matplotlib.cbook as cbook

plt.show()
print y
print mn
print mx

wsdata = np.array([17092, 17915, 16401, 16791, 22304, 19873, 20014, 15936, 23901, 9414, 8981, 8905, 8620, 11096, 8685, 9026, 9116, 9136, 9133, 8828, 9224, 9197, 9308, 9073, 8999, 8870, 9281, ])
sdata = np.array([12, 12, 11, 22, 9, 15, 66, 46, 11, 6, 10, 4, 13, 59, 10, 52, 11, 58, 40, 54, 10, 10, 92, 29, 10, 8, 102, 14, 13, 14, 14, 12, 14, 12, 12, 30, 11, 10, 10, 26, 9, 13, 17, 10,])
gdata = np.array([1349, 2945, 3480, 4783, 1601, 3500, 1662, 4384, 1367, 1269, 1309, 1286, 1283, 1266, 1270, 1817, 1520, 1306, 1283, 1247, 1265, 1270, 1262, 1262, 1256, 1262, 1251, ])

wsdata = wsdata/1000.
sdata = sdata/1000.
gdata = gdata/1000.

fs = 10 # fontsize
x = np.array([wsdata, sdata, gdata,])
labels = ['Websocket', 'TCP/IP Socket', "HTTP 'Get'",]
stats = cbook.boxplot_stats(x, labels=labels, bootstrap=10000)


fig, ax0 = plt.subplots(nrows=1, ncols=2, sharex=True)  

ax0[0].bxp(stats, showmeans=True)
ax0[0].set_title('Localhost Comparision', fontsize=fs)

ax0[1].set_yscale('log')
ax0[1].bxp(stats, showmeans=True)
ax0[1].set_title('Localhost Comparision (Log Scale)', fontsize=fs)
ax0[1].set_ylim([0,25])
plt.show()