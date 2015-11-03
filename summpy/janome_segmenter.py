#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from janome.tokenizer import Tokenizer
import tools

tokenizer = Tokenizer()


def is_stopword(n):  # <- mecab node
    if len(n.surface) == 0:
        return True
    elif re.search(r'^[\s!-@\[-`\{-~　、-〜！-＠［-｀]+$', n.surface):
        return True
    elif re.search(r'^(接尾|非自立)', n.part_of_speech.split(',')[1]):
        return True
    elif 'サ変・スル' == n.infl_form or 'ある' == n.base_form:
        return True
    elif re.search(r'^(名詞|動詞|形容詞)', n.part_of_speech.split(',')[0]):
        return False
    else:
        return True


def not_stopword(n):
    return not is_stopword(n)


def _node2word(n):  # <- janome token node
    return n.surface.encode('utf-8')


def _node2norm_word(n):  # janome token node
    if n.base_form != '*':
        return n.base_form
    else:
        return n.surface.encode('utf-8')


def word_segmenter_ja(sent, node_filter=not_stopword,
                      node2word=_node2norm_word):
    nodes = tokenizer.tokenize(sent)

    if node_filter:
        nodes = [n for n in nodes if node_filter(n)]
    words = [node2word(n) for n in nodes]

    return words


def test_janome():
    text = u'今日はいい天気ですね。太郎は今日学校に行こうとしています。'
    sents = tools.sent_splitter_ja(text)
    for s in sents:
        ws = word_segmenter_ja(s)
        print '|'.join(ws)

if __name__ == '__main__':
    test_janome()
