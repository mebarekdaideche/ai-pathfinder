import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.solver import Solver, ALGORITHMES
from problems.loup_chevre import LoupChevreSalade
from problems.die_hard import DieHard
from problems.taquin import Taquin
from problems.hanoi import Hanoi

BG = "#1e1e2e"
BG2 = "#2a2a3e"
PURPLE = "#6c63ff"
FG = "#cdd6f4"
FG_TITLE = "#cba6f7"
FG_OK = "#a6e3a1"
FG_ERR = "#f38ba8"
FG_INFO = "#89dceb"
FG_STEP = "#fab387"
FONT = ("Consolas", 11)
FONT_B = ("Segoe UI", 13, "bold")

PROBLEMS = {
    "Loup, Chevre et Salade": LoupChevreSalade,
    "Die Hard (seaux)": DieHard,
    "Taquin (8-puzzle)": Taquin,
    "Tour de Hanoi (3 disques)": lambda: Hanoi(3),
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Pathfinder")
        self.geometry("1000x700")
        self.configure(bg=BG)
        self.solver = Solver()
        self._build()

    def _build(self):
        tk.Label(self, text="AI Pathfinder", font=("Segoe UI", 18, "bold"),
                 fg=FG_TITLE, bg=BG).pack(pady=(16, 2))
        tk.Label(self, text="graph search — BFS / DFS / Dijkstra / A*",
                 font=("Segoe UI", 10), fg=FG_INFO, bg=BG).pack(pady=(0, 10))

        ctrl = tk.Frame(self, bg=BG2, padx=16, pady=10)
        ctrl.pack(fill='x', padx=20)

        tk.Label(ctrl, text="Probleme:", font=FONT_B, fg=FG, bg=BG2).grid(row=0, column=0, sticky='w')
        self.pb_var = tk.StringVar(value=list(PROBLEMS)[0])
        ttk.Combobox(ctrl, textvariable=self.pb_var, values=list(PROBLEMS),
                     state='readonly', width=26, font=FONT).grid(row=0, column=1, padx=(6, 20), pady=4)

        tk.Label(ctrl, text="Algo:", font=FONT_B, fg=FG, bg=BG2).grid(row=0, column=2, sticky='w')
        self.algo_var = tk.StringVar(value='A*')
        ttk.Combobox(ctrl, textvariable=self.algo_var, values=list(ALGORITHMES),
                     state='readonly', width=12, font=FONT).grid(row=0, column=3, padx=(6, 20))

        self.btn_run = tk.Button(ctrl, text="Run", font=FONT_B, bg=PURPLE, fg='white',
                                 relief='flat', cursor='hand2', command=self._run)
        self.btn_run.grid(row=0, column=4, padx=4)

        self.btn_cmp = tk.Button(ctrl, text="Compare all", font=FONT_B, bg="#45475a", fg='white',
                                 relief='flat', cursor='hand2', command=self._compare)
        self.btn_cmp.grid(row=0, column=5, padx=4)

        # tabs
        s = ttk.Style()
        s.theme_use('default')
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=BG2, foreground=FG, padding=[12, 6], font=FONT)
        s.map("TNotebook.Tab", background=[("selected", PURPLE)], foreground=[("selected", "white")])

        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=20, pady=10)
        self.nb = nb

        f1 = tk.Frame(nb, bg=BG)
        nb.add(f1, text="  Solution  ")
        self.out = scrolledtext.ScrolledText(f1, font=FONT, bg=BG2, fg=FG,
                                             relief='flat', wrap='word', state='disabled')
        self.out.pack(fill='both', expand=True, padx=4, pady=4)
        self._setup_tags(self.out)

        f2 = tk.Frame(nb, bg=BG)
        nb.add(f2, text="  Comparaison  ")
        self.cmp_out = scrolledtext.ScrolledText(f2, font=FONT, bg=BG2, fg=FG,
                                                 relief='flat', wrap='word', state='disabled')
        self.cmp_out.pack(fill='both', expand=True, padx=4, pady=4)
        self._setup_tags(self.cmp_out)

        self.status = tk.StringVar(value="pret.")
        tk.Label(self, textvariable=self.status, font=("Segoe UI", 9),
                 fg=FG_INFO, bg=BG, anchor='w').pack(fill='x', padx=20, pady=(0, 6))

    def _setup_tags(self, w):
        w.tag_config('title', foreground=FG_TITLE, font=("Segoe UI", 12, "bold"))
        w.tag_config('ok',    foreground=FG_OK,    font=FONT)
        w.tag_config('err',   foreground=FG_ERR,   font=FONT)
        w.tag_config('info',  foreground=FG_INFO,  font=FONT)
        w.tag_config('dim',   foreground=FG,       font=FONT)
        w.tag_config('step',  foreground=FG_STEP,  font=("Consolas", 11, "bold"))

    def _write(self, w, txt, tag='dim'):
        w.configure(state='normal')
        w.insert('end', txt, tag)
        w.see('end')
        w.configure(state='disabled')

    def _clear(self, w):
        w.configure(state='normal')
        w.delete('1.0', 'end')
        w.configure(state='disabled')

    def _get_problem(self):
        return PROBLEMS[self.pb_var.get()]()

    def _run(self):
        self.btn_run.config(state='disabled')
        self.status.set("calcul en cours...")
        threading.Thread(target=self._run_thread, daemon=True).start()

    def _run_thread(self):
        try:
            pb = self._get_problem()
            res = self.solver.solve(pb, self.algo_var.get())
            self.after(0, self._show_result, pb, self.algo_var.get(), res)
        except Exception as e:
            self.after(0, lambda: self._write(self.out, f"\nerreur: {e}\n", 'err'))
        finally:
            self.after(0, lambda: self.btn_run.config(state='normal'))

    def _show_result(self, pb, algo, res):
        self._clear(self.out)
        name = self.pb_var.get()
        self._write(self.out, f"\n  {name} — {algo}\n\n", 'title')

        if not res['found']:
            self._write(self.out, "  pas de solution\n", 'err')
            self.status.set("aucune solution")
            return

        steps = len(res['path']) - 1
        self._write(self.out,
            f"  ok — {steps} etapes | {res['explored']} noeuds | {res['time']*1000:.2f}ms\n\n", 'ok')

        for i, (state, action) in enumerate(zip(res['path'], ['debut'] + res['actions'])):
            self._write(self.out, f"  [{i:>2}] {action}\n", 'step')
            desc = pb.describe_state(state) if hasattr(pb, 'describe_state') else str(state)
            for line in desc.split('\n'):
                self._write(self.out, f"       {line}\n", 'dim')
            self._write(self.out, "\n")

        self.nb.select(0)
        self.status.set(f"ok — {res['explored']} noeuds en {res['time']*1000:.2f}ms")

    def _compare(self):
        self.btn_cmp.config(state='disabled')
        self.status.set("comparaison...")
        threading.Thread(target=self._cmp_thread, daemon=True).start()

    def _cmp_thread(self):
        try:
            pb = self._get_problem()
            results = self.solver.compare_all(pb)
            self.after(0, self._show_cmp, results)
        except Exception as e:
            self.after(0, lambda: self._write(self.cmp_out, f"\nerreur: {e}\n", 'err'))
        finally:
            self.after(0, lambda: self.btn_cmp.config(state='normal'))

    def _show_cmp(self, results):
        self._clear(self.cmp_out)
        self._write(self.cmp_out, f"\n  {self.pb_var.get()} — comparaison\n\n", 'title')

        header = f"  {'algo':<12} {'ok':<6} {'etapes':<8} {'noeuds':<10} {'ms':<10}\n"
        self._write(self.cmp_out, header, 'step')
        self._write(self.cmp_out, "  " + "-" * 48 + "\n", 'info')

        found = {}
        for algo, res in results.items():
            ok = res['found']
            steps = len(res['path']) - 1 if ok else '-'
            line = f"  {algo:<12} {'v' if ok else 'x':<6} {str(steps):<8} {res['explored']:<10} {res['time']*1000:.2f}\n"
            self._write(self.cmp_out, line, 'ok' if ok else 'err')
            if ok:
                found[algo] = res

        if found:
            # TODO: afficher un vrai graph un jour
            best = min(found, key=lambda a: found[a]['explored'])
            self._write(self.cmp_out, f"\n  best: {best} ({found[best]['explored']} noeuds)\n", 'ok')

        self.nb.select(1)
        self.status.set("comparaison ok")
