bl_info = {
    'name' : 'Glitch',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (2, 79),
    'location' : 'View 3D > Tools > Glitch',
    'description' : 'Glitches the objects in the scene',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Glitch'
    }


import bpy
import random


#---the glitch script----------------------------------------------------------------------------------------------------------------------------------------------


def script_glitch_obj():

    #export obj
    def exportOBJ():
        bpy.ops.export_scene.obj(filepath = exportedFile, use_materials = False)


    #import OBJ
    def importOBJ():
        #delete all objects in scene
        bpy.ops.object.select_all(action = 'SELECT')
        bpy.ops.object.delete(use_global = False)

        #open glitched file
        bpy.ops.import_scene.obj(filepath = glitchedFile)


    #change numbers in obj file
    def randomNumbers(n):
        if n != 0:
            exportOBJ()
            f = open(exportedFile)
            fn = open(glitchedFile, 'w')
            for l in f:
                if l[0] == 'v':
                    if random.random() < n:
                        rn1 = random.choice(range(10))
                        rn2 = random.choice(range(10))
                        l = [str(rn1) if i == str(rn2) else i for i in l]

                fn.write(''.join(l))

            f.close()
            fn.close()
            importOBJ()
        else:
            pass


    #shuffle vertex lines
    def shuffleVertices(n):
        if n != 0:
            exportOBJ()
            f1 = open(exportedFile)
            f2 = open(exportedFile)
            fn = open(glitchedFile, 'w')

            a = [l for l in f1 if l[0:2] == 'v ']
            random.shuffle(a)

            for l in f2:
                if l[0:2] == 'v ':
                    if random.random() < n:
                        l = a[random.choice(range(len(a)))]

                fn.write(''.join(l))

            f1.close()
            f2.close()
            fn.close()
            importOBJ()
        else:
            pass


    #remove faces
    def removeFaces(n):
        if n != 0:
            exportOBJ()
            f = open(exportedFile)
            fn = open(glitchedFile, 'w')

            for l in f:
                if l[0] == 'f':
                    if random.random() < n:
                        l = ''

                fn.write(''.join(l))

            f.close()
            fn.close()
            importOBJ()
        else:
            pass


    def glitch(n1, n2, n3):
        shuffleVertices(n1)
        randomNumbers(n2)
        removeFaces(n3)


    #set shading to flat for all mesh objects in the scene
    def flatShadingAllObjects():
        for i in bpy.data.objects:
            if i.type == 'MESH':
                for p in i.data.polygons:
                    p.use_smooth = False


    #the obj file is saved to and loaded from the temp folder
    exportedFile = bpy.app.tempdir + 'modelExport.obj'
    glitchedFile = bpy.app.tempdir + 'modelGlitched.obj'


    #call the glitch function
    glitch(.1, .1, .1)
    flatShadingAllObjects()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------


#panel class
class Panel_Glitch(bpy.types.Panel):

    #panel attributes
    """Panel with glitch tools"""
    bl_label = 'Glitch'
    bl_idname = 'panel_glitch'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Glitch'

    #draw loop
    def draw(self, context):
        layout = self.layout
        layout.operator('glitch.glitch_obj', text="Glitch OBJ")


#operator class
class Operator_GlitchObj(bpy.types.Operator):

    #operator attributes
    """Glitches the objects in the scene"""
    bl_label = 'Glitch OBJ'
    bl_idname = 'glitch.glitch_obj'
    bl_options = {'REGISTER', 'UNDO'}

    #execute
    def execute(self, context):
        script_glitch_obj();

        return {'FINISHED'}


#registration
def register():
    bpy.utils.register_class(Panel_Glitch)
    bpy.utils.register_class(Operator_GlitchObj)


def unregister():
    bpy.utils.register_class(Panel_Glitch)
    bpy.utils.register_class(Operator_GlitchObj)


#enable to test the addon by running this script
if __name__ == '__main__':
    register()
