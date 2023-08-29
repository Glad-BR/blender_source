from . import common, tab0, tab1, tab2, tab3


def register():
    
    tab0.register()
    tab1.register()
    tab2.register()
    tab3.register()
    #tab4.register()
    
    common.register()


def unregister():
    
    tab0.unregister()
    tab1.unregister()
    tab2.unregister()
    tab3.unregister()
    #tab4.unregister()
    
    common.unregister()

