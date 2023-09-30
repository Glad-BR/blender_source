from . import common, tab0, tab1, tab01, tab2, tab3, ui_list


def register():
    
    common.register()
    
    tab0.register()
    tab01.register()
    tab1.register()
    tab2.register()
    tab3.register()
    
    ui_list.register()


def unregister():
    
    common.unregister()
    
    tab0.unregister()
    tab01.unregister()
    tab1.unregister()
    tab2.unregister()
    tab3.unregister()
    
    ui_list.unregister()

