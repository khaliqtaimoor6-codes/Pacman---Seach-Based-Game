Pacman Search Project - Assignment 01 (AI2002)
Roll: 24I3102 + partners
========================

Python version: 3.12.3 (requires 3.7+)
OS: Linux (Ubuntu)
Tested: 26 Sep 2026

Team split:
- Person 1 (khaliqtaimoor6-codes): search.py DFS/BFS/UCS/GBFS/A* base
- Person 2 (Ashar Ahmed): searchAgents.py CornersProblem, foodHeuristic, AnyFood, ClosestDot
- Person 3 (24I3102, me): DFS fix (q1 0/3->3/3), CSV trace logger evidence/,
  foodHeuristic maze-cache speedup (96s->2.5s), custom maze 24I3102Search.lay,
  README/report/screenshots/ZIP + all experiments.

Run commands (from search/ folder):
  python3 pacman.py
  python3 pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
  python3 pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
  python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs
  python3 pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
  python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs
  python3 pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
  python3 pacman.py -l testSearch -p SearchAgent -a fn=ucs
  python3 pacman.py -l mediumMaze -p StayEastSearchAgent
  python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
  python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
  python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
  python3 pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
  python3 pacman.py -l mediumCorners -p AStarCornersAgent -z .5
  python3 pacman.py -l trickySearch -p AStarFoodSearchAgent
  python3 pacman.py -l bigSearch -p ClosestDotSearchAgent
  python3 pacman.py -l 24I3102Search -p SearchAgent -a fn=dfs
  python3 pacman.py -l 24I3102Search -p SearchAgent -a fn=bfs
  python3 pacman.py -l 24I3102Search -p SearchAgent -a fn=ucs
  python3 pacman.py -l 24I3102Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
  python3 pacman.py -l 24I3102Search -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Autograder:
  python3 autograder.py --no-graphics
  Result: 26/25 (q1 3/3, q2 3/3, q3 3/3, q4 3/3, q5 3/3, q6 3/3, q7 5/4, q8 3/3)

CSV logging:
  search.py: startTracing(path)/stopTracing()/logExpansion(...)
  Columns: iteration,expanded_state,parent,action,generated_successors,frontier_before,frontier_after,explored,g,h,f
  evidence/*.csv (20 files) generated via /tmp/gen_evidence.py logic.
  Nested BFS inside mazeDistance pauses tracing to avoid pollution.

Custom maze:
  layouts/24I3102Search.lay (23x14, 1 food at (1,1), P at (19,7))
  Design: vertical barrier x=12 gaps y=3/11, horizontal wall y=6, east U-pocket, west branches.
  Result: BFS/UCS/A* 24 optimal, GBFS 28 (+4), DFS 42. GBFS 29 expanded vs A* 68 vs BFS 188.

Files edited:
  search.py (DFS fix + logger + GBFS + pauseTracing)
  searchAgents.py (Corners, foodHeuristic cache, mazeDistance pause)
  layouts/24I3102Search.lay (new)
  evidence/*.csv (new, 20 files)
  evidence/screenshots/*.png (new)
  report.pdf (new, this report)

Forbidden files untouched: pacman.py, game.py, util.py, layout.py,
graphicsDisplay.py, graphicsUtils.py, textDisplay.py (verified via diff).

System specs:
  CPU: x86_64 Linux, RAM 8GB+, Python 3.12.3, no GPU needed.
