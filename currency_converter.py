import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

# 設置環境變數來避免警告訊息
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
os.environ['QT_SCALE_FACTOR'] = '1'
#顯示中文標籤
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  

API_KEY = '2d35408bf4be897551ea1c7b'

# 定義幣值的中文名稱
currency_names = {
    "AED": "阿聯酋迪拉姆",
    "AFN": "阿富汗尼",
    "ALL": "阿爾巴尼亞列克",
    "AMD": "亞美尼亞德拉姆",
    "ANG": "荷屬安地列斯盾",
    "AOA": "安哥拉寬扎",
    "ARS": "阿根廷比索",
    "AUD": "澳大利亞元",
    "AWG": "阿魯巴弗羅林",
    "AZN": "亞塞拜然馬納特",
    "BAM": "波士尼亞馬克",
    "BBD": "巴貝多元",
    "BDT": "孟加拉塔卡",
    "BGN": "保加利亞列弗",
    "BHD": "巴林第納爾",
    "BIF": "蒲隆地法郎",
    "BMD": "百慕達元",
    "BND": "汶萊元",
    "BOB": "玻利維亞諾",
    "BRL": "巴西里亞伊",
    "BSD": "巴哈馬元",
    "BTN": "不丹努扎姆",
    "BWP": "波札那普拉",
    "BYN": "白俄羅斯盧布",
    "BZD": "貝里斯元",
    "CAD": "加拿大元",
    "CDF": "剛果法郎",
    "CHF": "瑞士法郎",
    "CLP": "智利比索",
    "CNY": "中國人民幣",
    "COP": "哥倫比亞比索",
    "CRC": "哥斯大黎加科郎",
    "CUP": "古巴比索",
    "CVE": "佛得角埃斯庫多",
    "CZK": "捷克克朗",
    "DJF": "吉布提法郎",
    "DKK": "丹麥克朗",
    "DOP": "多米尼加比索",
    "DZD": "阿爾及利亞第納爾",
    "EGP": "埃及鎊",
    "ERN": "厄立特里亞納克法",
    "ETB": "埃塞俄比亞比爾",
    "EUR": "歐元",
    "FJD": "斐濟元",
    "FKP": "福克蘭群島鎊",
    "FOK": "法羅群島克朗",
    "GBP": "英鎊",
    "GEL": "喬治亞拉里",
    "GGP": "根西鎊",
    "GHS": "迦納塞地",
    "GIP": "直布羅陀鎊",
    "GMD": "甘比亞達拉西",
    "GNF": "幾內亞法郎",
    "GTQ": "瓜地馬拉格查爾",
    "GYD": "蓋亞那元",
    "HKD": "港元",
    "HNL": "宏都拉斯倫皮拉",
    "HRK": "克羅埃西亞庫納",
    "HTG": "海地古德",
    "HUF": "匈牙利福林",
    "IDR": "印尼盾",
    "ILS": "以色列新謝克爾",
    "IMP": "曼島鎊",
    "INR": "印度盧比",
    "IQD": "伊拉克第納爾",
    "IRR": "伊朗里亞爾",
    "ISK": "冰島克朗",
    "JEP": "澤西鎊",
    "JMD": "牙買加元",
    "JOD": "約旦第納爾",
    "JPY": "日圓",
    "KES": "肯亞先令",
    "KGS": "吉爾吉斯索姆",
    "KHR": "柬埔寨瑞爾",
    "KID": "基里巴斯元",
    "KMF": "葛摩法郎",
    "KRW": "韓元",
    "KWD": "科威特第納爾",
    "KYD": "開曼群島元",
    "KZT": "哈薩克堅戈",
    "LAK": "寮國基普",
    "LBP": "黎巴嫩鎊",
    "LKR": "斯里蘭卡盧比",
    "LRD": "賴比瑞亞元",
    "LSL": "賴索托洛蒂",
    "LYD": "利比亞第納爾",
    "MAD": "摩洛哥迪拉姆",
    "MDL": "摩爾多瓦列伊",
    "MGA": "馬達加斯加阿里亞里",
    "MKD": "北馬其頓戴納",
    "MMK": "緬元",
    "MNT": "蒙古圖格里克",
    "MOP": "澳門元",
    "MRU": "茅利塔尼亞烏吉亞",
    "MUR": "模里西斯盧比",
    "MVR": "馬爾地夫盧非亞",
    "MWK": "馬拉威克瓦查",
    "MXN": "墨西哥比索",
    "MYR": "馬來西亞令吉",
    "MZN": "莫三比克梅蒂卡爾",
    "NAD": "納米比亞元",
    "NGN": "奈及利亞奈拉",
    "NIO": "尼加拉瓜科多巴",
    "NOK": "挪威克朗",
    "NPR": "尼泊爾盧比",
    "NZD": "紐西蘭元",
    "OMR": "阿曼里亞爾",
    "PAB": "巴拿馬巴波亞",
    "PEN": "秘魯新索爾",
    "PGK": "巴布亞紐幾內亞基那",
    "PHP": "菲律賓比索",
    "PKR": "巴基斯坦盧比",
    "PLN": "波蘭茲羅提",
    "PYG": "巴拉圭瓜拉尼",
    "QAR": "卡達里亞爾",
    "RON": "羅馬尼亞列伊",
    "RSD": "塞爾維亞戴納",
    "RUB": "俄羅斯盧布",
    "RWF": "盧安達法郎",
    "SAR": "沙烏地里亞爾",
    "SBD": "索羅門群島元",
    "SCR": "塞席爾盧比",
    "SDG": "蘇丹鎊",
    "SEK": "瑞典克朗",
    "SGD": "新加坡元",
    "SHP": "聖赫勒拿鎊",
    "SLE": "獅子山利昂",
    "SOS": "索馬利亞先令",
    "SRD": "蘇利南元",
    "SSP": "南蘇丹鎊",
    "STN": "聖多美和普林西比多布拉",
    "SYP": "敘利亞鎊",
    "SZL": "史瓦帝尼里朗吉尼",
    "THB": "泰銖",
    "TJS": "塔吉克索莫尼",
    "TMT": "土庫曼馬納特",
    "TND": "突尼斯第納爾",
    "TOP": "湯加潘加",
    "TRY": "土耳其里拉",
    "TTD": "千里達及托巴哥元",
    "TVD": "圖瓦盧元",
    "TWD": "台灣新台幣",
    "TZS": "坦尚尼亞先令",
    "UAH": "烏克蘭赫里夫尼亞",
    "UGX": "烏干達先令",
    "USD": "美金",
    "UYU": "烏拉圭比索",
    "UZS": "烏茲別克索姆",
    "VES": "委內瑞拉玻利瓦爾",
    "VND": "越南盾",
    "VUV": "瓦努阿圖瓦圖",
    "WST": "薩摩亞塔拉",
    "XAF": "中非金融合作法郎",
    "XCD": "東加勒比元",
    "XDR": "特別提款權",
    "XOF": "西非金融合作法郎",
    "XPF": "太平洋法郎",
    "YER": "葉門里亞爾",
    "ZAR": "南非蘭特",
    "ZMW": "尚比亞克瓦查",
    "ZWL": "辛巴威元"
}

def get_exchange_rate(from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"取得匯率資料時發生錯誤： {response.status_code} {response.text}")
    data = response.json()
    return data['conversion_rate']

def get_historical_rates(from_currency, to_currency, days=180):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_list = [start_date + timedelta(days=x) for x in range(0, days, 7)]
    rates = {}
    
    for date in date_list:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/history/{from_currency}/{date.year}/{date.month}/{date.day}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"取得歷史匯率資料時發生錯誤： {response.status_code} {response.text}")
        data = response.json()
        if 'conversion_rates' not in data:
            raise Exception(f"API回應格式錯誤： {data}")
        rates[date.strftime('%Y-%m-%d')] = data['conversion_rates'].get(to_currency)
    
    return rates

def plot_historical_rates(canvas, rates, from_currency, to_currency):
    dates = list(rates.keys())
    rates = list(rates.values())

    df = pd.DataFrame({'Date': dates, 'Rate': rates})
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df = df.set_index('Date')

    # 清空當前圖表
    canvas.figure.clf()

    fig = canvas.figure
    ax = fig.add_subplot(111)
    ax.plot(df.index, df['Rate'], marker='o', linestyle='-')
    ax.set_title(f'{currency_names[from_currency]} 轉 {currency_names[to_currency]} 歷史匯率')
    ax.set_xlabel('日期')
    ax.set_ylabel('匯率')
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    canvas.draw()

def on_plot():
    try:
        from_currency = from_currency_var.get().split()[0]
        to_currency = to_currency_var.get().split()[0]
        historical_rates = get_historical_rates(from_currency, to_currency)
        plot_historical_rates(canvas, historical_rates, from_currency, to_currency)
    except Exception as e:
        messagebox.showerror("錯誤", str(e))

def convert_currency():
    try:
        amount = amount_entry.get().strip()
        if not amount:
            messagebox.showerror("輸入無效", "請輸入金額")
            return
        
        from_currency_str = from_currency_var.get().strip()
        if not from_currency_str:
            messagebox.showerror("選擇無效", "請選擇轉換貨幣")
            return

        to_currency_str = to_currency_var.get().strip()
        if not to_currency_str:
            messagebox.showerror("選擇無效", "請選擇目標貨幣")
            return

        amount = float(amount)
        from_currency = from_currency_str.split()[0]
        to_currency = to_currency_str.split()[0]
        rate = get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate
        result_var.set(f"{amount} {currency_names[from_currency]} = {converted_amount:.2f} {currency_names[to_currency]}")
    except ValueError:
        messagebox.showerror("輸入無效", "請輸入有效金額")
    except Exception as e:
        messagebox.showerror("錯誤", str(e))

app = ttkb.Window(themename="cerculean")
app.title("貨幣轉換器")
app.iconbitmap('icon.ico')  # 設置應用程式圖示

# 建立主框架
mainframe = ttk.Frame(app, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# 設置基礎貨幣選擇
ttk.Label(mainframe, text="轉換貨幣").grid(row=0, column=0, sticky=tk.W, pady=(10, 2))  # 調整pady值
from_currency_var = tk.StringVar()
base_currency_combobox = ttk.Combobox(mainframe, textvariable=from_currency_var)
base_currency_combobox['values'] = [f"{code} {name}" for code, name in currency_names.items()]
base_currency_combobox.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)  # 調整行號

# 設置目標貨幣選擇
ttk.Label(mainframe, text="目標貨幣").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))  # 調整pady值
to_currency_var = tk.StringVar()
target_currency_combobox = ttk.Combobox(mainframe, textvariable=to_currency_var)
target_currency_combobox['values'] = [f"{code} {name}" for code, name in currency_names.items()]
target_currency_combobox.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)  # 調整行號

# 設置金額輸入
ttk.Label(mainframe, text="金額").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))  # 調整pady值
amount_var = tk.StringVar()
amount_entry = ttk.Entry(mainframe, textvariable=amount_var)
amount_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)  # 調整行號

# 設置結果顯示
ttk.Label(mainframe, text="轉換結果").grid(row=6, column=0, sticky=tk.W, pady=(10, 2))  # 調整pady值
result_var = tk.StringVar()
result_label = ttk.Label(mainframe, textvariable=result_var, foreground="blue", font=("Arial", 12))
result_label.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=2)  # 調整行號

# 設置轉換按鈕
convert_button = ttk.Button(mainframe, text="轉換", command=convert_currency)
convert_button.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

# 設置匯率走勢圖按鈕
plot_button = ttk.Button(mainframe, text="顯示匯率走勢圖", command=on_plot)
plot_button.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)


# 設置匯率走勢圖顯示區域
trend_frame = ttk.LabelFrame(app, text="匯率走勢圖", padding="10")
trend_frame.grid(row=0, column=1, rowspan=6, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
trend_frame.columnconfigure(0, weight=1)
trend_frame.rowconfigure(0, weight=1)

# 創建圖表畫布
fig = plt.Figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=trend_frame)
canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

app.mainloop()