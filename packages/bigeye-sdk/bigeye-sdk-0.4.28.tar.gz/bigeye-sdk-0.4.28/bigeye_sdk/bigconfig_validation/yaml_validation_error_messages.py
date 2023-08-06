DUPLICATE_SAVED_METRIC_ID_EXISTS_ERRMSG = "Duplicate saved_metric_id: '{saved_metric_id}' has multiple definitions."
SAVED_METRIC_ID_NOT_EXISTS_IN_SAVED_METRICS_DEFINITION_ERRMSG = \
    "Undefined saved_metric_id: '{saved_metric_id}' does not exist in saved_metric_definitions."
DUPLICATE_TAG_EXISTS_ERRMSG = "Duplicate tag_id: '{tag_id}' has multiple definitions."
TAG_ID_NOT_EXISTS_IN_TAG_DEFINITION_ERRMSG = "Undefined tag_id: '{tag_id}' does not exist in tag_definitions."
FQ_COL_NOT_RESOLVES_TO_COLUMN_ERRMSG = "Invalid column_selector: '{fq_column_name}' does not resolve to a column. Names " \
                                       "must have either 4 elements or 5 elements.  For example: " \
                                       "source.schema.table.column OR " \
                                       "source.database.schema.table.column.  Wild cards are accepted."
WILD_CARDS_NOT_SUPPORT_IN_FQ_TABLE_NAMES_ERRMSG = \
    "Invalid fq_table_name: '{fq_table_name}' is not valid; wildcards are not supported."
FQ_TABLE_NAME_MUST_RESOLVE_TO_TABLE_ERRMSG = "Invalid fq_table_name: '{fq_table_name}' does not resolve to a table.  Names " \
                                             "must have either 3 elements or 4 elements.  For example: " \
                                             "source.schema.table OR " \
                                             "source.database.schema.table."
SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG = "Invalid source: '{fq_name}' does not exist in workspace."
FORMATTING_ERRMSG = "Invalid formatting: {s}"
OVERRIDE_METRIC_TYPE_SAVED_METRIC_ERRMSG = \
    "Invalid metric configuration: Cannot override the metric_type in a saved_metric_definition: {config_error_lines}"
MUST_HAVE_METRIC_TYPE_ERRMSG = "Invalid metric configuration: definition must include metric type {config_error_lines}"
MUST_HAVE_METRIC_ID_ERRMSG = "Each Saved Metric Definition must contain a saved_metric_id.  " \
                             "Saved Metric: {config_error_lines}"
METRIC_TYPE_NOT_EXISTS_ERRMSG = "Invalid metric: {metric} does not exist. {match_message}"
INVALID_DECLARED_ATTRIBUTE_ERRMSG = "Invalid attribute: '{err_attrib}' is not a valid attribute in {cls_name}. {match_message}"
POSSIBLE_MATCH_ERRMSG = "Try '{possible_matches}' instead."
NO_POSSIBLE_MATCH_ERRMSG = " "
INVALID_OBJECT_TYPE_ERRMSG = "Invalid Object Type: {data_type} not a supported supported type. {match_message}"
OBJECT_HAS_NO_TYPE_ERRMSG = "Object requires a type declaration but one was not provided."
METRIC_APPLICATION_ERROR = "Invalid Metric Application: {errmsg}"
