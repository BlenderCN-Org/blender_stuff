bl_info = {
    'name' : 'Batch Render',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (2, 79),
    'location' : 'View 3D > Tools > Batch Render',
    'description' : 'Batch render blend files.',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Render'
    }


#imports
import bpy
import os
from shutil import copyfile


#path to folder
batch_file = 'C:/Users/Hans-Willem/Documents/blender_batch_render/batch_render.bat'


#the main functions called by the operators
def main_add_to_queue():
    print('adding to queue...')
    f = open(batch_file, 'a')
    render_string = 'blender -b "' + str(bpy.data.filepath) + '" -x 1 -a' + '\n'
    f.write(render_string)
    f.close()

    removeDuplicates()


def main_clear_queue():
    print('clearing the queue...')
    createBatchFile()


def main_edit_queue():
    print('opening queue in atom...')
    os.system('atom ' + batch_file)


def main_open_folder():
    print('opening folder...')
    os.startfile(os.path.dirname(batch_file))


#helper functions
def getQueueLength():
    count = 0;
    f = open(batch_file, 'r')
    for i in f:
        count += 1
    f.close()
    return count


def removeDuplicates():
    f = open(batch_file, 'r')
    l = set([i for i in f])
    f.close()
    f = open(batch_file, 'w')
    for i in l:
        f.write(i)
    f.close()


def createBatchFile():
    f = open(batch_file, 'w')
    f.close()


#panel class
class MyPanel(bpy.types.Panel):

    #panel attributes
    """Batch Render Panel Class"""
    bl_label = 'Batch Render'
    bl_idname = 'tools_my_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Batch Render'

    #draw loop
    def draw(self, context):
        layout = self.layout
        if not os.path.isfile(batch_file):
            createBatchFile()
        layout.label('In Queue: ' + str(getQueueLength()))
        col = layout.column(align = True)
        col.operator('script.operator_add_to_queue', text="Add Current File To Queue")
        col.operator('script.operator_clear_queue', text="Clear Queue")
        col.operator('script.operator_edit_queue', text="Edit Queue In Atom")
        col.operator('script.operator_open_folder', text="Open Folder")



#operator class
class MyOperator_add_to_queue(bpy.types.Operator):

    #operator attributes
    """Add Current Blend File To The Queue"""
    bl_label = 'Add To Queue'
    bl_idname = 'script.operator_add_to_queue'
    bl_options = {'REGISTER', 'UNDO'}

    #execute
    def execute(self, context):
        main_add_to_queue()

        return {'FINISHED'}


class MyOperator_clear_queue(bpy.types.Operator):

    #operator attributes
    """Clear The Queue"""
    bl_label = 'Clear The Queue'
    bl_idname = 'script.operator_clear_queue'
    bl_options = {'REGISTER', 'UNDO'}

    #execute
    def execute(self, context):
        main_clear_queue()

        return {'FINISHED'}


class MyOperator_edit_queue(bpy.types.Operator):

    #operator attributes
    """Edit The Queue In Atom"""
    bl_label = 'Edit Queue'
    bl_idname = 'script.operator_edit_queue'
    bl_options = {'REGISTER', 'UNDO'}

    #execute
    def execute(self, context):
        main_edit_queue()

        return {'FINISHED'}


class MyOperator_open_folder(bpy.types.Operator):

    #operator attributes
    """Open the folder with the batch file"""
    bl_label = 'Open Folder'
    bl_idname = 'script.operator_open_folder'
    bl_options = {'REGISTER', 'UNDO'}

    #execute
    def execute(self, context):
        main_open_folder()

        return {'FINISHED'}


#registration
def register():
    bpy.utils.register_class(MyPanel)
    bpy.utils.register_class(MyOperator_add_to_queue)
    bpy.utils.register_class(MyOperator_edit_queue)
    bpy.utils.register_class(MyOperator_open_folder)
    bpy.utils.register_class(MyOperator_clear_queue)


def unregister():
    bpy.utils.register_class(MyPanel)
    bpy.utils.register_class(MyOperator_add_to_queue)
    bpy.utils.register_class(MyOperator_edit_queue)
    bpy.utils.register_class(MyOperator_open_folder)
    bpy.utils.register_class(MyOperator_clear_queue)


#enable to test the addon by running this script
if __name__ == '__main__':
    register()