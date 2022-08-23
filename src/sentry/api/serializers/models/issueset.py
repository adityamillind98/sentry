from sentry.api.serializers import Serializer, register, serialize
from sentry.models.issueset import IssueSet
from sentry.models.issuesetitem import IssueSetItem


# HACK: Registry can't find my serializer so I have to call it manually everytime
@register(IssueSet)
class IssueSetSerializer(Serializer):
    def get_attrs(self, item_list, user, **kwargs):
        attrs = {}
        issue_set_map = {}
        issue_set_ids = [issue_set.id for issue_set in item_list]

        for issue_set in item_list:
            issue_set_map[issue_set.id] = issue_set
            attrs[issue_set] = {"items": []}

        issue_set_items_qs = IssueSetItem.objects.filter(id__in=issue_set_ids)
        issue_set_items = serialize(
            list(issue_set_items_qs), user, serializer=IssueSetItemSerializer()
        )

        for issue_set_item in issue_set_items:
            issue_set = issue_set_map[issue_set_item.get("issueSetId")]
            attrs[issue_set]["items"].append(issue_set_item)

        return attrs

    def serialize(self, obj, attrs, user):
        return {
            "id": str(obj.id),
            "name": obj.name,
            "items": attrs["items"],
        }


@register(IssueSetItem)
class IssueSetItemSerializer(Serializer):
    def serialize(self, obj, attrs, user):
        return {
            "issueId": obj.group.id,
            "issueSetId": obj.issue_set.id,
            "project": obj.project.id,
        }
