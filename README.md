# **pyUnit-NER** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]

## NER模块集合
[![](https://img.shields.io/badge/Python-3.7-green.svg)](https://pypi.org/project/pyunit-ner/)
[![](https://img.shields.io/badge/Docker-Eboby-red.svg)](https://github.com/jtyoui/eboby)
[![](https://img.shields.io/badge/Email-jtyoui@qq.com-red.svg)]()

### 安装
    pip install pyunit-ner
    
### 默认官方数据集训练的模型（只能识别：人名、地名、机构名）
[点击下载模型](http://oss.tyoui.cn/model.zip)

### docker安装
[点击查看](https://github.com/jtyoui/eboby)

### 默认的参数和映射表
```python
from pyunit_ner import ernie_st,ernie_match,ERNIE_MODEL_PARAMETER,ERNIE_LABEL_MAP,parseNER
model = 'D://model' #解压的文件夹的地址
s = ernie_st(new_model_path=model, new_config=ERNIE_MODEL_PARAMETER, new_label_map_config=ERNIE_LABEL_MAP)
data = ernie_match('刘万光对李伟说：在贵阳市南明村永乐乡发生了一件恐怖的事情', s)
print(parseNER(data))
# {'number': ['0', '1', '1', '6', '0', '1', '6', '6', '6', '4', '5', '5', '4', '5', '5', '4', '5', '5', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6'], 'word': ['刘', '万', '光', '对', '李', '伟', '说', '：', '在', '贵', '阳', '市', '南', '明', '村', '永', '乐', '乡', '发', '生', '了', '一', '件', '恐', '怖', '的', '事', '情'], 'person': ['刘万光', '李伟'], 'organization': [], 'address': ['贵阳市南明村永乐乡']}
```


### 其他模型需要更改参数
```python
from pyunit_ner import ernie_st,ernie_match,parseNER

if __name__ == '__main__':
    ERNIE_MODEL_PATH = 'D://new_model'

    ERNIE_CONFIG = {
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

    ERNIE_LABEL_MAP = {
        "B-PER": 0,  # 人名
        "I-PER": 1,
        "B-ORG": 2,  # 机构名
        "I-ORG": 3,
        "B-LOC": 4,  # 地名
        "I-LOC": 5,
        "B-GUE": 6,  # 办事指南
        "I-GUE": 7,
        "O": 8
    }
    s = ernie_st(ERNIE_MODEL_PATH, ERNIE_CONFIG, ERNIE_LABEL_MAP)
    data = ernie_match('我叫刘万光我是贵阳市南明叇村永乐乡水塘村的村民', s)
    print(parseNER(data))
```

### 需要三个条件
    第一个是模型的位置：ERNIE_MODEL_PATH
    第二个是模型的参数：ERNIE_CONFIG
    第三个是模型训练时候的IBO对应的标签和数字映射表：ERNIE_LABEL_MAP
    
### 官网地址
[点击ERNIE查看地址](https://github.com/PaddlePaddle/ERNIE)  

***
[1]: https://blog.jtyoui.com