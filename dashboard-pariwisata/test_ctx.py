import pandas as pd
from sentence_transformers import SentenceTransformer, util
from data.gap_score import get_all_demand_skills
from data.simulator_data import SINONIM

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
skills = get_all_demand_skills()
skill_to_synonyms = {}
for k, s in SINONIM.items():
    if s not in skill_to_synonyms:
        skill_to_synonyms[s] = []
    skill_to_synonyms[s].append(k)

ctx_skills = []
for s in skills:
    if s in skill_to_synonyms:
        ctx_skills.append(f"{s}: {', '.join(skill_to_synonyms[s])}")
    else:
        ctx_skills.append(s)

emb_skills = model.encode(ctx_skills, convert_to_tensor=True)
qs = ['pelatihan pijat relaksasi', 'pelatihan manajemen operasional event', 'pelatihan keamanan arung jeram']

for q in qs:
    sims = util.cos_sim(model.encode(q), emb_skills)[0]
    res = sorted([(skills[i], float(sim)) for i, sim in enumerate(sims) if float(sim) > 0.32], key=lambda x: x[1], reverse=True)
    print(q)
    print(res)
    print()
