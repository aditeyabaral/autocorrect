import spacy
import neuralcoref

nlp = spacy.load("en_core_web_md")

#text = "The mitochondrion is a double membrane bound organelle found in most eukaryotic organisms. Some cells in some multicellular organisms may however lack them. A number of unicellular organisms have transformed this into other structures. They are also known as the powerhouse of the cell. They take in nutrients breaks then down and creates energy rick molecules for the cells. The biochemical processes of the cell are known as cellular respiration"


text = "The mitochondrion is a double membrane bound organelle found in most eukaryotic organisms.\
            They are also known as the powerhouse of the cell.\
            Some cells in some multicellular organisms may however lack them.\
            A number of unicellular organisms have transformed this into other structures.\
            They take in nutrients breaks them down and creates energy rich molecules for the cells.\
            The biochemical processes of the cell are known as cellular respiration"

greedyness = [0,1, 0.2, 0,3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
max_dist = [20, 50, 75, 100, 150, 250, 400, 500]
max_dist_match = [100, 250, 500, 750, 1000]

f = open("neucor.csv", "w")

for g in greedyness:
    for md in max_dist:
        for mdm in max_dist_match:
            neuralcoref.add_to_pipe(nlp, max_dist=md, greedyness=g, max_dist_match=mdm)
            doc = nlp(text)
            f.write(f"{doc._.coref_resolved},{md},{mdm},{g}\n")
            nlp.remove_pipe("neuralcoref")

