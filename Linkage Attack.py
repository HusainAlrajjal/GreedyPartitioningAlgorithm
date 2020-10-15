# ***
# This is a Python Implemenetation of Applying Linkage Attack
# Implemented by Hussain Alrajjal for COE526 - HW1
# ID: 201550190     KFUPM
#
#
# TO START USING, GO TO main() AT THE END OF THE CODE
#
#
# ***


# Conducting Attack and save the result in a txt file in the source folder
def linkage_attack(dataset, name, supplied_set):
    # Conducting Attack
    linkage_attack_result = list()
    for i in supplied_set:
        for j in dataset:
            # print(i[1], j[0], i[2], j[1], i[3], j[4])
            if i[1] == j[0] and i[2] == j[1] and i[3] == j[4]:
                linkage_attack_result.append([i[0]] + j)
    print("Conducted>>>>", end="")

    # Save the result in a txt file in the source folder
    with open("Linkage Attack Result on (" + name + ") file.txt", "w") as output:
        for k in linkage_attack_result:
            for p in k:
                output.write(p + "\t")
            output.write("\n")
    print("Saveed>>>> ", end="")
    print("Linkage Attack Result on (" + name + ") file.txt")

    return linkage_attack_result


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
            dataset[i][j] = dataset[i][j]

    file1.close()
    return dataset


def main():
    # enter the name of the numerical dataset in address variable
    # NOTE: It has to be in the source folder, otherwise enter the full path
    address = "ipums.txt"
    # (Change the name if using the full path)
    name = address.split(".")[0]

    dataset = import_dataset(address)

    # the file used in the attack
    supplied_set = import_dataset("supplied_text.txt")

    # Conducting Attack and save the result in a txt file in the source folder
    result = linkage_attack(dataset, name, supplied_set)


if __name__ == '__main__':
    main()
