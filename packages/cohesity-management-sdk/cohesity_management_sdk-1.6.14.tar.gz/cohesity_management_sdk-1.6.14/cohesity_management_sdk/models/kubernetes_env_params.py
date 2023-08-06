# -*- coding: utf-8 -*-
# Copyright 2022 Cohesity Inc.

import cohesity_management_sdk.models.k_8_s_filter_params

class KubernetesEnvParams(object):

    """Implementation of the 'KubernetesEnvParams' model.

    Attributes:
        exclude_params (K8SFilterParams): If specified, any objects matching
            the filter params will be excluded from backup, even those that are
            explicitly specified by include_params.
        include_params (K8SFilterParams: If not specified, all objects,
            including volumes, will be included by default, except those
            filtered by exclude_params. Otherwise, only the below objects
            (volumes) will be included by default, except those filtered
            by exclude_params.
        leverage_csi_snapshot (bool): If specified, the backup job will use
            CSI snapshot for backups.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "exclude_params":'excludeParams',
        "include_params":'includeParams',
        "leverage_csi_snapshot":'leverageCsiSnapshot'
    }

    def __init__(self,
                 exclude_params=None,
                 include_params=None,
                 leverage_csi_snapshot=None):
        """Constructor for the KubernetesEnvParams class"""

        # Initialize members of the class
        self.exclude_params = exclude_params
        self.include_params = include_params
        self.leverage_csi_snapshot = leverage_csi_snapshot


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        exclude_params = cohesity_management_sdk.models.k_8_s_filter_params.K8SFilterParams.from_dictionary(dictionary.get('excludeParams')) if dictionary.get('excludeParams') else None
        include_params = cohesity_management_sdk.models.k_8_s_filter_params.K8SFilterParams.from_dictionary(dictionary.get('includeParams')) if dictionary.get('includeParams') else None
        leverage_csi_snapshot = dictionary.get('leverageCsiSnapshot')

        # Return an object of this model
        return cls(exclude_params,
                   include_params,
                   leverage_csi_snapshot)


