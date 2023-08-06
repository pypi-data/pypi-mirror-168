import pandas    as pd

# =============================================================================
# LAMMPS Frame (Multiple Frames)
# =============================================================================
class LmpMultiFrame:   
	""" Create an Object of multi-FRAME of LAMMPS (use for XYZ files)
	This class implemented the ways to create `lmpFRAME` object <br>
		- read frome XYZ file 
	""" 
	def __init__(self, **kwargs):
		""" ** Optional Inputs: (3 ways to create FRAME)
				readXYZ: read input in format of "XYZ file"
		"""
		##==== optional Inputs 
		## read DumpFile
		if 'readXYZ' in kwargs:
			file_name = kwargs['readXYZ']
			self.readXYZ(file_name)
		elif 'readPDB' in kwargs:
			file_name = kwargs['readPDB']
			self.readPDB(file_name)	
		else: raise Exception('file format is unsupported')
		## some initial setting
		self.fmtSTR = "%.6f"    # dont use %g, because it will lost precision

		return
	#####=======
	

	def readXYZ(self, file_name):
		"""The **method** create Multi-FRAME object by reading XYZ file.
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of XYZ file 
		* Inputs-Optional: <br> 
		* Outputs: <br> 
			- .frame = ldf  |`list-DataFrame`| list-of-frames of configurations
		* Usage: <br> 
			da = thaFileType.lmpFRAME()
			da.readXYZ('dump.xyz')
		"""
		## Read whole text and break lines
		with open(file_name,'r') as fileID:
			C = fileID.read().splitlines()              # a list of strings

		## Extract positions of block
		P = [line.split(" ") for line in C]          # list-of-lists
		blockIndex=[i for i,line in enumerate(P) if len(line)==1 ]
		## Extract each block as frame
		ldf = [None]*(len(blockIndex))
		for i,item in enumerate(blockIndex):
			if i < (len(blockIndex)-1):
				data = P[blockIndex[i]+2 : blockIndex[i+1]]    # list-of-lists
			else: 
				data = P[blockIndex[i]+2 :] 

			## extract columns
			if i==0:
				myColumn = ['element','x','y','z']
				if len(data[0])>4:
					for k in range(4,len(data[0])):
						myColumn = myColumn + ['c'+str(k-3)]
			## Conert type on some columns of DataFrame
			df0 = pd.DataFrame(data, columns=myColumn)  # create DataFrame
			df1 = df0.drop('element',axis=1).astype(float)
			df = pd.concat([df0['element'],df1], axis=1)
			ldf[i] = df

		## Save out put to CLASS's attributes
		self.name      = file_name
		self.frame     = ldf           # List of DataFrame
		return
	#####=======

