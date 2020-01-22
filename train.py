import getopt, sys
import json
from OpenKE.config import Config
from OpenKE.models import TransE
from export_embeddings import export


def train(config_data):
    #os.environ['CUDA_VISIBLE_DEVICES']= config_data["gpu_number"]
    con = Config()

    if "use_gpu" in config_data.keys():
        if config_data["use_gpu"] == "True":
            con.set_use_gpu(True)
        else:
            con.set_use_gpu(False)
    else:
        con.set_use_gpu(False)
    con.set_in_path(config_data["input_dir"]+"/")
    con.set_work_threads(20)
    ## epoch
    con.set_train_times(int(config_data["epochs"]))
    ## batch size
    con.set_nbatches(int(config_data["batch_size"]))
    ## learning rate
    con.set_alpha(float(config_data["learning_rate"]))
    con.set_bern(0)
    ## embedding dimension
    con.set_dimension(int(config_data["embedding_dimension"]))
    con.set_margin(1.0)
    con.set_ent_neg_rate(1)
    con.set_rel_neg_rate(0)
    con.set_opt_method(config_data["optimizer"])
    con.set_save_steps(100)
    con.set_valid_steps(100)
    con.set_early_stopping_patience(10)
    con.set_checkpoint_dir("checkpoint")
    con.set_result_dir(config_data["output_dir"])
    con.set_test_link(True)
    con.set_test_triple(True)
    con.init()
    con.set_train_model(TransE)
    con.train()



if __name__ == "__main__":
    argv = (sys.argv[1:])
    config_path = ''
    try:
        opts, args = getopt.getopt(argv, "hc:o:", ["ifile="])
    except getopt.GetoptError:
        print('train.py -c <config_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('train.py -c <config_path>')
            sys.exit()
        elif opt in ("-c", "--ifile"):
            config_path = arg

    if config_path != '':
        print('Training with the config: ', config_path)

        config_data = dict()
        with open(config_path) as json_file:
            config_data = json.load(json_file)

        print(config_data)

        train(config_data)

        print("Training finished. Extracting embeddings ...")

        export(config_data)

    else:
        print('Usage: train.py -c <config_path>')