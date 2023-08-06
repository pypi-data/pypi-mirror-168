# experiment, hardware
experiment_tag = "default"
gpus = [1, 2, 3]
n_workers = 16
seed = 1234
auto_lr_find = False
auto_scale_batch_size = False

# dataset
dataset_dir = "./data/ESC-50-master"
n_classes = 50
light_loader = False

# acoustic parameters
sr = 8000
hop_time = 0.01
win_time = 0.025
window_kind = "hamming"
n_mel = 128
melspec_len = 501
clamp_min_db = -140.0

# model parameters
embed_dim = 768
n_layers = 12
n_heads = 12
input_seq_len = 589
dim_feedforward = 1024
dropout = 0.1

# optimizer
batch_size = 12
learning_rate = 1e-4
opt_params = {"betas": (0.9, 0.999), "eps": 1e-8}  # torch.optim.Adam defaults
lr_decay = 0.85
start_lr_scheduler = 10
clip_grad_norm = None
n_epochs = 50
fast_dev_run = False
ema_decay = 0.999
ema_warmup_steps = 1_000
checkpoint_step = 10
summary_step = 10
