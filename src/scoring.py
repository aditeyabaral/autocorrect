# import logging
# 
# import networkx as nx
from gensim.models.fasttext import FastText

import utils

# logging.basicConfig(
#     format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
# )

model = FastText.load("../ft_model/ft.model")


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
                max_sim = 0
                max_sim_node = 0
                for ans_keyword in sp_ans:
                    cur_sim = utils.getSimilarity(keyword, ans_keyword["node"], model)
                    if cur_sim > max_sim:
                        max_sim = cur_sim
                        max_sim_node = ans_keyword
                    # print("Trying to match", keyword, ans_keyword["node"])

                if max_sim >= 0.75:
                    # print("Matched")
                    best_edge_sim = max(
                        [
                            utils.getSimilarity(
                                key_graph[mp_key][keyword][key_edge]["edge"],
                                ans_graph[max_sim_node["parent"]["node"]][
                                    max_sim_node["node"]
                                ][ans_edge]["edge"],
                                model,
                            )
                            for key_edge in key_graph[mp_key][keyword]
                            for ans_edge in ans_graph[max_sim_node["parent"]["node"]][
                                max_sim_node["node"]
                            ]
                        ]
                    )

                    best_edge_sim = 1 if best_edge_sim > 0.85 else best_edge_sim
                    score_for_kw = best_edge_sim * max_sim_node["parent"]["sim"]
                    # print(
                    #     "Score for keyword\n",
                    #     "Key keyword:",
                    #     keyword,
                    #     "Ans keyword:",
                    #     max_sim_node["node"],
                    #     "Key relation:",
                    #     key_graph[mp_key][keyword][0]["edge"],
                    #     "Ans relation:",
                    #     ans_graph[max_sim_node["parent"]["node"]][max_sim_node["node"]][
                    #         0
                    #     ]["edge"],
                    #     "Score:",
                    #     score_for_kw,
                    # )
                    kw_score += score_for_kw
                # else:
                #     print("Unmatched score:", max_sim)

            kw_score_ratio = kw_score / len(sp_key)
            # print(kw_score_ratio)
            # print("Score for key kw", keyword, kw_score_ratio * marks_per_mp)
            total_score += kw_score_ratio * marks_per_mp

    return total_score
