



def show_wrist_fk(theta_4, theta_5, theta_6, or_obj):
        import show_axes
        from numpy import identity, matrix, array, pi
        from transformations import euler_matrix

        origin_pose = identity(4)

        # show ground plane
        #show_axes.show_ground_plane(or_obj)

        # show origin
        show_axes.show_axes('origin', origin_pose, or_obj, 'small')
        
        # show the solution
        # theta 4
        raw_input("<Enter> to show theta_4")
        joint_xform = euler_matrix(0.0, 0.0, theta_4)
        theta_4_pose = matrix(origin_pose) * matrix(joint_xform)
        show_axes.show_axes('theta_4', array(theta_4_pose), or_obj, 'colored')
        
        # theta 5
        raw_input("<Enter> to show theta_5")
        show_axes.hide_axes('theta_4', or_obj)  # hide previous axes (comment this out to keep it)
        offset_xform = euler_matrix(pi/2, 0.0, 0.0)
        joint_xform = euler_matrix(0.0, 0.0, theta_5)
        theta_5_pose = theta_4_pose * matrix(offset_xform) * matrix(joint_xform)
        show_axes.show_axes('theta_5', array(theta_5_pose), or_obj, 'colored')

        # theta 6
        raw_input("<Enter> to show theta_6")
        show_axes.hide_axes('theta_5', or_obj)  # hide previous axes (comment this out to keep it)
        offset_xform = euler_matrix(-pi/2, 0.0, 0.0)
        joint_xform = euler_matrix(0.0, 0.0, theta_6)
        theta_6_pose = theta_5_pose * matrix(offset_xform) * matrix(joint_xform)
        show_axes.show_axes('theta_6', array(theta_6_pose), or_obj, 'colored')

        raw_input("<Enter> to hide solution")
        show_axes.hide_axes('theta_6', or_obj)
        
        return



def test_wrist_ik(goal_roll, goal_pitch, goal_yaw, or_obj = None):
    from math import cos, sin, atan2
    from transformations import euler_matrix
    # try:
    #     import tf
    #     R = tf.transformations.euler_matrix(goal_roll, goal_pitch, goal_yaw)
    # except ImportError:
    #     print 'TF module not found, using local euler_matrix()'
    #     R = euler_matrix(goal_roll, goal_pitch, goal_yaw)

    R = euler_matrix(goal_roll, goal_pitch, goal_yaw)

    # do the math
    theta_4 = atan2(-R[1,2], -R[0,2])
    
    s_theta_5 = -R[0,2] * cos(theta_4) - R[1,2] * sin(theta_4)
    c_theta_5 = R[2,2]
    theta_5 = atan2(s_theta_5, c_theta_5)

    s_theta_6 = -R[0,0] * sin(theta_4) + R[1,0] * cos(theta_4)
    c_theta_6 = -R[0,1] * sin(theta_4) + R[1,1] * cos(theta_4)
    theta_6 = atan2(s_theta_6, c_theta_6)

    print 'Solution:', (theta_4, theta_5, theta_6)

    # visualize if an OpenRave object is provided
    if or_obj:
        import show_axes

        # show goal
        show_axes.show_axes('goal', R, or_obj, 'small')

        show_wrist_fk(theta_4, theta_5, theta_6, or_obj)

    return 
    




if __name__ == '__main__':
    import sys
    import show_axes

    # setup goal orientation
    goal_roll  = 0.5
    goal_pitch = 0.7
    goal_yaw   = 0.9


