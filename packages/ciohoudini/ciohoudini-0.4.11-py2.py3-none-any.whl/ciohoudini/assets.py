import hou
import re
import os
from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
from ciopath.gpath import Path
from ciohoudini import common

def resolve_payload(node, do_asset_scan, **kwargs):
    """
    Resolve the upload_paths field for the payload.

    """

    path_list = PathList()
    path_list.add(hou.hipFile.path())
    path_list.add(*extra_paths(node))
    
    ocio_file = os.environ.get("OCIO")
    if ocio_file:
        path_list.add(os.path.dirname(ocio_file))

    if do_asset_scan:
        path_list.add(*scan_paths(node))

    render_script = node.parm("render_script").eval()
    if render_script:
        # Make the render script optional, by putting the last char in sq brackets 
        render_script = "{}[{}]".format(render_script[:-1], render_script[-1])
        path_list.add(render_script)

    # Prefix any relative paths with HIP. It's the best we can do for now.
    # However some relative paths may be internal stuff like op:blah or temp:blah,
    # we'll ignore them for now.
    root = hou.getenv("HIP")
    valid_path_list = PathList()
    for path in path_list:
        if path.relative:
            if ":" not in path.fslash():
                valid_path = os.path.join(root, path.fslash())
                valid_path_list.add(valid_path)
        else:
            valid_path_list.add(path)

    # Print the list of missing files:
    for path in valid_path_list:
        pp = path.fslash()
        if GLOBBABLE_REGEX.search(pp):
            continue
        if not os.path.exists(pp):
            print( "Skipping: '{}'. No such file or directory.".format(pp))

    valid_path_list.remove_missing()
    valid_path_list.glob()

    # Make sure none of the paths are in the output folder.
    out_folder =  Path(node.parm('output_folder').eval())
    for path in valid_path_list:
        if path.startswith(out_folder):
            print( "The asset {} exists in the output folder '{}'. It will not be uploaded.".format(path.fslash(), out_folder.fslash()))
            valid_path_list.remove(path)

    return {"upload_paths": sorted([p.fslash() for p in valid_path_list])}
  
def extra_paths(node, **kwargs):
    path_list = PathList()
    num = node.parm("extra_assets_list").eval()
    for i in range(1, num + 1):
        asset = node.parm("extra_asset_{:d}".format(i)).eval()
        if asset:
            path_list.add(asset)

    return path_list


def scan_paths(node):
    """
    Scan for assets.

    If we are generating data for the preview panel, then only show assets if the button was
    explicitly clicked, since dep scan may be expensive.
    """

    path_list = PathList()
    parms = _get_file_ref_parms()

    # regex to find all patterns in an evaluated filename that could represent a varying parameter.
    regex = node.parm("asset_regex").unexpandedString()
    REGEX = re.compile(regex, re.IGNORECASE)

    for parm in parms:
        evaluated = parm.eval()
        if evaluated:
            pth = REGEX.sub(r"*", evaluated)
            path_list.add(pth)

    return path_list


def _get_file_ref_parms():
    parms = []
    refs = hou.fileReferences()
    for parm, _ in refs:
        if not parm:
            continue
        if parm.node().type().name().startswith("conductor::job"):
            continue
        parms.append(parm)
    return parms


def clear_all_assets(node, **kwargs):
    node.parm("extra_assets_list").set(0)


def browse_files(node, **kwargs):
    files = hou.ui.selectFile(
        title="Browse for files to upload",
        collapse_sequences=True,
        file_type=hou.fileType.Any,
        multiple_select=True,
        chooser_mode=hou.fileChooserMode.Read,
    )
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)


def browse_folder(node, **kwargs):

    files = hou.ui.selectFile(title="Browse for folder to upload", file_type=hou.fileType.Directory)
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)



def add_entries(node, *entries):
    """
    Add entries to the asset list.
    
    These new entries and the existing entries are deduplicated. PathList object automatically
    deduplicates on access.
    """

    path_list = PathList()
    
    num = node.parm("extra_assets_list").eval()
    for i in range(1, num + 1):
        asset = node.parm("extra_asset_{:d}".format(i)).eval()
        if asset:
            path_list.add(asset)

    for entry in entries:
        path_list.add(entry)

    paths = [p.fslash() for p in path_list]

    node.parm("extra_assets_list").set(len(paths))
    for i, arg in enumerate(paths):
        index = i + 1
        node.parm("extra_asset_{:d}".format(index)).set(arg)

def remove_asset(node, index):
    curr_count = node.parm("extra_assets_list").eval()
    for i in range(index + 1, curr_count + 1):
        from_parm = node.parm("extra_asset_{}".format(i))
        to_parm = node.parm("extra_asset_{}".format(i - 1))
        to_parm.set(from_parm.unexpandedString())
    node.parm("extra_assets_list").set(curr_count - 1)

def add_hdas(node, **kwargs):
    """
    Add all hda folders to the asset list.

    Called from a button in the UI. It's just a convenience. User could also browse for HDAs by
    hand.
    """
 
    hda_paths = [hda.libraryFilePath() for hda in common.get_plugin_definitions()]
    if not hda_paths:
        return

    add_entries(node, *hda_paths)
