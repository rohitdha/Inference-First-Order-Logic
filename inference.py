"""
  Author: Rohit Dhawan
  Algorithm: Backward Chaining
  Domain: Artificial Intelligence
"""
import sys
import collections
import re

class ReadData():
	
	no_of_clauses = 0
	no_of_queries = 0
	implication_list = []
	predicate_list = []
	query_list = []
	overall_list = []
	my_dict = {}
	LHS_VALUES = []
	RHS_VALUES = []
	LHS_VALUES_NEW = []
	RHS_VALUES_NEW = []
	answers = ""
	stack = [] 
	
	def readFile(self):
		with open(sys.argv[-1], 'r') as f:
			content = f.read()
		
		contents = re.sub("\n\s*\n*", "\n", content)
		contents = contents.replace('\r','')
		
		# Complete input_file is present in the overall_list 
		ReadData.overall_list = contents.splitlines()
		#for u in ReadData.overall_list:
		#	print u

		# Total number of queries are present in the no_of_queries
		ReadData.no_of_queries = ReadData.overall_list[0]
		#print "\n" + ReadData.no_of_queries + "\n"
		
		# Building Query_list
		for i in range(1, int(ReadData.no_of_queries)+1):		
			ReadData.query_list.append(ReadData.overall_list[i])
		
 		
		#Total number of clauses present in the knowledge base
		ReadData.no_of_clauses = ReadData.overall_list[int(ReadData.no_of_queries)+1]
		#print "\n" + ReadData.no_of_clauses + "\n"
		
		for i in range(int(ReadData.no_of_queries)+2,len(ReadData.overall_list)):
			if ReadData.overall_list[i].find("=>") != -1:
				ReadData.implication_list.append(ReadData.overall_list[i])
			else:
				ReadData.predicate_list.append(ReadData.overall_list[i])
			
		#print len(ReadData.predicate_list)
		
		for item in ReadData.implication_list:
			ReadData.RHS_VALUES.append(item[item.index("=>")+2:].lstrip().rstrip())
			
		for item in ReadData.implication_list:
			ReadData.LHS_VALUES.append(item.rpartition('=>')[0].lstrip().rstrip())
		
		for item in ReadData.predicate_list:
			ReadData.RHS_VALUES.append(item.lstrip().rstrip())
			ReadData.LHS_VALUES.append("")
		
		"""for i in ReadData.RHS_VALUES:
			print i
			
		for i in ReadData.LHS_VALUES:
			print i
		print "\n"
		"""
		list = []
		and_ = "^"
		for count,item in enumerate(ReadData.LHS_VALUES):
			parts = item.split("^")
			#print parts
			list = []
			for it in parts:
				if it != '':
					k = self.args(it)
					k1 = k
					l = k.split(",")
					for itel in l:
						if(self.variable(itel)):
							k = k.replace(itel,itel+str(count+1))	
					#print it
					it = it.replace(k1,k)
					#print it
					list.append(it);
			L1 = and_.join(list)
			
			ReadData.LHS_VALUES_NEW.append(L1)
		
		list = []
		comma_ = ","
		for count,item in enumerate(ReadData.RHS_VALUES):
			k = self.args(item)
			u = item.rpartition('(')[0]
			#print u
			list = []
			l = k.split(",")
			#print l
			for itel in l:
				if(self.variable(itel)):
					itel = itel.replace(itel,itel+str(count+1))
				list.append(itel)
			l1 = comma_.join(list)
			#print l1
			complete_string = u + "(" + l1 + ")"
			#print complete_string
			ReadData.RHS_VALUES_NEW.append(complete_string)
	
		"""for i in ReadData.RHS_VALUES_NEW:
			print i
		
		for i in ReadData.LHS_VALUES_NEW:
			print i
		"""
	def replaceall(self,item,itel,itel1):
		item = item.replace(itel1,itel)
		return item
	
	def createImplicationMap(self):
		for item in ReadData.implication_list:
			ReadData.my_dict[item.rpartition('=>')[0]] = item[item.index("=>")+2:]
		#for keys,values in ReadData.my_dict.items():
		#	print keys + "  " + values
	
	def check_facts(self,val):
		for list in ReadData.predicate_list:
			if val == list:
				return "TRUE"
	
	def backward_chain(self,file):
		for val in ReadData.query_list:
			x = self.check_facts(val)
			if ( x == "TRUE" ):
				#print 'TRUE'
				file.write("TRUE")
			else:
				y = self.ask_backward_chain(val,"")
				ReadData.stack = []
				ReadData.answers = ""
				if y != "":
					#print 'TRUE'
					file.write('TRUE')
					
				else:
					#print 'FALSE'
					file.write('FALSE')
			file.write("\n")
				
	
	def ask_backward_chain(self, val, theta):

		if not val:
			return theta
		
		#print "\n","value of theta: ",theta,"\n";
		q = self.sub_str( theta, self.first_Quotient(val))
		#print "\n","value of q currently: ",q,"\n";
		
		for item in ReadData.stack:
			if item == q:
				if ReadData.stack.count(item) > 2:
					return ReadData.answers
		
		ReadData.stack.append(q)
		
		for i in range(0,len(ReadData.RHS_VALUES_NEW)):
			index = q.index("(")
			#print ReadData.RHS_VALUES[i]
			qindex = ReadData.RHS_VALUES[i].index("(")
			
			if ReadData.RHS_VALUES[i][0:qindex] == q[0:index]:
				yo = self.unify(q,ReadData.RHS_VALUES_NEW[i],"")
				#print "yo\t",yo
				if yo != "Failure":

					new_goals = ReadData.LHS_VALUES_NEW[i] + "^" + self.rest_Quotient(val)

					if new_goals[len(new_goals)-1] == '^':
						new_goals = new_goals[0:len(new_goals)-1]
					
					elif new_goals[0] == "^":
						new_goals = new_goals[1:len(new_goals)]
						
					new_goals = new_goals.lstrip()
					ReadData.answers = ReadData.answers + self.ask_backward_chain(new_goals,self.compose(yo,theta))
					#print "ReadData.answers\t",ReadData.answers

		return ReadData.answers
		
	
	def first_Quotient(self, val):
		part = val.split('^');
		return part[0]
	
	def rest_Quotient(self,val):
		parts = val.split("^")
		contents = ""
		if(len(parts) == 1):
			return ""
		else:
			for i in range(1, len(parts)):
				contents += parts[i] + "^"
		return contents[0:int(len(contents)-1)]
	
	def compose(self, q, theta):
		new_string = ""
		if not theta:
			new_string = q
		elif not q:
			new_string = theta
		else:
			new_string = q + "," + theta
		return new_string
	
	def checkargs(self, z):
		val = z.split(",")
		return len(val)
	
	def sub_str(self,theta,concl):
		start_index = concl.index('(')
		last_index = concl.index(')')
		result = concl[start_index+1:last_index]
		params = result.split(',')
		part = theta.split(',')
		"""print "Params\t ",params,"\n"
		print "Part\t ",part,"\n"
		print "theta\t ",theta,"\n"
		"""
		if(len(part) == 1):
			part2 = part[0].split("/")
			for i in params:
				if part2[0] == i:
					concl = concl.replace(i,part2[1])
		else:
			for j in part:
				part2 = j.split('/')
				for x in params:
					if part2[0] == x:
						concl = concl.replace(x,part2[1])
		return concl
	
	
	def unify(self,x,y,theta):
		
		#print "\n","inside unify, value of theta: ",x," ",y,"\n"
		if theta == "Failure":
			return "Failure"
		
		elif x == y:
			return theta;
		
		elif self.variable1( x ):
			return self.unifyvar( x, y, theta)
		
		elif self.variable1( y ):
			return self.unifyvar( y, x, theta)
		
		elif ( self.compound( x ) and self.compound( y ) ):
			return self.unify( self.args( x ), self.args( y ), self.unify( self.ops( x ), self.ops( y ), theta))
		
		elif ( self.list(x) and self.list(y) ):
			return self.unify( self.rest( x ), self.rest( y ), self.unify( self.first( x ), self.first( y ), theta)) 
		else:
			return "Failure"
	
	def unifyvar(self, x, y, theta):
		val = self.checkvar ( x, theta)
		val2 = self.checkvar( y, theta)
		if (self.belongs(x, val, theta)):
			return self.unify(val, y, theta)
		elif (self.belongs ( y, val, theta) ):
			return self.unify( x, val2, theta)
		else:
			if( theta == "" ):
				theta = theta + x + "/" + y
			else:
				theta = theta + "," + x + "/" + y
		return theta;
		
	def belongs(self,x,val,theta):
		part = theta.split(',')
		y =  x + "/" + val
		for l in part:
			if y in l:
				return True
		return False
	
	def checkvar(self,x,theta):
		val = ""
		if theta == "":
			return ""
		else:
			part = theta.split(',')
			if( len(part) > 1):
				for l in part:
					part2 = l.split('/')
					if part2[0] == x:
						val = part2[1]
						break;
			else:
				part2 = theta.split('/')
				if part2[0] == x:
					val = part2[1]
		
		return val;
	
	def rest(self, x):
		parts = x.split(",")
		contents = ""
		for i in range(1, len(parts)):
			contents += parts[i] + ","
		return contents[0:int(len(contents)-1)]
			
	def variable1(self,x):
		#if( x[0].islower() and len(x) == 2):
		if x.isalnum() and x.islower():
			return True
		return False
	
	def variable(self,x):
		if( x.isalpha() and x.islower() and len(x) == 1):
			return True
		return False
	
	def compound(self,x):
		if '(' in x and len(x) > 1 :
			return True;
		return False
	
	def ops(self,x):
		return x.rpartition('(')[0]
	
	def args(self,x):
		return x[x.index("(")+1:x.index(')')]
	
	def list(self,x):
		if ',' in x:
			if '(' not in x:
				return True
		return False
	
	def first(self,x):
		parts = x.split(',')
		return parts[0]
	
def main():
	c = ReadData()
	c.readFile()
	file = open("output.txt", "w")
	#c.createImplicationMap()
	c.backward_chain(file)
	
if __name__ == "__main__":
	main()
