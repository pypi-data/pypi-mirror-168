from ml_util.MLComponentBase import MLComponentBase
from code_util.structures import func_check
import re, os


# class default_bert(MLComponentBase):
#
#     def __init__(self):
#         super().__init__(["transformers"])
#         self.TFAutoModel = getattr(self['transformers'], 'TFAutoModel')
#         self.AutoTokenizer = getattr(self['transformers'], 'AutoTokenizer')
#
#         self.model_name = "hfl/chinese-electra-180g-small-discriminator"
#         self.tokenizer_lib_name = "hfl/chinese-electra-180g-small-discriminator"
#
#         self.model = None
#         self.tokenizer = None
#
#     def load_model(self, model_path):
#         if self.model is not None:
#             return
#
#         bert_model_path = os.path.join(model_path, "default_bert_model")
#         tokenizer_model_path = os.path.join(model_path, "default_bert_toeknizer")
#
#         if not os.path.exists(bert_model_path):
#             self.model = self.TFAutoModel.from_pretrained(self.model_name)
#             _ = self.model.save_pretrained(bert_model_path)
#         else:
#             self.model = self.TFAutoModel.from_pretrained(bert_model_path)
#
#         if not os.path.exists(tokenizer_model_path):
#             self.tokenizer = self.AutoTokenizer.from_pretrained(self.tokenizer_lib_name)
#             _ = self.tokenizer.save_pretrained(tokenizer_model_path)
#         else:
#             self.tokenizer = self.AutoTokenizer.from_pretrained(tokenizer_model_path)
#
#     @func_check
#     def call(self, linked_item: [str], ori_item=None):
#         vector = self.model(**linked_item).last_hidden_state
#         return vector.numpy()
