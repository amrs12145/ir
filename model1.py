import os,random,math


from flask import Flask,render_template,request

app = Flask(
    __name__
)




import os,random

if not os.path.exists('Documents'):
    os.mkdir('Documents')

def createDocs():

    for i in range(1,11):
        f =  open(f'Documents/Doc{i}.txt','w')
        for _ in range(0, random.randint(0,151) ):
            f.write( random.choice(['A','B','C','D','E','F']) + ' ' )
        f.close()

#createDocs()


def cleanQuery(query):
    query = query.replace('<','')
    query = query.replace('>','')
    query = query.replace(';','\n')
    query = query.replace(':',' ')
    return query




def calcQWeight(query,qweight):
    for i in range(0,len(query) ):
        if query[i] in ['A','B','C','D','E','F']:
            qweight[ query[i] ] = float( query[i+2:i+5] )
     
            
query = '<B:0.3;F:0.2;D:0.1;C:0.4>'
query = cleanQuery( query )

qweight ={'A':0, 'B':0,'C':0,'D':0,'E':0,'F':0}
calcQWeight(query,qweight)



def calcDocWeight(path):

    f =  open(path,'r')
    length = len(f.read())
    f.seek(0,0)
    counter ={'A':0, 'B':0,'C':0,'D':0,'E':0,'F':0}

    for _ in range(0,length ):
        char = f.read(1)
        if char == ' ':
            continue
        elif char in ['A','B','C','D','E','F']:
            counter[char]+=1
    else:
        f.seek(0,0)        

    docWeight = {
        'A':counter['A']/(length/2),
        'B':counter['B']/(length/2),
        'C':counter['C']/(length/2),
        'D':counter['D']/(length/2),
        'E':counter['E']/(length/2),
        'F':counter['F']/(length/2),
    }

    return docWeight



def sim( dw,qw ):
    tmp=0
    for k in dw.keys() :
        tmp += dw[k] * qw[k]
    return tmp




docs ={
 
}

def calcSim( docs ):
    for i in range(1,11):
        docs[f'Doc{i}'] = sim( calcDocWeight(f'Documents/Doc{i}.txt'), qweight )
    return docs

def sortDic( docs ):    
    import operator
    sortedDocs = sorted( docs.items(),key=operator.itemgetter(1),reverse=True )
    return sortedDocs


def printSorted():
    for _ in sortDic(docs):
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
        calcQWeight(query,qweight)
        return render_template('index.html',passed= sortDic(calcSim(docs)) )


if __name__ == '__main__':
    app.run(debug=True)