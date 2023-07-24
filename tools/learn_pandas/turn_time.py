import pandas as pd

dates = ['2017-5-19', 'Jun 5,2017', '01/05/2018', '2017.07.07', '20170506']
ad = pd.to_datetime(dates)
print(ad)

dates = ['2017-5-19 2:30:00 pm ', 'Jun 5,2017 14:00:00', '01/05/2018', '2017.07.07', '20170506']
asdad = pd.to_datetime(dates)
print(asdad)

print(pd.to_datetime(['2021-9-31'], errors='coerce'))
epoch = 134321323
print(pd.to_datetime(epoch, unit='s'))
t = pd.to_datetime([epoch], unit='s')
print(t.view())
print('#' * 100)
# period
import pandas as pd

# year period
y = pd.Period('2019')
print(y)
print(y.start_time)
print(y.end_time)
print(y.is_leap_year)
# month period
m = pd.Period('2019-6', 'm')
print(m)
print(m.start_time)
print(m.end_time)
print(m + 1)
# day period
d = pd.Period('2021-7-30', 'D')
print(d)
print(d.start_time)
print(d.end_time)
print(d + 10)
# hour period
h = pd.Period('2021-7-8 23:00', 'H')
print(h)
print(h.start_time)
print(h.end_time)
print(h + 12)
# quarterly period
q1 = pd.Period('2021q1', 'q-dec')
print(q1)
print(q1.start_time)
print(q1.end_time)
m1 = q1.asfreq('M', how='start')
m3 = q1.asfreq('M', how='end')
print(m1)
print(m3)

# week period
w = pd.Period('2021-7-6', 'w')
print(w)
print(w - 1)
# period index
r = pd.period_range('2011', '2012', freq='q')
print(r)
print(r[0])
m = pd.period_range('2011','2021',freq='m')
print(m)