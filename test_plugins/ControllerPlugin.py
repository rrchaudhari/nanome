import nanome
import os
import sys
from nanome.util.image_settings import ScalingOptions

class ControllerPlugin(nanome.PluginInstance):
    def __init__(self):
        self.outstanding_requests = 0

    # Function called when Nanome connects to the Plugin, after its instantiation
    def start(self):
        self.create_controller_feedback()
    # Function called when user clicks on the "Run" button in Nanome
    def on_run(self):
        self.open_menu()

    def on_advanced_settings(self):
        self.open_menu()

    def open_menu(self):
        menu = nanome.ui.Menu.get_plugin_menu()
        menu.enabled = True
        self.update_menu(menu)

    def update(self):
        if (self.outstanding_requests == 0):
            nanome.util.Logs.debug("sending reqs")
            self.update_menu(nanome.ui.Menu.get_plugin_menu())
            self.outstanding_requests = 3
            self.request_controller(nanome.util.enums.ControllerType.head, self.on_controller_request)
            self.request_controller(nanome.util.enums.ControllerType.left, self.on_controller_request)
            self.request_controller(nanome.util.enums.ControllerType.right, self.on_controller_request)

    def on_controller_request(self, controller):
        nanome.util.Logs.debug("received req")
        self.outstanding_requests -= 1
        root = nanome.ui.Menu.get_plugin_menu().root
        if(controller.controller_type == nanome.util.enums.ControllerType.head):
            self.update_controller(root.find_node("head"), controller)
        if(controller.controller_type == nanome.util.enums.ControllerType.left):
            self.update_controller(root.find_node("left"), controller)
        if(controller.controller_type == nanome.util.enums.ControllerType.right):
            self.update_controller(root.find_node("right"), controller)

    def update_controller(self, node, controller):
        controller_type = node.find_node("controller_type").get_content()
        controller_type.text_value = ("controller_type: " + str(controller.controller_type))
        position = node.find_node("position").get_content()
        position.text_value = ("position: " + str(controller.position))
        rotation = node.find_node("rotation").get_content()
        rotation.text_value = ("rotation: " + str(controller.rotation))
        thumb_padX = node.find_node("thumb_padX").get_content()
        thumb_padX.text_value = ("thumb_padX: " + str(controller.thumb_padX))
        thumb_padY = node.find_node("thumb_padY").get_content()
        thumb_padY.text_value = ("thumb_padY: " + str(controller.thumb_padY))
        trigger_position = node.find_node("trigger_position").get_content()
        trigger_position.text_value = ("trigger_position: " + str(controller.trigger_position))
        grip_position = node.find_node("grip_position").get_content()
        grip_position.text_value = ("grip_position: " + str(controller.grip_position))
        button1_pressed = node.find_node("button1_pressed").get_content()
        button1_pressed.text_value = ("button1_pressed: " + str(controller.button1_pressed))
        button2_pressed = node.find_node("button2_pressed").get_content()
        button2_pressed.text_value = ("button2_pressed: " + str(controller.button2_pressed))

    def create_controller_feedback(self):
        menu = nanome.ui.Menu.get_plugin_menu()
        root = menu.root
        INODE = nanome._internal._ui._LayoutNode
        root.layout_orientation = INODE.LayoutTypes.horizontal
        l1 = nanome.api.ui.LayoutNode()
        
        l_controller_type = l1.create_child_node("controller_type")
        l_controller_type.add_new_label("controller_type: ")
        l_position = l1.create_child_node("position")
        l_position.add_new_label("position: ")
        l_rotation = l1.create_child_node("rotation")
        l_rotation.add_new_label("rotation: ")
        l_thumb_padX = l1.create_child_node("thumb_padX")
        l_thumb_padX.add_new_label("thumb_padX: ")
        l_thumb_padY = l1.create_child_node("thumb_padY")
        l_thumb_padY.add_new_label("thumb_padY: ")
        l_trigger_position = l1.create_child_node("trigger_position")
        l_trigger_position.add_new_label("trigger_position: ")
        l_grip_position = l1.create_child_node("grip_position")
        l_grip_position.add_new_label("grip_position: ")
        l_button1_pressed = l1.create_child_node("button1_pressed")
        l_button1_pressed.add_new_label("button1_pressed: ")
        l_button2_pressed = l1.create_child_node("button2_pressed")
        l_button2_pressed.add_new_label("button2_pressed: ")

        head = l1
        left_controller = l1.clone()
        right_controller = l1.clone()

        head.name = "head"
        left_controller.name = "left"
        right_controller.name = "right"

        root.add_child(head)
        root.add_child(left_controller)
        root.add_child(right_controller)

if __name__ == "__main__":
    # Create the plugin, register Docking as the class to instantiate, and start listening
    plugin = nanome.Plugin("Controller Plugin", "Image Plugin.", "Test", False)
    plugin.set_plugin_class(ControllerPlugin)
    plugin.run('127.0.0.1', 8888)