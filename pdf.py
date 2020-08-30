from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
import os
import csv

result_file = 'pdf_result.csv'
key_list = ['贸易摩擦', '贸易战', '出口', '境外', '美国', '进口']

file_list = os.listdir('pdf')

# csv文件头
csv_dic = {'文件名': '', '证券代码': '', '证券简称': '', '测试字段': ''}
for key in key_list:
    csv_dic[key] = ''
with open(result_file, 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, csv_dic.keys())
    w.writeheader()

for file in file_list:
    code_name = file.split('：')[0]
    code = code_name[:6]
    name = code_name[6:]
    print(file)
    print(code)
    print(name)

    # 不用上下文管理器的话，内存要爆掉
    with open('pdf/' + file, 'rb') as fp:
        dic = {'文件名': file, '证券简称': name, '证券代码': code}
        # 获取文档对象
        fp = open('pdf/' + file, 'rb')
        # 创建一个与文档关联的解释器
        parser = PDFParser(fp)
        # pdf文档的对象
        doc = PDFDocument()
        # 链接解释器和文档对象
        parser.set_document(doc)
        doc.set_parser(parser)
        # 初始化文档
        doc.initialize('')
        # 创建PDF资源管理器
        resource = PDFResourceManager()
        # 参数分析器
        las = LAParams()
        # 创建一个聚合器
        device = PDFPageAggregator(resource, laparams=las)
        # 创建PDF页面解释器
        interpreter = PDFPageInterpreter(resource, device)
        # 使用文档对象得到页面的集合

        # pdf 内容
        pdf_text = ''
        for page in doc.get_pages():
            # page 内容
            page_text = ''
            # 使用页面解释器来读取
            interpreter.process_page(page)
            # 使用聚合器来获得内容
            layout = device.get_result()
            for out in layout:
                # 需要注意的是在PDF文档中不只有 text 还可能有图片等等，为了确保不出错先判断对象是否具有 get_text()方法
                if hasattr(out, 'get_text'):
                    page_text = page_text + out.get_text()

            # 加入 page_text 为了避免在 pdf_text 做replace，避免太卡
            page_text = page_text.replace('\r', '').replace('\n', '').replace(' ', '')
            pdf_text = pdf_text + page_text

        print(len(pdf_text))
        dic['测试字段'] = str(pdf_text.count(name))
        for key in key_list:
            value = pdf_text.count(key)
            dic[key] = str(value)

        print(dic)
        with open(result_file, 'a') as f:
            w = csv.DictWriter(f, dic.keys())
            w.writerow(dic)
