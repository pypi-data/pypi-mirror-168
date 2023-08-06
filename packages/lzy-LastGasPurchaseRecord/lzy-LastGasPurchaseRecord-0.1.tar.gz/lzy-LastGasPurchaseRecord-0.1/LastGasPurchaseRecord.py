import pandas as pd

def LastGasPurchaseRecord(GasPurchaseRecord_IC,GasPurchaseRecord_IOT):
    HandleAfter_IC = GasPurchaseRecord_IC.dropna(how='any') \
        .sort_values(by='recharge_time', ascending=False) \
        .drop_duplicates(subset=['account_number'])
    HandleAfter_IC.insert(loc=2, column='ICandIOT', value='0')

    HandleAfter_IOT = GasPurchaseRecord_IOT.dropna(how='any')\
    .sort_values(by='recharge_time',ascending=False)\
    .drop_duplicates(subset=['account_number'])
    HandleAfter_IOT.insert(loc=2,column='ICandIOT',value='1')

    MergeICandIOT = pd.merge(left=HandleAfter_IC, right=HandleAfter_IOT, on='account_number')
    SameBool = MergeICandIOT.recharge_time_x == MergeICandIOT.recharge_time_y
    BigBool = MergeICandIOT.recharge_time_x > MergeICandIOT.recharge_time_y
    SmallBool = MergeICandIOT.recharge_time_x < MergeICandIOT.recharge_time_y

    InICandIOT = MergeICandIOT[SameBool].rename(columns={'recharge_time_x':'recharge_time'})[['account_number','recharge_time']]
    LastInIC = MergeICandIOT[BigBool]
    LastInIOT = MergeICandIOT[SmallBool]

    InICandIOT.insert(loc=2, column='ICandIOT', value='3')
    AllLastInIC = HandleAfter_IC.set_index('account_number').drop(LastInIOT.account_number).drop(
        InICandIOT.account_number)
    AllLastInIOT = HandleAfter_IOT.set_index('account_number').drop(LastInIC.account_number).drop(
        InICandIOT.account_number)

    return  pd.concat(objs=(AllLastInIC, AllLastInIOT, InICandIOT.set_index('account_number')))
