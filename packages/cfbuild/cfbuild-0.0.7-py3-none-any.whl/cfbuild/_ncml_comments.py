from ._constants import VARIABLE_TYPE_INDICATORS

GLOBAL_ATTRIBUTES_COMMENT = 'These are global attributes'

DIMENSIONS = 'These are dimensions'

T_COORDINATE_VARIABLE = 'This is the time coordinate variables'

Z_COORDINATE_VARIABLE = 'This is the height coordinate variables'

Y_COORDINATE_VARIABLE = 'This is the y coordinate variables'

X_COORDINATE_VARIABLE = 'This is the x coordinate variables'

COORDINATE_VARIABLE = 'These are coordinate variables'

AUXILIARY_COORDINATE_VARIABLE = 'These are auxiliary coordinate variables'

SCALAR_COORDINATE_VARIABLE = 'these are scalar coordinate variables'

GEOREFERENCED_DATA_VARIABLE = 'These are the georeferenced data variables'

DATA_VARIABLE = 'These are the data variables'

ANCILLARY_DATA_VARIABLE = 'ancillary data variables'

GRID_MAPPING_VARIABLE = 'grid mapping variables' 

DOMAIN_VARIABLE = 'domain variables'

BOUNDARY_VARIABLE = 'boundary variables'

CELL_MEASURE_VARIABLE = 'cell measure variables'

UNKNOWN_VARIABLE = 'unknown variables'

STANDARD_NAME_WARNING = ['WARNING - The given standard name (', ') was not found in the standard name table: '
                                                                'https://cfconventions.org/Data/cf-standard-names/'
                                                                'current/build/cf-standard-name-table.html']

TEMPORAL_UNITS_WARNING = 'WARNING - Specify the temporal units in the form of UNITS since DATE'

UNITS_WARNING = ['WARNING - The given units (', 
                 ') are not equivalent to the canonical units for the given standard name (', ')']

OPENDAP_RESERVED_KEYWORDS_WARNING = ['WARNING - The variable name "', '" is a reserved OPeNDAP keyword. If the '
                                                                      'name is not changed, the dataset will not '
                                                                      'work properly with OPeNDAP.']

DATA_TYPE_WARNING = ['WARNING - The variable datatype "', '" is  not compatible with OPeNDAP. Please specify an int16, '
                                                          'int32, float32, float64, str, or char datatype.']

ADD_GRID_MAPPING_VARIABLE = ['WARNING - a grid mapping variable should be added that specifies the coordinate'
                             ' reference system used.']

MISSING_VALUES_ERROR = ['ERROR - The coordinate variable (', ') is missing values. Please specify new values.']

MONOTONIC_VALUES_ERROR = ['ERROR - The coordinate variable (', ') must have monotonically increasing values. '
                                                               'Please specify new values.']

CANT_GET_VALUES_WARNING = ['INFO - Cannot check values for ', '.']

MULTIDIMENSIONAL_WARNING = 'WARNING - Coordinate variables should be one dimensional.'

VALID_RANGE_WARNING = 'WARNING - The actual range of the data is outside the valid range'

FILL_VALUE_WARNING = 'WARNING - The _FillValue is within the valid data range. Please specify a _FillValue outside ' \
                     'the valid data range.'

MISSING_VALUE_WARNING = 'WARNING - The missing_value is within the valid data range. Please specify a missing_value ' \
                        'outside the valid data range.'

VARIABLE_COMMENTS = {
    VARIABLE_TYPE_INDICATORS['T']: T_COORDINATE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['Z']: Z_COORDINATE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['Y']: Y_COORDINATE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['X']: X_COORDINATE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['C']: COORDINATE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['AC']: AUXILIARY_COORDINATE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['S']: SCALAR_COORDINATE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['GD']: GEOREFERENCED_DATA_VARIABLE,
    VARIABLE_TYPE_INDICATORS['D']: DATA_VARIABLE,
    VARIABLE_TYPE_INDICATORS['AD']: ANCILLARY_DATA_VARIABLE,
    VARIABLE_TYPE_INDICATORS['G']: GRID_MAPPING_VARIABLE,
    VARIABLE_TYPE_INDICATORS['DO']: DOMAIN_VARIABLE,
    VARIABLE_TYPE_INDICATORS['B']: BOUNDARY_VARIABLE,
    VARIABLE_TYPE_INDICATORS['CM']: CELL_MEASURE_VARIABLE,
    VARIABLE_TYPE_INDICATORS['U']: UNKNOWN_VARIABLE
}
