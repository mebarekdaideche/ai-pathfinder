# ai-pathfinder

Visualiseur de résolution de problèmes par graphes d'états. Tu choisis un problème, un algo, et tu vois les étapes de la solution.

Fait dans le cadre d'un projet de cours sur les concepts d'IA (L2), puis refait proprement après.

---

## Install
```bash
git clone https://github.com/mebarekdaideche/ai-pathfinder.git
cd ai-pathfinder
pip install -r requirements.txt
python main.py
```

Tkinter est inclus avec Python sur Windows et Mac. Sur Linux : `sudo apt install python3-tk`.

---

## Ce que ça fait

Quatre problèmes classiques modélisés comme des graphes d'états :

- **Loup-Chèvre-Salade** — traversée de rivière, état = `(loup, chevre, salade, bateau)`
- **Die Hard** — obtenir 4L avec des seaux de 5L et 3L
- **Taquin (8-puzzle)** — grille 3x3, heuristique = distance de Manhattan
- **Hanoi** — 3 disques de A vers C

Quatre algos implémentés from scratch : BFS, DFS, Dijkstra, A*. L'onglet "Comparaison" les lance tous les quatre sur le même problème et affiche le tableau.

Sur le taquin, A* explore 12 noeuds contre 181 pour BFS — même solution, même nombre d'étapes.

---

## Tests
```bash
pytest tests/ -v
# 18 passed
```

---

## Limitations

- Pas de visualisation graphique du graphe (juste les étapes en texte)
- DFS ne garantit pas la solution optimale — c'est normal, c'est DFS
- Le taquin plante sur des configs non-solubles (pas de vérification de parité)
- Testé sur Python 3.10-3.14, Windows et Linux

---

## Licence

MIT
