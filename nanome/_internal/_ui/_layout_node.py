from nanome.util import Vector3, IntEnum
from nanome._internal._ui import _UIList

class _LayoutNode(object):

    @classmethod
    def _create(cls):
        return cls()

    id_gen = 0
    def __init__(self, name = "node"):
        # type: (str)
        #protocol vars
        self._id = _LayoutNode.id_gen
        self._enabled = True
        self._layer = 0
        self._layout_orientation = _LayoutNode.LayoutTypes.vertical
        self._sizing_type = _LayoutNode.SizingTypes.expand
        self._sizing_value = 1.0
        self._forward_dist = 0.0
        self._padding_type = _LayoutNode.PaddingTypes.fixed
        self._padding = (0.0, 0.0, 0.0, 0.0)
        self._children = []
        self._content = []
        #API
        self._name = name
        self._parent = None
        _LayoutNode.id_gen += 1

    def get_children(self):
        return self._children

    def get_content(self):
        return self._content
    
    class PaddingTypes(IntEnum):
        fixed = 0
        ratio = 1

    class SizingTypes(IntEnum):
        expand = 0
        fixed = 1
        ratio = 2

    class LayoutTypes(IntEnum):
        vertical = 0
        horizontal = 1

    def add_content(self, ui_content):
        #add to curr parent
        self._content.append(ui_content)
        self._save_changes()

    def remove_content(self, ui_content):
        self._content.remove(ui_content)
        self._save_changes()

    def clear_content(self):
        self._content = []
        self._save_changes()

    def add_child(self, child_node):
        #remove from old parent
        if (child_node._parent != None):
            child_node._parent.remove_child(child_node)
        #add to curr parent
        self._children.append(child_node)
        child_node._parent = self
        self._save_changes()

    def remove_child(self, child_node):
        self._children.remove(child_node)
        child_node._parent = None
        self._save_changes()

    def clear_children(self):
        for child in self._children:
            child._parent = None
        self._children = []
        self._save_changes()

    #copies node formatting but not children or content
    def copy_values_shallow(self, other):
        self._layer = other._layer
        self._layout_orientation = other._layout_orientation
        self._sizing_type = other._sizing_type
        self._sizing_value = other._sizing_value
        self._forward_dist = other._forward_dist
        self._padding = other._padding
        self._name = other._name
        self._save_changes()

    def _copy_values_deep(self, other):
        self.copy_values_shallow(other)
        for content in other._content:
            self._content.append(content._clone())
        for child in other._children:
            self._children.append(child._clone())

    def _clone(self):
        result = _LayoutNode._create()
        result._copy_values_deep(self)
        return result

#region non-api functions
    def _find_content(self, content_id):
        found_val = None
        for content in self._content:
            if content._content_id == content_id:
                return content
            elif isinstance(content, _UIList):
                for node in content.items:
                    found_val = node._find_content(content_id)
                    if found_val != None:
                        return found_val
        for child in self._children:
            found_val = child._find_content(content_id)
            if found_val != None:
                return found_val
        return None

    def _append_all_content(self, all_content = []):
        all_content.extend(self._content)
        for child in self._children:
            child._append_all_content(all_content)
        return all_content

    def _append_all_nodes(self, all_nodes = []):
        all_nodes.append(self)
        for child in self._children:
            child._append_all_nodes(all_nodes)
        return all_nodes
#endregion

    def _save_changes(self):
        pass
