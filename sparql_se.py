# coding: utf-8
import re, codecs
from SPARQLWrapper import SPARQLWrapper, JSON

request = u'кем создан Sony'
request1 = u'автор Серия романов о Гарри Поттере'
request2 = u'Пушкин Александр Сергеевич смерть'
request3 = u'когда умер Кутузов, Михаил Илларионович'
request4 = u'находится Москва'
request5 = u'Москва википедия'
abstract = [u'биография', u'википедия', u'информация']

quest = {u'когда':'Date', u'дата':'Date', u'год':'Date', u'месяц':'Date', u'день':'Date', u'где':'Place', u'место':'Place', u'кем':'By', u'кто':'By'}
facts = {u'рождения|родил[аи]?с[ья]':'dbo:birth', u'смерти|умер([лш][аи][ейя]?)?':'dbo:death', u'создан(а|ы|ия)?':'dbo:founding', u'основан(а|ы|ия)?':'dbo:established',u'автор(ы)?':'dbp:author',
         u'смерть':'dbo:deathDate', u'наход[ия]тся':'dbo:country'}

def whole(r):
    return extractSparqlInfo(sparqlmoded(trsl_n(r)))

def trsl_n(req):
    req1 = req.split()
    translation = []
    for word in req1:
        if word in quest:
            for i in facts:
                match = re.findall(i, req1[req1.index(word) + 1])
                if match:
                    if facts[i] == 'dbo:founding':
                        if quest[word] == 'By':
                            query = facts[i].replace('ing', 'ed') + quest[word]
                        elif quest[word] == 'Place':
                            query = facts[i].replace('ing', 'ation') + quest[word]
                        else:
                            query = facts[i] + quest[word]
                    else:
                        query = facts[i] + quest[word]
                    translation.append(query)
                    req1.remove(req1[req1.index(word) + 1])
                    req1.remove(word)
                    for it in req1:
                        translation.append(it)
                    return translation
        else:
            for i1 in facts:
                match = re.findall(i1, req1[req1.index(word)])
                if match:
                    query = facts[i1]
                    translation.append(query)
                    req1.remove(word)
                    for it in req1:
                        translation.append(it)
                    print (translation)
                    return translation

def sparqlmoded(req1):
    sparqlmode = {}
    syw = req1[1:]
    stroka = ''
    for q in range(len(syw)):
        stroka += syw[q]
        if q != len(syw) - 1:
            stroka += ' '
    sparqlmode[req1[0]] = stroka
    zapros = list(sparqlmode.keys())[0]
    sywnost =sparqlmode[list(sparqlmode.keys())[0]]
    return (zapros, sywnost)

def extractSparqlInfo(l):
    valueresults = []
    inquiry = l[0]
    essence = l[1]
    dbzapros = inquiry[4:]
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbpprop: <http://dbpedia.org/property/>
        SELECT DISTINCT ?e ?%(dbzapros)s
        WHERE {
	    ?e rdfs:label "%(essence)s"@ru .
	    ?e %(inquiry)s ?%(dbzapros)s
              }
        """  % locals())
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    u1 = results[u'results']
    u2 = u1[u'bindings']
    for j in u2:
        u4 = j[dbzapros]
        u5 = u4[u'value']
        valueresults.append(u5)
    return valueresults

print (whole(request2))
