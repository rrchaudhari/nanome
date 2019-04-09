import nanome
import sys
import time
class UpdateWorkspace(nanome.PluginInstance):
    def start(self):
        print("Start UpdateWorkspace Plugin")

    def on_workspace_received(self, workspace):
        print("running")
        atom_count = 0
        bond_count = 0
        for complex in workspace.complexes:
            for molecule in complex.molecules:
                for chain in molecule.chains:
                    for residue in chain.residues:
                        for bond in residue.bonds:
                            bond_count+=1
                        for atom in residue.atoms:
                            atom.molecular.position.x = -atom.molecular.position.x
                            atom.rendering.surface_rendering = True
                            atom.rendering.surface_color = nanome.util.Color.Red()
                            atom_count+=1
                            
        print("bonds:", bond_count)
        print("flipped", atom_count, "atoms")
        self.update_workspace(workspace)

    def on_run(self):
        self.request_workspace(self.on_workspace_received)

    def __init__(self):
        pass

if __name__ == "__main__":
    plugin = nanome.Plugin("Update Workspace", "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities", "Test", False)
    plugin.set_plugin_class(UpdateWorkspace)
    plugin.run('127.0.0.1', 8888)