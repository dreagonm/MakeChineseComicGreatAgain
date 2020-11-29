import jieba
from gensim import corpora, models, similarities
from Bullet.models import WordBullet


def get_custom_stopwords(stop_words_file):
    with open(stop_words_file, encoding='utf-8') as f:
        stopwords = f.read()

    stopwords_list = stopwords.split('\n')
    # custom_stopwords_list = [i for i in stopwords_list]

    return stopwords_list


def cut(text, stopwords):
    generator = [[i for i in jieba.lcut(item)] for item in text]
    l1 = []
    for word_list in generator:
        l2 = [word for word in word_list if word not in stopwords]
        l1.append(l2)
    return l1


def bullet_get(objs):
    bullet_dic = {}
    for obj in objs:
        message = {
            'bullet': obj.bullet,
            'typeface': obj.typeface,
            'color': obj.color,
            'type': obj.get_type_display(),
            'size': obj.size
        }
        bullet_dic['%s' % obj.id] = message
    return bullet_dic


def Re_Check(test_text):
    # 文本重复性检测，大于80%的文本不可通过 注：待优化
    stop_words_path = 'stop_words.txt'
    custom_stopwords_list = get_custom_stopwords(stop_words_path)
    objs = WordBullet.objects.all()

    base_data = [i.bullet for i in objs]

    base_items = cut(base_data, custom_stopwords_list)

    dictionary = corpora.Dictionary(base_items)

    corpus = [dictionary.doc2bow(item) for item in base_items]

    tf = models.TfidfModel(corpus)

    num_features = len(dictionary.token2id.keys())

    index = similarities.MatrixSimilarity(tf[corpus], num_features=num_features)

    test_words = [word for word in jieba.cut(test_text) if word not in custom_stopwords_list]

    new_vec = dictionary.doc2bow(test_words)

    sims = index[tf[new_vec]]
    max_Re = max(list(sims))

    if max_Re >= 0.8:
        return False
    return True
