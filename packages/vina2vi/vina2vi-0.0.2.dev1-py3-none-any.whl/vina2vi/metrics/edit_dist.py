import unicodedata

import numpy as np
import tensorflow as tf
import tensorflow_text as tf_text


COST = {
    "DELETE": 1,
    "INSERT": 1,
    "SUBSTITUTE": 2,
}

def lev(source:str, target:str, cost:dict=COST) -> float:
    """
    Levenshtein distance
    """
    m = len(source)
    n = len(target)
    # Think of distance_matrix as a (m+1, n+1)-matrix
    distance_matrix = dict()

    distance_matrix[0,0] = 0
    for i in range(1,m+1):
        distance_matrix[i,0] = distance_matrix[i-1,0] + cost["DELETE"]
    for j in range(1,n+1):
        distance_matrix[0,j] = distance_matrix[0,j-1] + cost["INSERT"]

    for i in range(1,m+1):
        for j in range(1,n+1):
            candidates = (
                distance_matrix[i-1, j-1] + (0 if source[i-1] == target[j-1] else cost["SUBSTITUTE"]),
                distance_matrix[i-1, j] + cost["DELETE"],
                distance_matrix[i, j-1] + cost["INSERT"],
            )
            distance_matrix[i,j] = min(candidates)

    return distance_matrix[m, n]


def norm_lev(
        source:str,
        target:str,
        form:str="NFD",
        cost:dict=COST,
    ):
    source = unicodedata.normalize(form, source)
    target = unicodedata.normalize(form, target)
    return lev(source, target, cost)


def similarity_score(
        source:str,
        target:str,
        alpha:float=1/3,
        soft:bool=True,
        proportional:bool=True,
    ) -> float:
    """
    The idea is that we need this function to return an
    accuracy-like score, in the range of [0, 1],
    to measure the similarity between two strings.

    We have provided two distinct definition for soft similarity,
    controlled by the boolean `proportional`
    """
    if soft:
        dist = lev(source, target)
        if proportional:
            proportion = dist / (COST["SUBSTITUTE"]*max(len(target), 1))
            similarity = 1 - min(1, proportion)
        else:
            if dist > len(target)*COST["SUBSTITUTE"]:
                # That is, when they are completely different strings
                similarity = 0
            else:
                similarity = 1 / (alpha*dist + 1)
    else:
        # hard similarity is binary: same string or not
        similarity = float(source == target)
    return similarity


def norm_similarity_score(
        source:str,
        target:str,
        alpha:float=1/3,
        soft:bool=True,
        proportional:bool=True,
        form:str="NFD",
    ) -> float:
    source = unicodedata.normalize(form, source)
    target = unicodedata.normalize(form, target)
    return similarity_score(source, target, alpha, soft, proportional)


distance_matrix = tf.Variable(tf.zeros([1000, 1000], tf.int32))

@tf.function(input_signature=[
    tf.TensorSpec([None], tf.int32),
    tf.TensorSpec([None], tf.int32),
    tf.TensorSpec(None, tf.int32),
    tf.TensorSpec(None, tf.int32),
    tf.TensorSpec(None, tf.int32),
])
def tf_codepoint_lev(
        u,
        v,
        delete=tf.constant(1),
        insert=tf.constant(1),
        substitute=tf.constant(2),
    ):
    """
    u, v: an array of codepoints
    """
    m = tf.shape(u)[0]
    n = tf.shape(v)[0]
    distance_matrix[:m+1, :n+1].assign(tf.zeros([m+1, n+1], tf.int32))

    start = delete
    delta = delete
    limit = (m+1) * delete
    distance_matrix[1:m+1, 0].assign(tf.range(start, limit, delta))

    start = insert
    step = insert
    limit = (n+1) * insert
    distance_matrix[0, 1:n+1].assign(tf.range(start, limit, delta))

    for i in tf.range(1, m+1):
        for j in tf.range(1, n+1):
            cond = u[i-1] == v[j-1]
            candidates = [
                distance_matrix[i-1, j-1] + tf.cond(
                    cond,
                    lambda: tf.constant(0),
                    lambda: substitute,
                ),
                distance_matrix[i-1, j] + delete,
                distance_matrix[i, j-1] + insert,
            ]
            #candidates = tf.constant([
            #    distance_matrix[i-1, j-1] + tf.cond(
            #        cond,
            #        lambda: tf.constant(0),
            #        lambda: substitute,
            #    ),
            #    distance_matrix[i-1, j] + delete,
            #    distance_matrix[i, j-1] + insert,
            #])
            distance_matrix[i,j].assign(tf.reduce_min(candidates))

    #return distance_matrix.value()[m, n]
    return distance_matrix[m, n]


#@tf.function
@tf.function(input_signature=[
    tf.TensorSpec([], tf.string),
    tf.TensorSpec([], tf.string),
    tf.TensorSpec(None, tf.int32),
    tf.TensorSpec(None, tf.int32),
    tf.TensorSpec(None, tf.int32),
])
def tf_byte_lev(
        u,
        v,
        delete=tf.constant(1),
        insert=tf.constant(1),
        substitute=tf.constant(2),
    ):
    u = tf_text.normalize_utf8(u, "NFKD")
    v = tf_text.normalize_utf8(v, "NFKD")
    u = tf.strings.unicode_decode(u, "UTF-8")
    v = tf.strings.unicode_decode(v, "UTF-8")
    return tf_codepoint_lev(
                u,
                v,
                delete,
                insert,
                substitute,
            )


if __name__ == "__main__":
    u = "Tôi ở Sài Gòn được 6 năm rồi."
    #v = "Tôi ở Sài Gòn được 7 năm."
    v = "Tôi ở đây chưa lâu."
    d = norm_lev(u, v, form="NFKD")
    print(f"(Python land) d = {d}")
    u = tf.constant(u)
    v = tf.constant(v)
    d = tf_byte_lev(u, v)
    print(f"(TF land)     d = {d}")
