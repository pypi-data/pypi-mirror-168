"""
Parse DFN to extract format for blocks.

Created on Thu Sep  1 22:34:27 2022

@author: mtoews
"""
import json
import hashlib
from collections import Counter
from pathlib import Path

mf6ivar_dir = Path("/data/mtoews/src/modflow6/doc/mf6io/mf6ivar")
dfn_dir = mf6ivar_dir / "dfn"
json_dir = mf6ivar_dir / "json"

# %%

def read_common_dfn(fname):
    common = {}
    for line in fname.read_text().split("\n"):
        if line == "" or line.startswith("#"):
            continue
        elif line.startswith("name "):
            name = line[5:]
        elif line.startswith("description "):
            assert name not in common
            common[name] = line[12:]
        else:
            raise ValueError(line)
    return common


type_map = {
    "string": "str",
    # "keyword": "str",
    "double precision": "float",
    "double": "float",
    "integer": "int",
}
type_cast_map = {
    "str": str,
    "float": float,
    "int": int,
}
bool_map = {
    "true": True,
    "True": True,
    None: True,
    "false": False,
}

label_c = Counter()
shape_c = Counter()
reader_c = Counter()


def read_blocks_dfn(fname):
    fname = Path(fname)
    blocks = {}
    var = None
    in_record_s = {}
    in_record_c = Counter()
    subvar_c = Counter()

    def append_block_variable(var):
        if var is None:
            return None
        block_name = var.pop("block")
        var_name = var.pop("name")
        # remove redundant info
        if "tagged" in var:
            if var["type"] == "keyword" and var["tagged"] is True:
                # almost always true except for one
                del var["tagged"]
            if var["type"] in (int,) and var["tagged"] is False:
                print("barf")
        if var.get("layered") is False:
            del var["layered"]
        if var.get("preserve_case") is False:
            del var["preserve_case"]
        if var.get("numeric_index") is False:
            del var["numeric_index"]
        if var.get("in_record") is True:
            in_record_c[var_name] += 1
            rec_md5 = hashlib.md5(repr(var).encode()).hexdigest()[:6]
            if var_name in in_record_s:
                in_record_s[var_name].add(rec_md5)
            else:
                in_record_s[var_name] = {rec_md5}
            # in_record[var_name] = var
        if block_name not in blocks:
            blocks[block_name] = {}
        if var_name in blocks[block_name]:
            if blocks[block_name][var_name] == var:
                print(f"dublicate {block_name}: {var_name}")
            else:
                print(f"replacing different {block_name}: {var_name}")
                print("old", blocks[block_name][var_name])
                print("new", var)
        blocks[block_name][var_name] = var
        return None

    for line in fname.read_text().split("\n"):
        if line.startswith("#"):
            continue
        elif line == "":
            append_block_variable(var)
            var = None
            continue
        pos = line.find(" ")
        if pos > 0:
            label = line[:pos]
            value = line[(pos + 1):]
        else:
            label = line
            value = None
        if var is None:  # Start of a new block variable
            assert label == "block", (fname.name, label, value)
            var = {"block": value}
        else:  # var is not None
            label_c[label] += 1
            if label == "reader":
                reader_c[value] += 1
                continue  # don't keep, just count
            elif label == "description":
                if isinstance(value, str) and value.startswith("REPLACE "):
                    pos = value.find(" ", 8)
                    word = value[8:pos].strip()
                    reptxt = value[pos:].strip()
                    rep = eval(reptxt)
                    value = common[word]
                    for find, replace in rep.items():
                        if find in value:
                            value = value.replace(find, replace)
                        # else:
                        #    print(f"{word}: {find!r} not found in '{value}'")
                    if "{#" in value:
                        print(f"{word}: missing replacement(s) in '{value}'")
            # elif label == "longname" and value is None:
            #    continue  # missing/empty
            elif label == "type":
                if value in type_map:
                    value = type_map[value]
                parts = value.split()
                if len(parts) > 2:
                    value = parts[0]
                    var["members_list"] = parts[1:]
                    for key in parts[1:]:
                        subvar_c[key] += 1

            elif label == "default_value":
                if var["type"] in type_cast_map:
                    try:
                        value = type_cast_map[var["type"]](value)
                    except TypeError:
                        # pass
                        raise ValueError(f"{line} with {var['type']}")
            elif label in (
                    "block_variable", "in_record", "just_data", "layered",
                    "numeric_index", "optional", "preserve_case", "repeating",
                    "support_negative_index", "tagged", "time_series"):
                value = bool_map[value]
            elif label == "shape":
                shape_c[value] += 1
                if value is None:
                    continue
            elif label == "valid":
                if value is not None:
                    value = value.split()
            var[label] = value
    append_block_variable(var)  # final block variable in file

    # Find vars shared between more than one record, don't move them
    shared_in_record_d = {}
    for block_name, block in blocks.items():
        in_record_c = Counter()
        subvar_c = Counter()
        for var_name, var in block.items():
            if "in_record" in var:
                in_record_c[var_name] += 1
            if "members_list" in var:
                for key in var["members_list"]:
                    subvar_c[key] += 1
        one_in_record = {key for key, cnt in in_record_c.items() if cnt == 1}
        multi_subvar = {key for key, cnt in subvar_c.items() if cnt > 1}
        shared_in_record_s = one_in_record.intersection(multi_subvar)
        shared_in_record_d[block_name] = {}
        for var_name in shared_in_record_s:
            var = block.pop(var_name)
            assert var.pop("in_record") is True
            shared_in_record_d[block_name][var_name] = var

    def nest_var(block, var_name):
        if var_name not in block:
            return
        var = block[var_name]
        if "members_list" in var:
            var["members_list"] = var.pop("members_list")  # move to end
            var["members"] = {}
            for key in var["members_list"]:
                if key in shared_in_record_d[block_name]:
                    var["members"][key] = shared_in_record_d[block_name][key]
                elif key in block:
                    if "in_record" in block[key]:
                        if block[key]["in_record"] is not True:
                            print(f"curious {fname.name}: {key}:", block[key]["in_record"])
                        else:
                            del block[key]["in_record"]
                    nest_var(block, key)  # recurse
                    var["members"][key] = block.pop(key)  # relocate
                else:
                    raise KeyError(
                        f"{fname.name} missing: {key} from {block_name} block")
        return

    for block_name, block in blocks.items():
        for var_name in list(block.keys()):
            nest_var(block, var_name)

    return blocks


# %%
fname_blocks = {}
for fname in sorted(dfn_dir.glob("*.dfn")):
    if fname.name == "common.dfn":
        common = read_common_dfn(fname)
    else:
        fname_blocks[fname.stem] = read_blocks_dfn(fname)
with open(mf6ivar_dir / "mf6ivar.json", "w") as fp:
    json.dump(fname_blocks, fp, indent=2, sort_keys=False)
    fp.write("\n")
