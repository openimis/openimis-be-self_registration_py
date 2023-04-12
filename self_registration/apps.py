from django.apps import AppConfig

MODULE_NAME = "self_registration"

DEFAULT_CFG = {
    "gql_query_insuree_perms": ['101101'],
    "gql_query_policies_by_insuree_perms": ['101201'],
    "gql_query_claims_by_insuree_perms": ['111001'],
    "gql_query_policies_by_family_perms": ['101201'],
    "gql_query_policy_remaining_days_perms": ['101201'],
    "gql_query_policy_recent_perms": ['101201'],
    "gql_query_voucher_perms": ['101401'],
    "gql_query_health_facility_perms": ['121101'],
    "gql_mutation_add_profile_perms": ['122002'],
    "gql_mutation_update_profile_perms": ['122003'],
    "gql_mutation_add_voucher_perms": ['101402'],
    "gql_mutation_add_feedback_perms": ['131106'],
    "gql_mutation_add_notification_perms": [],
    "gql_mutation_update_notification_perms": [],
    "gql_mutation_delete_notification_perms": [],
    "gql_mutation_add_insuree_reg_perms": ['101102'],
    "gql_mutation_add_insuree_perms": ['101102'],
}


class SelfRegistrationConfig(AppConfig):
    name = MODULE_NAME
    default_auto_field = 'django.db.models.AutoField'

    gql_query_insuree_perms = []
    gql_query_policies_by_insuree_perms = []
    gql_query_claims_by_insuree_perms = []
    gql_query_policies_by_family_perms = []
    gql_query_policy_remaining_days_perms = []
    gql_query_policy_recent_perms = []
    gql_query_voucher_perms = []
    gql_query_health_facility_perms = []
    gql_mutation_add_profile_perms = []
    gql_mutation_update_profile_perms = []
    gql_mutation_add_voucher_perms = []
    gql_mutation_add_feedback_perms = []
    gql_mutation_add_notification_perms = []
    gql_mutation_update_notification_perms = []
    gql_mutation_delete_notification_perms = []
    gql_mutation_add_insuree_reg_perms = []
    gql_mutation_add_insuree_perms = []

    def _configure_perms(self, cfg):
        SelfRegistrationConfig.gql_query_insuree_perms = cfg["gql_query_insuree_perms"]
        SelfRegistrationConfig.gql_query_policies_by_insuree_perms = cfg["gql_query_policies_by_insuree_perms"]
        SelfRegistrationConfig.gql_query_claims_by_insuree_perms = cfg["gql_query_claims_by_insuree_perms"]
        SelfRegistrationConfig.gql_query_policies_by_family_perms = cfg["gql_query_policies_by_family_perms"]
        SelfRegistrationConfig.gql_query_policy_remaining_days_perms = cfg["gql_query_policy_remaining_days_perms"]
        SelfRegistrationConfig.gql_query_policy_recent_perms = cfg["gql_query_policy_recent_perms"]
        SelfRegistrationConfig.gql_query_voucher_perms = cfg["gql_query_voucher_perms"]
        SelfRegistrationConfig.gql_query_health_facility_perms = cfg["gql_query_health_facility_perms"]
        SelfRegistrationConfig.gql_mutation_add_profile_perms = cfg["gql_mutation_add_profile_perms"]
        SelfRegistrationConfig.gql_mutation_update_profile_perms = cfg["gql_mutation_update_profile_perms"]
        SelfRegistrationConfig.gql_mutation_add_voucher_perms = cfg["gql_mutation_add_voucher_perms"]
        SelfRegistrationConfig.gql_mutation_add_feedback_perms = cfg["gql_mutation_add_feedback_perms"]
        SelfRegistrationConfig.gql_mutation_add_notification_perms = cfg["gql_mutation_add_notification_perms"]
        SelfRegistrationConfig.gql_mutation_update_notification_perms = cfg["gql_mutation_update_notification_perms"]
        SelfRegistrationConfig.gql_mutation_delete_notification_perms = cfg["gql_mutation_delete_notification_perms"]
        SelfRegistrationConfig.gql_mutation_add_insuree_reg_perms = cfg["gql_mutation_add_insuree_reg_perms"]
        SelfRegistrationConfig.gql_mutation_add_insuree_perms = cfg["gql_mutation_add_insuree_perms"]

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_perms(cfg)
