# _*_ coding : utf-8 _*_
# @Time : 2022/9/21 16:13
# @Author : 上应大高美珠
# @File : 12 
# @Project : sztestlib
def print_lol(movies):
    for item1 in movies:
        if isinstance(item1,list):
            print_lol(item1)
        else:
            print(item1)

movies = ["THE H G",1975,"TJ & TG",91,["gc",["M P","JC","TG","EI","TJ"]]]
# print_lol(movies)