import gzip
import os


entity_embeddings = list()
relation_embeddings = list()
class_embeddings = list()
category_embeddings = list()


def save_embeddings(input_list: list, file_path, embedding_dim):
    f = open(file_path, 'w')
    f.write(str(input_list.__len__())+" "+str(embedding_dim)+"\n")
    f.writelines(input_list)
    f.close()

dir_path = "wikidata_dim_200"
file_path = dir_path + "/wikidata_translation_v1.tsv.gz"


bufsize = 6005536
print("Reading the gzip file %s" %file_path)
with gzip.open(file_path, "rb") as f:
    while True:
        lines = f.readlines(bufsize)

        if not lines:
            break
        for l in lines:
            if not l.decode("utf-8").startswith("<http://www.wikidata.org/entity/"):
                continue
            line = l.decode("utf-8")
            tokens = line.split("\t")
            uri = tokens[0]
            if uri.startswith("<http://www.wikidata.org/entity/Q"):
                entity_embeddings.append(line.replace("\t", " "))
            elif uri.startswith("<http://www.wikidata.org/entity/P"):
                relation_embeddings.append(line.replace("\t", " "))

            if entity_embeddings.__len__() + relation_embeddings.__len__() % 10000 == 0:
                print("Processed #entities: ", str(entity_embeddings.__len__()+relation_embeddings.__len__()))



if not os.path.isdir(dir_path):
    try:
        os.mkdir(dir_path)
    except OSError:
        print ("Creation of the directory %s failed" % dir_path)

print("Saving embeddings")
save_embeddings(entity_embeddings, dir_path+"/entity_embeddings.txt", 200)
save_embeddings(relation_embeddings, dir_path+"/relation_embeddings.txt", 200)
save_embeddings(class_embeddings, dir_path+"/class_embeddings.txt", 200)
save_embeddings(category_embeddings, dir_path+"/category_embeddings.txt", 200)