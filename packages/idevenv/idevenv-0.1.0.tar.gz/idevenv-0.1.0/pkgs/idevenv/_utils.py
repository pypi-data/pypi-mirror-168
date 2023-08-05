# -*- coding: utf-8 -*-
import pprint
pp = pprint.PrettyPrinter(indent=2)


# idebug 패키지에 이미 존재.
# 단, site-packages 설치없이 사용하기 위해서 복사해서 붙여넣음
def pretty_title(s, simbol='*', width=100):
    space = " " * int((width - len(s)) / 2)
    line = simbol * width
    print(f"{line}\n{space}{s}{space}\n{line}")
