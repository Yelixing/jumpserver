from django.utils.translation import ugettext as _
from rest_framework import serializers

from ops.mixin import PeriodTaskSerializerMixin
from assets.models import Asset, Node, BaseAutomation, AutomationExecution
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from common.utils import get_logger
from common.const.choices import Trigger
from common.serializers.fields import ObjectRelatedField, LabeledChoiceField

logger = get_logger(__file__)

__all__ = [
    'BaseAutomationSerializer', 'AutomationExecutionSerializer',
    'UpdateAssetSerializer', 'UpdateNodeSerializer', 'AutomationAssetsSerializer',
]


class BaseAutomationSerializer(PeriodTaskSerializerMixin, BulkOrgResourceModelSerializer):
    assets = ObjectRelatedField(many=True, required=False, queryset=Asset.objects, label=_('Assets'))
    nodes = ObjectRelatedField(many=True, required=False, queryset=Node.objects, label=_('Nodes'))

    class Meta:
        read_only_fields = [
            'date_created', 'date_updated', 'created_by', 'periodic_display'
        ]
        fields = [
                     'id', 'name', 'is_periodic', 'interval', 'crontab', 'comment',
                     'type', 'accounts', 'nodes', 'assets', 'is_active'
                 ] + read_only_fields
        extra_kwargs = {
            'name': {'required': True},
            'type': {'read_only': True},
            'periodic_display': {'label': _('Periodic perform')},
        }


class AutomationExecutionSerializer(serializers.ModelSerializer):
    snapshot = serializers.SerializerMethodField(label=_('Automation snapshot'))
    trigger = LabeledChoiceField(choices=Trigger.choices, label=_("Trigger mode"))

    class Meta:
        model = AutomationExecution
        read_only_fields = [
            'trigger', 'date_start', 'date_finished', 'snapshot', 'status'
        ]
        fields = ['id', 'automation', 'trigger'] + read_only_fields

    @staticmethod
    def get_snapshot(obj):
        tp = obj.snapshot['type']
        snapshot = {
            'type': tp,
            'name': obj.snapshot['name'],
            'comment': obj.snapshot['comment'],
            'accounts': obj.snapshot['accounts'],
            'node_amount': len(obj.snapshot['nodes']),
            'asset_amount': len(obj.snapshot['assets']),
        }
        return snapshot


class UpdateAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAutomation
        fields = ['id', 'assets']


class UpdateNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAutomation
        fields = ['id', 'nodes']


class AutomationAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        only_fields = ['id', 'name', 'address']
        fields = tuple(only_fields)
