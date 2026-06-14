from __future__ import annotations

from dataclasses import dataclass, field

from core.models.connection import Connect
from core.models.node import MyNode


@dataclass
class ProjectModel:
    nodes: list[MyNode] = field(default_factory=list)

    def clear(self) -> None:
        self.nodes.clear()

    def add_node(self, node: MyNode) -> int:
        self.nodes.append(node)
        return len(self.nodes) - 1

    def create_node(
        self,
        hint: str = "Нова ціль",
        left: int = 100,
        top: int = 100,
        width: int = 140,
        height: int = 70,
        project: bool = False,
    ) -> MyNode:
        node = MyNode(
            hint=hint,
            left=left,
            top=top,
            width=width,
            height=height,
            project=project,
        )
        self.add_node(node)
        return node

    def remove_node(self, node: MyNode) -> None:
        if node in self.nodes:
            self.nodes.remove(node)

        for item in self.nodes:
            item.connect.remove(node)

        self.rebuild_sub_goal_lists()

    def connect_nodes(self, src: MyNode, dst: MyNode) -> int:
        return src.connect.add(dst)

    def rebuild_sub_goal_lists(self) -> None:
        for node in self.nodes:
            node.sub_goal_list_create(self.nodes)

    def to_dict(self) -> dict:
        node_id_map = {id(node): i for i, node in enumerate(self.nodes)}

        return {
            "nodes": [self._node_to_dict(node, i, node_id_map) for i, node in enumerate(self.nodes)]
        }

    def _node_to_dict(self, node: MyNode, node_index: int, node_id_map: dict[int, int]) -> dict:
        return {
            "id": node_index,
            "hint": node.hint,
            "left": node.left,
            "top": node.top,
            "width": node.width,
            "height": node.height,
            "sliding": node.sliding,
            "click_x": node.click_x,
            "click_y": node.click_y,
            "expert_list": list(node.expert_list),
            "complex_project_list": list(node.complex_project_list),
            "resource_inp": node.resource_inp,
            "measure_inp": node.measure_inp,
            "threshold": node.threshold,
            "project": node.project,
            "value_duration": node.value_duration,
            "start_time": node.start_time,
            "opening": node.opening,
            "determin_chkv": node.determin_chkv,
            "effect": node.effect,
            "fixed": node.fixed,
            "fulfilment": node.fulfilment,
            "method": node.method,
            "min_resources": node.min_resources,
            "min_degree": node.min_degree,
            "max_resources": node.max_resources,
            "max_degree": node.max_degree,
            "degree_reach": node.degree_reach,
            "time_of_reach": node.time_of_reach,
            "financing": node.financing,
            "fulfil": node.fulfil,
            "connect": [
                self._connect_to_dict(con, node_id_map)
                for con in node.connect
            ],
        }

    def _connect_to_dict(self, con: Connect, node_id_map: dict[int, int]) -> dict:
        return {
            "node_id": None if con.node is None else node_id_map[id(con.node)],
            "positive": con.positive,
            "direct_chkv": con.direct_chkv,
            "pref": list(con.pref),
            "rel_dyn": list(con.rel_dyn),
            "sca_typ": list(con.sca_typ),
            "effect_out": con.effect_out,
            "value_delay": con.value_delay,
            "character": [
                {"n_gr": item.n_gr, "ratio": item.ratio}
                for item in con.character
            ],
            "labeled": con.labeled,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectModel":
        project = cls()
        nodes_data = data.get("nodes", [])

        id_to_node: dict[int, MyNode] = {}

        for node_data in nodes_data:
            node = MyNode(
                hint=node_data.get("hint", "Це ціль (або підціль)"),
                left=node_data.get("left", 0),
                top=node_data.get("top", 0),
                width=node_data.get("width", 20),
                height=node_data.get("height", 20),
                sliding=node_data.get("sliding", False),
                click_x=node_data.get("click_x", 0),
                click_y=node_data.get("click_y", 0),
                expert_list=list(node_data.get("expert_list", [])),
                complex_project_list=list(node_data.get("complex_project_list", [])),
                resource_inp=node_data.get("resource_inp", -1.0),
                measure_inp=node_data.get("measure_inp", -1),
                threshold=node_data.get("threshold", 0),
                project=node_data.get("project", False),
                value_duration=node_data.get("value_duration", 0),
                start_time=node_data.get("start_time", 0),
                opening=node_data.get("opening", False),
                determin_chkv=node_data.get("determin_chkv", False),
                effect=node_data.get("effect", 0.0),
                fixed=node_data.get("fixed", False),
                fulfilment=node_data.get("fulfilment", 100),
                method=node_data.get("method", 0),
                min_resources=node_data.get("min_resources", 0),
                min_degree=node_data.get("min_degree", 0),
                max_resources=node_data.get("max_resources", 0),
                max_degree=node_data.get("max_degree", 10000),
                degree_reach=node_data.get("degree_reach", 0.0),
                time_of_reach=node_data.get("time_of_reach", 0),
                financing=node_data.get("financing", 0.0),
                fulfil=node_data.get("fulfil", 0),
            )
            project.add_node(node)
            id_to_node[node_data["id"]] = node

        for node_data in nodes_data:
            src_node = id_to_node[node_data["id"]]
            for con_data in node_data.get("connect", []):
                con = Connect(node=None)
                con.positive = con_data.get("positive", True)
                con.direct_chkv = con_data.get("direct_chkv", 0.0)
                con.pref = list(con_data.get("pref", []))
                con.rel_dyn = list(con_data.get("rel_dyn", []))
                con.sca_typ = list(con_data.get("sca_typ", []))
                con.effect_out = con_data.get("effect_out", -1.0)
                con.value_delay = con_data.get("value_delay", 0)
                con.labeled = con_data.get("labeled", False)

                con.character.clear()
                for item in con_data.get("character", []):
                    con.character.add(
                        int(item.get("n_gr", 0)),
                        float(item.get("ratio", 0.0))
                    )

                dst_id = con_data.get("node_id")
                if dst_id is not None:
                    con.node = id_to_node.get(dst_id)

                src_node.connect._items.append(con)

        project.rebuild_sub_goal_lists()
        return project

    @classmethod
    def create_demo(cls) -> "ProjectModel":
        project = cls()

        a = MyNode(hint="Головна ціль", left=100, top=80, width=28, height=28)
        b = MyNode(hint="Підціль 1", left=80, top=180, width=24, height=24)
        c = MyNode(hint="Підціль 2", left=180, top=180, width=28, height=20, project=True)

        project.add_node(a)
        project.add_node(b)
        project.add_node(c)

        project.connect_nodes(b, a)
        project.connect_nodes(c, a)

        project.rebuild_sub_goal_lists()
        return project
