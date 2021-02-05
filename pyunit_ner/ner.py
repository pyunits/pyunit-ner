# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2021/2/5 上午9:49
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes :
import os
import numpy as np
from paddle import fluid
from pyunit_ner.transformer_encoder import encoder, pre_process_layer
from pyunit_ner.vocab import vocal
import re
from paddle.fluid.transpiler.distribute_transpiler import DistributeTranspilerConfig

config = {
    "attention_probs_dropout_prob": 0.1,
    "hidden_act": "relu",
    "hidden_dropout_prob": 0.1,
    "hidden_size": 768,
    "initializer_range": 0.02,
    "max_position_embeddings": 513,
    "num_attention_heads": 12,
    "num_hidden_layers": 12,
    "type_vocab_size": 2,
    "vocab_size": 18000
}
label_map_config = {
    "B-PER": 0,  # 人名
    "I-PER": 1,
    "B-ORG": 2,  # 机构名
    "I-ORG": 3,
    "B-LOC": 4,  # 地名
    "I-LOC": 5,
    "O": 6
}
model_path = os.environ.get('MODEL_PATH', '/mnt/model')
exe = fluid.Executor()
startup_program = fluid.Program()
main_program = fluid.Program()

with fluid.program_guard(main_program, startup_program):
    reader = fluid.layers.py_reader(64, [[-1, 256, 1]] * 4, ['int64'] * 3 + ['float32'], [0] * 4)
    src_ids, sent_ids, pos_ids, input_mask = fluid.layers.read_file(reader)
    self_attn_mask = fluid.layers.matmul(x=input_mask, y=input_mask, transpose_y=True)
    self_attn_mask = fluid.layers.scale(x=self_attn_mask, scale=10000.0, bias=-1.0, bias_after_scale=False)
    n_head_self_attn_mask = fluid.layers.stack(x=[self_attn_mask] * config['num_attention_heads'], axis=1)
    n_head_self_attn_mask.stop_gradient = True
    param_initializer = fluid.initializer.TruncatedNormal(config['initializer_range'])

    emb_out = fluid.layers.embedding(
        input=src_ids,
        size=[config['vocab_size'], config['hidden_size']],
        dtype="float32",
        param_attr=fluid.ParamAttr(name="word_embedding", initializer=param_initializer), is_sparse=False)

    position_emb_out = fluid.layers.embedding(
        input=pos_ids,
        size=[config['max_position_embeddings'], config['hidden_size']],
        dtype="float32",
        param_attr=fluid.ParamAttr(name="pos_embedding", initializer=param_initializer))

    sent_emb_out = fluid.layers.embedding(
        sent_ids,
        size=[config['type_vocab_size'], config['hidden_size']],
        dtype="float32",
        param_attr=fluid.ParamAttr(name="sent_embedding", initializer=param_initializer))

    emb_out += position_emb_out + sent_emb_out
    emb_out = pre_process_layer(emb_out, 'nd', config['hidden_dropout_prob'], name='pre_encoder')

    enc_out = encoder(
        n_layer=config['num_hidden_layers'],
        enc_input=emb_out,
        attn_bias=n_head_self_attn_mask,
        n_head=config['num_attention_heads'],
        d_key=config['hidden_size'] // config['num_attention_heads'],
        d_value=config['hidden_size'] // config['num_attention_heads'],
        d_model=config['hidden_size'],
        d_inner_hid=config['hidden_size'] * 4,
        prepostprocess_dropout=config['hidden_dropout_prob'],
        attention_dropout=config['attention_probs_dropout_prob'],
        relu_dropout=0,
        hidden_act=config['hidden_act'],
        preprocess_cmd="",
        postprocess_cmd="dan",
        param_initializer=param_initializer,
        name='encoder')

    log = fluid.layers.fc(input=enc_out, size=len(label_map_config), num_flatten_dims=2,
                          param_attr=fluid.ParamAttr(name="cls_seq_label_out_w",
                                                     initializer=fluid.initializer.TruncatedNormal(scale=0.02)),
                          bias_attr=fluid.ParamAttr(name="cls_seq_label_out_b",
                                                    initializer=fluid.initializer.Constant(0.)))

    ret_infers = fluid.layers.reshape(x=fluid.layers.argmax(log, axis=2), shape=[-1, 1])
    ret_infers.persistable = True
    fetch_list = ret_infers.name

exe.run(startup_program)


def existed(var):
    if not fluid.io.is_persistable(var):
        return False
    paths = os.path.exists(os.path.join(model_path, var.name))
    return paths


fluid.io.load_vars(exe, model_path, main_program=main_program, predicate=existed)


def parse_ner(label, text) -> dict:
    number = [str(la) for la in label]
    data = {'number': number, 'word': text}
    num = ''.join(number)
    match = re.finditer('(?=0)[01]+', num)
    data['person'] = [text[r.start():r.end()] for r in match]
    match = re.finditer('(?=2)[23]+', num)
    data['organization'] = [text[r.start():r.end()] for r in match]
    match = re.finditer('(?=4)[45]+', num)
    data['address'] = [text[r.start():r.end()] for r in match]
    return data


def reader_text(texts):
    max_len = max(len(inst) + 2 for inst in texts)

    def wrapper():
        words_ls = [[1] + list(map(lambda x: vocal.get(x, 3), _text)) + [2] for _text in texts]

        padded_token_ids = np.array([inst + list([0] * (max_len - len(inst))) for inst in words_ls],
                                    dtype=np.int64).reshape([-1, max_len, 1])

        padded_input_mask = np.array([[1] * len(inst) + [0] * (max_len - len(inst)) for inst in words_ls],
                                     dtype=np.float32).reshape([-1, max_len, 1])

        padded_text_type_ids = np.zeros(padded_input_mask.shape, dtype=np.int64)

        padded_position_ids = np.array([list(range(len(words))) + [0] * (max_len - len(words)) for words in words_ls],
                                       dtype=np.int64).reshape([-1, max_len, 1])

        return_list = [padded_token_ids, padded_text_type_ids, padded_position_ids, padded_input_mask]
        yield return_list

    print('-------start-----------')
    reader.decorate_tensor_provider(wrapper)
    reader.start()
    np_infers = exe.run(program=main_program, fetch_list=fetch_list, use_program_cache=True)
    reader.reset()
    print('-------end-----------')
    labels = np.delete(np_infers[0].reshape(-1, max_len), [0, -1], axis=1)
    results = []
    for flag, text in zip(labels, texts):
        result = parse_ner(flag, text)
        results.append(result)
    return results
