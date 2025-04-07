import bpy
from bpy.types import Panel

# Draws the .blend file specific settings used in the
# Popover panel or Side Panel panel
def draw_settings(self, context):
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False
    
    settings = context.scene.batch_export
    self.layout.operator('export_mesh.batch', icon='EXPORT')

    self.layout.separator()
    col = self.layout.column(align=True)
    col.prop(settings, 'directory')
    col.prop(settings, 'prefix')
    col.prop(settings, 'suffix')

    self.layout.separator()
    col = self.layout.column(align=True)
    col.label(text="Export Settings:")
    col.prop(settings, 'file_format')
    col.prop(settings, 'mode')
    col.prop(settings, 'limit')
    if 'OBJECT' in settings.mode:
        col.prop(settings, 'prefix_collection')


    self.layout.separator()
    col = self.layout.column()

    col.label(text=settings.file_format + " Settings:")
    if settings.file_format == 'DAE':
        col.prop(settings, 'dae_preset_enum')
        self.layout.prop(settings, 'apply_mods')
    elif settings.file_format == 'ABC':
        col.prop(settings, 'abc_preset_enum')
        col.prop(settings, 'frame_start')
        col.prop(settings, 'frame_end')
    elif settings.file_format == 'USD':
        col.prop(settings, 'usd_format')
        col.prop(settings, 'usd_preset_enum')
    elif settings.file_format == 'OBJ':
        col.prop(settings, 'obj_preset_enum')
        self.layout.prop(settings, 'apply_mods')
    elif settings.file_format == 'PLY':
        col.prop(settings, 'ply_ascii')
        self.layout.prop(settings, 'apply_mods')
    elif settings.file_format == 'STL':
        col.prop(settings, 'stl_ascii')
        self.layout.prop(settings, 'apply_mods')
    elif settings.file_format == 'FBX':
        col.prop(settings, 'fbx_preset_enum')
        self.layout.prop(settings, 'apply_mods')
    elif settings.file_format == 'glTF':
        col.prop(settings, 'gltf_preset_enum')
        self.layout.prop(settings, 'apply_mods')
    elif settings.file_format == 'X3D':
        col.prop(settings, 'x3d_preset_enum')
        self.layout.prop(settings, 'apply_mods')

    self.layout.use_property_split = False
    self.layout.separator()
    self.layout.label(text="Object Types:")
    grid = self.layout.grid_flow(columns=3, align=True)
    grid.prop(settings, 'object_types')

    self.layout.separator()
    col = self.layout.column(align=True, heading="Transform:")
    col.prop(settings, 'set_location')
    if settings.set_location:
        col.prop(settings, 'location', text="")  # text is redundant
    col.prop(settings, 'set_rotation')
    if settings.set_rotation:
        col.prop(settings, 'rotation', text="")
    col.prop(settings, 'set_scale')
    if settings.set_scale:
        col.prop(settings, 'scale', text="")

# Draws the button and popover dropdown button used in the
# 3D Viewport Header or Top Bar
def draw_popover(self, context):
    row = self.layout.row()
    row = row.row(align=True)
    row.operator('export_mesh.batch', text='', icon='EXPORT')
    row.popover(panel='POPOVER_PT_batch_export', text='')

# Side Panel panel (used with Side Panel option)
class VIEW3D_PT_batch_export(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Export"
    bl_label = "Batch Export"

    def draw(self, context):
        draw_settings(self, context)

# Popover panel (used on 3D Viewport Header or Top Bar option)
class POPOVER_PT_batch_export(Panel):
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_label = "Batch Export"

    def draw(self, context):
        draw_settings(self, context)
