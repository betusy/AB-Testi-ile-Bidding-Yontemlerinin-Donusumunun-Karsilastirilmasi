## AB Testi ile Bidding Yontemlerinin Donusumunun Karsilastirilmasi

# Is Problemi

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi ve averagebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor. Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.


# Veri Seti

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleri ab_testing.xlsx excel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel('/Users/betulyilmaz/Documents/Miuul/Measurement Problems/Case Study 1-AB Testi ile Bidding Yontemlerinin Donusumunun Karsilastirilmasi/ab_testing.xlsx', sheet_name='Control Group')
dataframe_test = pd.read_excel('/Users/betulyilmaz/Documents/Miuul/Measurement Problems/Case Study 1-AB Testi ile Bidding Yontemlerinin Donusumunun Karsilastirilmasi/ab_testing.xlsx', sheet_name='Test Group')

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

def check_df(dataframe):
    print('------------- head -------------')
    print(dataframe.head())
    print('------------- shape -------------')
    print(dataframe.shape)
    print('------------- describe -------------')
    print(dataframe.describe().T)
    print('------------- type -------------')
    print(dataframe.dtypes)
    print('------------- NA -------------')
    print(dataframe.isnull().sum())

check_df(df_control)
check_df(df_test)

# Test ve Control grubunu birlestiriyoruz.
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control, df_test], axis=0, ignore_index=False)
df.head()
df.tail()

# Hipotez

# H0 : M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.)
# H1 : M1!= M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark vardır.)

# Gruplara gore purchase ortalamasi

df.groupby('group').agg({'Purchase': 'mean'})

# Normallik Varsayimi

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.

# p < 0.05 H0 red
# p > 0.05 H0 reddedilemez

test_stat, pvalue = shapiro(df.loc[df['group'] == 'control', 'Purchase'])
print('Test Stat: %.4f, p-value: %.4f' % (test_stat, pvalue)) # p=0.5891 Ho reddedilemez

test_stat, pvalue = shapiro(df.loc[df['group'] == 'test', 'Purchase'])
print('Test Stat: %.4f, p-value: %.4f' % (test_stat, pvalue)) # p=0.1541 Ho reddedilemez

# Varyans Homojenligi

# H0: Varyanslar homojendir.
# H1: Varyanslar homojen değildir.

# p < 0.05 H0 red
# p > 0.05 H0 reddedilemez

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p=0.1083 Ho reddedilemez. Varyanslar homojendir.

# Varsayimlar saglandigi icin parametrik yani bagimsiz iki orneklem t testi

# H0: M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark yoktur.)
# H1: M1 != M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark vardır)
# p<0.05 HO res , p>0.05 HO reddedilemez


test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p=0.3493 Ho reddedilemez.
# Kontrol ve test grubu satin alma ortalamalari arasinda isatistiksel olarak anlamli farklilik yoktur.











