#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import re
import json
import subprocess


def tree_encode(obj, encoding='utf-8'):
    type_ = type(obj)
    if type_ == list or type_ == tuple:
        return [tree_encode(e, encoding) for e in obj]
    elif type_ == dict:
        new_obj = dict(
            (tree_encode(k, encoding), tree_encode(v, encoding))
            for k, v in obj.iteritems()
        )
        return new_obj
    elif type_ == unicode:
        return obj.encode(encoding)
    else:
        return obj


def ppj(obj, sort_keys=False):
    obj_str = json.dumps(
        tree_encode(obj), indent=2, ensure_ascii=False, sort_keys=sort_keys
    )
    print obj_str


def fix_paren_sents(sents):
    '''
    sent_splitter_jaでは、
    "太郎は「明日は晴れるだろう。」といった。"
        -> ["太郎は「明日は晴れるだろう。", "」といった。"]
    に分割される。

    この関数はカッコの対応を見て、文を境界を修正する。
    exmaple:
      sents = ["太郎は「明日は晴れるだろう。", "」といった。"]
      returns ["太郎は「明日は晴れるだろう。」といった。"]
    '''
    # 開いた括弧は必ず閉じる．
    # 全角（） -> 半角()
    sents = [s.replace(u'（', u'(').replace(u'）', u')') for s in sents]
    parenthesis = u'（）「」『』()'
    close2open = dict(zip(parenthesis[1::2], parenthesis[0::2]))
    fixed_sents = []
    pstack = []
    buff = u''
    for sent in sents:
        pattern = re.compile(u'[' + parenthesis + u']')
        ps = re.findall(pattern, sent)
        if len(ps) > 0:
            for p in ps:
                if p in close2open.values():
                    # open
                    pstack.append(p)
                elif len(pstack) > 0 and pstack[-1] == close2open[p]:
                    # close
                    pstack.pop()
        # ここでpstackが空なら括弧の対応がとれている．
        if len(pstack) == 0:
            buff += sent
            if len(buff) > 0:
                fixed_sents.append(buff)
            buff = u''
        else:
            buff += sent
    if len(buff) > 0:
        fixed_sents.append(buff)

    return fixed_sents


def sent_splitter_ja(text, fix_paren=True):  # type(text) == unicode
    sents = re.sub(ur'([。．？！\n\r]+)', r'\1|', text).split('|')
    sents = [s for s in sents if len(s) > 0]
    if fix_paren:
        sents = fix_paren_sents(sents)
    return sents


def l2norm(xs):
    return math.sqrt(sum(x * x for x in xs))


def cos_sim(v1, v2):
    if len(v1) == 0 or len(v2) == 0:
        return 0
    a = 0
    for k in v1:
        a += v1[k] * (v2[k] if k in v2 else 0)
    b = l2norm(v1.values()) * l2norm(v2.values())
    return a / b
