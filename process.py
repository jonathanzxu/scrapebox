import json
import time

#arithmetic mean helper function
def mean(arr):
    sum = 0
    for x in arr:
        sum += x
    return sum / len(arr)

#formatting helper function
'''
example input: ("topic1", {
    "question1": {...},
    "question2": {...},
    "question3": {...},
    ...
})

example output: {
    "name": "topic1",
    "children": [
        {
            "name": "question1",
            "children": [...]
        },
        {
            "name": "question2",
            "children": [...]
        },
        {
            "name": "question3",
            "children": [...]
        }
    ]
}
'''
def format(name, obj):
    #base case for when we reach the end of the tree
    if type(obj) is float:
        return {
            "name": name if name is not None else "Overall",
            "children":[{
                "name": "mean: " + str(obj) + "%",
                "children": []
            }]
        }
    #general case
    children = []
    for x in obj:
        children.append(format(x, obj[x]))
    return {
        "name": name,
        "children": children
    }

mark = time.time()

print(f'Opening alzheimers.json...')

with open('alzheimers.json', 'r') as alzheimers:
    alzheimers_file = json.load(alzheimers)
    alzheimers_data = alzheimers_file["data"]
    # print(alzheimers_data[2][3])

print(f'Opened alzheimers.json in {time.time() - mark} seconds.')
mark = time.time()
print(f'Generating tree...')

# tree-like data structure to classify datapoints based on class -> topic -> question -> strat1 -> strat2
tree = {}
for row in alzheimers_data:
    '''
    ------Guide for this dataset------
    row[14]: Class
    row[15]: Topic
    row[19]: Data Type Code ('PRCTG')
    row[21]: Data Value
    row[29]: Stratification 1
    row[31]: Stratification 2
    '''
    #filter for only the percentage data points (the majority of data points are percentages)
    if not row[19] == 'PRCTG':
        continue
    #ensure data value can be parsed into a float
    try:
        row[21] = float(row[21])
    except:
        continue
    
    
    #create tree node if not already existing
    if tree.get(row[14]) == None:
        tree.setdefault(row[14], {})
    if tree.get(row[14]).get(row[15]) == None:
        tree.get(row[14]).setdefault(row[15], {})
    if tree.get(row[14]).get(row[15]).get(row[29]) == None:
        tree.get(row[14]).get(row[15]).setdefault(row[29], {})
    if tree.get(row[14]).get(row[15]).get(row[29]).get(row[31]) == None:
        tree.get(row[14]).get(row[15]).get(row[29]).setdefault(row[31], [])
    
    #add value to node's array
    tree.get(row[14]).get(row[15]).get(row[29]).get(row[31]).append(row[21])

print(f'Generated tree in {time.time() - mark} seconds.')

mark = time.time()
print(f'Condensing arrays...')

#condense node's array into one number (arithmetic mean for now)
for _class in tree.values():
    for topic in _class.values():
        for strat_1 in topic.values():
            for strat_2 in strat_1:
                strat_1[strat_2] = mean(strat_1[strat_2])
                #print(strat_1[strat_2])

print(f'Condensed arrays in {time.time() - mark} seconds.')
mark = time.time()
print(f'Formatting tree...')

#format into observable journal's format:
'''
data = {
        name: 'foo'
        children: [
            {
                name: 'bar'
                children: [
                    {...}
                ]
            },
            {
                name: 'baz'
                children: [...]
            }
        ]
    }
'''
#create new dictionary for output into json
#some recursion is the easiest way to do this
data = format('Alzheimer\'s Disease', tree)

print(f'Formatted tree in {time.time() - mark} seconds.')
mark = time.time()
print(f'Writing to output.json...')

with open('output.json', 'w') as outfile:
    json.dump(data, outfile)

print(f'Finished in {time.time() - mark} seconds.')
print(f'Exiting program.')


