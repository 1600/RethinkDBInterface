#!coding=utf-8
import rethinkdb as r
from ctypes import *
import urlparse


doc = {
	 "WebsiteURL": "http://jiangxi.gov.cn",
	 "WebsiteTitle": u"江西人民政府",
	 "MaliciousLinks": [ 
	   {
	       "Link": "http://jiangxi.gov.cn/xxaw/jwdaja.html?weja",
	       "DetectionRule" : "js",
	       "Keyword": u"色情",
	       "FromBaiduSearch": "http://www.baidu.com/s?wd=site:www.jiangxi.gov.cn%20%C9%AB%C7%E9&pn=1"
	   },
	   {
	       "Link": "http://jiangxi.gov.cn/xxaw/123412a.html?5151a",
	       "DetectionRule" : "js",
	       "Keyword": u"博彩",
	       "FromBaiduSearch": "http://www.baidu.com/s?wd=site:www.jiangxi.gov.cn%20%C9%AD%C7%E9&pn=1"
	   },
	 	]
	}


doc2 = {
	 "WebsiteURL": "http://jiangxi.gov.cn",
	 "WebsiteTitle": u"江西人民政府",
	 "MaliciousLinks": [ 
	   {
	       "Link": "http://jiangxi.gov.cn/hanm/00000000.html?2222c",
	       "DetectionRule" : "lucas",
	       "Keyword": u"枪支",
	       "FromBaiduSearch": "http://www.baidu.com/s?wd=site:www.jiangxi.gov.cn%20%C9%AD%C7%E9&pn=1"
	   },
	 	]
	}


class rtOperation():
	def __init__(self):

		self.conn = r.connect(host="192.168.10.28",port=28015,db='test')
		#self.table =r.table("MALINK")
		self.table = r.table("TEST")
		#r.table_create('TEST').run(rt.conn)

	def Insert(self,document):
		document["id"]=urlparse.urlparse(document["WebsiteURL"]).netloc
		try:
			self.table.get(document["id"]).merge(document).run(self.conn)
		except:
			println("<CONFLICT='UPDATE'>no such id in table, inserting new record with id ="+document["id"],11)
			return self.table.insert(document, conflict="update").run(self.conn)

	def SHOW_DBS(self):
		print r.db_list().run(self.conn)			# 列出数据库

	def SHOW_ALL_CONTENT(self):
		cursor = self.table.run(self.conn)	# 列出__init__中当前表的文档
		for document in cursor:
			print document

	def FilterByRule(self,filter_rule):
		cursor = self.table.filter(filter_rule).run(self.conn)	# filter(r.row["name"] == "William Adama")  # filter(r.row["posts"].count() > 2)
		sums=[]
		for document in cursor:
			sums.append(document)
		return sums

	def Update(self,filter_rule, dataToUpdate):
		self.table.filter(filter_rule).update(dataToUpdate).run(self.conn)

	def Delete(self,filter_rule):
		self.table.filter(filter_rule).delete().run(self.conn)

	def Upsert(self,dataToUpdate):
			# TODO
		pass


def println(s,color):
	windll.Kernel32.GetStdHandle.restype = c_ulong
	h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
	windll.Kernel32.SetConsoleTextAttribute(h, color)
	print s
	windll.Kernel32.SetConsoleTextAttribute(h, 10)			

if __name__ ==  "__main__":

	

	rt = rtOperation()



	# println("------------------ Test Query Begins -------------------------")
	# p = rt.table.pluck({"MaliciousLinks": ["Keyword"]}).run(rt.conn)	#[{u'MaliciousLinks': [{u'Keyword': u'\u8272\u60c5'}, {u'Keyword': u'\u535a\u5f69'}]}]
	# print p
	# print "type of p is:",type(p)  # <class 'rethinkdb.net.DefaultCursor'>
	# println("--------------------- Test Query Ends  -------------------------\n\n\n")

	println("----------------------- Test Upsert Begins ----------------------\n",11)
	rt.Delete({})
	#删除所有，重新开始"
	pool = {}

	rt.Insert(doc)
	#print rt.table.get(doc["id"]).run(rt.conn) #.merge(document).


	println("After initial insertion, TEST currently contains:\n",14)
	rt.SHOW_ALL_CONTENT()

	
	println("Now, we do insert with conflict='update'\n",14)

	rt.Insert(doc2)
	rt.SHOW_ALL_CONTENT()





	println("----------------------- Test Upsert Ends ----------------------\n",11)