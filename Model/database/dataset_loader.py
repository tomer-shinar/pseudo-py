class DatasetLoader:
    """
    class that loads the dataset and returns it.
    later will be replace with more complicated database
    """
    def load(self, input_file="database/generic-pseudo.txt", output_file="database/generic-python.txt"):
        dataset = []
        print(input_file)
        f1 = open(input_file, "r")
        f2 = open(output_file, "r")
        l1 = f1.readline()
        l2 = f2.readline()
        while l1 and l2:
            dataset.append((l1.split(), l2.split()))
            l1 = f1.readline()
            l2 = f2.readline()
        f1.close()
        f2.close()
        return dataset


