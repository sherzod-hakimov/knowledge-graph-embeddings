import gzip
import sys, getopt
import re
import os

def save_list_to_file(input_list: list, file_path):
    f = open(file_path, 'a+')
    f.writelines(input_list)
    f.close()

def main(input_file):
    bufsize = 6005536

    counter = 0
    # <http://www.wikidata.org/entity/Q31> <http://www.wikidata.org/prop/direct/P2936> <http://www.wikidata.org/entity/Q100103> .
    pattern = "^<http://www.wikidata.org/entity/Q.*> <http://www.wikidata.org/prop/direct/P.*> <http://www.wikidata.org/entity/Q.*"
    triple_list = list()

    ## create output file path and delete previous version
    output_file_path = os.path.dirname(os.path.realpath(input_file))+"/triples.nt"
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    print("Processing the gzip file %s" % input_file)

    ## loop over lines and extract valid triples
    with gzip.open(input_file, "rb") as f:
        while True:
            lines = f.readlines(bufsize)
            if not lines:
                break
            for l in lines:
                triple = l.decode("utf-8")
                if re.match(pattern, triple):
                    triple = triple.replace("http://www.wikidata.org/entity/", "wd:").replace("http://www.wikidata.org/prop/direct/", "wd:")
                    triple_list.append(triple)

            if len(triple_list) >= 1000000:
                save_list_to_file(triple_list, output_file_path)
                triple_list.clear()
                counter+=1
                print("Processed #triples: " +str(counter) +" (mln)")
    save_list_to_file(triple_list, output_file_path)
    triple_list.clear()
    counter += 1
    print("Processed #triples: " +str(counter) +" (mln)")

if __name__ == "__main__":
    argv = (sys.argv[1:])
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print('extract_wikidata_triples.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('extract_wikidata_triples.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg

    if input_file != '':
        print('Processing with the input file: ', input_file)
        main(input_file)
    else:
        print('Usage: extract_wikidata_triples.py -i <inputfile>')



