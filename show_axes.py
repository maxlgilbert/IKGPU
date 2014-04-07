#!/usr/bin/python


def setup_openrave():
    # this is needed for OpenRave 0.8:
    #__builtins__.__openravepy_version__ = '0.8'
   
    import openravepy as rave
    or_obj = rave.Environment()
    or_obj.SetViewer('qtcoin')
    return or_obj


def show_ground_plane(or_obj):
    ''' 
    Adds a dark brown flat box representing a ground plane.
    '''     
    kinbody_str  = '<KinBody name="ground_plane">'
    kinbody_str += '  <Body type="static">'
    kinbody_str += '    <Geom type="box" name="ground_plane_box">'
    kinbody_str += '      <extents>3 3 0.005</extents>'
    kinbody_str += '      <diffusecolor>0.5 0.3 0.1</diffusecolor>'
    kinbody_str += '    </Geom>'
    kinbody_str += '    <Translation>0 0 -0.005</Translation>'
    kinbody_str += '  </Body>'
    kinbody_str += '</KinBody>'
    kb_ptr = or_obj.ReadKinBodyData(kinbody_str)
    or_obj.AddKinBody(kb_ptr)



def spawn_kinbody(kb_name, or_obj, filename, pose = None):
    import numpy as np

    kb_ptr = or_obj.ReadKinBodyXMLFile(filename)
    kb_ptr.SetName(kb_name)
    or_obj.AddKinBody(kb_ptr)
    if pose is not None:
        kb_ptr.SetTransform(np.array(pose))
    return kb_ptr



def get_axes_kb_name(name_identifier):
    return 'axes_' + name_identifier


def show_axes(axes_identifier, pose, or_obj, type = 'small'):
    kb_name = get_axes_kb_name(axes_identifier)
    axes_kb = or_obj.GetKinBody(kb_name)
    if axes_kb is None: # spawn the axes if they don't already exist
        if type == 'small':
            axes_kb = spawn_kinbody(kb_name, or_obj, 'data/or_smallaxes.kb.xml', pose)
        elif type == 'big':
            axes_kb = spawn_kinbody(kb_name, or_obj, 'data/or_axes.kb.xml', pose)
        elif type == 'colored':
            axes_kb = spawn_kinbody(kb_name, or_obj, 'data/color_axes.kb.xml', pose)
        else:
            print 'ERROR: unknown axes type', type
            return None
    else:
        # already found this kinbody, just set its pose
        axes_kb.SetTransform(pose)
        axes_kb.SetVisible(True)
    return True



def hide_axes(axes_identifier, or_env):
    from numpy import identity, array

    axes_kb = or_env.GetKinBody(get_axes_kb_name(axes_identifier))
    if axes_kb is None: 
        print 'ERROR: no axes found by name:', axes_name
        return None
    axes_kb.SetVisible(False)
    return True



if __name__ == '__main__':
    import sys

    or_obj = setup_openrave()
    if or_obj is None:
        print 'Error setting up OpenRave'
        sys.exit(-1)
    show_ground_plane(or_obj)

    kb_axes = spawn_kinbody(or_obj, 'data/or_axes.kb.xml')

    kb_smallaxes = spawn_kinbody(or_obj, 'data/or_smallaxes.kb.xml')
    new_pose = [[0.70710678, -0.70710678, 0, 0], \
                [0.70710678,  0.70710678, 0, 0], \
                [0,           0,          1, 0], \
                [0,           0,          0, 1]]
    kb_smallaxes.SetTransform(new_pose)

    new_pose = [[1, 0,           0,          0.1], \
                [0, 0.70710678, -0.70710678, 0.2], \
                [0, 0.70710678,  0.70710678, 0.3], \
                [0, 0,           0,          1]]
    kb_color_axes = spawn_kinbody(or_obj, 'data/color_axes.kb.xml', new_pose)

    raw_input('Press <Enter> when done')
    or_obj.Destroy()
