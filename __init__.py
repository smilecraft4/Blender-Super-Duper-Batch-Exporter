# SPDX-FileCopyrightText: 2016-2024 Bastian L. Strube
#
# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "Super Duper Batch Exporter",
    "author": "Bastian L Strube, Mrtripie",
    "version": (2, 4, 0),
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
    bpy.utils.register_class(operators.EXPORT_MESH_OT_batch)

    # Add batch export settings to Scene type
    bpy.types.Scene.batch_export = bpy.props.PointerProperty(type=properties.BatchExportSettings)

    # Show addon UI
    prefs = bpy.context.preferences.addons[__name__].preferences
    if prefs.addon_location == 'TOPBAR':
        bpy.types.TOPBAR_MT_editor_menus.append(panels.draw_popover)
    if prefs.addon_location == '3DHEADER':
        bpy.types.VIEW3D_MT_editor_menus.append(panels.draw_popover)
    elif prefs.addon_location == '3DSIDE':
        bpy.utils.register_class(panels.VIEW3D_PT_batch_export)


def unregister():
    # Delete the settings from Scene type (Doesn't actually remove existing ones from scenes)
    del bpy.types.Scene.batch_export

    # Unregister Classes
    bpy.utils.unregister_class(preferences.BatchExportPreferences)
    bpy.utils.unregister_class(properties.BatchExportSettings)
    bpy.utils.unregister_class(panels.POPOVER_PT_batch_export)
    bpy.utils.unregister_class(operators.EXPORT_MESH_OT_batch)

    # Remove UI
    bpy.types.TOPBAR_MT_editor_menus.remove(panels.draw_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(panels.draw_popover)
    if hasattr(bpy.types, "VIEW3D_PT_batch_export"):
        bpy.utils.unregister_class(panels.VIEW3D_PT_batch_export)


if __name__ == '__main__':
    register()