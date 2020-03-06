

def dataRootDir():
    import pkg_resources

    dataroot = pkg_resources.resource_filename(
        'epidemic_models',
        'data')
    return dataroot
