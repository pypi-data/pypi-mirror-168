from einops import rearrange, repeat
import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torchaudio.transforms as tat


class TransformerEncoder(nn.Module):
    def __init__(self, embed_dim, n_heads, dim_feedforward, dropout, n_layers):
        super().__init__()
        self.layers = nn.ModuleList([])

        for _ in range(n_layers):
            self.layers.append(TransformerEncoderLayer(embed_dim, n_heads, dim_feedforward, dropout))
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return self.norm(x)


class TransformerEncoderLayer(nn.Module):
    def __init__(self, dim, n_heads, dim_feedforward, dropout, activation='gelu'):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.attention = nn.MultiheadAttention(embed_dim=dim, num_heads=n_heads, dropout=dropout)
        self.feed_forward = FeedForward(dim, dim_feedforward, dropout)

    def forward(self, x):
        x = self.norm(x)
        x = self.attention(x, x, x)[0] + x
        x = self.norm(x)
        x = self.feed_forward(x) + x
        return x


class FeedForward(nn.Module):
    def __init__(self, dim, hidden_dim, dropout=0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        return self.net(x)


def get_sinusoid_encoding_table(n_position, d_hid, padding_idx=None):
    """ Sinusoid position encoding table """

    def cal_angle(position, hid_idx):
        return position / np.power(10000, 2 * (hid_idx // 2) / d_hid)

    def get_posi_angle_vec(position):
        return [cal_angle(position, hid_j) for hid_j in range(d_hid)]

    sinusoid_table = np.array([get_posi_angle_vec(pos_i) for pos_i in range(n_position)])

    sinusoid_table[:, 0::2] = np.sin(sinusoid_table[:, 0::2])  # dim 2i
    sinusoid_table[:, 1::2] = np.cos(sinusoid_table[:, 1::2])  # dim 2i+1

    if padding_idx is not None:
        # zero vector for padding dimension
        sinusoid_table[padding_idx] = 0.

    return torch.FloatTensor(sinusoid_table)


class AST(pl.LightningModule):
    """Audio Spectrogram Transformer"""

    def __init__(self, cfg):
        super().__init__()

        self.augmentation = nn.Sequential(
            tat.TimeMasking(cfg.n_mel // 4, iid_masks=True),
            tat.FrequencyMasking(cfg.melspec_len // 4, iid_masks=True),
        )

        self.cls_token = nn.Parameter(torch.randn(1, 1, cfg.embed_dim))
        self.patch_linear_projection = nn.Conv2d(1, cfg.embed_dim, kernel_size=(16, 16), stride=(10, 10))
        self.pos_emb = nn.Embedding.from_pretrained(
            get_sinusoid_encoding_table(cfg.input_seq_len + 1, cfg.embed_dim, padding_idx=0),
            freeze=True)
        self.transformer_encoder = TransformerEncoder(cfg.embed_dim,
                                                      cfg.n_heads,
                                                      cfg.dim_feedforward,
                                                      cfg.dropout,
                                                      cfg.n_layers)
        self.linear_output = nn.Sequential(
            nn.LayerNorm(cfg.embed_dim),
            nn.Linear(cfg.embed_dim, cfg.n_classes))
        self.activation = nn.Softmax(dim=-1)

    def forward(self, data):
        """get valid raw logits from a batch of melspecs"""
        data = data.float() # B T C

        data = rearrange(data, 'b t c -> b c t')

        if self.training:
            with torch.no_grad():
                data = torch.unsqueeze(data, 1)
                data = self.augmentation(data)
                data = torch.squeeze(data)  # B C T

        data = data.unsqueeze(1)    # B 1 C T
        proj_patches = self.patch_linear_projection(data)
        proj_patches = rearrange(proj_patches, 'b c w t -> (t w) b c')
        T, B, C = proj_patches.shape

        cls_tokens = repeat(self.cls_token, '1 1 d -> 1 b d', b=B)
        proj_patches = torch.cat((cls_tokens, proj_patches), dim=0)

        pos = torch.arange(1, T + 2, device=proj_patches.device)
        pos = self.pos_emb(pos)
        proj_patches += pos.unsqueeze(1)
        cls_encodings = self.transformer_encoder(proj_patches).permute(1, 2, 0)[:, :, 0]
        logits = self.linear_output(cls_encodings)
        return logits

