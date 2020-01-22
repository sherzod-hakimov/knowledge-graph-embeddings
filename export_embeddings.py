import getopt
import json
import sys

def load_dict(file_path):
    dictionary = dict()

    with open(file_path) as fp:
        while True:
            lines = fp.readlines()
            if not lines:
                break
            for line in lines:
                tokens = line.split("\t")
                if tokens.__len__() == 2:
                    key = int(tokens[1])
                    dictionary[key] = tokens[0]
    return dictionary

def save_embeddings(input_list: list, file_path, embedding_dim):
    f = open(file_path, 'w')
    f.write(str(input_list.__len__())+" "+str(embedding_dim)+"\n")
    f.writelines(input_list)
    f.close()

def process(file_path, relation2id, entity2id):
    entity_embeddings = list()
    relation_embeddings = list()
    category_embeddings = list()
    class_embeddings = list()

    with open(file_path) as json_file:
        data = json.load(json_file)
        entity_id = 0

        for embedding_vec in data['ent_embeddings.weight']:
            entity_uri = entity2id[entity_id]
            vec = ""
            for e in embedding_vec:
                vec += str(e)+" "
            vec = vec.strip()

            if entity_uri.startswith("<dbr:Category:") or entity_uri.startswith("<http://dbpedia.org/resource/Category:"):
                category_embeddings.append(entity_uri +" "+vec+"\n")
            elif entity_uri.startswith("<dbo:") or entity_uri.startswith("<http://dbpedia.org/ontology"):
                class_embeddings.append(entity_uri +" "+vec+"\n")
            else:
                entity_embeddings.append(entity_uri + " " + vec + "\n")

            entity_id += 1
        relation_id = 0
        for embedding_vec in data['rel_embeddings.weight']:
            relation_uri = relation2id[relation_id]
            vec = ""
            for e in embedding_vec:
                vec += str(e)+ " "
            vec = vec.strip()
            relation_embeddings.append(relation_uri +" "+vec+"\n")
            relation_id += 1
    return entity_embeddings, relation_embeddings, category_embeddings, class_embeddings

def export(config_data):
    print("Loading the dictionary")
    entity2id = load_dict(config_data["input_dir"] + "/entity2id.txt")
    relation2id = load_dict(config_data["input_dir"] + "/relation2id.txt")
    print("Extracting the embeddings")
    entity_embeddings, relation_embeddings, category_embeddings, class_embeddings = process(
        config_data["output_dir"] + "/TransE.json", relation2id, entity2id)
    print("Saving the embeddings ...")
    save_embeddings(entity_embeddings, config_data["output_dir"] + "/entity_embeddings.txt",
                    config_data["embedding_dimension"])
    save_embeddings(relation_embeddings, config_data["output_dir"] + "/relation_embeddings.txt",
                    config_data["embedding_dimension"])
    save_embeddings(category_embeddings, config_data["output_dir"] + "/category_embeddings.txt",
                    config_data["embedding_dimension"])
    save_embeddings(class_embeddings, config_data["output_dir"] + "/class_embeddings.txt",
                    config_data["embedding_dimension"])

if __name__ == "__main__":
    argv = (sys.argv[1:])
    config_path = ''
    try:
        opts, args = getopt.getopt(argv, "hc:o:")
    except getopt.GetoptError:
        print('export_embeddings.py -c <config_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('export_embeddings.py -c <config_path>')
            sys.exit()
        elif opt in ("-c"):
            config_path = arg

    if config_path != '':
        print('Exporting embeddings using the config: ', config_path)

        config_data = dict()
        with open(config_path) as json_file:
            config_data = json.load(json_file)

        if config_data.__len__() != 0:
            export(config_data)


    else:
        print('Usage: export_embeddings.py -c <config_path>')