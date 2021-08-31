# coding: utf-8
"""
基于聚宽数据的实时日线因子监控
"""

# 首次使用需要设置聚宽账户
# from czsc.data.jq import set_token
# set_token("phone number", 'password') # 第一个参数是JQData的手机号，第二个参数是登录密码
from czsc.data.jq import set_token
from czsc.data.jq import get_query_count
import traceback
import time
import shutil
import os
from datetime import datetime
from czsc.data.jq import JqCzscTrader as CzscTrader
from czsc.objects import Signal, Factor, Event, Operate
from czsc.utils.qywx import push_text, push_file
from czsc.utils.io import read_pkl, save_pkl
import traceback
import time
import pymysql
import random
from czsc.data.jq import get_kline, get_index_stocks

# =======================================================================================================
# 基础参数配置
ct_path = os.path.join(".", "czsc_traders_11")
os.makedirs(ct_path, exist_ok=True)

# 关于企业微信群聊机器人的使用文档，参考：https://work.weixin.qq.com/api/doc/90000/90136/91770
# 企业微信群聊机器人的key

qywx_key_073="*********"

qywx_key_073_buy="********"
# 定义需要监控的股票列表
# =======================================================================================================

tokens = ['1392*****853',"177*****619","150****614","159****724"]
symbols=[]
    #配置数据库连接信息
connect_obj = pymysql.connect(
        host='localhost', user='root', password='123456', database='ipay', port=3306)

#产生一个游标,可以获取数据库的操作权限
cursor1 = connect_obj.cursor()
sqlselect1 = "select tag_num from tag_inc where tag_name='cszc_result' limit 1"
cursor1.execute(sqlselect1)
data = cursor1.fetchone()
print(data[0])


cursor = connect_obj.cursor()
if data[0] == 1:
    sqlselect = "select id,code,name,status,status,price,huanshoulv,shiyinglv,liuzhi,zongshizhi,shijinglv from myself_choose "
else:
    sqlselect = "select id,code,name,status,status,price,huanshoulv,shiyinglv,liuzhi,zongshizhi,shijinglv from myself_choose where id>"+str(data[0])
cursor.execute(sqlselect)
    #获取结果
res = cursor.fetchall()


#symbols: List = get_index_stocks("000016.XSHG")
var = "0"
status = "1"
for everyOne in res:
    symbols.append(everyOne[1]+'.XSHE')


def monitor(use_cache=True):
    push_text("自选股CZSC笔因子监控启动 @ {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")), qywx_key_073)
    push_text("自选股CZSC笔因子监控启动 @ {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")), qywx_key_073_buy)
    moni_path = os.path.join(ct_path, "monitor")
    # 首先清空历史快照
    if os.path.exists(moni_path):
        shutil.rmtree(moni_path)
    os.makedirs(moni_path, exist_ok=True)

    events_monitor_buy = [
        # 开多
        Event(name="一买", operate=Operate.LO, factors=[

            Factor(name="60分钟类一买", signals_all=[Signal("60分钟_倒1笔_类买卖点_类一买_任意_任意_0")]),
            Factor(name="60分钟形一买", signals_all=[Signal("60分钟_倒1笔_基础形态_类一买_任意_任意_0")]),

            Factor(name="日线类一买", signals_all=[Signal("日线_倒1笔_类买卖点_类一买_任意_任意_0")]),
            Factor(name="日线形一买", signals_all=[Signal("日线_倒1笔_基础形态_类一买_任意_任意_0")]),
        ]), Event(name="二买", operate=Operate.LO, factors=[


            Factor(name="60分钟类二买", signals_all=[Signal("60分钟_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="60分钟形二买", signals_all=[Signal("60分钟_倒1笔_基础形态_类二买_任意_任意_0")]),

            Factor(name="日线类二买", signals_all=[Signal("日线_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="日线形二买", signals_all=[Signal("日线_倒1笔_基础形态_类二买_任意_任意_0")]),
            Factor(name="周线类二买", signals_all=[Signal("周线_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="周线形二买", signals_all=[Signal("周线_倒1笔_基础形态_类二买_任意_任意_0")]),
        ]),Event(name="三买", operate=Operate.LO, factors=[

            Factor(name="30分钟类三买", signals_all=[Signal("30分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="30分钟形三买", signals_all=[Signal("30分钟_倒1笔_基础形态_类三买_任意_任意_0")]),
            Factor(name="60分钟类三买", signals_all=[Signal("60分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="60分钟形三买", signals_all=[Signal("60分钟_倒1笔_基础形态_类三买_任意_任意_0")]),

            Factor(name="日线类三买", signals_all=[Signal("日线_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="日线形三买", signals_all=[Signal("日线_倒1笔_基础形态_类三买_任意_任意_0")]),
            Factor(name="周线类三买", signals_all=[Signal("周线_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="周线形三买", signals_all=[Signal("周线_倒1笔_基础形态_类三买_任意_任意_0")]),
        ])
    ]





    events_monitor = [
        # 开多
        Event(name="一买", operate=Operate.LO, factors=[
            
            Factor(name="60分钟类一买", signals_all=[Signal("60分钟_倒1笔_类买卖点_类一买_任意_任意_0")]),
            Factor(name="60分钟形一买", signals_all=[Signal("60分钟_倒1笔_基础形态_类一买_任意_任意_0")]),
            
            Factor(name="日线类一买", signals_all=[Signal("日线_倒1笔_类买卖点_类一买_任意_任意_0")]),
            Factor(name="日线形一买", signals_all=[Signal("日线_倒1笔_基础形态_类一买_任意_任意_0")]),
        ]),

        Event(name="二买", operate=Operate.LO, factors=[

            Factor(name="30分钟类二买", signals_all=[Signal("30分钟_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="30分钟形二买", signals_all=[Signal("30分钟_倒1笔_基础形态_类二买_任意_任意_0")]),
            Factor(name="60分钟类二买", signals_all=[Signal("60分钟_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="60分钟形二买", signals_all=[Signal("60分钟_倒1笔_基础形态_类二买_任意_任意_0")]),
            
            Factor(name="日线类二买", signals_all=[Signal("日线_倒1笔_类买卖点_类二买_任意_任意_0")]),
            Factor(name="日线形二买", signals_all=[Signal("日线_倒1笔_基础形态_类二买_任意_任意_0")]),
        ]),
        Event(name="三买", operate=Operate.LO, factors=[

            Factor(name="15分钟类三买", signals_all=[Signal("15分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="15分钟形三买", signals_all=[Signal("15分钟_倒1笔_基础形态_类三买_任意_任意_0")]),

            Factor(name="30分钟类三买", signals_all=[Signal("30分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="30分钟形三买", signals_all=[Signal("30分钟_倒1笔_基础形态_类三买_任意_任意_0")]),
            Factor(name="60分钟类三买", signals_all=[Signal("60分钟_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="60分钟形三买", signals_all=[Signal("60分钟_倒1笔_基础形态_类三买_任意_任意_0")]),
            
            Factor(name="日线类三买", signals_all=[Signal("日线_倒1笔_类买卖点_类三买_任意_任意_0")]),
            Factor(name="日线形三买", signals_all=[Signal("日线_倒1笔_基础形态_类三买_任意_任意_0")]),
        ]),

        # 平多
        Event(name="一卖", operate=Operate.LE, factors=[

            Factor(name="30分钟类一卖", signals_all=[Signal("30分钟_倒1笔_类买卖点_类一卖_任意_任意_0")]),
            Factor(name="30分钟形一卖", signals_all=[Signal("30分钟_倒1笔_基础形态_类一卖_任意_任意_0")]),
            Factor(name="60分钟类一卖", signals_all=[Signal("60分钟_倒1笔_类买卖点_类一卖_任意_任意_0")]),
            Factor(name="60分钟形一卖", signals_all=[Signal("60分钟_倒1笔_基础形态_类一卖_任意_任意_0")]),
            Factor(name="日线类一卖", signals_all=[Signal("日线_倒1笔_类买卖点_类一卖_任意_任意_0")]),
            Factor(name="日线形一卖", signals_all=[Signal("日线_倒1笔_基础形态_类一卖_任意_任意_0")]),
        ]),
        Event(name="二卖", operate=Operate.LE, factors=[


            Factor(name="30分钟类二卖", signals_all=[Signal("30分钟_倒1笔_类买卖点_类二卖_任意_任意_0")]),
            Factor(name="30分钟形二卖", signals_all=[Signal("30分钟_倒1笔_基础形态_类二卖_任意_任意_0")]),
            Factor(name="60分钟类二卖", signals_all=[Signal("60分钟_倒1笔_类买卖点_类二卖_任意_任意_0")]),
            Factor(name="60分钟形二卖", signals_all=[Signal("60分钟_倒1笔_基础形态_类二卖_任意_任意_0")]),
            Factor(name="日线类二卖", signals_all=[Signal("日线_倒1笔_类买卖点_类二卖_任意_任意_0")]),
            Factor(name="日线形二卖", signals_all=[Signal("日线_倒1笔_基础形态_类二卖_任意_任意_0")]),
        ]),
        Event(name="三卖", operate=Operate.LE, factors=[
            Factor(name="5分钟类三卖", signals_all=[Signal("5分钟_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="5分钟形三卖", signals_all=[Signal("5分钟_倒1笔_基础形态_类三卖_任意_任意_0")]),

            Factor(name="15分钟类三卖", signals_all=[Signal("15分钟_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="15分钟形三卖", signals_all=[Signal("15分钟_倒1笔_基础形态_类三卖_任意_任意_0")]),

            Factor(name="30分钟类三卖", signals_all=[Signal("30分钟_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="30分钟形三卖", signals_all=[Signal("30分钟_倒1笔_基础形态_类三卖_任意_任意_0")]),
            Factor(name="60分钟类三卖", signals_all=[Signal("60分钟_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="60分钟形三卖", signals_all=[Signal("60分钟_倒1笔_基础形态_类三卖_任意_任意_0")]),
            Factor(name="日线类三卖", signals_all=[Signal("日线_倒1笔_类买卖点_类三卖_任意_任意_0")]),
            Factor(name="日线形三卖", signals_all=[Signal("日线_倒1笔_基础形态_类三卖_任意_任意_0")]),
        ]),
    ]
    for s in symbols:
        print(s)
        a=0
        m=0
        while(a<1):
         try:
          vvv =random.randint(0,len(tokens)-1)
          m=m+1;
          if(m>8):
            break
          print(tokens[vvv])
          set_token(tokens[vvv], '*************')
          
          count = get_query_count()
          print(tokens[vvv] + " 数量：" + str(count))
          a=1
        
         except Exception as e:
          #traceback.print_exc()
          print("{} 执行失败 - {}")
          tokens.remove(tokens[vvv])
        
        print(s)
        connect_obj1 = pymysql.connect(
             host='***', user='***', password='***', database='****', port=3306)
        
          
        
             #产生一个游标,可以获取数据库的操作权限
        cursor1 = connect_obj1.cursor()
        print(format(datetime.now().strftime("%Y-%m-%d %H:%M"))+" CODE："+format(s[:6]))
        try:
            file_ct = os.path.join(ct_path, "{}.ct".format(s))
            if os.path.exists(file_ct) and use_cache:
                ct: CzscTrader = read_pkl(file_ct)
                ct.update_factors()
            else:
                ct = CzscTrader(s, max_count=1000)
            save_pkl(ct, file_ct)

            # 每次执行，会在moni_path下面保存一份快照
            file_html = os.path.join(moni_path, f"{ct.symbol}_{ct.end_dt.strftime('%Y%m%d%H%M')}.html")
            ct.take_snapshot(file_html, width="1400px", height="580px")

            msg = format(datetime.now().strftime("%Y-%m-%d %H:%M")) + f"标的代码：{s}\n同花顺F10：http://basic.10jqka.com.cn/{s.split('.')[0]}\n"
            msgBuy = format(datetime.now().strftime(
                "%Y-%m-%d %H:%M")) + f"标的代码：{s}\n同花顺F10：http://basic.10jqka.com.cn/{s.split('.')[0]}\n"
            nnam = ''
            ff = ''
            nnamBuy = ''
            ffBuy = ''
            for event in events_monitor_buy:
                m, f = event.is_match(ct.s)
                if m:
                    msgBuy += "Buy监控提醒：{}@{}\n".format(event.name, f)
                    nnamBuy = event.name
                    ffBuy = f
            for event in events_monitor:
                m, f = event.is_match(ct.s)
                if m:
                    msg += "监控提醒：{}@{}\n".format(event.name, f)
                    nnam = event.name
                    ff = f


            var = ''
            for everyOne in res:
             if everyOne[1] == s[:6]:
                 var = everyOne[2]
                 status = everyOne[3]
                 price = everyOne[5]
                 huanshoulv = everyOne[6]
                 shiyinglv = everyOne[7]
                 liuzhi = everyOne[8]
                 zongshizhi = everyOne[9]
                 shijinglv = everyOne[10]
                 sqlupdate = "update tag_inc set tag_num = "+str(everyOne[0])+" where tag_name='cszc_result'"
                 cursor1.execute(sqlupdate)
                 connect_obj1.commit()
            if "监控提醒" in msg:
                msg += var+"  行情：";
                msg += " http://stockpage.10jqka.com.cn/{}/#hqzs".format(s[:6]) +" 市盈: "+ str(shiyinglv) + " 总市值:"+str(zongshizhi) + " 市净："+str(shijinglv);
                push_text(msg.strip("\n"), key=qywx_key_073)
                print(msg)
                sqlinsert = "insert into `czsc_result` (code,name,result,level) values ('"+s[:6]+"','"+var+"','"+nnam+"','"+ff+"')"
                print(sqlinsert)
                cursor1.execute(sqlinsert)
                connect_obj1.commit()
            if "Buy监控提醒" in msgBuy:
                msgBuy += var +"  行情：";
                msgBuy += " http://stockpage.10jqka.com.cn/{}/#hqzs".format(s[:6]) +" 市盈: "+ str(shiyinglv) + " 流值:"+str(liuzhi) + " 市净："+str(shijinglv);
                push_text(msgBuy.strip("\n"), key=qywx_key_073_buy)
                print(msgBuy)
                sqlinsert = "insert into `czsc_result_buy` (code,name,result,level) values ('" + s[
                                                                                                 :6] + "','" + var + "','" + nnamBuy + "','" + ffBuy + "')"
                print(sqlinsert)
                cursor1.execute(sqlinsert)
                connect_obj1.commit()

        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(s, e))
       


    push_text("自选股CZSC笔因子监控结束 @ {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")), qywx_key_073)
    push_text("自选股CZSC笔因子监控结束 @ {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")), qywx_key_073_buy)
    connect_obj3 = pymysql.connect(
        host='localhost', user='root', password='123456', database='ipay', port=3306)

    # 产生一个游标,可以获取数据库的操作权限
    cursor3 = connect_obj3.cursor()
    sqlupdate = "update tag_inc set tag_num = 1 where tag_name='cszc_result'"
    cursor3.execute(sqlupdate)
    connect_obj3.commit()

def run_monitor():
    mdt = ["14:50"]
    monitor()
    while 1:
        print(datetime.now().strftime("%H:%M"))
        if datetime.now().strftime("%H:%M") in mdt:
            monitor()
        time.sleep(3)


if __name__ == '__main__':
    run_monitor()

