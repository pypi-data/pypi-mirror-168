# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# -*- coding: utf-8 -*- #
"""*********************************************************************************************"""
#   FileName     [ upstream/wavlm/expert.py ]
#   Synopsis     [ the WavLM wrapper ]
#   Author       [ Microsoft ]
"""*********************************************************************************************"""


###############
# IMPORTATION #
###############

import torch
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence

from ..interfaces import UpstreamBase
from .WavLM import WavLM, WavLMConfig

############
# CONSTANT #
############
SAMPLE_RATE = 16000
EXAMPLE_SEC = 5


###################
# UPSTREAM EXPERT #
###################
class UpstreamExpert(UpstreamBase):
    def __init__(self, ckpt, **kwargs):
        super().__init__(**kwargs)

        checkpoint = torch.load(ckpt)
        self.cfg = WavLMConfig(checkpoint["cfg"])
        self.model = WavLM(self.cfg)
        self.model.load_state_dict(checkpoint["model"])

        self.model.feature_grad_mult = 0.0
        self.model.encoder.layerdrop = 0.0

        if len(self.hooks) == 0:
            module_name = "self.model.encoder.layers"
            for module_id in range(len(eval(module_name))):
                self.add_hook(
                    f"{module_name}[{module_id}]",
                    lambda input, output: input[0].transpose(0, 1),
                )
            self.add_hook("self.model.encoder", lambda input, output: output[0])

        self._init_layerdrop = self.model.encoder.layerdrop

    @property
    def layer_drop(self):
        return self.model.encoder.layerdrop

    def set_layer_drop(self, layerdrop: float = None):
        if isinstance(layerdrop, float):
            self.model.encoder.layerdrop = layerdrop
        elif layerdrop is None:
            self.model.encoder.layerdrop = self._init_layerdrop
        else:
            raise ValueError("layerdrop can only be float or None")

    def get_downsample_rates(self, key: str) -> int:
        return 320

    def forward(self, wavs):
        if self.cfg.normalize:
            wavs = [F.layer_norm(wav, wav.shape) for wav in wavs]

        device = wavs[0].device
        wav_lengths = torch.LongTensor([len(wav) for wav in wavs]).to(device)
        wav_padding_mask = ~torch.lt(
            torch.arange(max(wav_lengths)).unsqueeze(0).to(device),
            wav_lengths.unsqueeze(1),
        )
        padded_wav = pad_sequence(wavs, batch_first=True)

        features, feat_padding_mask = self.model.extract_features(
            padded_wav,
            padding_mask=wav_padding_mask,
            mask=False,
        )

        # This forward function only does the model forward
        # The return dict is then handled by UpstreamBase's hooks
