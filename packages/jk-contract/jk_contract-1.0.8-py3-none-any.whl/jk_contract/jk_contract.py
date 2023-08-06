# -*- coding: GBK -*-

import sys
import os

from docx2python import docx2python
from pathlib import Path
import regex
import re

import pandas as pd
import numpy as np

from .regex_dictionary import get_chapter_beg_end
from .regex_dictionary import get_chapter_regex
from .regex_dictionary import get_section_beg_end
from .regex_dictionary import get_section_regex

class Contract:
    def __init__(self, path):
        print(path)
        self.exp = '(华泰)|(招商)(?!银行)|(中信)(?!建投)|(国信)|(广发)|(海通)|(申万)|(光大)|(平安)|(国君)|(兴业)|(招行)|(招)(?:商银)(行)|(建投)'
        self.path = path
        self.product_name = regex.search('(九坤|方达).+?基金', path).group()
        self.document = docx2python(path)
        self.full_text = ''
        for table in self.document.body:
            for row in table:
                for cell in row:
                    for para in cell:
                        self.full_text += para
        try:
            self.tg = ''.join(filter(None,regex.search(self.exp, path).groups()))
        except:
            self.tg = ''

    def get_front_page(self):
        firstpages = {"光大":25,"平安":25,"招商":28,"海通":18,"申万":22,"国信":19,"广发":0,"国君":25,"中信":28,"华泰":23}
        return firstpages[self.tg]

    def get_risk_level(self):
        try:
            return re.search("R[0-9]",re.search("本基金属于[^。]+合格投资者", self.full_text).group()).group()
        except:
            return ""

    def get_full_text(self):
        return self.full_text

    def get_chapter(self, chapter): #works
        beg_chapter_name = get_chapter_beg_end(self.tg, chapter)[0][0]
        end_chapter_name = get_chapter_beg_end(self.tg, chapter)[0][1]
        chapter_regex = get_chapter_regex(self.tg, beg_chapter_name, end_chapter_name)
        try:
            self.chapter = regex.search(chapter_regex, self.full_text).group()
            return self.chapter
        except:
            return 'No Regex Matches'
            

    def get_section_of_chapter(self, chapter, section):
        chapter = self.get_chapter(chapter)
        beg_section_name = get_section_beg_end(self.tg, section)[0][0]
        end_section_name = get_section_beg_end(self.tg, section)[0][1]
        section_regex = get_section_regex(self.tg, beg_section_name, end_section_name)
        try:
            self.section = regex.search(section_regex, chapter).group()
            if self.section[0] == '：':
                self.section = self.section.replace('：','')
            return self.section
        except:
            return 'No Regex Matches'

    # def to_pdf(): #under construnction, same as Contracts method, but only exports pdf of one contract document

class Contracts:
    def __init__(self, folder_path):
        self.exp = '(华泰)|(招商)(?!银行)|中信|(中信)(?!建投)|(国信)|(广发)|(海通)|(申万)|(光大)|(平安)|(国君)|(兴业)|(招行)|(招)(?:商银)(行)|(建投)'
        self.folder_path = folder_path
        self.all_files = []
        self.tg = []
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                if ('output' not in path) and ('docx' or 'doc' in path) and ('补充协议' not in path):
                    try:
                        self.tg.append(''.join(filter(None,regex.search(self.exp, path).groups())))
                        self.all_files.append(path)
                    except:
                        print('目前只支持：华泰|招商|中信建投|国信|广发|海通|申万|光大|平安|国君|兴业|招行|建投的word文档，其他托管的产品将会被忽略。')
                else:
                    pass
    def get_chapters(self, chapter_names):
        out = {}
        for file_path in self.all_files:
            contract = Contract(file_path)
            if contract.tg!='广发': out[contract.product_name] = [contract.get_chapter(chapter_name).replace('\t', ' ').replace('\n', '') for chapter_name in chapter_names]
        return out, chapter_names
    
    def get_sections(self, chapter_name, section_names):
        out = {} #dict(per tg) of list(per product) of list(per regex expression)
        for file_path in self.all_files:
            contract = Contract(file_path)
            if contract.tg!='广发': out[contract.product_name] = [contract.get_section_of_chapter(chapter_name, section_name).replace('\t', ' ').replace('\n', '') for section_name in section_names]
        return out, section_names
        
    def get_df(self, dict):
        data = dict[0]
        names = list(data.keys())
        matrix = np.array([data[product] for product in names])
        df = pd.DataFrame(matrix, index=[names], columns=list(dict[1]))
        return df
    
    def to_excel(self, df, out_path):
        abs_path = Path(out_path).absolute()
        df.to_excel(out_path)
        print(f'Spreadsheet successfully exported to {abs_path}.')
        return df

    # def to_pdf(self, regex): under construction, to include functions from strategy_extract to export pdf of only regexed contents

# in_path = sys.argv[1]
# out_path = sys.argv[2]
# chapter = sys.argv[3]
# sections = list(sys.argv[4:])

# def main():
#     contracts = Contracts(in_path)
#     contracts.to_excel(contracts.get_df(contracts.get_sections(chapter, sections)), out_path) # works

# if __name__=='__main__':

    ### single contract class
    # contract = Contract('/Users/andy/Desktop/work/ubiquant/合同提取/首页和投资策略提取/申万/九坤交易精选2号私募证券投资基金基金合同托管版-根据第一次补充协议更新（投资端含打新）V1.2.8TX-20210302（清洁稿）.docx')
    # print(contract.get_chapter('基金的投资'))
    # print(contract.get_section_of_chapter('基金的投资','投资限制'))

    ### folder of contracts class
    
    # main()