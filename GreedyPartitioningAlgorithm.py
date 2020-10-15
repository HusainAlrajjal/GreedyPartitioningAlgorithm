# ***
# This is a Python Implemenetation of Greedy Partitioning Algorithm
# Implemented by Hussain Alrajjal for COE526 - HW1
# ID: 201550190     KFUPM
#
#
# TO START USING, GO TO main() AT THE END OF THE CODE
#
#
# ***


# Calculate Frequency set of (a) list in dimension (dim)
def frequency_set(a, dim):
    fs = list()
    a.sort(key=lambda x: x[dim])
    count = 0
    value = a[0][dim]
    for i in a:
        if value == i[dim]:
            count += 1
        else:
            fs.append([value, count])
            value = i[dim]
            count = 1
    fs.append([value, count])
    fs.append(['TOTAL', len(a)])

    return fs, a


# to find the best dimension to start partitionin with and find MAX and MIN values in each column
def analyze_dataset_columns(dataset):
    col_count = len(dataset[0])
    analysis = list()

    # -1 means except the last attribute (assumption: it is sensitive attribute)
    for i in range(col_count - 1):
        dataset.sort(key=lambda x: int(x[i]))
        analysis.append([i, dataset[0][i], dataset[-1][i], int(dataset[-1][i]) - int(dataset[0][i])])
    analysis.sort(key=lambda x: int(x[-1]), reverse=True)

    # the order of choosing the next dimension to split
    spliting_order = list()
    for j in analysis:
        spliting_order.append(j[0])

    return analysis, spliting_order


# find median and provide list of upper and lower records
def find_median(f_s):
    mid = f_s[-1][1] / 2
    trace = 0
    lower_partition = list()
    upper_partition = list()
    for i in f_s[:-1]:
        if trace >= mid:
            upper_partition.append(i)
        else:
            lower_partition.append(i)
        trace += i[1]
    return lower_partition, upper_partition


# read datset from a txt file
def import_dataset(address):
    dataset = list()
    file1 = open(address, "r")
    content = file1.read()
    records = content.split("\n")
    for i in records:
        dataset.append(i.split("\t"))

    for i in range(len(dataset)):
        for j in range(len(dataset[i])):
            dataset[i][j] = int(dataset[i][j])

    file1.close()
    return dataset


#  Find MAX and MIN in col of a list
def max_min(list0, col):
    max_value = max([sublist[col] for sublist in list0])
    min_value = min([sublist[col] for sublist in list0])

    return max_value, min_value


# partition a partition based on values list provided
def partition_partition(partition, dimension, based_on_values_list):
    new_partition = list()
    for i in partition:
        for j in based_on_values_list:
            if i[dimension] == j[0]:
                new_partition.append(i)
    return new_partition


# Write the values as ranges
def summarize_ECs(ECs):
    all_summarized_ECs = list()
    summarized_EC = list()
    max_min_list = list()

    fs, kill = frequency_set(ECs, 0)
    for j in fs:
        for i in ECs:
            if i[0] == j[0]:
                summarized_EC.append(i)
        if len(summarized_EC) > 0:
            for i in range(1, len(summarized_EC[0]) - 1):
                x = max_min(summarized_EC, i)
                max_min_list.append([x[1], x[0]])
            for i in summarized_EC:
                for k in range(1, len(summarized_EC[0]) - 1):
                    i[k] = max_min_list[k - 1]
                all_summarized_ECs.append(i)
            max_min_list.clear()
            summarized_EC.clear()

    return all_summarized_ECs, fs


# Find CDM, I_loss, Utility, and Freq_Set of ECs
def stats(ECs, fs, analysis):
    # Find CDM
    CDM = 0
    for i in fs[:-1]:
        CDM += i[1] ** 2
    I_loss = 0
    T = fs[-1][1]
    n = len(ECs[0]) - 2
    I_loss = 1 / (T * n)

    # find I_loss
    analysis.sort()
    # analysis = analysis[:-1]
    sum = 0
    for i in range(n):
        for j in range(T):
            record_limit = ECs[j][i + 1][1] - ECs[j][i + 1][0]
            attribute_limit = analysis[i][2] - analysis[i][1]
            if record_limit > 0:
                sum += record_limit / attribute_limit
    I_loss *= sum
    I_loss = round(I_loss, 4)

    # find Utility
    Utility = 1 - I_loss

    return CDM, I_loss, Utility, fs


def l_diversity(name, ECs, l_value, k):
    # Checking violating l-diversity
    fs, kill = frequency_set(ECs, 0)
    violating_ECs = list()
    test_l_diversity_Class = list()
    for j in fs[:-1]:
        for i in ECs:
            if i[0] == j[0]:
                test_l_diversity_Class.append(i)
        EC_sensitive_value_frequncey_set, kill = frequency_set(test_l_diversity_Class, -1)

        if l_value > len(EC_sensitive_value_frequncey_set) - 1:
            for i in test_l_diversity_Class:
                violating_ECs.append(i)
        test_l_diversity_Class.clear()
    print(str(l_value) + "-diversity checked>>>> ", end="")
    with open("violating " + str(l_value) + "-diveristy ECs -" + name + "-k(" + str(k) + ").txt", "w") as output:
        output.write("***** " + str(k) + "-anonymised dataset and non-" + str(l_value) + "-diveristy ECs *****\n")
        for kq in violating_ECs:
            for p in kq:
                output.write(str(p) + "\t")
            output.write("\n")
    print("Saveed>>>> ", end="")
    print("violating " + str(l_value) + "-diveristy ECs -" + name + "-k(" + str(k) + ").txt")
    return violating_ECs


def anonymize(name, raw_dataset, k=2):
    # possible partitions to partition.
    partitions_stack = list()

    # the Equivalence Classes
    ECs = list()

    # to find the best dimension to start partitionin with and find MAX and MIN values in each column
    analysis = analyze_dataset_columns(raw_dataset)
    dim_order = analysis[1]

    raw_dataset.sort(key=lambda x: int(x[dim_order[0]]))
    partitions_stack.append(raw_dataset)

    ECs_count = 1
    index = 0

    # As long as the stack contains something we gonna partition it.
    while len(partitions_stack) > 0:

        # choose the dimension
        dim = dim_order[index]

        # take the recent partition inside the stack
        partition = partitions_stack.pop()

        # Do Greedy algorithm
        fs = frequency_set(partition, dim)[0]
        lower_partition, upper_partition = find_median(fs)

        # find how many records we gonna have if we split
        upper_partition_count = 0
        lower_partition_count = 0
        for i in upper_partition:
            upper_partition_count += i[1]
        for i in lower_partition:
            lower_partition_count += i[1]

        if lower_partition_count >= k and upper_partition_count >= k:
            # the partition might be partitioned again
            partitions_stack.append(partition_partition(partition, dim, upper_partition))
            partitions_stack.append(partition_partition(partition, dim, lower_partition))
            index = 0
        elif dim == dim_order[-1]:
            # when you try all possible dimension and reach the last one but still doesnt work .
            # this mean this is a new EC
            for p in partition:
                ECs.append(["EC#" + str(ECs_count)] + p)
            ECs_count += 1
            index = 0
        else:
            # to try another dimension
            partitions_stack.append(partition)
            index += 1

    # Summirze the ECs with ranges
    ECs, freq_set = summarize_ECs(ECs)

    # Find CDM, I_loss, Utility, and Freq_Set of ECs
    statisics = stats(ECs, freq_set, analysis[0])
    print("Anonymized>>>> ", end="")
    # this section of code will save the k-anonymised dataset in a txt file including stats
    with open("anonymized_result-" + name + "-k(" + str(k) + ").txt", "w") as output:
        output.write("***** " + "anonymised result of (" + name + ") *****\n")
        output.write("***** " + str(k) + "-anonymised dataset  *****\n")
        for kq in ECs:
            for p in kq:
                output.write(str(p) + "\t")
            output.write("\n")
        output.write("\n***** Equivalence Classes Statistics *****\n")
        for kw in statisics[3]:
            for p in kw:
                output.write(str(p) + "\t")
            output.write("\n")
        output.write("CDM = " + str(statisics[0]) + "\n")
        output.write("I_Loss = " + str(statisics[1]) + " or %" + str(statisics[1] * 100) + "\n")
        output.write("Utility = " + str(statisics[2]) + " or %" + str(statisics[2] * 100) + "\n")
    print("Saveed>>>> ", end="")
    print("anonymized_result-" + name + "-k(" + str(k) + ").txt")
    return ECs


def main():
    # enter the name of the numerical dataset in address variable
    # NOTE: It has to be in the source folder, otherwise enter the full path
    address = "class_ex.txt"
    # (Change the name if using the full path)
    name = address.split(".")[0]

    dataset = import_dataset(address)
    k = 2
    # In the source folder, you will find the a txt file with the dataset anonymised.
    Equivalence_Classes = anonymize(name, dataset, k=k)

    for l in [2]:
        l_diversity(name, Equivalence_Classes, l, k)


if __name__ == '__main__':
    main()
