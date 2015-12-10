# Introduction:
As mobiles, wearables and other tiny gadgets surround us more and more in our day to day life, we are sharing more and more information with enterprises that provide us with their services. But what do we lose in return? How much control do we have on over our private information? These question seem simple to answer at the first glance. You share what you want to share. But, it’s not like that with the use of AI methods that can mine your shared data to infer your private non-shared personal information. In this assignment, we want to help users to find out what an enterprise can do with their data before giving permission to their applications to access that.
We are going to implement a backward chaining system that gets the rules of data-mining and the abilities that an enterprise has at its disposal. Then it will help customers to find out if a certain type of personal information can be extracted by that enterprise if it gains access to another set of information about the user.

### Problem:
Given a knowledge base and a number of queries. Job is to determine if the queries can be inferred from the knowledge base or not, used backward chaining algorithm to solve this problem

### Input Format: 
Given an input file. Read the input file name from the command line.The first line of the input will be the number of queries [(n)]. Following n lines will be the queries, one per line. For each of them, need todetermine whether it can be proved form the knowledge base or not. Next line of the input will contain the number of clauses in the knowledge base (m).

Following, there will be m lines each containing a statement in the knowledge base. Each clause is in one of these two formats:
1- p1 ∧ p2 ∧ ... ∧ pn => q
2- facts: which are atomic sentences. Such as p or ~p


* All the p s and also q are either a literal such as HasPermission(Google,Contacts) or negative of a literal such as ~HasPermission(Google,Contacts).
* Queries will not contain any variables.
* Variables are all single lowercase letters.
* All predicates (such as HasPermission) and constants (such as Google) are case-sensitive alphabetical strings that begin with uppercase letters.
* Each predicate has at least one argument. (There is no upper bound for the number of arguments). Same predicate will not appear with different number of arguments.
* All of the arguments of the facts are constants. i.e. you can assume that there will be no fact such as HasPermission(x,Contacts) ( which says that everyone has permission to see the contacts!) in the knowledge base.

### Output Format:
Develop code in a file called “inference.py”. Output the results into a file ‘output.txt’. For each query, determine if that query can be inferred from the knowledge base or not, one query per line. If true, print “TRUE” and if not, print “FALSE”. (without the double quotes)
