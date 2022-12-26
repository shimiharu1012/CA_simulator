from flask import Flask, render_template,request   #webアプリフレームワーク用のライブラリをimport
import random   #初期状態のランダム生成用


app=Flask(__name__)



#新しいセルオートマトンを生成する関数
def ReturnNewCells(cells,rule):
    
    cells_len=len(cells)    #セルオートマトンの長さをcell_lenに代入
    NewCells=[0 for i in range(0,cells_len)]    #更新後のセルオートマトンを宣言（すべて０）
    ReturnCell=format(int(rule),'08b')  #ルールを８桁の二進数（文字列）に変換

    for x in range(0,len(cells)):   #対象のセルおよび前後のセルの状態とルールを基に対象セルを更新

        if cells[x-1]==0 and cells[x]==0 and cells[(x+1)%cells_len]==0:
            NewCells[x]=int(ReturnCell[7])
        elif cells[x-1]==0 and cells[x]==0 and cells[(x+1)%cells_len]==1:
            NewCells[x]=int(ReturnCell[6])
        elif cells[x-1]==0 and cells[x]==1 and cells[(x+1)%cells_len]==0:
            NewCells[x]=int(ReturnCell[5])
        elif cells[x-1]==0 and cells[x]==1 and cells[(x+1)%cells_len]==1:
            NewCells[x]=int(ReturnCell[4])
        elif cells[x-1]==1 and cells[x]==0 and cells[(x+1)%cells_len]==0:
            NewCells[x]=int(ReturnCell[3])
        elif cells[x-1]==1 and cells[x]==0 and cells[(x+1)%cells_len]==1:
            NewCells[x]=int(ReturnCell[2])
        elif cells[x-1]==1 and cells[x]==1 and cells[(x+1)%cells_len]==0:
            NewCells[x]=int(ReturnCell[1])
        elif cells[x-1]==1 and cells[x]==1 and cells[(x+1)%cells_len]==1:
            NewCells[x]=int(ReturnCell[0])


    return NewCells #新しいオートマトンを返す




@app.route('/',methods=['GET'])
def get():
    
    form_data=[]
    ch0="selected"
    return render_template('CA_simulator.html',
    form_data=form_data,    #form_dat'CA_simulator.htmlにおけるvalueの参照ミスを防ぐ
    ch0=ch0                 #CA_simulator.html内のセレクトボックスでデフォルトの選択を保持
    )    
    

@app.route('/',methods=['POST'])
def post():

    #CA_simulator.htmlのinputから受け取る各種パラメータ
    initial_state=request.form.get('initial_state') #初期状態
    rule=request.form.get('rule')                   #ルール     
    times=int(request.form.get('times'))            #世代数
    cells_len=int(request.form.get('cells_len'))     #オートマトンののセル数(120~240)


    #セルオートマトンの挙動を分類するλパラメータを計算()
    #8は近傍の状態数の総パターン数=ルールあたりの生成パターン数である
    b_rule=format(int(rule),'08b')  #b_ruleはルールをbit列に変換したもの
    _lambda=b_rule.count('1')/8 
    
    

    #初期状態のセルを生成

    ch0=ch1=ch2=ch3=ch4=ch5=ch6=ch7=ch8=""  #CA_simulator.html内のセレクトボックスで選択を保持するための埋め込み変数
    

    if initial_state=="ランダム":
        cells=[round(random.random()) for i in range(0,cells_len)]
        ch0="selected"
    elif initial_state=="右端のみ1":
        cells=[0 for i in range(0,cells_len-1)]+[1]
        ch1="selected"
    elif initial_state=="左端のみ1":
        cells=[1]+[0 for i in range(0,cells_len-1)]
        ch2="selected"
    elif initial_state=="中央のみ1":
        cells=[0 for i in range(0,int(cells_len/2))]+[1]+[0 for i in range(0,int(cells_len/2-1))]
        ch3="selected"
    elif initial_state=="0と1が交互":
        cells=[i%2 for i in range(0,cells_len)]
        ch4="selected"
    elif initial_state=="右半分が1":
        cells=[0 for i in range(0,int(cells_len/2))]+[1 for i in range(0,int(cells_len/2))]
        ch5="selected"
    elif initial_state=="左半分が1":
        cells=[1 for i in range(0,int(cells_len/2))]+[0 for i in range(0,int(cells_len/2))]
        ch6="selected"
    elif initial_state=="すべて0":
        cells=[0 for i in range(0,cells_len)]
        ch7="selected"
    elif initial_state=="すべて1":
        cells=[1 for i in range(0,cells_len)]
        ch8="selected"


    cells_list=[cells]      #初期セルをセルリスト一番最初に差し込む

    #生成したセルをセルリストに追加するのを、世代数分繰り返す
    i=0
    while i<times:
        cells=ReturnNewCells(cells,rule)
        cells_list.append(cells)
        i+=1


    return render_template('CA_simulator.html',
    rule=rule,
    message=f"λ={f'{_lambda:.03f}'}",
    cells_list=cells_list,  #時系列に並んだオートマトンのリスト（実行結果）
    cells_len=cells_len,    #オートマトンのセル数
    form_data=request.form,  #request.formは入力フォームからの入力データを保持している
    ch0=ch0,ch1=ch1,ch2=ch2,ch3=ch3,ch4=ch4,ch5=ch5,ch6=ch6,ch7=ch7,ch8=ch8,    #chはセレクトボックスの入力データを保持するのに使う
    )




if __name__ =="__main__":
    app.run()
    