dependencies = {
    'asp/environment_property/position.lp': 
        [],
    'asp/environment_property/conflict_point.lp': 
        ['asp/environment_property/position.lp'],

    'asp/environment_property/delta.lp': 
        ['asp/environment_property/conflict_point.lp',
         'asp/environment_property/position.lp'],

    'asp/environment_property/conflict_point_edge.lp': 
        ['asp/environment_property/conflict_point.lp',
         'asp/environment_property/position.lp'],

    'asp/environment_property/delta_conflict_point.lp': 
        ['asp/environment_property/conflict_point.lp',
         'asp/environment_property/position.lp',
         'asp/environment_property/conflict_point_edge.lp',
         'asp/environment_property/delta.lp'],
    
    'asp/environment_property/delta_conflict_point_edge.lp':
        ['asp/environment_property/conflict_point_edge.lp'],
}