from flask import Flask
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
 
import MeCab;tagging = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
import nltk
from random import *
 
app = Flask(__name__)
api = Api(app)
 
mariadb = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'mgmtsv'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mgmtsv1!'
app.config['MYSQL_DATABASE_DB'] = 'mgmtsv'
app.config['MYSQL_DATABASE_HOST'] = '10.178.87.140'
mariadb.init_app(app)
 
class RecommendCompany(Resource):
    def get(self, _serialNo, _userId):
        try:           
            result = self.analysis(_serialNo, _userId)
 
            return result
        except Exception as e:
            return {'error':str(e)}
 
    def analysis(self, _sn, _id):
        # inquery self-introduce text in DB by userId
        conn = mariadb.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT cover_letter FROM sv_applies WHERE serial_number = %s and apply_user_id = %s', (_sn, _id))
        introduce_text = cursor.fetchall()
 
        if len(introduce_text) == 0:
            return {'error':'SN or ID is not exists!'}
        else:
            introduce_text = introduce_text[0][0]
 
        cursor.execute('SELECT company_id, keyword FROM sv_dictionaries')
        company_keyword = cursor.fetchall()
        cursor.close()
        conn.close()
 
        # find matching company
        tokens_ko = self.getNouns(introduce_text)
        #print('------token(getNouns)')
        #print(tokens_ko)
        ko = nltk.Text(tokens_ko, name='content')
 
        user_keywords = ko.vocab().most_common(30)
        #print('------user_keywords')
        #print(user_keywords)
        #print('------company_keyword')
        #print(company_keyword)
 
        company_set = set([c1 for (c1, c2) in company_keyword])
        freq = dict(zip(list(company_set),[0]*len(company_set)))
 
        for (c1, c2) in company_keyword:
            freq[c1] += sum([ u2 for (u1, u2) in user_keywords if c2==u1 ])
 
        sorted_freq = sorted(freq, key = lambda k : (freq[k], random()), reverse=True)
        #print('------sorted_freq')
        #print(sorted_freq)
 
        result = [
            {'order':1,'company_id':sorted_freq[0]},
            {'order':2,'company_id':sorted_freq[1]},
            {'order':3,'company_id':sorted_freq[2]}
        ]
 
        return result

    def getNouns(self, _sentense):
        tag = tagging.parseToNode(_sentense)
        analyzed = []

        while tag:
            if tag.feature.split(',')[0] == 'NNG' :
                analyzed.append(tag.surface)
            tag = tag.next

        return analyzed
 
api.add_resource(RecommendCompany, '/analysis/<string:_serialNo>/<string:_userId>', endpoint='analysis')
 
if __name__ == '__main__':
    app.run(port=8082, debug=True)