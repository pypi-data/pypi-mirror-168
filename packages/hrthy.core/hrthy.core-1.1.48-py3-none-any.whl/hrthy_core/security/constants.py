from hrthy_core.security.scopes import (
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_CREATE, SCOPE_CANDIDATE_ADDITIONAL_FIELDS_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_CREATE, SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_UPDATE, SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_CREATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_DELETE, SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_CREATE, SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_UPDATE, SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_VALUE_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_VALUE_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_VALUE_MY_UPDATE, SCOPE_CANDIDATE_ADDITIONAL_FIELDS_VALUE_UPDATE,
    SCOPE_CANDIDATE_CREATE, SCOPE_CANDIDATE_DELETE,
    SCOPE_CANDIDATE_LIST, SCOPE_CANDIDATE_MYSELF_GET,
    SCOPE_CANDIDATE_MYSELF_UPDATE, SCOPE_CANDIDATE_MY_CREATE, SCOPE_CANDIDATE_MY_DELETE, SCOPE_CANDIDATE_MY_LIST,
    SCOPE_CANDIDATE_MY_UPDATE, SCOPE_CANDIDATE_UPDATE, SCOPE_COMPANY_CREATE, SCOPE_COMPANY_DELETE, SCOPE_COMPANY_LIST,
    SCOPE_COMPANY_MYSELF_GET, SCOPE_COMPANY_MY_DELETE, SCOPE_COMPANY_MY_UPDATE, SCOPE_COMPANY_RESTORE,
    SCOPE_COMPANY_UPDATE,
    SCOPE_LICENSE_POOL_CREATE, SCOPE_LICENSE_POOL_DELETE, SCOPE_LICENSE_POOL_LIST, SCOPE_LICENSE_POOL_MY_LIST,
    SCOPE_LICENSE_POOL_UPDATE, SCOPE_PIPELINE_ADDITIONAL_FIELDS_LIST, SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_UPDATE, SCOPE_PIPELINE_ADDITIONAL_FIELDS_UPDATE,
    SCOPE_PIPELINE_CANDIDATE_ASSIGN, SCOPE_PIPELINE_CANDIDATE_MY_ASSIGN,
    SCOPE_PIPELINE_CANDIDATE_MY_UNASSIGN, SCOPE_PIPELINE_CANDIDATE_UNASSIGN, SCOPE_PIPELINE_CREATE,
    SCOPE_PIPELINE_DELETE, SCOPE_PIPELINE_LIST, SCOPE_PIPELINE_MYSELF_GET, SCOPE_PIPELINE_MY_CREATE,
    SCOPE_PIPELINE_MY_DELETE, SCOPE_PIPELINE_MY_LIST, SCOPE_PIPELINE_MY_UPDATE, SCOPE_PIPELINE_UPDATE,
    SCOPE_ROLE_CREATE, SCOPE_ROLE_DELETE, SCOPE_ROLE_LIST, SCOPE_ROLE_MYSELF_GET, SCOPE_ROLE_MY_ASSIGN_GLOBAL,
    SCOPE_ROLE_MY_CREATE, SCOPE_ROLE_MY_DELETE, SCOPE_ROLE_MY_LIST, SCOPE_ROLE_MY_UPDATE, SCOPE_ROLE_UPDATE,
    SCOPE_USER_CREATE, SCOPE_USER_DELETE, SCOPE_USER_LIST, SCOPE_USER_MYSELF_GET, SCOPE_USER_MYSELF_UPDATE,
    SCOPE_USER_MY_CREATE, SCOPE_USER_MY_DELETE, SCOPE_USER_MY_LIST, SCOPE_USER_MY_UPDATE, SCOPE_USER_UPDATE,
)

DEFAULT_SUPER_ADMIN_SCOPES = [
    SCOPE_ROLE_MY_ASSIGN_GLOBAL,
    SCOPE_COMPANY_LIST,
    SCOPE_COMPANY_CREATE,
    SCOPE_COMPANY_UPDATE,
    SCOPE_COMPANY_DELETE,
    SCOPE_COMPANY_RESTORE,
    SCOPE_COMPANY_MY_UPDATE,
    SCOPE_COMPANY_MY_DELETE,
    SCOPE_COMPANY_MYSELF_GET,
    SCOPE_USER_LIST,
    SCOPE_USER_CREATE,
    SCOPE_USER_UPDATE,
    SCOPE_USER_DELETE,
    SCOPE_USER_MY_LIST,
    SCOPE_USER_MY_CREATE,
    SCOPE_USER_MY_UPDATE,
    SCOPE_USER_MY_DELETE,
    SCOPE_USER_MYSELF_GET,
    SCOPE_USER_MYSELF_UPDATE,
    SCOPE_ROLE_LIST,
    SCOPE_ROLE_CREATE,
    SCOPE_ROLE_UPDATE,
    SCOPE_ROLE_DELETE,
    SCOPE_ROLE_MY_LIST,
    SCOPE_ROLE_MY_CREATE,
    SCOPE_ROLE_MY_UPDATE,
    SCOPE_ROLE_MY_DELETE,
    SCOPE_ROLE_MYSELF_GET,
    SCOPE_CANDIDATE_LIST,
    SCOPE_CANDIDATE_CREATE,
    SCOPE_CANDIDATE_UPDATE,
    SCOPE_CANDIDATE_DELETE,
    SCOPE_CANDIDATE_MY_LIST,
    SCOPE_CANDIDATE_MY_CREATE,
    SCOPE_CANDIDATE_MY_UPDATE,
    SCOPE_CANDIDATE_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_CREATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_CREATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_CREATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_CREATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_VALUE_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_VALUE_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_VALUE_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_VALUE_MY_UPDATE,
    SCOPE_PIPELINE_LIST,
    SCOPE_PIPELINE_CREATE,
    SCOPE_PIPELINE_UPDATE,
    SCOPE_PIPELINE_DELETE,
    SCOPE_PIPELINE_MY_LIST,
    SCOPE_PIPELINE_MY_CREATE,
    SCOPE_PIPELINE_MY_UPDATE,
    SCOPE_PIPELINE_MY_DELETE,
    SCOPE_PIPELINE_MYSELF_GET,
    SCOPE_PIPELINE_CANDIDATE_ASSIGN,
    SCOPE_PIPELINE_CANDIDATE_UNASSIGN,
    SCOPE_PIPELINE_CANDIDATE_MY_ASSIGN,
    SCOPE_PIPELINE_CANDIDATE_MY_UNASSIGN,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_LIST,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_UPDATE,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_UPDATE,
    SCOPE_LICENSE_POOL_LIST,
    SCOPE_LICENSE_POOL_CREATE,
    SCOPE_LICENSE_POOL_UPDATE,
    SCOPE_LICENSE_POOL_DELETE,
    SCOPE_LICENSE_POOL_MY_LIST
]

DEFAULT_ADMIN_SCOPES = [
    SCOPE_COMPANY_MYSELF_GET,
    SCOPE_COMPANY_MY_UPDATE,
    SCOPE_COMPANY_MY_DELETE,
    SCOPE_USER_MY_LIST,
    SCOPE_USER_MY_CREATE,
    SCOPE_USER_MY_UPDATE,
    SCOPE_USER_MY_DELETE,
    SCOPE_USER_MYSELF_GET,
    SCOPE_USER_MYSELF_UPDATE,
    SCOPE_ROLE_MY_LIST,
    SCOPE_ROLE_MY_CREATE,
    SCOPE_ROLE_MY_UPDATE,
    SCOPE_ROLE_MY_DELETE,
    SCOPE_ROLE_MYSELF_GET,
    SCOPE_CANDIDATE_MY_LIST,
    SCOPE_CANDIDATE_MY_CREATE,
    SCOPE_CANDIDATE_MY_UPDATE,
    SCOPE_CANDIDATE_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_CREATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_CREATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_VALUE_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_VALUE_MY_UPDATE,
    SCOPE_PIPELINE_MY_LIST,
    SCOPE_PIPELINE_MY_CREATE,
    SCOPE_PIPELINE_MY_UPDATE,
    SCOPE_PIPELINE_MY_DELETE,
    SCOPE_PIPELINE_MYSELF_GET,
    SCOPE_PIPELINE_CANDIDATE_MY_ASSIGN,
    SCOPE_PIPELINE_CANDIDATE_MY_UNASSIGN,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_UPDATE,
    SCOPE_LICENSE_POOL_MY_LIST,
]

DEFAULT_USER_SCOPES = [
    SCOPE_COMPANY_MYSELF_GET,
    SCOPE_ROLE_MYSELF_GET,
    SCOPE_USER_MYSELF_GET,
    SCOPE_USER_MYSELF_UPDATE,
    SCOPE_CANDIDATE_MY_LIST,
    SCOPE_CANDIDATE_MY_CREATE,
    SCOPE_CANDIDATE_MY_UPDATE,
    SCOPE_CANDIDATE_MY_DELETE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_MY_LIST,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_VALUE_MY_UPDATE,
    SCOPE_CANDIDATE_ADDITIONAL_FIELDS_PROTECTED_VALUE_MY_UPDATE,
    SCOPE_PIPELINE_MY_CREATE,
    SCOPE_PIPELINE_MY_UPDATE,
    SCOPE_PIPELINE_MY_DELETE,
    SCOPE_PIPELINE_MYSELF_GET,
    SCOPE_PIPELINE_CANDIDATE_MY_ASSIGN,
    SCOPE_PIPELINE_CANDIDATE_MY_UNASSIGN,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_LIST,
    SCOPE_PIPELINE_ADDITIONAL_FIELDS_MY_UPDATE,
    SCOPE_LICENSE_POOL_MY_LIST,
]

DEFAULT_CANDIDATE_SCOPES = [
    SCOPE_CANDIDATE_MYSELF_GET,
    SCOPE_CANDIDATE_MYSELF_UPDATE,
    SCOPE_PIPELINE_MYSELF_GET
]

# Scopes that are always assigned to all the roles
DEFAULT_SCOPES = [
    SCOPE_COMPANY_MYSELF_GET,
    SCOPE_USER_MYSELF_GET,
    SCOPE_ROLE_MYSELF_GET
]
