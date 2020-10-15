# GreedyPartitioningAlgorithm
This is a Python code that apply K-anonymization using Greedy Partitioning Algorithm 


++++++++++++(GreedyPartitioningAlgorithm.py)++++++++++++:

Assumptions:
1- the dataset must be numerical dataset.
2- the dataset must have ONE sensetive attribute and it has to be the last column.
3- the dataset should be in (the source folder) and in .txt format.
4- the dataset must split between its record values using TAB space (or \t or 	).

Usage:
- open the source file(GreedyPartitioningAlgorithm.py) and go to the main().
- Enter the name of the txt file in (address variable).
- Choose the K value you want
- Run 
- in the same the source folder, the k-anonymized table will be stored in a file with this name structure:
	- anonymized_result-{dataset_name}-k({k_value}).txt
- the output file will include CDM, I_loss, Utility, and Frequncy_set of each EC.

- in the same the source folder, the table of non-l-divergentrec ECs will be stored in a file with this name structure:
	- violating {l_value}-diveristy ECs -{dataset_name}-k({k_value}).txt
- the output file will include ECs that violate l-diversity table.


