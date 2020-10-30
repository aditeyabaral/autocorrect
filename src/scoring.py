import logging

import networkx as nx
from gensim.models.fasttext import FastText

import embedding
import utils

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

model = FastText.load("../ft_models/machine_learning/ai-norvig.model")


def evaluate(key_graph, ans_graph, total_marks=5):
    main_points_key = [x for x in key_graph.nodes if key_graph.out_degree(x) != 0]
    main_points_ans = [x for x in ans_graph.nodes if ans_graph.out_degree(x) != 0]
    marks_per_mp = total_marks / len(main_points_key)

    most_similar = dict((x, []) for x in main_points_key)

    for mp_ans in main_points_ans:
        best_match = 0
        best_match_sim = 0
        for mp_key in main_points_key:
            mp_sim = utils.getSimilarity(mp_key, mp_ans, model)
            if best_match_sim < mp_sim:
                best_match_sim = mp_sim
                best_match = mp_key
        most_similar[best_match].append({"node": mp_ans, "sim": best_match_sim})

    total_score = 0
    for mp_key in most_similar:
        if most_similar[mp_key]:
            sp_key = [
                x for x in key_graph.neighbors(mp_key) if key_graph.out_degree(x) == 0
            ]
            sp_ans = [
                {"node": x, "parent": a} if ans_graph.out_degree(x) == 0 else None
                for a in most_similar[mp_key]
                for x in ans_graph.neighbors(a["node"])
            ]
            sp_ans = list(filter(lambda x: x is not None, sp_ans))
            kw_score = 0
            for keyword in sp_key:
                for ans_keyword in sp_ans:
                    if utils.getSimilarity(keyword, ans_keyword["node"], model) >= 0.85:
                        kw_score += (
                            utils.getSimilarity(
                                key_graph[mp_key][keyword][0]['edge'],
                                ans_graph[ans_keyword["parent"]["node"]][ans_keyword["node"]][0]['edge'],
                                model,
                            )
                            * ans_keyword["parent"]["sim"]
                        )
                        break

            kw_score_ratio = kw_score / len(sp_key)
            total_score += kw_score_ratio * marks_per_mp

    return total_score
