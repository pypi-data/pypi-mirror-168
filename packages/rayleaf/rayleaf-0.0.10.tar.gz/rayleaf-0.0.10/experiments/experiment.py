from datetime import datetime


import rayleaf

from rayleaf.entities import Server, Client
from rayleaf.utils.logging_utils import log


from fedavg import fedavg


NUM_ROUNDS = 100
EVAL_EVERY = 1
NUM_CLIENTS = 10
CLIENTS_PER_ROUND = 5
BATCH_SIZE = 64
SEED = 0
NUM_EPOCHS = 25
GPUS_PER_CLIENT_CLUSTER = 1
NUM_CLIENT_CLUSTERS = 1
SAVE_MODEL = False
USE_GRADS = False
CPD_RANK = 10
RSVD_RANK = 16
ARCH_AWARE = True

OUTPUT = f"output/"
LR = 0.05

fedavg(
    dataset="femnist",
    output_dir= OUTPUT,
    num_rounds = NUM_ROUNDS,
    eval_every = EVAL_EVERY,
    num_clients = NUM_CLIENTS,
    clients_per_round = CLIENTS_PER_ROUND,
    client_lr = LR,
    batch_size = BATCH_SIZE,
    seed = SEED,
    num_epochs = NUM_EPOCHS,
    gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
    num_client_clusters = NUM_CLIENT_CLUSTERS,
    save_model = SAVE_MODEL
)

# for mu in [0.001, 0.01, 0.1, 1, 10]:
#     fedprox(
#         dataset="femnist",
#         output_dir= PAPER_OUTPUT,
#         mu=mu,
#         num_rounds = NUM_ROUNDS,
#         eval_every = EVAL_EVERY,
#         num_clients = NUM_CLIENTS,
#         clients_per_round = CLIENTS_PER_ROUND,
#         client_lr = FEMNIST_LR,
#         batch_size = BATCH_SIZE,
#         seed = SEED,
#         num_epochs = NUM_EPOCHS,
#         gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#         num_client_clusters = NUM_CLIENT_CLUSTERS,
#         save_model = SAVE_MODEL
#     )

# comp_bz2(
#     dataset="femnist",
#     output_dir= PAPER_OUTPUT,
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = FEMNIST_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )


# for stdev in [10 ** n for n in range(-4, 2)]:
#     for C in [10 ** n for n in range(-2, 4)]:
#         dpsgd_cnn(
#             stdev = stdev,
#             C = C,
#             num_rounds = NUM_ROUNDS,
#             eval_every = EVAL_EVERY,
#             num_clients = NUM_CLIENTS,
#             clients_per_round = CLIENTS_PER_ROUND,
#             client_lr = CLIENT_LR,
#             batch_size = BATCH_SIZE,
#             seed = SEED,
#             num_epochs = NUM_EPOCHS,
#             gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#             num_client_clusters = NUM_CLIENT_CLUSTERS,
#             save_model = SAVE_MODEL,
#             notes = f"stdev = {stdev}, C = {C}"
#         )

# sign_femnist(
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )

# for comp in ["rsvd", "svd", "qrcp"]:
#     for rank in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
#         if comp == "rsvd" or (comp == "svd" and rank in (1, 2)):
#             continue
#         else:
#             nla_cnn(
#                 compression=comp,
#                 rank=rank,
#                 num_rounds = NUM_ROUNDS,
#                 eval_every = EVAL_EVERY,
#                 num_clients = NUM_CLIENTS,
#                 clients_per_round = CLIENTS_PER_ROUND,
#                 client_lr = CLIENT_LR,
#                 batch_size = BATCH_SIZE,
#                 seed = SEED,
#                 num_epochs = NUM_EPOCHS,
#                 gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#                 num_client_clusters = NUM_CLIENT_CLUSTERS,
#                 save_model = SAVE_MODEL
#             )

# for rank in [2 ** n for n in range(0, 11)]:
# nla_cnn(
#     output_dir=f"output/cpd/rsvd",
#     rank=RSVD_RANK,
#     arch_aware=ARCH_AWARE,
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )

# scaffold(
#     dataset="femnist",
#     global_lr="0.005",
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL,
# )

# for cpd_rank in [1, 2, 4, 8, 16]:
#     cpd(
#         output_dir=f"output/cpd/cpd-layer0-r{cpd_rank}",
#         cpd_rank=cpd_rank,
#         rsvd_rank=RSVD_RANK,
#         num_rounds = NUM_ROUNDS,
#         eval_every = EVAL_EVERY,
#         num_clients = NUM_CLIENTS,
#         clients_per_round = CLIENTS_PER_ROUND,
#         client_lr = CLIENT_LR,
#         batch_size = BATCH_SIZE,
#         seed = SEED,
#         num_epochs = NUM_EPOCHS,
#         gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#         num_client_clusters = NUM_CLIENT_CLUSTERS,
#         save_model = SAVE_MODEL
#     )

# for rank in [32]:
#     try:
#         cpd(
#             output_dir=f"output/compression/conv1-r{rank}",
#             conv1_rank=rank,
#             num_rounds = NUM_ROUNDS,
#             eval_every = EVAL_EVERY,
#             num_clients = NUM_CLIENTS,
#             clients_per_round = CLIENTS_PER_ROUND,
#             client_lr = CLIENT_LR,
#             batch_size = BATCH_SIZE,
#             seed = SEED,
#             num_epochs = NUM_EPOCHS,
#             gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#             num_client_clusters = NUM_CLIENT_CLUSTERS,
#             save_model = SAVE_MODEL
#         )
#     except:
#         continue
# for rank in [1, 2, 4, 8, 16, 32, 64, 128]:
#     try:
#         cpd(
#             output_dir=f"output/compression/conv2-r{rank}",
#             conv2_rank=rank,
#             num_rounds = NUM_ROUNDS,
#             eval_every = EVAL_EVERY,
#             num_clients = NUM_CLIENTS,
#             clients_per_round = CLIENTS_PER_ROUND,
#             client_lr = CLIENT_LR,
#             batch_size = BATCH_SIZE,
#             seed = SEED,
#             num_epochs = NUM_EPOCHS,
#             gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#             num_client_clusters = NUM_CLIENT_CLUSTERS,
#             save_model = SAVE_MODEL
#         )
#     except:
#         continue
# for rank in [4]:
#     try:
#         cpd(
#             output_dir=f"output/compression/fc2-r{rank}",
#             fc2_rank=rank,
#             num_rounds = NUM_ROUNDS,
#             eval_every = EVAL_EVERY,
#             num_clients = NUM_CLIENTS,
#             clients_per_round = CLIENTS_PER_ROUND,
#             client_lr = CLIENT_LR,
#             batch_size = BATCH_SIZE,
#             seed = SEED,
#             num_epochs = NUM_EPOCHS,
#             gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#             num_client_clusters = NUM_CLIENT_CLUSTERS,
#             save_model = SAVE_MODEL
#         )
#     except:
#         continue

# cpd_femnist(
#     output_dir=f"output/compression/all_layers-r4-r16-r16-r8",
#     conv1_rank=4,
#     conv2_rank=16,
#     fc1_rank=16,
#     fc2_rank=8,
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )

# cpd_sc(
#     output_dir=f"output/cpd/sc/no_comp",
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )

# class PrintServer(Server):
#     def init(self):
#         log(f"Model layer shapes: {self.model_params.shapes}")


# rayleaf.run_experiment(
#     dataset = "shakespeare",
#     dataset_dir = "data/shakespeare/",
#     output_dir= f"output/shakespeare/{datetime.now()}/",
#     model = "stacked_lstm",
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     ServerType=PrintServer,
#     client_types=[(Client, NUM_CLIENTS)],
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     use_val_set = False,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )

# for r in [8, 16]:
# rsvd_shakespeare(
#     output_dir=f"output/shakespeare/compression/rsvd_r{8}_{datetime.now()}/",
#     # rank=r,
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )