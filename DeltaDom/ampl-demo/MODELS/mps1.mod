# AMPL model for an MPS file: this one preserves row order.
# Use the awk script "m2a" to turn an MPS file into suitable data.

set Aij dimen 2;		#constraint matrix indices
set I1;				# to allow empty rows
set J := setof{(i,j) in Aij} j;	#columns
param A{Aij};			#constraint matrix nonzeros

param b{I1} default 0;		#right-hand side
param db{I1};			#for ranges

set ctypes := {'N', 'L', 'E', 'G', 'LR', 'GR'};

param ctype{I1} symbolic within ctypes;

param lb{J} default 0;
param ub{J} default Infinity;

var x{j in J}	>= if lb[j] <= -1.7e38 then -Infinity else lb[j]
		<= ub[j];

set zork := setof{i in I1} (i,ctype[i]);

c{i in I1: ctype[i] != 'N'}:

	(if ctype[i] == 'N' || ctype[i] == 'L' then -Infinity
		else if ctype[i] == 'G' || ctype[i] == 'GR'
			|| ctype[i] == 'E' then b[i]
		else b[i] - db[i])

	<= sum{(i,j) in Aij} A[i,j]*x[j] <=

	(if ctype[i] == 'N' || ctype[i] == 'G' then Infinity
		else if ctype[i] == 'L' || ctype[i] == 'LR'
			|| ctype[i] == 'E' then b[i]
		else b[i] + db[i]);

minimize Obj{(i,'N') in zork}:  sum{(i,j) in Aij} A[i,j]*x[j];
