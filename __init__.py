# SPDX-FileCopyrightText: 2016-2024 Bastian L. Strube
#
# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "Super Duper Batch Exporter",
    "author": "Bastian L Strube, forked from Mrtripie",
    "version": (2, 5, 0),
    "blender": (4, 2, 0),
    "category": "Import-Export",
    "location": "Set in preferences below. Default: Top Bar (After File, Edit, ...Help)",
    "description": "Batch export the objects in your scene into seperate files",
    "warning": "Relies on the export add-on for the format used being enabled",
    "doc_url": "https://github.com/bastianlstrube/Blender-Super-Duper-Batch-Exporter",
}
from bpy.types import Scene, TOPBAR_MT_editor_menus, VIEW3D_MT_editor_menus
from bpy.props import PointerProperty
from bpy.utils import register_class, unregister_class
import importlib

from . import panels, properties

module_names = [
    "preferences",
    "properties",
    "panels",
    "operators", 
]

modules = [
    __import__(__package__ + "." + submod, {}, {}, submod)
    for submod in module_names
]


def register_unregister_modules(modules: list, register: bool):
    """Recursively register or unregister modules by looking for either
    un/register() functions or lists named `registry` which should be a list of
    registerable classes.
    """
    register_func = register_class if register else unregister_class
    un = 'un' if not register else ''

    for m in modules:
        if register:
            importlib.reload(m)
        if hasattr(m, 'registry'):
            for c in m.registry:
                try:
                    register_func(c)
                except Exception as e:
                    print(
                        f"Warning: Pie Menus failed to {un}register class: {c.__name__}"
                    )
                    print(e)

        if hasattr(m, 'modules'):
            register_unregister_modules(m.modules, register)

        if register and hasattr(m, 'register'):
            m.register()
        elif hasattr(m, 'unregister'):
            m.unregister()


def register():
    register_unregister_modules(modules, True)

    # Add batch export settings to Scene type
    Scene.batch_export = PointerProperty(type=properties.BatchExportSettings)
    
    # Always append the draw_popover function to menus
    TOPBAR_MT_editor_menus.append(panels.draw_popover)
    VIEW3D_MT_editor_menus.append(panels.draw_popover)


def unregister():
    register_unregister_modules(reversed(modules), False)

    # Remove the panel from menus
    TOPBAR_MT_editor_menus.remove(panels.draw_popover)
    VIEW3D_MT_editor_menus.remove(panels.draw_popover)

    # Remove properties
    #del bpy.types.Scene.batch_export  # THIS SHOULD BE ADDED AS A BUTTON IN THE PREFERENCES INSTEAD