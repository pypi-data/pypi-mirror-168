import inspect
from modulefinder import ModuleFinder


class importedModule():

    def __init__(self, script):
        self.script = script

    # get modules from script
    def modules(self):
        finder = ModuleFinder()
        finder.run_script(self.script)

        self.filtered = []
        modules = finder.modules.items()

    # search in globalnames with logic: globalnames.keys = modules.keys
        globals = []
        for name, mod in modules:
            globals.append(mod.globalnames.keys())

        l_globals = []
        for g in globals:
            l_globals.append(list(g))

        for m in list(modules):
            if any(m[0] in x for x in l_globals):
                self.filtered.append(m)
        return self.filtered

    # get classes and functions defined in modules
    def objects(self):
        self.contents = []
        for m in self.filtered:
            for name, obj in inspect.getmembers(m):
                if not name.startswith('__'):
                    self.contents.append(obj)
        return self.contents

    # get class and function definitions in modules
    def code(self):
        self.syntax = []
        for elements in self.contents:
            for i in elements:
                lines = inspect.getsource(i)
                self.syntax.append(lines)
        return self.syntax
