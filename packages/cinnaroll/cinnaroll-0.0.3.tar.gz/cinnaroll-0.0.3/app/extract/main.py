import crawler as cl

# define path to project
project = '/Users/beniamin/PycharmProjects/bentest'

# path to script containing predict function
script = '/Users/beniamin/PycharmProjects/cinnaroll-python-lib/app/extract/main.py'

if __name__ == '__main__':
    script = cl.importedModule(script)
    modules = script.modules()
    objects = script.objects()
    code = script.code()

    print(objects)

    # cl.get_objects(cl)
