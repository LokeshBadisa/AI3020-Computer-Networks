from utils import generatecsv
from tqdm import tqdm

#The below output is taken directly from https://www.cogentco.com/en/looking-glass which is an IPV4 Trace from London
s1 = "traceroute to google.com (172.217.169.14), 30 hops max, 60 byte packets\
   gi0-0-1-15.7.nr12.b025687-0.lon13.atlas.cogentco.com (130.117.254.57)  0.868 ms  0.903 ms\
   te0-0-1-0.agr12.lon13.atlas.cogentco.com (154.25.4.173)  0.713 ms te0-0-1-0.agr11.lon13.atlas.cogentco.com (154.25.4.169)  0.679 ms\
   te0-19-0-3.ccr42.lon13.atlas.cogentco.com (154.54.39.25)  0.902 ms te0-3-0-3.ccr42.lon13.atlas.cogentco.com (154.54.39.21)  0.914 ms\
   be2350.rcr21.b023101-0.lon13.atlas.cogentco.com (130.117.51.138)  1.102 ms be2348.rcr21.b023101-0.lon13.atlas.cogentco.com (130.117.51.74)  1.192 ms\
   ae39-xcr1.ltw.cw.net (195.2.26.25)  0.526 ms  0.494 ms\
   ae8-xcr1.lnt.cw.net (195.2.24.130)  1.342 ms  0.493 ms\
   google-gw1.lnt.cw.net (195.2.5.10)  0.636 ms  0.606 ms\
   108.170.246.161 (108.170.246.161)  8.877 ms 108.170.246.129 (108.170.246.129)  0.526 ms\
   209.85.241.95 (209.85.241.95)  7.591 ms  7.465 ms\
  lhr25s26-in-f14.1e100.net (172.217.169.14)  7.871 ms  7.868 ms"

s2 = "traceroute to ntt.com (61.113.104.9), 30 hops max, 60 byte packets\
 1  gi0-0-1-15.7.nr12.b025687-0.lon13.atlas.cogentco.com (130.117.254.57)  0.829 ms  0.853 ms\
 2  te0-0-1-0.agr11.lon13.atlas.cogentco.com (154.25.4.169)  0.895 ms  0.929 ms\
 3  te0-1-0-2.ccr41.lon13.atlas.cogentco.com (154.54.39.97)  2.250 ms te0-1-0-13.ccr41.lon13.atlas.cogentco.com (154.54.38.49)  1.141 ms\
 4  be12488.ccr42.ams03.atlas.cogentco.com (130.117.51.42)  7.766 ms be12194.ccr41.ams03.atlas.cogentco.com (154.54.56.94)  7.664 ms\
 5  be2440.agr21.ams03.atlas.cogentco.com (130.117.50.6)  8.011 ms be2434.agr21.ams03.atlas.cogentco.com (130.117.2.241)  7.657 ms\
 6  ntt.ams03.atlas.cogentco.com (130.117.15.130)  7.633 ms  7.630 ms\
 7  ae-3.r20.amstnl07.nl.bb.gin.ntt.net (129.250.7.86)  10.537 ms  9.571 ms\
 8  ae-15.r20.londen12.uk.bb.gin.ntt.net (129.250.5.1)  20.413 ms  20.313 ms\
 9  ae-7.r20.nwrknj03.us.bb.gin.ntt.net (129.250.6.147)  73.208 ms  73.096 ms\
10  ae-13.r25.asbnva02.us.bb.gin.ntt.net (129.250.2.111)  86.145 ms  86.177 ms\
11  * *\
12  ae-14.r33.tokyjp05.jp.bb.gin.ntt.net (129.250.3.192)  242.638 ms ae-1.r03.tokyjp05.jp.bb.gin.ntt.net (129.250.5.7)  236.155 ms\
13  * ae-0.ocn.tokyjp05.jp.bb.gin.ntt.net (120.88.53.18)  237.002 ms\
14  ae-1.r03.tokyjp05.jp.bb.gin.ntt.net (129.250.5.7)  245.203 ms 122.1.245.70 (122.1.245.70)  246.967 ms\
15  ae-0.ocn.tokyjp05.jp.bb.gin.ntt.net (120.88.53.18)  238.971 ms ae-1.ocn.tokyjp05.jp.bb.gin.ntt.net (120.88.53.22)  238.333 ms\
16  * 60.37.54.166 (60.37.54.166)  243.590 ms\
17  211.0.210.114 (211.0.210.114)  251.520 ms *\
18  * *\
19  * *\
20  * *\
21  * *\
22  * *\
23  * *\
24  * *\
25  * *\
26  * *\
27  * *\
28  * *\
29  * *\
30  * *"

traces=[s1,s2]
names=['google','ntt']


for count,trace in tqdm(enumerate(traces)):
    generatecsv(trace,names[count],True)