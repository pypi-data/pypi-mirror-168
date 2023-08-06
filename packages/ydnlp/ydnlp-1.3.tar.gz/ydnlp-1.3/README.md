## 简介 
利用 onnxruntime以及PaddleNLP提供的UIE模型,对文本，段落，篇章内容进行结构化提取

## 使用模型
UIE(Universal Information Extraction)：Yaojie Lu等人在ACL-2022中提出了通用信息抽取统一框架UIE。该框架实现了实体抽取、关系抽取、事件抽取、情感分析等任务的统一建模，并使得不同任务间具备良好的迁移和泛化能力。为了方便大家使用UIE的强大能力，PaddleNLP借鉴该论文的方法，基于ERNIE 3.0知识增强预训练模型，训练并开源了首个中文通用信息抽取模型UIE。该模型可以支持不限定行业领域和抽取目标的关键信息抽取，实现零样本快速冷启动，并具备优秀的小样本微调能力，快速适配特定的抽取目标。


### UIE的优势
- 使用简单：用户可以使用自然语言自定义抽取目标，无需训练即可统一抽取输入文本中的对应信息。实现开箱即用，并满足各类信息抽取需求。

- 降本增效：以往的信息抽取技术需要大量标注数据才能保证信息抽取的效果，为了提高开发过程中的开发效率，减少不必要的重复工作时间，开放域信息抽取可以实现零样本（zero-shot）或者少样本（few-shot）抽取，大幅度降低标注数据依赖，在降低成本的同时，还提升了效果。

- 效果领先：开放域信息抽取在多种场景，多种任务上，均有不俗的表现。
## 参考
- [PaddleNLP-UIE](https://github.com/PaddlePaddle/PaddleNLP/tree/develop/model_zoo/uie)

## 安装

```bash
pip install ydnlp
```
## 实例代码
```Python
from ydnlp.uie_predict import UIEPredictor
# 开放域抽取
texts = ['个人经济收入证明抽取兹证明张三为本单位职工，已连续在我单位工作5年。学历为ABC大学毕业，目前在我单位担任总经理助理职位。近一年内该员工在我单位平均月收入（税后）为63500元。（大写：陆万叁仟伍佰元']
schema1 = {'姓名','工作时间','毕业学校','职位','收入'}
predictor = UIEPredictor(512, 4, schema1, position_prob=0.5) 
outputs = predictor.predict(texts)
print(outputs)

# 开放域抽取
texts = ['2月8日上午北京冬奥会自由式滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌！']
schema1 = {'时间', '选手', '赛事名称'}
predictor = UIEPredictor(512, 4, schema1, position_prob=0.5) 
outputs = predictor.predict(texts)
print(outputs)

# 情感分类
texts = ['这个产品用起来真的很流畅，我非常喜欢']
schema1 = {'情感倾向[正向，负向]'}
predictor = UIEPredictor(512, 4, schema1, position_prob=0.5)
outputs = predictor.predict(texts)
print(outputs)

# 评价维度抽取
texts = ['总体挺好的，电池续航不行']
schema1 = {'评价维度': ['观点词', '情感倾向[正向，负向]']}
predictor = UIEPredictor(512, 4, schema1, position_prob=0.5)
outputs = predictor.predict(texts)
print(outputs)

# 触发词抽取
texts = ['中国地震台网正式测定：5月16日06时08分在云南临沧市凤庆县(北纬24.34度，东经99.98度)发生3.5级地震，震源深度10千米。']
schema1 = {'地震触发词': ['地震强度', '时间', '震中位置', '震源深度']}
predictor = UIEPredictor(512, 4, schema1, position_prob=0.5)
outputs = predictor.predict(texts)
print(outputs)

```
## TODO
1. 支持自定义schema的微调工具包
2. 丰富常见的schema种类
3. 更多需求调研:505991554@qq.com

## Q&A
1. 预置的schema列表是否可以查询？  
预设的schema没有统计过，提供预设的schema对抽取没有多大用处，因为不同的样本形式同一个schema抽取效果也是不一样，我们给出的建议是对于自己任务，都是需要微调一下 
