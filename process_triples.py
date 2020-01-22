import random
import os
import sys, getopt

def generate_constraint_files(dir_path):
    lef = {}
    rig = {}
    rellef = {}
    relrig = {}

    triple = open( dir_path+"/train2id.txt", "r")
    valid = open(dir_path+"/valid2id.txt", "r")
    test = open(dir_path+"/test2id.txt", "r")

    tot = (int)(triple.readline())
    for i in range(tot):
        content = triple.readline()
        h, t, r = content.strip().split()
        if not (h, r) in lef:
            lef[(h, r)] = []
        if not (r, t) in rig:
            rig[(r, t)] = []
        lef[(h, r)].append(t)
        rig[(r, t)].append(h)
        if not r in rellef:
            rellef[r] = {}
        if not r in relrig:
            relrig[r] = {}
        rellef[r][h] = 1
        relrig[r][t] = 1

    tot = (int)(valid.readline())
    for i in range(tot):
        content = valid.readline()
        h, t, r = content.strip().split()
        if not (h, r) in lef:
            lef[(h, r)] = []
        if not (r, t) in rig:
            rig[(r, t)] = []
        lef[(h, r)].append(t)
        rig[(r, t)].append(h)
        if not r in rellef:
            rellef[r] = {}
        if not r in relrig:
            relrig[r] = {}
        rellef[r][h] = 1
        relrig[r][t] = 1

    tot = (int)(test.readline())
    for i in range(tot):
        content = test.readline()
        h, t, r = content.strip().split()
        if not (h, r) in lef:
            lef[(h, r)] = []
        if not (r, t) in rig:
            rig[(r, t)] = []
        lef[(h, r)].append(t)
        rig[(r, t)].append(h)
        if not r in rellef:
            rellef[r] = {}
        if not r in relrig:
            relrig[r] = {}
        rellef[r][h] = 1
        relrig[r][t] = 1

    test.close()
    valid.close()
    triple.close()

    f = open(dir_path+"/type_constrain.txt", "w")
    f.write("%d\n" % (len(rellef)))
    for i in rellef:
        f.write("%s\t%d" % (i, len(rellef[i])))
        for j in rellef[i]:
            f.write("\t%s" % (j))
        f.write("\n")
        f.write("%s\t%d" % (i, len(relrig[i])))
        for j in relrig[i]:
            f.write("\t%s" % (j))
        f.write("\n")
    f.close()

    rellef = {}
    totlef = {}
    relrig = {}
    totrig = {}
    # lef: (h, r)
    # rig: (r, t)
    for i in lef:
        if not i[1] in rellef:
            rellef[i[1]] = 0
            totlef[i[1]] = 0
        rellef[i[1]] += len(lef[i])
        totlef[i[1]] += 1.0

    for i in rig:
        if not i[0] in relrig:
            relrig[i[0]] = 0
            totrig[i[0]] = 0
        relrig[i[0]] += len(rig[i])
        totrig[i[0]] += 1.0

    s11 = 0
    s1n = 0
    sn1 = 0
    snn = 0
    f = open(dir_path+"/test2id.txt", "r")
    tot = (int)(f.readline())
    for i in range(tot):
        content = f.readline()
        h, t, r = content.strip().split()
        rign = rellef[r] / totlef[r]
        lefn = relrig[r] / totrig[r]
        if (rign < 1.5 and lefn < 1.5):
            s11 += 1
        if (rign >= 1.5 and lefn < 1.5):
            s1n += 1
        if (rign < 1.5 and lefn >= 1.5):
            sn1 += 1
        if (rign >= 1.5 and lefn >= 1.5):
            snn += 1
    f.close()

    f = open(dir_path+"/test2id.txt", "r")
    f11 = open(dir_path+"/1-1.txt", "w")
    f1n = open(dir_path+"/1-n.txt", "w")
    fn1 = open(dir_path+"/n-1.txt", "w")
    fnn = open(dir_path+"/n-n.txt", "w")
    fall = open(dir_path+"/test2id_all.txt", "w")
    tot = (int)(f.readline())
    fall.write("%d\n" % (tot))
    f11.write("%d\n" % (s11))
    f1n.write("%d\n" % (s1n))
    fn1.write("%d\n" % (sn1))
    fnn.write("%d\n" % (snn))
    for i in range(tot):
        content = f.readline()
        h, t, r = content.strip().split()
        rign = rellef[r] / totlef[r]
        lefn = relrig[r] / totrig[r]
        if (rign < 1.5 and lefn < 1.5):
            f11.write(content)
            fall.write("0" + "\t" + content)
        if (rign >= 1.5 and lefn < 1.5):
            f1n.write(content)
            fall.write("1" + "\t" + content)
        if (rign < 1.5 and lefn >= 1.5):
            fn1.write(content)
            fall.write("2" + "\t" + content)
        if (rign >= 1.5 and lefn >= 1.5):
            fnn.write(content)
            fall.write("3" + "\t" + content)
    fall.close()
    f.close()
    f11.close()
    f1n.close()
    fn1.close()
    fnn.close()

def process(line, entity2id: dict, relation2id: dict):
    tokens = line.split(" ")
    entity1 = tokens[0]
    relation = tokens[1]
    entity2 = tokens[2]

    if entity1 not in entity2id:
        entity2id[entity1] = entity2id.__len__()
    if entity2 not in entity2id:
        entity2id[entity2] = entity2id.__len__()
    if relation not in relation2id:
        relation2id[relation] = relation2id.__len__()

    training_point = str(entity2id[entity1]) + "\t" +str(entity2id[entity2] ) +"\t" +str(relation2id[relation] ) +"\n"
    return training_point, entity2id, relation2id


def save_dict_to_file(input_dict: dict, file_path):
    output_str = str(input_dict.__len__() ) +"\n"

    for k in input_dict.keys():
        output_str += str(k ) +"\t " +str(input_dict[k] ) +"\n"

    f = open(file_path ,'w')
    f.write(output_str)
    f.close()

def save_list_to_file(input_list: list, file_path):
    f = open(file_path, 'w')
    f.write(str(input_list.__len__() ) +"\n")
    f.writelines(input_list)
    f.close()


def main(file_path):
    triples = list()
    dir_path = os.path.dirname(os.path.realpath(file_path))
    relation2id = dict()
    entity2id = dict()
    bufsize = 65536
    with open(file_path) as infile:
        while True:
            lines = infile.readlines(bufsize)
            if not lines:
                break
            for line in lines:
                triple, entity2id, relation2id = process(line, entity2id, relation2id)
                triples.append(triple)
                if triples.__len__() % 10000000 == 0:
                    print("Processed #lines: ", str(triples.__len__()))

    total_size = triples.__len__()
    random.shuffle(triples)
    validation_size = min(int(total_size * 0.01), 1000)
    validation_points = triples[0: validation_size]
    test_points = triples[validation_size: validation_size*2]
    training_points = triples[validation_size*2:]
    print("saving entity2id to the file")
    save_dict_to_file(entity2id, dir_path+"/entity2id.txt")
    print("saving relation2id to the file")
    save_dict_to_file(relation2id, dir_path+"/relation2id.txt")
    print("saving train2id to the file")
    save_list_to_file(training_points, dir_path+"/train2id.txt")
    print("saving valid2id to the file")
    save_list_to_file(validation_points,dir_path+"/valid2id.txt")
    print("saving test2id to the file")
    save_list_to_file(test_points, dir_path+"/test2id.txt")

    print("Generating constraint files...")
    generate_constraint_files(dir_path)

if __name__ == "__main__":
    argv = (sys.argv[1:])
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print('process_triples.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('process_triples.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg

    if input_file != '':
        print('Processing with the input file: ', input_file)
        main(input_file)
    else:
        print('Usage: process_triples.py -i <inputfile>')

