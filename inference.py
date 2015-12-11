"""
  Author: Rohit Dhawan
  Algorithm: Backward Chaining
  Domain: Artificial Intelligence
  
  Sample Input Format:
	2                // 2 Queries
	H(Bob)
	F(Hello)
	3                // 3 Entries in the KB: Knowledge base
	R(x) => H(x)
	R(Tom)
	F(Hi)
	
  Sample Output Format:
	TRUE
	FALSE
	
  Statement:
  	R(x) => H(x)
  	H(Bob)
  	RHS LIST: H(x)
  	LHS LIST: R(x),H(Bob)
"""
import sys
import collections
import re

# Defined a class for reading the data, implementing Backward Chaining and generating the output
class Backward_Chain():
	
	# Variables used 
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
	
	# Function to read and manipulate the input from the file
	def readFile(self):
		with open(sys.argv[-1], 'r') as f:
			content = f.read()
		
		# To handle file formatting 
		contents = re.sub("\n\s*\n*", "\n", content)
		contents = contents.replace('\r','')
		
		# Storing complete input_file in the overall_list 
		Backward_Chain.overall_list = contents.splitlines()

		# Storing number of queries in the no_of_queries variable
		Backward_Chain.no_of_queries = Backward_Chain.overall_list[0]
		
		# Building Query_list
		for i in range(1, int(Backward_Chain.no_of_queries)+1):		
			Backward_Chain.query_list.append(Backward_Chain.overall_list[i])
		
 		
		#Total number of clauses present in the no_of_clauses
		Backward_Chain.no_of_clauses = Backward_Chain.overall_list[int(Backward_Chain.no_of_queries)+1]
		
		#Traversing the Knowledge base to figure out Compound Statements and Predicate Statments
		for i in range(int(Backward_Chain.no_of_queries)+2,len(Backward_Chain.overall_list)):
			if Backward_Chain.overall_list[i].find("=>") != -1:
				Backward_Chain.implication_list.append(Backward_Chain.overall_list[i])
			else:
				Backward_Chain.predicate_list.append(Backward_Chain.overall_list[i])
		
		#Creating RHS VALUE LIST from compound list
		for item in Backward_Chain.implication_list:
			Backward_Chain.RHS_VALUES.append(item[item.index("=>")+2:].lstrip().rstrip())
		
		# Creating LHS VALUE LIST from compound list
		for item in Backward_Chain.implication_list:
			Backward_Chain.LHS_VALUES.append(item.rpartition('=>')[0].lstrip().rstrip())
		
		# Creating LHS and RHS VALUE LIST from the Predicate list 
		for item in Backward_Chain.predicate_list:
			Backward_Chain.RHS_VALUES.append(item.lstrip().rstrip())
			Backward_Chain.LHS_VALUES.append("")
		
		# Handles variable standardization 
		# Creating new LHS value list after Standardization 
		list = []
		and_ = "^"
		for count,item in enumerate(Backward_Chain.LHS_VALUES):
			parts = item.split("^")
			list = []
			for part in parts:
				if part != '':
					arguments = self.args(part)
					new_arguments = arguments
					single_variable = arguments.split(",")
					for vars in single_variable:
						if(self.variable(vars)):
							arguments = arguments.replace(vars,vars+str(count+1))	
					part = part.replace(new_arguments,arguments)
					list.append(part);
			new_list = and_.join(list)
			
			Backward_Chain.LHS_VALUES_NEW.append(new_list)
		
		# Creating new RHS Value list after Standardization
		list = []
		comma_ = ","
		for count,item in enumerate(Backward_Chain.RHS_VALUES):
			arguments = self.args(item)
			predicate_ = item.rpartition('(')[0]
			list = []
			single_variable = arguments.split(",")
			for vars in single_variable:
				if(self.variable(vars)):
					vars = vars.replace(vars,vars+str(count+1))
				list.append(vars)
			new_list_ = comma_.join(list)
			complete_string = predicate_ + "(" + new_list_ + ")"
			Backward_Chain.RHS_VALUES_NEW.append(complete_string)
	
	# Function to carry out Replacements in a string
	def replaceall(self,item,var,var_1):
		item = item.replace(var_1,var)
		return item
	
	# A dictionary object that stores KB
	def createImplicationMap(self):
		for item in Backward_Chain.implication_list:
			Backward_Chain.my_dict[item.rpartition('=>')[0]] = item[item.index("=>")+2:]
	
	# Backward Chaining Algorithm 
	def backward_chain(self,file):
		for val in Backward_Chain.query_list:
			x = self.check_facts(val) # Check if predicate is already present in the Knowledge base 
			if ( x == "TRUE" ):
				file.write("TRUE")
			else:
				y = self.ask_backward_chain(val,"") # Do Substitutions and traverse through KB to infer results
				Backward_Chain.stack = []
				Backward_Chain.answers = ""
				if y != "":
					file.write('TRUE')
				else:
					file.write('FALSE')
			file.write("\n")
	
	# Traverse KB to see if Predicate in the KB
	def check_facts(self,val):
		for list in Backward_Chain.predicate_list:
			if val == list:
				return "TRUE"
				
	"""
	theta : Stores appended substitution from the repetitive recursive calls initially blank{" "} 
	val:    Predicate from the Query to be proved
	Backward_Chain.answers: if "val"{Query} is proved from the KB:
					return "complete substitution list"
				else 
					return "empty string" 
	"""
	def ask_backward_chain(self, val, theta):

		if not val:
			return theta
			
		# Substitutes variable {has(x), has(john) {x/John}}
		q = self.sub_str( theta, self.first_Quotient(val))
		
		# To detect infinite loops
		for item in Backward_Chain.stack:
			if item == q:
				if Backward_Chain.stack.count(item) > 2:
					return Backward_Chain.answers
		
		Backward_Chain.stack.append(q)
		
		for i in range(0,len(Backward_Chain.RHS_VALUES_NEW)):
			index = q.index("(")
			qindex = Backward_Chain.RHS_VALUES[i].index("(")
			
			if Backward_Chain.RHS_VALUES[i][0:qindex] == q[0:index]:
				yo = self.unify(q,Backward_Chain.RHS_VALUES_NEW[i],"")
				if yo != "Failure":

					new_goals = Backward_Chain.LHS_VALUES_NEW[i] + "^" + self.rest_Quotient(val)

					if new_goals[len(new_goals)-1] == '^':
						new_goals = new_goals[0:len(new_goals)-1]
					
					elif new_goals[0] == "^":
						new_goals = new_goals[1:len(new_goals)]
						
					new_goals = new_goals.lstrip()
					Backward_Chain.answers = Backward_Chain.answers + self.ask_backward_chain(new_goals,self.compose(yo,theta))
		# contains the substitution list, retuns "" if Query can't be proved
		return Backward_Chain.answers
		
	# Splits the the compound statement like " p1^p2^p3 " and return p1 
	def first_Quotient(self, val):
		part = val.split('^');
		return part[0]
	
	# Splits the the compound statement like " p1^p2^p3 " and return p2^p3
	def rest_Quotient(self,val):
		parts = val.split("^")
		contents = ""
		if(len(parts) == 1):
			return ""
		else:
			for i in range(1, len(parts)):
				contents += parts[i] + "^"
		return contents[0:int(len(contents)-1)]
	
	# Appends new substitution
	def compose(self, q, theta):
		new_string = ""
		if not theta:
			new_string = q
		elif not q:
			new_string = theta
		else:
			new_string = q + "," + theta
		return new_string
	
	# Return the number of the arguments
	def checkargs(self, z):
		val = z.split(",")
		return len(val)
	
	# Apply substitition {Has(x),Has(john) -- {x/John}}
	# {theta : x/john} returns Has(john) if Has(x) is passed
	def sub_str(self,theta,concl):
		start_index = concl.index('(')
		last_index = concl.index(')')
		result = concl[start_index+1:last_index]
		params = result.split(',')
		part = theta.split(',')
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
	
	# Unification Algorithm
	def unify(self,x,y,theta):
		
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
	
	# Formation of Overall Substitution list
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
	
	# Checks to see if a particular substitution is part of overall Substitution list{theta}
	# Example: Particular Substitution {x/okay}, Overall Substitution {theta = "x/Hello,y/Hi,z/Okay"} retuns False  
	def belongs(self,x,val,theta):
		part = theta.split(',')
		y =  x + "/" + val
		for l in part:
			if y in l:
				return True
		return False
	
	# Finds the substitution value for a particular variable if not found returns ""
	# Example: theta = "x/Hello,y/Hi,z/Okay", if we are looking for substitution value of z, it returns "Okay"
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
	
	# Returns the argument list array except first argument 
	def rest(self, x):
		parts = x.split(",")
		contents = ""
		for i in range(1, len(parts)):
			contents += parts[i] + ","
		return contents[0:int(len(contents)-1)]
	
	# Check if variable is of alphanumeric type		
	def variable1(self,x):
		if x.isalnum() and x.islower():
			return True
		return False
	
	# Check if variable is just a single lowercase character of length 1.
	def variable(self,x):
		if( x.isalpha() and x.islower() and len(x) == 1):
			return True
		return False
	
	# Check for compound statement 
	def compound(self,x):
		if '(' in x and len(x) > 1 :
			return True;
		return False
	
	# Returns the name of the predicate 
	def ops(self,x):
		return x.rpartition('(')[0]
	
	# Return the arguments
	def args(self,x):
		return x[x.index("(")+1:x.index(')')]
	
	# Check to see if it is a argument list
	def list(self,x):
		if ',' in x:
			if '(' not in x:
				return True
		return False
	
	# Returns the first argument
	def first(self,x):
		parts = x.split(',')
		return parts[0]

#Main Function
def main():
	c = Backward_Chain()
	c.readFile()
	file = open("output.txt", "w")
	c.backward_chain(file)
	
if __name__ == "__main__":
	main()
#-----END-----#
