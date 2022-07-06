bl_info = {
    "name": "Naolito Panel",
    "version": (1, 0, 0),
    "author": "Naolito Animation Studios",
    "blender": (3, 2, 0),
    "description": "Naolito utilities",
    "category": "Animation",
}

import bpy
from bpy.types import Panel, Operator

COLORSPACE_DATA = 'role_data'
COLORSPACE_TEXTURE = 'role_matte_paint'

class TexturesToACEScg(Operator):
    bl_idname = "object.toacescg"
    bl_label = "toacescg"
    
    def detectTextureType(self, textureNode):
        sockets = []
        sockTemp = []
        outputFound = False
        
        for output in textureNode.outputs:
            for link in output.links:
                sockets.append(link.to_socket)

        while not outputFound and sockets:
            for socket in sockets:
                node = socket.node
                for output in node.outputs:
                    if output.is_linked:
                        linkedSockets = []
                        for link in output.links:
                            linkedSockets.append(link.to_socket)
                        linkedSockets = list(set(linkedSockets))
                        for linkedSocket in linkedSockets:
                            if linkedSocket.type == 'SHADER' or (linkedSocket.type == 'VECTOR' and linkedSocket.node.type == 'OUTPUT_MATERIAL'):
                                print('Output Found!',socket.node.name,'>>',socket.name)
                                outputFound = True
                            else:
                                sockTemp.append(linkedSocket)
                if outputFound:
                    if socket.type == 'RGBA':
                        return 'TEXTURE'
                    elif socket.type in ('VALUE','VECTOR'):
                        return 'DATA'
                    break
            else:
                sockets = list(set(sockTemp[::]))
                sockTemp = []

        if not sockets:
            print('Textures node is not connected')
            return False

    def execute(self, context):
        materials = [m for m in bpy.data.materials if m.use_nodes]
        for m in materials:
            for node in m.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    type = self.detectTextureType(node)
                    if type:
                        if type == 'TEXTURE':
                            node.image.colorspace_settings.name = COLORSPACE_TEXTURE
                        elif type == 'DATA':
                            node.image.colorspace_settings.name = COLORSPACE_DATA
                    else: continue

        return {'FINISHED'}
            
class NaolitoPanel(Panel):
    bl_idname = "panel.naolito"
    bl_label = "Naolito"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Naolito'

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Naolito", icon='WORLD_DATA')
        row = box.row()
        row.operator("object.toacescg",text='Textures to ACEScg')
        
def register():
    bpy.utils.register_class(NaolitoPanel)
    bpy.utils.register_class(TexturesToACEScg)


def unregister():
    bpy.utils.unregister_class(NaolitoPanel)
    bpy.utils.unregister_class(TexturesToACEScg)

if __name__ == "__main__":
    register()
