import operator
import config
from utils.tokenizer import split_2_short_text
import random
from detector import Detector

num_dict = {0: "零", 1: "一", 2: "二", 3: "三", 4: "四",
            5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
unit_map = [["", "十", "百", "千"], ["万", "十万", "百万", "千万"],
            ["亿", "十亿", "百亿", "千亿"], ["兆", "十兆", "百兆", "千兆"]]
unit_step = ["万", "亿", "兆"]

class Corrector(Detector):
    def __init__(self,num_confusion_path=config.num_confusion_path):
        super(Corrector,self).__init__(num_confusion_path=num_confusion_path)
        self.name='corrector'
        self.initialized_corrector = False
        self.result = ""
    def _initialize_corrector(self):
        self.initialized_corrector = True
    def check_corrector_initialized(self):
        if not self.initialized_corrector:
            self._initialize_corrector()
    def number_to_str_10000(self,data_str):
        res = []
        count = 0
        str_rev = reversed(data_str)
        for i in str_rev:
            if i is not "0":
                count_cos=count//4
                count_col=count%4
                res.append(unit_map[count_cos][count_col])
                res.append(num_dict[int(i)])
                count +=1
            else:
                count +=1
                if not res:
                    res.append("零")
                elif res[-1] is not "零":
                    res.append("零")
        res.reverse()
        if res[-1] is '零' and len(res) is not 1:
            res.pop()
        return "".join(res)
    def number_to_str(self,data):
        assert type(data) ==float or int
        data_str = str(data)
        len_data=len(data_str)
        count_cos=len_data //4
        count_col=len_data -count_cos*4
        if count_col>0:
            count_cos += 1
        res=""
        for i in range(count_cos):
            if i ==0:
                data_in =data_str[-4:]
            elif i==count_cos -1 and count_col >0:
                data_in = data_str[:count_col]
            else:
                data_in = data_str[-(i+1) *4:-(i*4)]
            res_ = self.number_to_str_10000(data_in)
            if "0000" ==data_in:
                continue
            res = res_ + unit_map[i][0] +res
        return res
    def decimal_chinese(self,data):
        assert type(data) == float or int
        data_str = str(data)
        if "." not in data_str:
            res = self.number_to_str(data_str)
        else:
            data_str_split = data_str.split('.')
            if len(data_str_split) is 2:
                res_start = self.number_to_str(data_str_split[0])
                res_end = "".join([num_dict[int(number)] for number in data_str_split[1]])
                res=res_start + random.sample(["点","."],1)[0] + res_end
            else:
                res = str(data)
        return res


    def correct(self,text,include_symbol=True,**kwargs):
        text_new=''
        details=[]
        self.check_corrector_initialized()
        sentences=split_2_short_text(text,include_symbol=include_symbol)
        for sentence,idx in sentences:
            maybe_errors,proper_details = self.detect_sentence(sentence,idx,**kwargs)
            for cur_item,begin_idx,end_idx in maybe_errors:
                before_sent = sentence[:(begin_idx-idx)]
                after_sent = sentence[(end_idx - idx):]
                chinese_num = self.decimal_chinese(cur_item)
                if list(chinese_num)[0]=='一' and list(chinese_num)[1]=='十':
                    chinese_num = chinese_num[1:]
                    sentence = before_sent + chinese_num +after_sent
                else:
                    sentence = before_sent + chinese_num + after_sent
                details_word = (cur_item,chinese_num,begin_idx,end_idx)
                details.append(details_word)
            text_new+=sentence
        details = sorted(details,key=operator.itemgetter(2))
        return text_new,details





