import getopt
import sys

import numpy as np



if __name__ == "__main__":
    argv = (sys.argv[1:])
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
    except getopt.GetoptError:
        print('convert_binary_embeddings.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('convert_binary_embeddings.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i"):
            input_file = arg
        elif opt in ("-o"):
            output_file = arg

    if input_file != '' and output_file != '':
        print('Processing with the input file: {0} and output file: {1}'.format(input_file, output_file))
        vec = np.memmap(input_file , dtype='float32', mode='r')
        print("Saving the vector to the file {0}".format(output_file))
        np.savetxt(output_file, vec, delimiter=" ", fmt='%d')
    else:
        print('Usage: convert_binary_embeddings.py -i <inputfile> -o <outputfile>')
