import re


andidate_list = ["J909.G120", "12J"]


pic_pre_simple = [
    "京",
    "津",
    "冀",
    "黑",
    "吉",
    "辽",
    "内",
    "沪",
    "苏",
    "浙",
    "皖",
    "闽",
    "赣",
    "鲁",
    "豫",
    "鄂",
    "湘",
    "粤",
    "桂",
    "琼",
    "川",
    "贵",
    "云",
    "渝",
    "藏",
    "陕",
    "甘",
    "青",
    "宁",
    "港",
    "澳",
    "台",
    "中南",
    "国标",
    "国",
    "东南",
    "西南",
    "陕",
    "新",
    "陕标",
    "中南标",
    "L",
    "l",
]

hard_sp = [
    
    "加气混凝土墙",
    "要求选材及施工",
    "8~10厚",
    "总",
    "。",
    "；",
    "高度",
    "宽度",
    "厚",
    "长度",
    "宽",
    "H=",
    "下设",
    "设",
    "说明",
    "mm",
    "改为",
    "材料",
    "深度",
    "用于",
    "采用",
    "内径",
    "规格",
    "0x", 
    "取消",
    "踢脚高",
    "0X",
    "第4条改为",
    "1、",
    "2、",
    "3、",
    "4、",
    "5、",
    "6、",
    "7、",
    "8、",
    "9、",
    "预留",
    "φ",
    "标高",
    "300\*300",
    "高1",
    "长1",
    "0高",
    "四周高",
    "%"
]

# 不保留的软间隔
zuofa_name = [
    "龙骨",
    "穿孔板吸音板", 
    "水泥",
    "保温",
    "墙面",
    "真石",
    "环氧",
    "陶瓷",
    "铝合金",
    "合成树脂",
    "石质板",
    "贴耐酸耐碱砖墙裙",
    "混凝土",
    "抹",
    "混合砂浆",
    "面砖墙面",
    "刮腻子顶棚",
    "轻钢龙骨",
    "调和漆",
    "面砖踢脚",
    "涂料",
    "延伸至室外地坪以下",
    "涂层踢脚",
    "釉面砖防水墙",
    "楼板",
    "防水",
    "低温热水辐射供暖",
    "型轻钢",
    "非石棉纤维",
    "订",
    "轻钢主龙骨",
    "主龙骨", 
    "次龙骨",
    "增强硅酸钙",
    "为",
    "米黄色",
    "浅灰色",
    "白色",
    "钢筋混凝土墙",
    "地面清理干净", 
    "刮涂",
    "底油",
    "深褐色醇酸磁漆",
]

# 需要保留的软间隔
soft_sp = ["\.", "\ ", "\，", "\·"]


def reverse_maximum_match(candidate_list: list, sentence: str):
    ans_reverse = list()
    if len(candidate_list) < 1:
        return ans_reverse
    candidate_list = [str(item) for item in candidate_list]
    max_length: int = len(sorted(candidate_list, key=lambda x: len(x))[-1])
    len_row: int = len(sentence)
    while len_row > 0:
        divide: str = sentence[-max_length:]
        while divide not in candidate_list:
            if len(divide) == 1:
                break
            divide = divide[1:]
        divide_index: int = len(sentence) - len(divide)
        if divide in candidate_list:
            ans_reverse.append((divide, divide_index))
        sentence = sentence[0 : len(sentence) - len(divide)]
        len_row = len(sentence)
    return ans_reverse[::-1]


# def get_pre_picture(andidate_list, sentence):
#    res_list = reverse_maximum_match(andidate_list, sentence)
#    if res_list:
#        if len(res_list) > 1:
#            pre = "，".join(list(map(lambda x: x[0], res_list)))
#        else:
#            pre = res_list[0][0]
#    else:
#        # 如果匹配没有找到前缀则使用正则进行查找
#        pic_key = "J" # 装饰
#        pattern_1 = "|".join(pic_pre_simple)
#        pattern = ".*?(" + pattern_1 + "?)(" + "[0-9A-Z]+" + pic_key + "[0-9A-Z]+)" + ".*?"
#        temp = re.findall(pattern, sentence)
#        res = list(map(lambda x: x[0] + x[1], temp))
#        pre = "，".join(res)
#    # 接下来需要根据pre来进行后缀正则匹配，这里暂留
#    return pre


def _get_pre(andidate_list, sentence):
    pic_key = "J"  # 装饰
    pattern_1 = "|".join(pic_pre_simple)
    pattern = ".*?(" + pattern_1 + "?)(" + "[0-9A-Z]+" + pic_key + "[0-9A-Z]+)" + ".*?"
    temp = re.findall(pattern, sentence)
    pre_list = list(set(map(lambda x: x[0] + x[1], temp)))
    if not pre_list:
        res = reverse_maximum_match(andidate_list, sentence)
        pre_list = list(map(lambda x: x[0], res))
    return pre_list


def _trans(q, q_input):
    knd = q_input[0][0]
    q_list = q.split("^")
    h = 0
    for i, h in enumerate(q_list):
        if knd in h:
            h = i
            break
    if h == 0:
        return q, q_input
    if h == len(q_list) - 1:
        oq = q_list[h] + "^" + q.replace("^" + q_list[h], "")
    else:
        oq = q_list[h] + "^" + q.replace(q_list[h] + "^", "")
    print("oq：", oq)
    q_output = [(knd, oq.index(knd))] + q_input[1:]
    return oq, q_output


def _get_suffix(sentence, ps, hard_sp=hard_sp, soft_sp=soft_sp, zuofa_name=zuofa_name):
    tuji_list = []
    for i, (k, j) in enumerate(ps):
        start_index = j + len(k)
        print(start_index)
        if i + 1 < len(ps):
            end_index = ps[i + 1][1]
        else:
            end_index = len(sentence)
        print(end_index)
        chunk = sentence[start_index:end_index]
        print("块内容:", chunk)
        # 对块进行硬分隔过滤
        if hard_sp:
            chunk_part = re.sub("|".join(hard_sp), "@", chunk).split("@")[0]
        else:
            chunk_part = chunk
        print("硬分隔之后的内容：", chunk_part)

        # 在软分隔分组前，对一些空格进行处理，如踢 35变为踢35，墙 A1 --> 墙A1使其不作为软分隔符号

        pattern = ".*?([\u4e00-\u9fa5]\s+[A-Z,\d+]).*?"
        td = re.findall(pattern, chunk_part)
        if td:
            for tdd in td:
                chunk_part = chunk_part.replace(tdd, tdd.replace(" ", ""))
        # 对-后面的空格进行去除
        pattern = "-\s+"
        chunk_part = re.sub(pattern, "-", chunk_part)

        # 对过滤后的文件进行软分隔分组
        # 因为这里的软分隔很多与正则表达式中的符号重复，所以都需要加上\才能使用re.sub
        soft_sp1 = list(map(lambda x: x[1:], soft_sp))
        chunk_part_group = re.sub(
            "|".join(soft_sp + zuofa_name), "^", chunk_part
        ).split("^")
        # for ss in soft_sp:
        #    chunk_part1 = chunk_part.replace(ss, "^")
        # chunk_part_group = chunk_part1.split("^")
        print(chunk_part_group)

        # 对每一组的内容进行检测，将所有可能成为图集后缀的进行拼接
        suf_list = []
        for cpg in chunk_part_group:
            # 全部为数字，那么不是图集后缀
            if cpg.isdigit():
                continue

            ci = chunk_part.index(cpg)
            print("ci：", ci)
            # 当不是全为数字，但包含数字时为图集后缀
            for c in list(cpg):
                if c.isdigit():
                    # 一旦成为后缀，那么需要包含前面（如果存在）的弱分隔符
                    if ci != 0:
                        if chunk_part[ci - 1] in soft_sp1:
                            sl = chunk_part[ci - 1] + cpg
                        else:
                            sl = cpg
                    else:
                        sl = cpg
                    # 防止不同单元重复出现图集后缀
                    if sl not in suf_list:
                        suf_list.append(sl)

                    break
        suffix = "".join(suf_list)
        # 对后缀进行括号内容处理，按照业务情况括号内容只有全部为数字时才能保留
        k_index = suffix.find("（")
        if k_index != -1:
            kc = suffix[k_index + 1 :].replace("）", "")
            print("括号里的内容:", kc)
            # 如果括号里什么也没有或者括号内容包括汉字且不是涂304，那么括号连带内容都是不需要的
            if (
                not kc
                or ("\u4e00" <= kc <= "\u9fff" and kc != "涂304")
                or suffix.find("）") == -1
            ):
                suffix = suffix[:k_index]
        # 对组合之后可能存在的图集常用字进行处理
        stop_word = ["参", "见", "参见", "详"]
        suffix = re.sub("|".join(stop_word), "", suffix)
        if suffix:
            tuji = k + suffix
            tuji_list.append(tuji)
    return tuji_list


def get_pre_picture(andidate_list, sentence, global_text):

    # 整体的文本与处理
    sentence = (
        sentence.replace("@@", "")
        .replace("(", "（")
        .replace(")", "）")
        .replace(",", "，")
        .replace(";", "；")
        .replace("\n", "")
    )

    # 如果全局存在，优先使用全局作为图集前缀
    if global_text:
        pre_list = _get_pre(andidate_list, global_text)
        print("全局中获取的前缀：", pre_list)
        # 如果在全局文本中找到图集前缀
        if pre_list:
            # 这里会假设全局文本只会找到一个图集前缀
            pre = pre_list[0]
            # 在找图集后缀时，会把整个句子作为一个块
            # 而且所有sentence中的图集前缀会被作为硬间隔
            pre_hard = _get_pre(andidate_list, sentence)
            gr = _get_suffix(str(pre) + sentence, [(str(pre), 0)], hard_sp=hard_sp, soft_sp=soft_sp, zuofa_name=zuofa_name)
            print("获取的图集:", gr)
            if gr:
                return gr[0]

    # 获取图集前缀
    pre_list = _get_pre(andidate_list, sentence)
    tuji_list = []
    # 按照图集前缀进行分块
    if pre_list:
        print(pre_list)
        ps = reverse_maximum_match(pre_list, sentence)
        # 获取图集后缀
        tuji_list = _get_suffix(sentence, ps)
        print("*******")
        print(tuji_list)
        if not tuji_list:
            # 为了防止图集后缀写在前缀的前面，这里会对sentence以及对应的索引进行一次调整
            sentence_f, ps_f = _trans(sentence, ps)
            print("需要进行反查")
            print(sentence_f)
            print(ps_f)
            if sentence != sentence_f:
                tuji_list = _get_suffix(sentence_f, ps_f)
        return "｜".join(list(set(tuji_list)))
    else:
        return ""


if __name__ == "__main__":
    sentence = "as" + "黑09J01" + "a sd踢 35a，rr,rs；da下设sda。sdsd" + "陕09J01" + "asd"
    sentence = "楼/地面^楼109环氧树脂自流平地面^L13J1^dsaL13J2^用于污泥脱水机房、负一层地面(包括预处理、AAO、MBR、车道、送、排风机房、控制室、配电室、 鼓风机房等),其中车道、污泥脱水机房下采用150mm厚C40细石混凝土下铺设C10@150×150钢筋网。"
    sentence = "参12J1-92页- 顶5,面层乳胶漆,选材由甲方统一确定,用于室内顶棚。"
    sentence = "屋面出入口建筑做法详见L13J5-1/A14页/做法1与2 屋面检修爬梯的具体构造做法详见L13J8/97页、护笼做法详见02J401@@透气管出屋面的具体构造做法详见L13J5-1/A16页@@高低屋面雨水管抗冲层做法参见L13J5-1中节点2做法"
    sentence = "参见图集详见L13J6第40页2;"
    sentence = "顶1^水 泥@@砂@@浆@@顶@@棚^1).现浇钢筋混凝土板底面清理干净;^12J1 顶6-92 总厚度:8"
    sentence = "12YJ1-73-裙3(CF)"
    sentence = "参12J1-78页- 内墙3-B"
    sentence = "12YJ1-28-地104F、楼104F"
    sentence = "屋 面^卷材防水屋面^05J909^WM15^屋 15^除刚性外其余屋面^50 厚XPS保温板。@@K=0.38W/(m .k)@@2@@ 3厚SBS改性沥青防水卷材两道"
    sentence = "水簸箕^中南标15ZJ201-C/18^400x400x40 C20 细石混凝土预制。"
    sentence = "中南标11ZJ901-A/25、B/25^用于外挑雨蓬、突出外墙线条、 窗台等部位的滴水线"
    sentence = (
        "屋 面^主楼屋面^细石混凝土防水屋面(上人)^12J1^138页-屋103^防水层为12J1-133页-1F1(3+3厚SBS 高聚物改性沥青防水卷材)"
    )

    sentence = "内 墙@@面^水、电、风井^水泥石灰砂浆^11J930--1/H3( 涂料面层不计)^11J930--1/H3( 涂料面层不计)"
    sentence = "1^屋顶^屋顶^1^挤塑聚苯板^50^08BJ1-1 平屋@@4^0.57"
    sentence = "坡道 坡道 水泥面层锯齿坡道 陕09J01-室外5-坡3 厨房及设备房入口处坡道 坡道扶手仿陕09J09-70-2"
    sentence = "详12J1-140页,屋105,用于住宅机房及楼梯间、门厅等屋面。"
    sentence = "外 墙^外墙9C 真石漆外墙面+涂306合成树脂乳液砂壁状建筑涂料^L13J1^颜色及样式仅供参考,用于风井、吊装孔外露墙面"
    sentence = "贴耐酸耐碱砖地面,参照05J909 -LD52-地49A 05J909"
    sentence = "外墙^12YJ1,外墙9B、C^外墙面^颜色见立面图"
    sentence = "地 面^客厅、卧室、书房、餐厅、楼梯间、电梯厅、阳台^水泥砂浆面^11J930-- 地@@1/G2"
    sentence = "12YJ1^细石混凝土屋面12YJ1屋103^上人"
    sentence = "12YJ1^内墙 8B@@面砖墙面"
    sentence = "台 1^开凹槽花岗石板台阶^12BJ1-1 台@@4B^商业出口台阶"
    sentence = "丙烯酸弹性高级涂料外墙面 13BJ2-12 外墙 H1@@涂料(丙烯酸)饰面 外墙 A1@@涂料(丙烯酸)饰面 地上外墙"
    sentence = "国标 10J121 第 H-1@@页@@2 散水以上至首层顶 板部分垂直墙面"
    sentence = "地 面^地101 水泥砂浆地面^L13J1^用于机修间和仓库"
    sentence = "内 墙^内墙1C 水泥砂浆墙面(涂304)^L13J1^用于机修间和仓库"
    # sentence = "12J1踢1(B)^楼梯间,电梯机房、"
    # sentence = "12J1内墙7(AF、BF)-F1 用于卫生间、厨房"
    sentence = "散3水泥砂浆散水^L13J1"
    sentence = "溶剂型氟碳树脂漆 国05J909-TL20-油32 漏明金属件 银白色"
    sentence = "地下室底板^10J301-16-底板1^4mm厚SBS改性沥青卷材"
    sentence = "楼 15 水泥砂浆楼面4@@(设备房、前室、走道)@@(回填大于300)^·20厚1:2(M20)水泥砂浆抹面压光 ·刷素水泥浆一道@@·80厚C15砼垫层@@·素土夯实(压实系数≥.94,回填至建筑完成面下100)@@·现浇钢筋砼楼板"
    sentence = "参12J1-117页,外墙16,第4条改为聚合物抗裂砂浆复合热镀锌电焊网,"
    sentence = "内墙1A水泥砂浆墙面+参涂304合成树脂乳液内墙涂料^L13J1^抹2mm厚柔性耐水腻子(分遍批刮磨平),刷白色涂料(防霉、防腐),用于23.500以下地下箱体砌体内墙"
    sentence = "丙烯酸弹性高级涂料外墙面^13BJ2-12^外墙 A1@@涂料(丙烯酸)饰面^外墙 A1@@涂料(丙烯酸)饰面^地上外墙^颜色参见立面图"
    # global_text = "建筑材料做法总说明注:套用《05J909》(国标:工程做法)"
    global_text = ""
    sentence = "散水^水泥面层散水^散3B^SW18(32)^宽度600"
    sentence = "混凝土坡道^12J6-1- 1^下设300mm中粗砂防冻层"
    sentence = "11J930--1/H3( 涂料面层不计)"
    sentence = "按柱网设分仓缝,做法参见01J304第4页3.08条。"
    sentence = "地面^素土夯实,200mm厚碎石垫层,150mmC30混凝土 面层,4-6mm厚非金属骨料耐磨地面面层。@@按柱网设分仓缝,做法参见01J304第4页3.08条。^地面与墙体及柱均 设20宽缝,采用泡@@沫塑料浇筑前隔开"
    sentence = "12J1-24-楼101(30厚)^楼梯间"
    sentence = "参12J1-117页,外墙16,第4条改为聚合物抗裂砂浆复合热镀锌电焊网,"
    sentence = "内墙面^釉面砖墙面12J1内墙 6-B,C^用于厨房"
    sentence = "12BJ1-1 03J203^平屋 ZZ-3@@P52页做法1.^平屋面 坡屋面^平屋面 坡屋面^正置式,保温层厚度 80mm"
    sentence = "顶1^水 泥@@砂@@浆@@顶@@棚^3).3厚1:2水泥砂浆抹平;^12J1 顶6-92 总厚度:8"
    # sentence = "面砖内墙面 12J-82-内墙8-B@@300*300^20mm"
    sentence = "暗散水护坡 构造做法详05J909@@-SW20-种植散水"
    #global_text = "工程做法表(选自陕标09J01)"
    sentence = "内墙面^设备间,管井,风井^毛坯墙面^内墙 4^卫生间及厨房墙面做防水砂浆一道四周高1800高 面层由主户自理"
    #sentence = "踢 脚^水泥砂浆楼地面^水泥砂浆踢脚^踢 2^高 150"
    # sentence = "散 水^全 部^水泥砂浆面层散水^散 2^宽 1500"
    sentence = "1.材料选用抗倍特; 2.做法及尺寸详见02J915第39页和第40页;^公共卫生间蹲便 及小便器隔断" 
    print(get_pre_picture(andidate_list, sentence, global_text))
