#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from janome.tokenizer import Tokenizer
import tools

tokenizer = Tokenizer()

# 品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
_mecab_feat_labels = 'pos cat1 cat2 cat3 conj conj_t orig read pron'.split(' ')


def _mecab_parse_feat(feat):
    return dict(zip(_mecab_feat_labels, feat.split(',')))


def _mecab_node2seq(node, decode_surface=True, feat_dict=True,
                    mecab_encoding='utf-8'):
    # MeCab.Nodeはattributeを変更できない。
    while node:
        if decode_surface:
            node._surface = node.surface.decode(mecab_encoding)
        if feat_dict:  # 品詞の情報をdictで保存
            node.feat_dict = _mecab_parse_feat(
                node.feature.decode(mecab_encoding)
            )
        yield node
        node = node.next


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


def _node2word(n):  # <- mecab node
    return n.surface


def _node2norm_word(n):  # mecab node
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
