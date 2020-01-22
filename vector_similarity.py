import json
import getopt
import sys
import gensim

def load_model(model_path):
    try:
        model = gensim.models.KeyedVectors.load_word2vec_format(model_path)
        return model
    except:
        print("Error occured!")

def most_similar(model, uri):
    try:
        print(str(model.most_similar(positive=[uri]))+"\n")
    except:
        print("Error occured")

def most_similar_analogy(model, positives: list(), negatives: list()):
    try:
        print(str(model.most_similar(positive=positives, negative=negatives)) +"\n")
    except:
        print("Error occured")

def is_class(uri):
    if uri.startswith("<dbo:") or uri.startswith("<http://dbpedia.org/ontology/"):
        first_character = uri.replace("<dbo:", "").replace("<http://dbpedia.org/ontology/", "")[0:1]
        if first_character.isupper():
            return True
    return False

def is_relation(uri):
    if uri.startswith("<dbo:") or uri.startswith("<http://dbpedia.org/ontology/"):
        first_character = uri.replace("<dbo:", "").replace("<http://dbpedia.org/ontology/", "")[0:1]
        if first_character.islower():
            return True
    elif uri.startswith("<http://www.wikidata.org/entity/P"):
        return True
    return False

def is_category(uri):
    if uri.startswith("<dbr:Category") or uri.startswith("<http://dbpedia.org/resource/Category"):
        return True
    return False

def is_resource(uri):
    if uri.startswith("<dbr:") or uri.startswith("<http://dbpedia.org/resource/") or uri.startswith(
        "<http://www.wikidata.org/entity/Q"):
        return True
    return False

if __name__ == "__main__":
    argv = (sys.argv[1:])
    config_path = ''
    try:
        opts, args = getopt.getopt(argv, "hc:o:")
    except getopt.GetoptError:
        print('vector_similarity.py -c <config_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('vector_similarity.py -c <config_path>')
            sys.exit()
        elif opt in ("-c"):
            config_path = arg

    if config_path != '':
        print('Loading embeddings using the config: ', config_path)

        config_data = dict()
        with open(config_path) as json_file:
            config_data = json.load(json_file)

        if config_data.__len__() != 0:

            print("Loading category embeddings")
            category_model = load_model(config_data["output_dir"] + "/category_embeddings.txt")

            print("Loading class embeddings")
            class_model = load_model(config_data["output_dir"] + "/class_embeddings.txt")

            print("Loading relation embeddings")
            relation_model = load_model(config_data["output_dir"] + "/relation_embeddings.txt")

            print("Loading entity embeddings")
            entity_model = load_model(config_data["output_dir"]+ "/entity_embeddings.txt")



            while True:
                print("\nChoose a number:\n1) Most similar \n2) Analogy calculation\n")
                type = input()

                if type in ["stop", "exit"]:
                    break

                if type =="1":
                    print("\nWrite your URI:\n")
                    uri = input()
                    print("\n\nMost similar ones:\n")

                    if (is_category(uri)):
                        most_similar(category_model, uri)
                    elif (is_resource(uri)):
                        most_similar(entity_model, uri)
                    elif (is_relation(uri)):
                        most_similar(relation_model, uri)
                    elif (is_class(uri)):
                        most_similar(class_model, uri)
                    else:
                        print("Try another uri, e.g. <dbr:Aristotle>  <dbo:birthPlace>  <dbo:City>  <dbr:Category:City>")

                elif type == "2":
                    exists = False
                    positive_1 = ''
                    positive_2 = ''
                    negative_1 = ''
                    expected = ''
                    print("\nFirst positive:\n")
                    positive_1 = input()
                    print("\nSecond positive:\n")
                    positive_2 = input()
                    print("\nNegative:\n")
                    negative_1 = input()

                    print("\n\nResult:\n")

                    if (is_category(positive_1)):
                        most_similar_analogy(category_model, [positive_1, positive_2], [negative_1])
                    elif (is_resource(positive_1)):
                        most_similar_analogy(entity_model, [positive_1, positive_2], [negative_1])
                    elif (is_relation(positive_1)):
                        most_similar_analogy(relation_model, [positive_1, positive_2], [negative_1])
                    elif (is_class(positive_1)):
                        most_similar_analogy(class_model, [positive_1, positive_2], [negative_1])
                    else:
                        print("Try URIs from the same type, e.g. <dbr:Aristotle>  <dbo:birthPlace>  <dbo:City>  <dbr:Category:City>")


        else:
            print("vector_similarity.py -c <config_path>")