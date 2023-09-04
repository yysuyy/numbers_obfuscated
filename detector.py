import os.path
from loguru import logger
import config
from utils.text_utils import is_chinese_string, is_alphabet_string
import re
from utils.tokenizer import Tokenizer, split_2_short_text
#
#
# class Detector(object):
#     def __init__(self, num_confusion_path=config.num_confusion_path):
#         self.initialized_detector = False
#         self.name = 'detector'
#         self.num_confusion_path = num_confusion_path
#         self.num_confusion = None
#         self.is_num_confusion = True
#
#     def _initialize_detector(self):
#         self.num_confusion = self.load_num_confusion(self.num_confusion_path)
#         self.tokenizer = Tokenizer(dict_path=self.num_confusion_path)
#
#     def check_detector_initialized(self):
#         if not self.initialized_detector:
#             self._initialize_detector()
#
#     @staticmethod
#     def load_num_confusion(path):
#         num_confusion = {}
#         if path:
#             if not os.path.exists(path):
#                 logger.warning('file not found.%s' % path)
#                 return num_confusion
#             else:
#                 with open(path, 'r', encoding='utf-8') as f:
#                     for line in f:
#                         info = line.strip()
#                         if line.startswith('#'):
#                             continue
#                         word = info[0]
#                         freq = int(info[1] if len(info) > 1 else 1)
#                         num_confusion[word] = freq
#         return num_confusion
#
#     @staticmethod
#     def is_filter_token(token):
#         """
#         是否为需过滤字词
#         :param token: 字词
#         :return: bool
#         """
#         result = False
#         # pass blank
#         if not token.strip():
#             result = True
#         # pass alpha
#         if is_alphabet_string(token.lower()):
#             result = True
#         # pass chinese
#         if is_chinese_string(token):
#             result = True
#         if not token.isdigit():
#             result = True
#         return result
#
#     @staticmethod
#     def _check_contain_error(maybe_err, maybe_errors):
#         error_word_idx = 0
#         begin_idx = 1
#         end_idx = 2
#         # 检测maybe_err是否在maybe_errors中
#         for err in maybe_errors:
#             if maybe_err[error_word_idx] in err[error_word_idx] and maybe_err[begin_idx] >= err[begin_idx] and \
#                     maybe_err[end_idx] <= err[end_idx]:
#                 return True
#         return False
#
#     def _add_maybe_error_item(self, maybe_err, maybe_errors):
#         if maybe_err not in maybe_errors and not self._check_contain_error(maybe_err, maybe_errors):
#             maybe_errors.append(maybe_err)
#
#     def detect(self, text):
#         maybe_errors = []
#         if not text.strip():
#             return maybe_errors
#         self.check_detector_initialized()
#         text.uniform(text)
#         sentences = split_2_short_text(text)
#         for sentence, idx in sentences:
#             maybe_errors += self.detect_sentence(sentence, idx)[0]
#         return maybe_errors
#
#     def detect_sentence(self, sentence, start_idx=0, **kwargs):
#         maybe_errors = []
#         proper_details = []
#         self.check_detector_initialized()
#         # 我1直都在思考这件事合不合理
#         if self.is_num_confusion:
#             tokens = self.tokenizer.tokenize(sentence, mode='search')
#             for token, begin_idx, end_idx in tokens:
#                 if self.is_filter_token(token):
#                     continue
#                 before_token = sentence[(begin_idx - start_idx - 1):(begin_idx - start_idx)]#数字的前一个字
#                 after_token = sentence[(end_idx - start_idx+1):(end_idx - start_idx + 2)]#数字的后一个字
#                 before_token1 = sentence[(begin_idx - start_idx - 2):(begin_idx - start_idx)]
#                 after_token1 = sentence[(end_idx - start_idx+1):(end_idx - start_idx + 2)]
#                 for test in self.num_confusion:
#                     for i in range(len(test)):
#                         if len(test) == 2:
#                             if test[i] ==before_token or test[i] ==after_token:
#                                 maybe_err = [token,begin_idx + start_idx,end_idx + start_idx]
#                                 self._add_maybe_error_item(maybe_err,maybe_errors)
#                         else:
#                             if(test[i:i+2]) == before_token1 or test[i:(i+2)] == after_token1 or (test[i] == before_token and test[i+2] == after_token):
#                                 maybe_err = [token, begin_idx + start_idx, end_idx + start_idx]
#                                 self._add_maybe_error_item(maybe_err, maybe_errors)
#         return sorted(maybe_errors, key=lambda k: k[1], reverse=False), proper_details
#
#
# # 另一种思路，找出有问题的句子，利用cn2an工具包直接进行数字转中文
#
# if __name__ == '__main__':
#     detect = Detector()
#     detect.detect('长征1号')
#     # idx_errors = detect()
#     # 长征1号 长征一号
#     print(detect.detect('长征1号'))

import re,cn2an
f =open('./data/confusion.txt','r',encoding='utf-8')
lines = f.readlines()
def detect(text):
    maybe_errors = {}
    if not text.strip():
        return maybe_errors
    sentences =split_2_short_text(text)
    for sentence in sentences:
        for line in lines:
            line = line.strip()
            line_str = ''.join(line)
            if re.findall(line_str,sentence[0])!= []:
                rp = re.search(line_str,sentence[0])
                rp_str = ''.join(rp.group())
                rp_trans = cn2an.transform(rp_str,"an2cn")
                maybe_errors[rp_str] = rp_trans
    print(maybe_errors)
detect('提高1029成')



