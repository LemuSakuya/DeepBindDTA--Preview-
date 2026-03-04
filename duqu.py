import csv   
import pandas as pd
def duqudrug(names, input_file):   
    output_file = 'Case/drug.tsv'  
    target_name = names  # 你想要查找的名字  
    found = False  # 初始化一个标志，用于判断是否找到了目标行  
    df = pd. read_csv (input_file, sep="\t")
    found = df.iloc[:, 0].str.contains(target_name, na=False).any()  
    if found:  
        # 找到目标名字所在的行  
        matching_rows = df[df.iloc[:, 0].str.contains(target_name, na=False)]  
        # 将找到的行保存到输出文件  
        matching_rows.to_csv(output_file, sep='\t', index=False, encoding='utf-8')  
        print(f"已将 {input_file} 中名字为 {target_name} 的行保存到 {output_file}")  
    else:  
        print(f"在 {input_file} 中未找到名字为 {target_name} 的行")  

def protdrug1(names, input_file):
    output_file = 'Case/prot.tsv'  
    target_name = names  # 你想要查找的名字  
    found = False  # 初始化一个标志，用于判断是否找到了目标行  
    df = pd. read_csv (input_file, sep=",")
    found = df.iloc[:, 0].str.contains(target_name, na=False).any()  
    if found:  
        # 找到目标名字所在的行  
        matching_rows = df[df.iloc[:, 0].str.contains(target_name, na=False)]  
        # 将找到的行保存到输出文件  
        matching_rows.to_csv(output_file, sep='\t', index=False, encoding='utf-8')  
        print(f"已将 {input_file} 中名字为 {target_name} 的行保存到 {output_file}")  
    else:  
        print(f"在 {input_file} 中未找到名字为 {target_name} 的行")


def protdrug(names, input_file):
    output_file = 'Case/prot.tsv'
    target_name = names  # 你想要精确查找的名字
    df = pd.read_csv(input_file, sep=",")

    # 检查第一列是否精确包含目标名字
    found = (df.iloc[:, 0] == target_name).any()

    if found:
        # 找到目标名字所在的行
        matching_rows = df[df.iloc[:, 0] == target_name]
        # 将找到的行保存到输出文件
        matching_rows.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
        print(f"已将 {input_file} 中名字为 {target_name} 的行保存到 {output_file}")
    else:
        print(f"在 {input_file} 中未找到名字为 {target_name} 的行")