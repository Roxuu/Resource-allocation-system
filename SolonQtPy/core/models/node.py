from __future__ import annotations

from dataclasses import dataclass, field

from core.models.connection import ConnectList



@dataclass
class MyNode:
    # Базові властивості вузла
    hint: str = "Це ціль (або підціль)"
    left: int = 0
    top: int = 0
    width: int = 20
    height: int = 20

    sliding: bool = False
    click_x: int = 0
    click_y: int = 0

    expert_list: list[str] = field(default_factory=list)
    complex_project_list: list[str] = field(default_factory=list)

    resource_inp: float = -1.0
    measure_inp: int = -1
    threshold: int = 0

    project: bool = False
    value_duration: int = 0
    start_time: int = 0
    opening: bool = False
    determin_chkv: bool = False
    effect: float = 0.0
    fixed: bool = False
    fulfilment: int = 100
    method: int = 0
    min_resources: int = 0
    min_degree: int = 0
    max_resources: int = 0
    max_degree: int = 10000

    degree_reach: float = 0.0
    time_of_reach: int = 0
    financing: float = 0.0
    fulfil: int = 0

    connect: ConnectList = field(default_factory=ConnectList)
    sub_goal_list: list["MyNode"] = field(default_factory=list)

    def set_threshold(self, value: int) -> None:
        if value < 0 or value > 100:
            raise ValueError("Threshold must be in range 0..100")
        self.threshold = value

    def sub_goal_list_create(self, all_nodes: list["MyNode"]) -> None:
        self.sub_goal_list = []
        for node in all_nodes:
            if node is self:
                continue
            if node.connect.index_of(self) != -1:
                self.sub_goal_list.append(node)

    def sub_goal_list_free(self) -> None:
        self.sub_goal_list.clear()

    def has_way_to(self, dest: "MyNode") -> bool:
        way_list: list[MyNode] = []
        return self._way_to(dest, way_list)

    def _way_to(self, dest: "MyNode", way_list: list["MyNode"]) -> bool:
        way_list.append(self)

        result = False
        for con in self.connect:
            next_node = con.node
            if next_node is None:
                continue

            if next_node not in way_list:
                result = ((len(way_list) > 1) and (next_node is dest)) or next_node._way_to(dest, way_list)
                if result:
                    break

        way_list.remove(self)
        return result

    def number_of_groups(self) -> int:
        result = 0
        if self.sub_goal_list is not None:
            for sub_goal in self.sub_goal_list:
                idx = sub_goal.connect.index_of(self)
                if idx == -1:
                    continue
                con = sub_goal.connect[idx]
                for char_item in con.character:
                    if result < char_item.n_gr:
                        result = char_item.n_gr
        return result

    def absorption(self) -> int:
        ng = self.number_of_groups()
        k = ng

        while k > 0:
            l = ng
            while l > 0:
                if k != l:
                    l_m = -1
                    for m in range(len(self.sub_goal_list)):
                        con_m = self.sub_goal_list[m].connect[
                            self.sub_goal_list[m].connect.index_of(self)
                        ]

                        k_m = con_m.character.index_of(k)
                        if k_m != -1:
                            l_m = con_m.character.index_of(l)
                            if l_m == -1:
                                break

                    if l_m != -1:
                        for m in range(len(self.sub_goal_list)):
                            con_m = self.sub_goal_list[m].connect[
                                self.sub_goal_list[m].connect.index_of(self)
                            ]
                            n = 0
                            while n <= con_m.character.count() - 1:
                                n_gr = con_m.character[n].n_gr
                                if n_gr >= k:
                                    if n_gr == k:
                                        con_m.character.remove(k)
                                        n -= 1
                                    else:
                                        con_m.character[n].n_gr = n_gr - 1
                                n += 1

                        ng -= 1
                        l = 1
                        k = ng + 1
                l -= 1
            k -= 1

        return ng

    def delete_pwc(self, sub_g: "MyNode") -> None:
        self.sub_goal_list_create(self.sub_goal_list + [self] if self not in self.sub_goal_list else self.sub_goal_list)

        try:
            del_index = self.sub_goal_list.index(sub_g)
        except ValueError:
            self.sub_goal_list_free()
            return

        for i, item in enumerate(self.sub_goal_list):
            if i == del_index:
                continue

            del_ind = del_index - 1 if i < del_index else del_index
            idx = item.connect.index_of(self)
            if idx == -1:
                continue

            con = item.connect[idx]
            if del_ind < len(con.pref):
                del con.pref[del_ind]
                if del_ind < len(con.rel_dyn):
                    del con.rel_dyn[del_ind]
                if del_ind < len(con.sca_typ):
                    del con.sca_typ[del_ind]

        self.sub_goal_list_free()

    def delete_compatible(self, i: int, j: int) -> None:
        ng = self.number_of_groups()
        ig = 0

        con_i_idx = self.sub_goal_list[i].connect.index_of(self)
        con_j_idx = self.sub_goal_list[j].connect.index_of(self)

        if con_i_idx == -1 or con_j_idx == -1:
            return

        while ig < self.sub_goal_list[i].connect[con_i_idx].character.count():
            n_gr = self.sub_goal_list[i].connect[con_i_idx].character[ig].n_gr

            if self.sub_goal_list[j].connect[con_j_idx].character.index_of(n_gr) != -1:
                ng += 1

                for k in range(len(self.sub_goal_list)):
                    con_k_idx = self.sub_goal_list[k].connect.index_of(self)
                    if con_k_idx == -1:
                        continue

                    con_k = self.sub_goal_list[k].connect[con_k_idx]

                    if k != i:
                        if k == j:
                            con_k.character.replace_n_gr(n_gr, ng)
                        else:
                            if con_k.character.index_of(n_gr) != -1:
                                con_k.character.add(ng, 0.0)

                ng = self.absorption()

            ig += 1
