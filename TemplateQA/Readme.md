# 基于模板的方法

## 说明

基于进行编写，需下载hanlp词向量txt放到data/文件夹下，文件链接：https://pan.baidu.com/s/18bocfuOeDqkX2ZpiX2b5jg 密码：mf8d。

采用java编写，这里指上传了src部分。

运行效果截图如下:

![example](example.jpg)

## 步骤

### 配置初始化
- 设置知识库
- 设置virtuoso用户名密码
- 设置前缀

### 词向量初始化
- 加载词向量文件，归一化存储至hashmap中
- 加载同义词文件

### 资源加载初始化
- 加载模版文件，建立意图模板索引goalmap<string,template>
  - json读取模版文件，建立<模板名，模板>映射，存入goalmap中。
  - 加载指代词、停用词文件
  - 遍历goalmap的每个模版，对于每个模版，遍历它的槽列表slotlist，在槽索引slotmap<string,list<string>>中添加<槽名，模板名>的映射，相当于现在就建立了一个槽所能配对的模板列表的索引
  - 将slotmap里面的槽加载到goalmap里去，这样goalmap里的每个模板的slotmap<string,slot>都有<槽名，槽（包含槽名和对应的slotmap模板名列表）>的索引
- 加载实体
  - 加载实体/属性的同义词
  - 读取slot-class-map文件，遍历各个类型的槽，从中读取对应的类，然后查询知识库，返回所有该类的实体(IRI，label，type)，加至all-entity-pro-info
  - 遍历slot-class-map里的所有class下的property，当作entity加入all-entity-pro-info；同时将该property加入typed_propertys<string,set<entity>>（不同槽下的属性）；若slotmap中含有该property的type对应的槽，遍历该槽拥有的模版，将property加进去
- 建立简单索引
  - 遍历all-entity-pro-info的所有实体，观察其type，如果是_name结尾的，则说明是实体，否则就说明是属性。建立槽类型与实体属性候选集合的索引typed-entity-inverted-index<槽类型，map<token关键词，set<实体>>>。之后用n-gram获取实体的所有token，然后根据不同的槽类型，为各实体/属性的label的n-gram生成候选实体存储起来。

### 识别槽值对
- 预统计
  - 遍历各个人工编写的Template，统计各个模版的触发词们在句子中出现了几次，得到意图模板列表HashMap<模板名, 触发词出现次数>goallist
- 槽识别
  - 首先利用已经建立好的槽类型与实体属性候选集合的索引typed-entity-inverted-index，得到以token为key，以其对应的实体集合为value的哈希列表。然后生成问句的n-gram的token们，利用上述的哈希列表，看问句的每个token是不是在预哈希列表中存在，若存在则说明该token是个关键词，进而寻找该token在问句中的mention是什么，以及根据最长上升子序列LCS的方法来计算label和mention之间的平均距离作为该slotMode的得分，最终生成slotMode{entity，mention，起始位置，得分}的数组，可以理解为候选槽集合Set<Slot>slotlist
  - 称上一步得到的结果是entities，是一个slotMode的列表。根据这个列表去生成有哪些属性，具体而言就是把type的xxname改成property，比如person_name改为person-property，这样直接能确定有多少种property，比如说把所有property的类型存到ptype这么一个集合里，把所有property的内容存到property这么一个集合中。之后利用hanlp工具分词，计算LCS之类的进行属性识别和链接

### 选择模版
- 计算意图模板得分
  - 给定了问句的意图模板列表和槽列表，然后根据关键字、候选槽得分等信息计算各个意图模板的分数，从大到小排序，选择分数最高的意图模板作为意图，若分数相同优先返回槽个数少者
- 填槽
  - 根据识别出来的槽，和识别出的实体/属性，进行填槽，补全意图，填完槽值后匹配pattern查询结果
- 运行Sparql返回结果