#-*- coding=utf-8 -*-

'''
Created on Mar 1, 2016

@author: enming.zhang

All files which this scripr can handler is must be encoding in utf-8
'''

import re

class batch_handler:
    m_ThostFtdcReq_list = []
    CThostFtdc_list     = []
    functions_list      = []
    Old_FemasTHelper_cpp_file_line_list = []
    
    m_ThostFtdcReq_CThostFtdc_dict = {}
    CThostFtdc_m_ThostFtdcReq_dict = {}
    Fields_Relation_dict = {}
    Functions_Relation_dict = {}
    
    The_InitMember_pos = 0
    
    '''
    get the content we need from FemasTHelper.h
    '''
    def extract_m_ThostFtdcReq_and_CThostFtdc_and_functions(self):
        FemasTHelper_h_file = open("FemasTHelper.h", 'r')
        
        '''
        analysis every line in FemasTHelper.h 
        '''
        FemasTHelper_h_line = FemasTHelper_h_file.readline()
        
        while FemasTHelper_h_line:
            FemasTHelper_h_match_object = re.findall("m_ThostFtdcReq\w+", FemasTHelper_h_line)   
            if FemasTHelper_h_match_object != []:
                self.m_ThostFtdcReq_list.extend(FemasTHelper_h_match_object)
                CThostFtdc_match_object = re.findall("CThostFtdc\w+", FemasTHelper_h_line)
                self.CThostFtdc_list.extend(CThostFtdc_match_object)
                self.m_ThostFtdcReq_CThostFtdc_dict[FemasTHelper_h_match_object[0]] = CThostFtdc_match_object[0]
                self.CThostFtdc_m_ThostFtdcReq_dict[CThostFtdc_match_object[0]] = FemasTHelper_h_match_object[0]
            
            FemasTHelper_h_match_object_2 = re.findall("OnRsp(\w+)", FemasTHelper_h_line)
            if FemasTHelper_h_match_object_2 != []:
                self.functions_list.extend(FemasTHelper_h_match_object_2)
            
            FemasTHelper_h_line = FemasTHelper_h_file.readline()
            
        FemasTHelper_h_file.close()
        
    '''
    get the content we need from ThostFtdcTraderApi.h
    '''
    def ThostFtdcTraderApi_h_parser(self, key_char):
        ThostFtdcTraderApi_h_line_prev = ""
        ThostFtdcTraderApi_h_file = open("ThostFtdcTraderApi.h", 'r')
        ThostFtdcTraderApi_h_line = ThostFtdcTraderApi_h_file.readline()
        while ThostFtdcTraderApi_h_line:
            ThostFtdcTraderApi_h_match_object = re.findall("Req" + key_char, ThostFtdcTraderApi_h_line)
            if ThostFtdcTraderApi_h_match_object != [] and re.findall("virtual", ThostFtdcTraderApi_h_line) != []:
                every_function_list = []
                '''
                the format should be:
                /// comment
                var declaration
                '''
                comment_match_object = re.findall(r"///([\x80-\xff','', '\w\d'/']+)", ThostFtdcTraderApi_h_line_prev)
                if comment_match_object != []:
                    every_function_list.extend(comment_match_object)
                else:
                    print "the function has no comment"
                    every_function_list.append(" ")
                param_match_object = re.findall("CThostFtdc\w+", ThostFtdcTraderApi_h_line)
                if param_match_object != []:
                    every_function_list.extend(param_match_object)
                
                self.Functions_Relation_dict["Req" + key_char] = every_function_list
            
                break
            ThostFtdcTraderApi_h_line_prev = ThostFtdcTraderApi_h_line
            ThostFtdcTraderApi_h_line = ThostFtdcTraderApi_h_file.readline()
        
        ThostFtdcTraderApi_h_file.close()        
        
    def extract_need_functions(self):
        for function_ele in self.functions_list:
            self.ThostFtdcTraderApi_h_parser(function_ele)
    
    '''
    get the content we need from ThostFtdcUserApiStruct.h
    '''
    def ThostFtdcUserApiStruct_h_parser(self, key_char):
        struct_element_list = []
        ThostFtdcUserApiStruct_h_file = open("ThostFtdcUserApiStruct.h", 'r')
        ThostFtdcUserApiStruct_h_line = ThostFtdcUserApiStruct_h_file.readline()
        while ThostFtdcUserApiStruct_h_line:
            ThostFtdcUserApiStruct_h_match_object = re.findall(key_char, ThostFtdcUserApiStruct_h_line)
            if ThostFtdcUserApiStruct_h_match_object != [] and re.findall("struct", ThostFtdcUserApiStruct_h_line) != []:
                '''
                the format should be:
                /// comment
                var declaration
                '''
                ThostFtdcUserApiStruct_h_line = ThostFtdcUserApiStruct_h_file.readline()
                while ThostFtdcUserApiStruct_h_line != "};\n": 
                    comment_match_object = re.findall(r"///([\x80-\xff','', '\w\d'/']+)", ThostFtdcUserApiStruct_h_line)
                    if comment_match_object != []:
#                        tmp_str = unicode(comment_match_object[0], "ascii")
                        every_line_list = []
                        every_line_list.extend(comment_match_object)
                    
                        ThostFtdcUserApiStruct_h_line = ThostFtdcUserApiStruct_h_file.readline()
                        declaration_match_object = re.findall("[\\t' ']+(.*?)[\\t' ']+(.*?);", ThostFtdcUserApiStruct_h_line)
                        if declaration_match_object != []:
                            every_line_list.append(declaration_match_object[0][0])
                            every_line_list.append(declaration_match_object[0][1])
                            struct_element_list.append(every_line_list)
                    ThostFtdcUserApiStruct_h_line = ThostFtdcUserApiStruct_h_file.readline()
                break
            ThostFtdcUserApiStruct_h_line = ThostFtdcUserApiStruct_h_file.readline()
        self.Fields_Relation_dict[key_char] = struct_element_list
        ThostFtdcUserApiStruct_h_file.close()
        
    def extract_need_fields(self):      
        for field_ele in self.CThostFtdc_list:
            self.ThostFtdcUserApiStruct_h_parser(field_ele)

    '''
    convert the content of FemasTHelper.cpp into a list
    '''
    def transition_content_in_cpp_to_list(self):
        self.Old_FemasTHelper_cpp_file_line_list = []
        FemasTHelper_cpp_file = open("FemasTHelper.cpp", 'r')
        FemasTHelper_cpp_line = FemasTHelper_cpp_file.readline()
        
        while FemasTHelper_cpp_line:
            self.Old_FemasTHelper_cpp_file_line_list.append(FemasTHelper_cpp_line)
            FemasTHelper_cpp_line = FemasTHelper_cpp_file.readline()
        FemasTHelper_cpp_file.close()
    
    '''
    update the FemasTHelper.cpp
    '''
    def update_FemasTHelper_cpp_file(self):
        Input_Content = ''.join(self.Old_FemasTHelper_cpp_file_line_list)
        FemasTHelper_cpp_file = open("FemasTHelper.cpp", 'r+')
        FemasTHelper_cpp_file.seek(0)
        FemasTHelper_cpp_file.write(Input_Content)
        FemasTHelper_cpp_file.close()
        
        
    '''
    update InitMembers
    '''
    def update_InitMembers(self):
        self.transition_content_in_cpp_to_list()
        self.The_InitMember_pos = 0
        for line in self.Old_FemasTHelper_cpp_file_line_list:
            if (re.search("InitMembers", line) != None):
                self.The_InitMember_pos += 1
                '''
                clear the current content of InitMembers
                '''
                Need_Delete_line = self.The_InitMember_pos
                while self.Old_FemasTHelper_cpp_file_line_list[Need_Delete_line] != "}\n":
                    self.Old_FemasTHelper_cpp_file_line_list.pop(Need_Delete_line)
                self.Old_FemasTHelper_cpp_file_line_list.pop(Need_Delete_line)
    
        
                '''
                insert the updating content into InitMembers
                '''
                self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "{\n")
                self.The_InitMember_pos += 1
                for ele in self.m_ThostFtdcReq_list:
                    self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "\tZeroMemory(&" + ele + ", sizeof(" + ele + "));\n")
                    self.The_InitMember_pos += 1
                self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "}\n")
                break;
            else:
                self.The_InitMember_pos += 1
        
        self.update_FemasTHelper_cpp_file()
        
        
    '''
    update the InitFields
    '''
    def update_InitFields(self):
        self.transition_content_in_cpp_to_list()
        self.The_InitMember_pos = 0
        for line in self.Old_FemasTHelper_cpp_file_line_list:
            if (re.search("InitFields", line) != None):
                self.The_InitMember_pos += 1
                '''
                clear the current content of InitFields
                '''
                Need_Delete_line = self.The_InitMember_pos
                while self.Old_FemasTHelper_cpp_file_line_list[Need_Delete_line] != "}\n":
                    self.Old_FemasTHelper_cpp_file_line_list.pop(Need_Delete_line)
                self.Old_FemasTHelper_cpp_file_line_list.pop(Need_Delete_line)
                
                '''
                insert the updating content into InitFields
                '''
                self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "{\n")
                self.The_InitMember_pos += 1
                for ele in self.CThostFtdc_list:
                    if self.Fields_Relation_dict.has_key(ele):
                        for declaration_var_ele in self.Fields_Relation_dict[ele]:
                            self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "\tRegField(\"" + ele + "\",\"" + 
                                                                            declaration_var_ele[0] + "\",\"" + declaration_var_ele[1] +
                                                                            "\", \"" + declaration_var_ele[2] + "\", &(" + 
                                                                            self.CThostFtdc_m_ThostFtdcReq_dict[ele] + "." + declaration_var_ele[2]
                                                                            + "));\n")
                            self.The_InitMember_pos += 1
                        self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "\n")
                        self.The_InitMember_pos += 1
                            
                    else:
                        print "Extract ThostFtdcUserApiStruct.h Error"
                        return False
                self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "}\n")
                break
            else:
                self.The_InitMember_pos += 1
                
        self.update_FemasTHelper_cpp_file()
    
    '''
    update InitFunctions
    '''
    def update_InitFunctions(self):
        self.transition_content_in_cpp_to_list()
        self.The_InitMember_pos = 0
        for line in self.Old_FemasTHelper_cpp_file_line_list:
            if (re.search("InitFunctions", line) != None):
                self.The_InitMember_pos += 1
                '''
                clear the current content of InitFields
                '''
                Need_Delete_line = self.The_InitMember_pos
                while self.Old_FemasTHelper_cpp_file_line_list[Need_Delete_line] != "}\n":
                    self.Old_FemasTHelper_cpp_file_line_list.pop(Need_Delete_line)
                self.Old_FemasTHelper_cpp_file_line_list.pop(Need_Delete_line)
                
                '''
                insert the updating content into InitFields
                '''
                self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "{\n")
                self.The_InitMember_pos += 1
                for ele in self.functions_list:
                    if self.Functions_Relation_dict.has_key("Req" + ele):
                        self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "\tRegFun(m_pMainDlg->m_pList->InsertString(-1, \"" + self.Functions_Relation_dict["Req" + ele][0] +
                                                                        "\"), \"" + "Req" + ele + "\", std::function<int(int)>(std::bind(&CThostFtdcTraderApi::" + "Req" + ele + ", m_pTraderApi, &" + 
                                                                        self.CThostFtdc_m_ThostFtdcReq_dict[self.Functions_Relation_dict["Req" + ele][1]] + ", std::placeholders::_1)), \""
                                                                        + self.Functions_Relation_dict["Req" + ele][1] + "\");\n")
                        self.The_InitMember_pos += 1
                    else:
                        print "Extract ThostFtdcTraderApi.h Error"
                        return False
                self.Old_FemasTHelper_cpp_file_line_list.insert(self.The_InitMember_pos, "}\n")
                break
            else:
                self.The_InitMember_pos += 1
                
        self.update_FemasTHelper_cpp_file()
    
    
    
if __name__ == "__main__":
    ctp_handler = batch_handler()
    #解析FemasTHelper.h文件
    ctp_handler.extract_m_ThostFtdcReq_and_CThostFtdc_and_functions()
    #解析ThostFtdcUserApiStruct.h文件
    ctp_handler.extract_need_fields()
    #解析ThostFtdcTraderApi.h文件
    ctp_handler.extract_need_functions()
    #更新InitMembers函数
    ctp_handler.update_InitMembers()
    #更新InitFields()函数
    ctp_handler.update_InitFields()
    #更新InitFunctions()函数
    ctp_handler.update_InitFunctions()
    
    print "Updated FemasTHelper.cpp"

