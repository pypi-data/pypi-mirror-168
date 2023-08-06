DATA_TYPES = {
    "Mutation": [
        {
            "format": ["maf"],
            "supported_repo": [
                {
                    "name": "cbioportal",
                    "header_mapping": {
                        "gene": "Hugo_Symbol",
                        "chr": "Chromosome",
                        "startPosition": "Start_Position",
                        "endPosition": "End_Position",
                        "referenceAllele": "Reference_Allele",
                        "variantAllele": "Tumor_Seq_Allele2",
                        "mutationType": "Variant_Classification",
                        "variantType": "Variant_Type",
                        "uniqueSampleKey": "Tumor_Sample_Barcode",
                    },
                },
                {"name": "tcga", "header_mapping": {}},
            ],
        }
    ]
}

# endpoints
CONSTANTS_ENDPOINT = "/constants"
REPOSITORIES_ENDPOINT = "/repositories"
REPOSITORY_PACKAGE_ENDPOINT = REPOSITORIES_ENDPOINT + "/{}/packages"
IMAGE_URL_ENDPOINT = (
    "https://elucidatainc.github.io/PublicAssets/discover-fe-assets/omixatlas_hex.svg"
)

# statuscodes
OK = 200
CREATED = 201
COMPUTE_ENV_VARIABLE = "POLLY_TYPE"
UPLOAD_URL_CREATED = 204

# cohort constants
COHORT_VERSION = "0.2"
COHORT_CONSTANTS_URL = (
    "https://elucidatainc.github.io/PublicAssets/cohort_constants.txt"
)
REPORT_FIELDS_URL = "https://elucidatainc.github.io/PublicAssets/report_fields.txt"
OBSOLETE_METADATA_FIELDS = [
    "package",
    "region",
    "bucket",
    "key",
    "file_type",
    "file_location",
    "src_uri",
    "timestamp_",
]
dot = "."

GETTING_UPLOAD_URLS_PAYLOAD = {"data": {"type": "files", "attributes": {"folder": ""}}}

INGESTION_LEVEL_METADATA = {
    "id": "metadata/ingestion",
    "type": "ingestion_metadata",
    "attributes": {
        "ignore": "false",
        "urgent": "true",
        "v1_infra": False,
        "priority": "low",
    },
}

METADATA = {"data": []}

GET_SCHEMA_RETURN_TYPE_VALS = ["dataframe", "dict"]

COMBINED_METADATA_FILE_NAME = "combined_metadata.json"

FILES_PATH_FORMAT = {"metadata": "<metadata_path>", "data": "<data_path>"}

FORMATTED_METADATA = {"id": "", "type": "", "attributes": {}}

FILE_FORMAT_CONSTANTS_URL = (
    "https://elucidatainc.github.io/PublicAssets/file_format_constants.txt"
)

COMPRESSION_TYPES = [
    ".br," ".bz2",
    ".bz",
    ".gz",
    ".lz",
    ".lz4",
    ".sz",
    ".rz",
    ".xz",
    ".zip",
    ".tar",
    ".bgz",
]

FILE_FORMAT_CONSTANTS = {
    "data": [
        ".gct",
        ".vcf",
        ".h5ad",
        ".mmcif",
        ".h5seurat",
        ".biom",
        ".zip",
        ".fs",
        ".tar.gz",
        ".fcs",
        ".vcf.bgz",
        ".gct.bz",
    ],
    "metadata": [".json", ".jpco"],
}
NOT_NEEDED_SCHEMA_FIELDS = [
    "is_current",
    "data_table_version",
    "data_table_name",
    "timestamp_",
]

VALIDATION_LEVEL_CONSTANTS = {"advanced": "value", "basic": "schema"}

BASE_TEST_FORMAT_CONSTANTS_URL = "https://github.com/ElucidataInc/PublicAssets/blob/master/internal-user/add_dataset_test_file"

ELUCIDATA_LOGO_URL = (
    "https://elucidatainc.github.io/PublicAssets/dashboardFrontend/elucidata-logo.svg"
)

REPORT_GENERATION_SUPPORTED_REPOS = ["geo"]

VALIDATION_STATUS_FILE_NAME = "validation_status.json"

DDL_CONST_LIST = [
    "ALL",
    "ALTER",
    "AND",
    "ARRAY",
    "AS",
    "AUTHORIZATION",
    "BETWEEN",
    "BIGINT",
    "BINARY",
    "BOOLEAN",
    "BOTH",
    "BY",
    "CASE",
    "CASHE",
    "CAST",
    "CHAR",
    "COLUMN",
    "CONF",
    "CONSTRAINT",
    "COMMIT",
    "CREATE",
    "CROSS",
    "CUBE",
    "CURRENT",
    "CURRENT_DATE",
    "CURRENT_TIMESTAMP",
    "CURSOR",
    "DATABASE",
    "DATE",
    "DAYOFWEEK",
    "DECIMAL",
    "DELETE",
    "DESCRIBE",
    "DISTINCT",
    "DOUBLE",
    "DROP",
    "ELSE",
    "END",
    "EXCHANGE",
    "EXISTS",
    "EXTENDED",
    "EXTERNAL",
    "EXTRACT",
    "FALSE",
    "FETCH",
    "FLOAT",
    "FLOOR",
    "FOLLOWING",
    "FOR",
    "FOREIGN",
    "FROM",
    "FULL",
    "FUNCTION",
    "GRANT",
    "GROUP",
    "GROUPING",
    "HAVING",
    "IF",
    "IMPORT",
    "IN",
    "INNER",
    "INSERT",
    "INT",
    "INTEGER",
    "INTERSECT",
    "INTERVAL",
    "INTO",
    "IS",
    "JOIN",
    "LATERAL",
    "LEFT",
    "LESS",
    "LIKE",
    "LOCAL",
    "MACRO",
    "MAP",
    "MORE",
    "NONE",
    "NOT",
    "NULL",
    "NUMERIC",
    "OF",
    "ON",
    "ONLY",
    "OR",
    "ORDER",
    "OUT",
    "OUTER",
    "OVER",
    "PARTIALSCAN",
    "PARTITION",
    "PERCENT",
    "PRECEDING",
    "PRECISION",
    "PRESERVE",
    "PRIMARY",
    "PROCEDURE",
    "RANGE",
    "READS",
    "REDUCE",
    "REGEXP",
    "REFERENCES",
    "REVOKE",
    "RIGHT",
    "RLIKE",
    "ROLLBACK",
    "ROLLUP",
    "ROW",
    "ROWS",
    "SELECT",
    "SET",
    "SMALLINT",
    "START",
    "TABLE",
    "TABLESAMPLE",
    "THEN",
    "TIME",
    "TIMESTAMP",
    "TO",
    "TRANSFORM",
    "TRIGGER",
    "TRUE",
    "TRUNCATE",
    "UNBOUNDED",
    "UNION",
    "UNIQUEJOIN",
    "UPDATE",
    "USER",
    "USING",
    "UTC_TIMESTAMP",
    "VALUES",
    "VARCHAR",
    "VIEWS",
    "WHEN",
    "WHERE",
    "WINDOW",
    "WITH",
]

DML_CONST_LIST = [
    "ALTER",
    "AND",
    "AS",
    "BETWEEN",
    "BY",
    "CASE",
    "CAST",
    "CONSTRAINT",
    "CREATE",
    "CROSS",
    "CUBE",
    "CURRENT_DATE",
    "CURRENT_PATH",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "CURRENT_USER",
    "DEALLOCATE",
    "DELETE",
    "DESCRIBE",
    "DISTINCT",
    "DROP",
    "ELSE",
    "END",
    "ESCAPE",
    "EXCEPT",
    "EXECUTE",
    "EXISTS",
    "EXTRACT",
    "FALSE",
    "FIRST",
    "FOR",
    "FROM",
    "FULL",
    "GROUP",
    "GROUPING",
    "HAVING",
    "IN",
    "INNER",
    "INSERT",
    "INTERSECT",
    "INTO",
    "IS",
    "JOIN",
    "LAST",
    "LEFT",
    "LIKE",
    "LOCALTIME",
    "LOCALTIMESTAMP",
    "NATURAL",
    "NORMALIZE",
    "NOT",
    "NULL",
    "OF",
    "ON",
    "OR",
    "ORDER",
    "OUTER",
    "PREPARE",
    "RECURSIVE",
    "RIGHT",
    "ROLLUP",
    "SELECT",
    "TABLE",
    "THEN",
    "TRUE",
    "UNESCAPE",
    "UNION",
    "UNNEST",
    "USING",
    "VALUES",
    "WHEN",
    "WHERE",
    "WITH",
]

# curation_library constants
SUPPORTED_ENTITY_TYPES = [
    "disease",
    "drug",
    "species",
    "tissue",
    "cell_type",
    "cell_line",
    "gene",
]

SCHEMA_VALIDATION_BASE_URL = (
    "https://raw.githubusercontent.com/ElucidataInc/PublicAssets/master/"
    + "internal-user/schema_validation"
)

SCHEMA_VALIDATION = {
    "wrong_repo_id": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_wrong_repo_id.json",
    "field_name_cap": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_capital.json",
    "field_name_underscore": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_with_underscore.json",
    "field_name_resv_keyword": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_with_resv_keyword.json",
    "original_name_empty": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_original_name_empty.json",
    "original_name_grtr_50": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_original_name_gtr_50.json",
    "type_cosco": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_type_cosco.json",
    "is_arr_str": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_is_arr_str.json",
    "is_keyword_str": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_is_keywrd_str.json",
    "filter_size_less": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_filter_size_less.json",
    "filter_size_greater": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_filter_size_greater.json",
    "display_name_empty": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_display_name_empty.json",
    "display_name_grtr_50": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_display_name_grtr_50.json",
    "is_keywrd_is_filter": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_is_keywrd_is_filter.json",
    "is_keywrd_is_ontology": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_is_filter_is_ontology.json",
}
