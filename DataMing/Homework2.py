raw_data = open('iris.data.txt')
line = raw_data.readline()
dataset = []
# iris label map
iris_map = {
    'Iris-setosa': 1,
    'Iris-versicolor': 2,
    'Iris-virginica': 3
}
while line:
    if line == ' ' or '':
        break
    line_data = line.strip('\n').split(',')
    new_record = []
    # add the third data(petal_length) into new dataset
    new_record.append(float(line_data[2]))
    # add label as 1,2,3 for setosa, versicolor and virginica
    new_record.append(iris_map[line_data[-1]])
    dataset.append(new_record)
    line = raw_data.readline()

#print dataset

concept_data = open('concept hierarchy.txt')
line = concept_data.readline()
concept_dataset = []
while line:
    line_data = line.strip('\n').split(',')
    new_record = []
    new_record.append(line_data[0])
    new_record.append(line_data[1])
    new_record.append(line_data[2])
    concept_dataset.append(new_record)
    line = concept_data.readline()

autodata = open('automobile.txt')
line = autodata.readline()
autodataset = []
while line:
    line_data = line.strip('\n').split(',')
    new_record = []
    new_record.append(line_data[2])
    new_record.append(line_data[3])
    new_record.append(line_data[6])
    autodataset.append(new_record)
    line = autodata.readline()


def distinctValueSplit(dataset):
    country = []
    state = []
    city = []
    for data in dataset:
        country.append(data[0])
        state.append(data[1])
        city.append(data[2])
    distinct_dict = {}

    distinct_dict['Country'] = len(set(country))
    distinct_dict['State'] = len(set(state))
    distinct_dict['City'] = len(set(city))
    sorted_list = sorted(distinct_dict.items(), key=lambda item:item[1])
    return sorted_list


def equalWidthSplit(dataset, partition):
    dataset = sorted(dataset,key=lambda data: data[0]) # sort the dataset according to petal length
    width = (dataset[-1][0] - dataset[0][0])/partition
    layer_splited = []
    i = 0
    for part in range(partition):
        layer_splited.append([])
        while i < len(dataset):
            layer_splited[part].append(dataset[i])
            i += 1
            if i < 150:
                if dataset[i][0] > dataset[0][0]+width*(part+1):
                    break
    return layer_splited


def equalFrequencySplit(dataset, partition):
    dataset = sorted(dataset,key=lambda data: data[0]) # sort the dataset according to petal length
    frequency = len(dataset)/partition
    layer_splited = []
    i = 0
    for part in range(partition):
        layer_splited.append([])
        while i < len(dataset):
            layer_splited[part].append(dataset[i])
            i += 1
            if i == frequency * (part+1):
                break
    return layer_splited



# split by distinct values
distinctValue = distinctValueSplit(concept_dataset)
print distinctValue

# split by equal width, given the number of partitions
equalWidth = equalWidthSplit(dataset, 5)
print equalWidth

# split by equal frequency, given the number partitions
equalFrequency = equalFrequencySplit(dataset, 5)
print equalFrequency