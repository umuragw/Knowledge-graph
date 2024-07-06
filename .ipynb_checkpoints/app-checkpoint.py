import streamlit as st
from module import run_spider # 假设你已经有一个爬虫模块
import pandas as pd
import csv
import pandas as pd
from py2neo import Graph, Node, Relationship

# 设置Streamlit页面标题
st.title('知识图谱爬虫自动生成器平台')

# 获取用户输入
url = st.text_input('请输入目标网站URL', '')

# 爬虫参数设置（根据需要调整）
if st.button('开始爬取'):
    if url:
        # 执行爬虫任务
        data = run_spider(url)
        # 显示爬取结果
        st.write(data)
    else:
        st.error('请输入有效的URL')

if st.button('构建知识图谱'):
    # 读取 xlsx 文件
    df = pd.read_excel('input3.xlsx')

    # 将 DataFrame 写入 csv 文件（确保编码设置正确，例如 'utf-8'）
    df.to_csv('input3.csv', index=False, encoding='utf-8')
    import jiagu
    import py2neo

    # 连接本地 Neo4j 图数据库
    graph = Graph('http://localhost:7474', user='neo4j', password='ws20210602', name="neo4j")
    graph.delete_all()

    # 构建知识图谱
    with open('input3.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for item in reader:
            if reader.line_num == 1:  # 过滤掉第 1 列（0， 1， 2）
                continue
            print("当前行数: ", reader.line_num, "当前内容: ", item)
            start_node = Node("姓名", name=item[0])
            end_node = Node("属性值", value=item[2])
            relation = Relationship(start_node, item[1], end_node)

            graph.merge(start_node, "姓名", "name")
            graph.merge(end_node, "属性值", "value")
            graph.merge(relation, "值", "属性")
    st.success('知识图谱已成功创建！')
    st.markdown("点击[这里](http://localhost:7474)在新标签页中查看知识图谱。")
