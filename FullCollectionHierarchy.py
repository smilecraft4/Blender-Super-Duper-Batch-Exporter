# Blender Python Snippet: Check Collection Hierarchy

import bpy
import os

def find_parent_collection(target_coll):
    """
    Finds the immediate parent collection of a given collection within the scene.

    Args:
        target_coll (bpy.types.Collection): The collection whose parent is to be found.

    Returns:
        bpy.types.Collection or None: The parent collection, or None if no parent
                                       is found within the standard hierarchy
                                       (e.g., orphaned, or already the scene collection).
    """
    # Check if it's a direct child of the master scene collection first
    # Ensure we have a valid context and scene
    if bpy.context and bpy.context.scene:
        scene_collection = bpy.context.scene.collection
        if target_coll in scene_collection.children.values():
            return None

    # If not directly under the scene collection, check other collections
    for coll in bpy.data.collections:
        # Avoid checking the collection against itself if it has children
        if coll == target_coll:
            continue
        if target_coll in coll.children.values():
            return coll

    # Return None if no parent is found (should typically only happen for the Scene Collection itself)
    return None

def check_collection_hierarchy(start_coll_name, top_level_coll_name="Scene Collection"):
    """
    Checks if a collection is ultimately part of a specified top-level collection
    (defaults to the Scene Collection) by traversing up the hierarchy. Prints the path.

    Args:
        start_coll_name (str): The name of the collection to start checking from.
        top_level_coll_name (str, optional): The name of the target top-level collection.
                                             Defaults to "Scene Collection".

    Returns:
        bool: True if the start collection is part of the top-level collection's
              hierarchy, False otherwise.
    """
    start_coll = bpy.data.collections.get(start_coll_name)
    if not start_coll:
        print(f"Error: Start collection '{start_coll_name}' not found.")
        return False

    top_level_coll = None
    # Special handling for the main "Scene Collection"
    if top_level_coll_name == "Scene Collection":
        if bpy.context and bpy.context.scene:
            top_level_coll = bpy.context.scene.collection
        else:
            print(f"Error: Cannot access Scene Collection. No active scene context.")
            # As a fallback, try name lookup, though it's usually accessed via context
            top_level_coll = bpy.data.collections.get(top_level_coll_name)
    else:
        # For any other named collection
        top_level_coll = bpy.data.collections.get(top_level_coll_name)

    if not top_level_coll:
        # Avoid repeating the context error message if that was the issue
        if not (top_level_coll_name == "Scene Collection" and not (bpy.context and bpy.context.scene)):
             print(f"Error: Top-level collection '{top_level_coll_name}' not found.")
        return False

    print(f"Checking hierarchy for collection: '{start_coll.name}' up to '{top_level_coll.name}'")

    current_coll = start_coll
    path = [current_coll.name]

    # Handle cases where the start collection *is* the top-level collection
    if current_coll == top_level_coll:
        print(f"'{current_coll.name}' is the specified top-level collection.")
        return True

    # Loop upwards through parents
    while True:
        parent_coll = find_parent_collection(current_coll)

        if parent_coll:
            path.append(parent_coll.name)
            if parent_coll == top_level_coll:
                print("Hierarchy path found:")
                print(os.path.join(*reversed(path)))
                return True
            else:
                # Move up to the parent for the next iteration
                current_coll = parent_coll
        else:
            # No parent found, means we've hit the top without finding the target
            # (or the collection is orphaned)
            print(f"Error: Could not trace '{start_coll.name}' back to '{top_level_coll.name}'.")
            print("Path traced:")
            print(os.path.join(*reversed(path)))
            return False

# --- Example Usage ---
# IMPORTANT: Replace 'My Sub Collection' with the actual name of a collection
#            in your Blender scene hierarchy.

# Example: Check if 'My Sub Collection' is under 'Scene Collection'
COLLECTION_TO_CHECK = "Collection 25" # <-- CHANGE THIS NAME
check_collection_hierarchy(COLLECTION_TO_CHECK)

# Example: Check if 'My Sub Collection' is under another collection named 'Parent Group'
# check_collection_hierarchy(COLLECTION_TO_CHECK, top_level_coll_name="Parent Group")


# --- How to run in Blender ---
# 1. Open Blender.
# 2. Create some nested collections if you don't have any (e.g., Scene Collection > Parent Collection > My Sub Collection).
# 3. Go to the 'Scripting' workspace tab.
# 4. Click '+ New' to create a new text file.
# 5. Paste this entire code block into the Blender Text Editor.
# 6. **Crucially:** Modify the `COLLECTION_TO_CHECK = "My Sub Collection"` line to use the exact name of a collection present in your scene.
# 7. Click the 'Run Script' button (it looks like a play icon ▶️).
# 8. Look for the output in the Blender System Console (Window menu -> Toggle System Console).