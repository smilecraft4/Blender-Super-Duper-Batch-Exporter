# SPDX-FileCopyrightText: 2016-2024 Bastian L. Strube
#
# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "Super Duper Batch Exporter",
    "author": "Bastian L Strube, Mrtripie",
    "version": (2, 4, 1),
    "blender": (4, 2, 0),
    "category": "Import-Export",
    "location": "Set in preferences below. Default: Top Bar (After File, Edit, ...Help)",
    "description": "Batch export the objects in your scene into seperate files",
    "warning": "Relies on the export add-on for the format used being enabled",
    "doc_url": "https://github.com/bastianlstrube/Blender-Super-Duper-Batch-Exporter",
}

import bpy
from . import utils
from . import operators
from . import panels
from . import preferences
from . import properties

def register():
    # Register classes
    bpy.utils.register_class(preferences.BatchExportPreferences)
    bpy.utils.register_class(properties.BatchExportSettings)
    bpy.utils.register_class(panels.POPOVER_PT_batch_export)
    bpy.utils.register_class(panels.VIEW3D_PT_batch_export)
    bpy.utils.register_class(operators.EXPORT_MESH_OT_batch)
    
    # Add batch export settings to Scene type
    bpy.types.Scene.batch_export = bpy.props.PointerProperty(type=properties.BatchExportSettings)
    
    # Always append the draw_popover function to menus
    bpy.types.TOPBAR_MT_editor_menus.append(panels.draw_popover)
    bpy.types.VIEW3D_MT_editor_menus.append(panels.draw_popover)
    
    # Print to console for debugging
    print("Batch Export addon registered successfully")

def unregister():
    # Remove the panel from menus
    bpy.types.TOPBAR_MT_editor_menus.remove(panels.draw_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(panels.draw_popover)
    
    # Unregister classes
    bpy.utils.unregister_class(panels.VIEW3D_PT_batch_export)
    bpy.utils.unregister_class(panels.POPOVER_PT_batch_export)
    bpy.utils.unregister_class(operators.EXPORT_MESH_OT_batch)
    bpy.utils.unregister_class(properties.BatchExportSettings)
    bpy.utils.unregister_class(preferences.BatchExportPreferences)
    
    # Remove properties
    del bpy.types.Scene.batch_export
    
    print("Batch Export addon unregistered")



if __name__ == '__main__':
    register()