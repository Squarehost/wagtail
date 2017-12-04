from django.conf import settings
from django.utils.module_loading import import_string

from wagtail.admin.rich_text.editors.hallo import (
    HalloFormatPlugin, HalloHeadingPlugin, HalloListPlugin, HalloPlugin, HalloRichTextArea
)  # NOQA


DEFAULT_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.HalloRichTextArea'
    }
}


def get_rich_text_editor_widget(name='default', features=None):
    editor_settings = getattr(settings, 'WAGTAILADMIN_RICH_TEXT_EDITORS', DEFAULT_RICH_TEXT_EDITORS)

    editor = editor_settings[name]
    options = editor.get('OPTIONS', None)

    if features is None and options is not None:
        # fall back on 'features' list within OPTIONS, if any
        features = options.get('features', None)

    cls = import_string(editor['WIDGET'])

    kwargs = {}

    if options is not None:
        kwargs['options'] = options

    if getattr(cls, 'accepts_features', False):
        kwargs['features'] = features

    return cls(**kwargs)
