from OpenSoftCoreV4.utils.model_view_set.__all__ import AllMVS
from d_services.models.GrantSource import GrantSource
from utils.BranchMixinQuerset import BranchViewSetMixin
from d_services.serializers.GrantSource import GrantSourceSerializer


class GrantSourceMVS(BranchViewSetMixin, AllMVS):
    """ViewSet for Grant Sources"""
    queryset = GrantSource.objects.prefetch_related()
    serializer_class = GrantSourceSerializer
    enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
