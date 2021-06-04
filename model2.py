
import os,random,math


from flask import Flask,render_template,request

app = Flask(
    __name__
)





if not os.path.exists('Documents'):
    os.mkdir('Documents')


def createDocs():

    for i in range(1,11):
        f =  open(f'Documents/Doc{i}.txt','w')
        for _ in range(0,random.randint(0,151) ):
            f.write( random.choice(['A','B','C','D','E','F']) + ' ' )
        f.close()

#createDocs()



query = 'A C F B B'


def pr():
    print(query)
    
idf = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'E': 0,
    'F': 0,
}

def calcIDF(idf):
    for i in range(1,11):    
        f = open(f'Documents/Doc{i}.txt','r')
        flist = f.read().split(' ')

        for i in idf.keys():
            if i in flist:
                idf[i]+=1
        else:
            for i in idf.keys():
                idf[i] = math.log2(10/idf[i])




def calcTF(path):

    f = open(path,'r')
    flist = f.read().split(' ')
    f.seek(0,0)
    f.close()#
    counter ={
        'A': flist.count('A'),
        'B': flist.count('B'),
        'C': flist.count('C'),
        'D': flist.count('D'),
        'E': flist.count('E'),
        'F': flist.count('F'),
    }

    maxTF = max(counter.values())

    tf = {
        'A': counter['A']/maxTF,
        'B': counter['B']/maxTF,
        'C': counter['C']/maxTF,
        'D': counter['D']/maxTF,
        'E': counter['E']/maxTF,
        'F': counter['F']/maxTF,
    }
    return tf



def calcWeight(path):
    weight = {
        'A': calcTF(path)['A']*idf['A'],
        'B': calcTF(path)['B']*idf['B'],
        'C': calcTF(path)['C']*idf['C'],
        'D': calcTF(path)['D']*idf['D'],
        'E': calcTF(path)['E']*idf['E'],
        'F': calcTF(path)['F']*idf['F'],
    }
    return weight




def calcQTF(str):

    str = str.split(' ')

    counter ={
        'A': str.count('A'),
        'B': str.count('B'),
        'C': str.count('C'),
        'D': str.count('D'),
        'E': str.count('E'),
        'F': str.count('F'),
    }

    maxTF = max(counter.values())

    tf = {
        'A': counter['A']/maxTF,
        'B': counter['B']/maxTF,
        'C': counter['C']/maxTF,
        'D': counter['D']/maxTF,
        'E': counter['E']/maxTF,
        'F': counter['F']/maxTF,
    }
    return tf

def calcQWeight(str):
    weight = {
        'A': calcQTF(str)['A']*idf['A'],
        'B': calcQTF(str)['B']*idf['B'],
        'C': calcQTF(str)['C']*idf['C'],
        'D': calcQTF(str)['D']*idf['D'],
        'E': calcQTF(str)['E']*idf['E'],
        'F': calcQTF(str)['F']*idf['F'],
    }
    return weight



def cosSim(qweight,dweight):

    top=0

    for i in dweight.keys():
        top+= dweight[i] * qweight[i]


    bottom1=0
    bottom2=0

    for i in qweight.values():
        bottom1 += i**2
    for i in dweight.values():
        bottom2 += i**2

    return( top/math.sqrt( bottom1*bottom2 ) )



cosSimDic ={

}

def allCalc():
    for i in range(1,11):
        qweight = calcQWeight(query)
        dweight = calcWeight(f'Documents/Doc{i}.txt')

        cosSimDic[f'Doc{i}'] = cosSim( qweight , dweight )
    return cosSimDic




def sortDic( docs ):    
    import operator  
    sortedDocs = sorted( docs.items(),key=operator.itemgetter(1),reverse=True )
    return sortedDocs


def printSorted():
    for _ in sortDic(cosSimDic):
        print(_[0])



@app.route('/create')
def create():
    createDocs()
    return 'Files Created Successfully'

@app.route('/form')
def f():
    return render_template('form.html')


@app.route('/',methods=['POST'])

def local():
    if request.method=='POST':
        global query
        query = request.form['btn']
        calcIDF(idf)
        return render_template('index.html',passed= sortDic(allCalc()) )


if __name__ == '__main__':
    app.run(debug=True)