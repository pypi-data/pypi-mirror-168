# Refactoring non-idiomatic Python code with Python idioms


## Install:
For command line use, the package is installed with 

    python3 -m pip install RefactoringIdioms

 ## Running:
1).  Default command is to get <non-idiomatic code, idiomatic code> pairs for all Python files in the current directory for all Python idioms, and the result is saved in result.json in the current directory: 
	
     RIdiom

2).  To get <non-idiomatic code, idiomatic code> pairs for a Python idiom for a given file/given directory and save the result in the given path, you can execute the following command: 
	
    RIdiom --filepath "your filepath" (e.g., main.py) --idiom "IdiomName" (e.g., List Comprehension) --outputpath "your outputpath" (e.g., result.json)

## Web application: 
We also develop a web application for the code refactoring, you could access the application through the url: 47.242.131.128:5000
	
Each time, you could click code area to refresh.
	