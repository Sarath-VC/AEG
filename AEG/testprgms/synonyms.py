import json
import nltk
from nltk.corpus import wordnet

sttnew=["word"]
with open('/AEG/aegdataset/datajson.json', 'r') as f:
    distros_dict = json.load(f)
# print(sttnew)
# vocabulary = []
# for s in sttnew:
#     vocabulary = vocabulary + (distros_dict[s])
#
# synonyms = []
# for word in vocabulary:
#     for syn in wordnet.synsets(word):
#         for l in syn.lemmas():
#             synonyms.append(l.name())
# g=set(synonyms)
# j=list(g)

# for word in distros_dict["word"]:
#     distros_dict["word"].append(i)
m=set(distros_dict["word"])
print(m)
n={"word":list(m)}

print(n)
distros_dict.update(n)
with open('/AEG/aegdataset/datajson.json', 'w') as f:
    dictdata = json.dump(distros_dict, f)

