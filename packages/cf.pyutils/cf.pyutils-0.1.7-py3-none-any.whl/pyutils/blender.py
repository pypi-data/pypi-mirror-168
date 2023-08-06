import shutil
import zipimport, zipfile
import copy

class Addon:

    @staticmethod
    def list_extentions(path):
        reslist = list()
        for root, dir, files in os.walk(path):
            if "__init__.py" in files:
                full_path = os.path.join(root, "__init__.py")
                addon_name = os.path.basename(root)
                spec = importlib.util.spec_from_file_location(addon_name, full_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                reslist.append(mod)
        return reslist

@persistent
def load_addons(dummy):

    bpy.ops.wm.addon_refresh()

    bpy.app.handlers.load_post.remove(Addon.load_addons)

    if ATOM.extentions:
        for i in ATOM.extentions:
            print(i)
            bpy.ops.wm.addon_enable(module=i)
    
    bpy.ops.wm.save_userpref()

    return None

@staticmethod  
def check_addon(code):
    
    try:
        offset = code.index("bl_info")
    except ValueError:
        return None

    if code[offset-1] == "\n":  
        no_name = code[offset+7:].replace(" ", "").replace("\t", "").replace("\n","").replace("\r", "")

        if no_name[0] == "=" and no_name[1] == "{":  
            bracket_count = 0
            for i,c in enumerate(no_name[2:]):
                if c == "{":
                    bracket_count += 1
                    continue
                if c == "}":
                    if bracket_count:
                        bracket_count -= 1
                    else:
                        try:
                            exec("dic = %s"%no_name[1:i+3])
                        except SyntaxError:
                            return None
                        var = locals()["dic"]
                        if isinstance(var, dict):
                            if "name" in var:
                                return var

if config.DEBUG:
    
    @staticmethod
    def install_addons(path, mode):

        list = []
        dest_root = None

        def search(path, out):
            
            if "__init__.py" in os.listdir(path):
                full_path = os.path.join(path, "__init__.py")
                if os.path.isfile(full_path):
                    spec = importlib.util.spec_from_file_location("__init__", full_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, "bl_info"):
                        addon_name = os.path.basename(path)
                        out_dir = os.path.join(out, addon_name)
                        if os.path.exists(out_dir):
                            shutil.rmtree(out_dir)
                        shutil.copytree(path, out_dir)
                        list.append(addon_name)
            else:
                for i in os.listdir(path):
                    full_path = os.path.join(path, i)
                    if os.path.isfile(full_path):
                        if i[-3:] == ".py":
                            spec = importlib.util.spec_from_file_location(i[:-3], full_path)
                            mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(mod)
                            if hasattr(mod, "bl_info"):
                                shutil.copy(full_path, out)
                                list.append(i[:-3])
                    else:
                        search(full_path, out)

        if mode == ATOM_Types.InstallMod.USER:
            dest_root = os.path.join(os.environ['APPDATA'], "Roaming", "Blender Foundation", "Blender", bpy.app.version_string, "scripts", "addons")
            if not os.path.exists(dest_root):
                try:
                    os.makedirs(dest_root)
                except os.error:
                    raise "Cannot create install directory : %s"%sys.exc_info()[1]
                        
        if mode == ATOM_Types.InstallMod.LOCAL:
            dest_root = os.path.join(bpy.utils.script_path_user(), "addons")
        
        if dest_root:
            search(path, dest_root)

        return list

else:
    @staticmethod
    def install_addons(path, mode):
        
        addon_list = []

        if mode == ATOM_Types.InstallMod.USER:
            dest_root = os.path.join(os.environ['APPDATA'], "Roaming", "Blender Foundation", "Blender", bpy.app.version_string, "scripts", "addons")
            if not os.path.exists(dest_root):
                try:
                    os.makedirs(dest_root)
                except os.error:
                    raise "Cannot create install directory : %s"%sys.exc_info()[1]

        if mode == ATOM_Types.InstallMod.LOCAL:
            dest_root = os.path.join(bpy.utils.script_path_user(), "addons")

        for root, dir, files in os.walk(path):

            for file in files:

                full_path = os.path.join(root, file)

                if file[-3:] == ".py" and not file == "__init__.py":
                    dic = check_addon(open(full_path, "r").read())
                    if not dic == None:
                        if 
                        shutil.copy(full_path, dest_root)
                        addon_list.append(file[:-3])
                    continue

                if file[-4:] == ".zip":

                    zip_file = zipfile.ZipFile(full_path)
                    elements = zip_file.namelist()

                    if "__init__.py" in elements:
                        out_path = os.path.join(dest_root, file[:-4])
                        if check_addon(zip_file.read("__init__.py").decode("utf-8")) == None:
                            continue
                        else:
                            addon_list.append(file[:-4])
                        if not os.path.exists(out_path):
                            try:
                                os.makedirs(out_path)
                            except os.error:
                                raise "Cannot create install directory : %s"%sys.exc_info()[1]
                                continue
                    else:
                        out_path = dest_root
                        match = fnmatch.filter(elements, "*/__init__.py")
                        if match:
                            folder = os.path.join(full_path, match[0])
                            if check_addon(zip_file.read(match[0]).decode("utf-8")) == None:
                                continue
                            else:
                                addon_list.append(match[0][:-12])
                        else:
                            continue

                    zip_file.extractall(out_path)
                    zip_file.close()

        return addon_list

@staticmethod
def pack_addons(path, out):
    
    if "__init__.py" in os.listdir(path):
        full_path = os.path.join(path, "__init__.py")
        if os.path.isfile(full_path):
            spec = importlib.util.spec_from_file_location("__init__", full_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "bl_info"):
                shutil.make_archive(os.path.join(out,os.path.basename(path)),"zip", path)
    else:
        for i in os.listdir(path):
            full_path = os.path.join(path, i)
            if not os.path.isfile(full_path):
                Addon.pack_addons(full_path, out)

def resolve_tags(self, string):
    
    open = None
    out = ""
    max = len(string)

    for i,c in enumerate(string):
        if open == None:
            if c == "$":
                if i+1<max:
                    if string[i+1] == "(":   
                        open = i+2
            else:
                out += c
        elif c == ")":
            tag = self.checkTag(string[open:i])
            open = None
            if not tag == None:
                out += tag
    return out

def token(self, var):

    var = var.lower()

    if var.count(".") == 1 and i.replace(".", "").isdigit():
        return float(var)

    if var.isdigit():
        return int(var)

    if var in ("true", "on"):
        return True
    
    if var in ("false", "off"):
        return False

    if var in ("none", "null"):
        return None

    return var

def parse(self, varname, var):

    tmp = 1
    closure = ("[]", "{}", "()")
    start = (i[0] for i in closure)
    stop = (i[1] for i in closure)

    if var[0]+var[-1] in closure:
        for i in closure:
            if not var.count(i[0]) == var.count(i[1]):
                if DEBUG:
                    ERROR.raise_error(0,key=varname, file=self.__file)
                return var
        
        def recurse():


        for c in var:

            if 

            


        if var[0] == "[" and var[-1] == "]":
            return [i]

        if var[0] == "{" and var[-1] == "}":
            out = {}
            error_flag = 0x000
            for i in var.split(","):
                if len(i.split(":")) == 2:
                    if not i[0] or not i[1]:
                        
                    else:
                        out[i[0]] = out[1]
                else:
                    if DEBUG:
                        
                    return self.token()
        if DEBUG

def checkList(self, var):
    

def checkTag(self, tag):
    
    if tag in self.__vars:
        return self.__vars[tag]

    # if tag == "ADDON_ROOT":
    #     return os.path.dirname(__file__)
    
    return None
