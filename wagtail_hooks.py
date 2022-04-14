import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.templatetags.static import static
from django.utils.html import format_html_join
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
)
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_placeholders_feature(features):
    """
    Registering the `placeholders` feature, which uses the `PLACEHOLDERS` Draft.js
    entity type, and is stored as HTML with a
    `<placeholders id="">short-id</placeholders>` tag.
    """
    feature_name = "placeholders"
    type_ = "PLACEHOLDERS"

    control = {
        "type": type_, 
        "label": "<Tt>", 
        "description": "Template Tags"
    }

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            control,
            js = [
                # make sure this loads first
                'wagtailadmin/js/draftail.js', 
                'placeholders/js/placeholders.js'
            ]
        ),
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                "placeholder[id]": PlaceholdersEntityElementHandler(type_)
            },
            "to_database_format": {
                "entity_decorators": {
                    type_: placeholders_entity_decorator
                }
            },
        },
    )


def placeholders_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the PLACEHOLDERS entities into a placeholder tag.
    """
    return DOM.create_element("placeholder", {"id": props["placeholder"]}, props["children"])


class PlaceholdersEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the placeholder tag into a PLACEHOLDERS entity, with the right data.
    """

    mutability = "IMMUTABLE"

    def get_attribute_data(self, attrs):
        """
        Take the ``placeholder tag`` value from the ``id`` HTML attribute.
        """
        return {"placeholder": attrs["id"]}